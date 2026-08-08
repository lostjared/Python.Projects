#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import tempfile
import torch
import torch.nn.functional as F
from torchvision import models, transforms
from torchvision.models import Inception_V3_Weights
from PIL import Image
import numpy as np
import cv2

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Deep Dream a video, optionally upscale it, and write a video."
    )
    parser.add_argument('-i', '--input', type=str, required=True, help="Path to input video")
    parser.add_argument('-o', '--output', type=str, required=True, help="Path to output video (for example, output.mp4)")
    parser.add_argument('-l', '--layer', type=str, default="Mixed_6c", help="Target network layer")
    parser.add_argument('-c', '--channel', type=int, default=None, help="Target specific feature channel (e.g., 138 for eyes)")
    parser.add_argument('-n', '--iters', type=int, default=10, help="Number of gradient ascent iterations per octave")
    parser.add_argument('--lr', type=float, default=0.05, help="Learning rate for gradient ascent")
    parser.add_argument('--octaves', type=int, default=4, help="Number of scales to process")
    parser.add_argument('--scale', type=float, default=1.4, help="Scale factor between octaves")
    parser.add_argument('--jitter', type=int, default=32, help="Max pixel shift for smoothing")
    parser.add_argument(
        '--batch-size',
        type=int,
        default=25,
        help="Frames kept in each temporary Real-ESRGAN batch",
    )
    parser.add_argument(
        '--no-upscale',
        action='store_false',
        dest='upscale_enabled',
        help="Skip Real-ESRGAN and write Deep Dream frames at their processed resolution",
    )
    parser.set_defaults(upscale_enabled=True)
    parser.add_argument(
        '--realesrgan-bin',
        default='/home/jared/reales/realesrgan-ncnn-vulkan-v0.2.0-ubuntu/realesrgan-ncnn-vulkan',
        help="Path to realesrgan-ncnn-vulkan",
    )
    parser.add_argument('--realesrgan-model', default='realesrgan-x4plus', help="Real-ESRGAN model name")
    parser.add_argument('--upscale', type=int, choices=(2, 3, 4), default=4, help="Real-ESRGAN output scale")
    parser.add_argument('--tile-size', type=int, default=0, help="Real-ESRGAN tile size (0 selects automatically)")
    parser.add_argument('--gpu-id', type=int, default=-1, help="Real-ESRGAN GPU id (-1 selects automatically)")
    parser.add_argument('--codec', default='mp4v', help="FourCC used by OpenCV VideoWriter")
    parser.add_argument('--fps', type=float, default=None, help="Output FPS (defaults to the input FPS)")
    parser.add_argument('--temp-dir', default=None, help="Parent directory for bounded temporary batches")
    return parser.parse_args()

def frame_to_tensor(frame, max_size=2048):
    # Convert OpenCV BGR to RGB for PIL
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb)
    
    size = max(image.size)
    if size > max_size:
        ratio = max_size / size
        image = image.resize((int(image.size[0] * ratio), int(image.size[1] * ratio)), Image.LANCZOS)
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])
    return transform(image).unsqueeze(0)

def deprocess(tensor, stretch=True):
    image = tensor.to('cpu').clone().detach().squeeze(0)
    image = image.numpy().transpose(1, 2, 0)
    
    image = image * np.array(IMAGENET_STD) + np.array(IMAGENET_MEAN)
    
    if stretch:
        p2, p98 = np.percentile(image, (2, 98))
        image = np.clip((image - p2) / (p98 - p2 + 1e-8), 0, 1)
    else:
        image = image.clip(0, 1)
        
    return (image * 255).astype(np.uint8)

def deep_dream_step(image_tensor, model, args):
    device = next(model.parameters()).device
    image_tensor = image_tensor.to(device).requires_grad_(True)
    optimizer = torch.optim.Adam([image_tensor], lr=args.lr)
    channel_mean = image_tensor.new_tensor(IMAGENET_MEAN).view(1, 3, 1, 1)
    channel_std = image_tensor.new_tensor(IMAGENET_STD).view(1, 3, 1, 1)
    normalized_min = -channel_mean / channel_std
    normalized_max = (1.0 - channel_mean) / channel_std

    for i in range(args.iters):
        optimizer.zero_grad()
        
        shift_x, shift_y = np.random.randint(-args.jitter, args.jitter + 1, 2)
        jittered_tensor = torch.roll(image_tensor, shifts=(shift_x, shift_y), dims=(2, 3))
        
        out = jittered_tensor
        
        layer_found = False
        for name, module in model.named_children():
            if name == 'AuxLogits':
                continue
            out = module(out)
            if name == args.layer:
                layer_found = True
                break
                
        if not layer_found:
            print(f"Error: Layer '{args.layer}' not found.")
            sys.exit(1)
            
        if args.channel is not None:
            loss = -out[:, args.channel].norm()
        else:
            loss = -out.norm()
            
        loss.backward()
        
        image_tensor.grad /= torch.max(torch.abs(image_tensor.grad)) + 1e-8
        optimizer.step()
        
        with torch.no_grad():
            # The optimized tensor is ImageNet-normalized, so its valid bounds
            # are channel-specific rather than the unnormalized [0, 1] range.
            image_tensor.copy_(torch.maximum(
                torch.minimum(image_tensor, normalized_max), normalized_min
            ))
            
    return image_tensor.detach()

def run_octaves(img_tensor, model, args):
    octaves = [img_tensor]
    for _ in range(args.octaves - 1):
        hw = octaves[-1].shape[-2:]
        new_hw = [int(dim / args.scale) for dim in hw]
        scaled = F.interpolate(octaves[-1], size=new_hw, mode='bilinear', align_corners=False)
        octaves.append(scaled)
        
    octaves = octaves[::-1]
    dream_tensor = octaves[0].clone()
    
    for i in range(len(octaves)):
        if i > 0:
            hw = octaves[i].shape[-2:]
            dream_tensor = F.interpolate(dream_tensor, size=hw, mode='bilinear', align_corners=False)
            prev_orig_upscaled = F.interpolate(octaves[i-1], size=hw, mode='bilinear', align_corners=False)
            high_freq_detail = octaves[i] - prev_orig_upscaled
            dream_tensor = dream_tensor + high_freq_detail.to(dream_tensor.device)
            
        dream_tensor = deep_dream_step(dream_tensor, model, args)
        
    return dream_tensor


def upscale_batch(frames, first_frame_number, args):
    """Upscale one bounded batch and yield decoded frames in order."""
    temp_parent = os.path.abspath(args.temp_dir) if args.temp_dir else None
    if temp_parent:
        os.makedirs(temp_parent, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix='ddream_upscale_', dir=temp_parent) as batch_dir:
        source_dir = os.path.join(batch_dir, 'source')
        upscaled_dir = os.path.join(batch_dir, 'upscaled')
        os.makedirs(source_dir)
        os.makedirs(upscaled_dir)

        for offset, frame in enumerate(frames):
            frame_number = first_frame_number + offset
            frame_path = os.path.join(source_dir, f'frame_{frame_number:08d}.jpg')
            if not cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95]):
                raise RuntimeError(f'Could not write temporary frame {frame_path}')

        executable = os.path.abspath(args.realesrgan_bin)
        command = [
            executable,
            '-i', source_dir,
            '-o', upscaled_dir,
            '-n', args.realesrgan_model,
            '-s', str(args.upscale),
            '-t', str(args.tile_size),
            '-f', 'jpg',
        ]
        if args.gpu_id >= 0:
            command.extend(['-g', str(args.gpu_id)])

        print(f'Upscaling frames {first_frame_number}-{first_frame_number + len(frames) - 1}...')
        subprocess.run(command, cwd=os.path.dirname(executable), check=True)

        output_paths = sorted(
            os.path.join(upscaled_dir, name)
            for name in os.listdir(upscaled_dir)
            if name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
        )
        if len(output_paths) != len(frames):
            raise RuntimeError(
                f'Real-ESRGAN produced {len(output_paths)} frames; expected {len(frames)}'
            )

        for output_path in output_paths:
            frame = cv2.imread(output_path, cv2.IMREAD_COLOR)
            if frame is None:
                raise RuntimeError(f'Could not decode upscaled frame {output_path}')
            yield frame


def append_batch(frames, first_frame_number, writer, video_size, fps, args):
    output_frames = (
        upscale_batch(frames, first_frame_number, args)
        if args.upscale_enabled
        else iter(frames)
    )

    for frame in output_frames:
        if writer is None:
            height, width = frame.shape[:2]
            video_size = (width, height)
            fourcc = cv2.VideoWriter_fourcc(*args.codec)
            writer = cv2.VideoWriter(args.output, fourcc, fps, video_size)
            if not writer.isOpened():
                raise RuntimeError(
                    f"Could not open {args.output} with codec '{args.codec}'. "
                    "Try --codec avc1 or another codec installed for OpenCV."
                )

        size = (frame.shape[1], frame.shape[0])
        if size != video_size:
            raise RuntimeError(f'Upscaled frame size changed from {video_size} to {size}')
        writer.write(frame)

    return writer, video_size

if __name__ == '__main__':
    args = parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Could not find video at {args.input}")
        sys.exit(1)
    if args.batch_size < 1:
        print("Error: --batch-size must be at least 1")
        sys.exit(1)
    if len(args.codec) != 4:
        print("Error: --codec must be a four-character FourCC")
        sys.exit(1)
    if args.upscale_enabled and (
        not os.path.isfile(args.realesrgan_bin)
        or not os.access(args.realesrgan_bin, os.X_OK)
    ):
        print(f"Error: Real-ESRGAN executable not found or not executable: {args.realesrgan_bin}")
        sys.exit(1)

    output_parent = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(output_parent, exist_ok=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = models.inception_v3(weights=Inception_V3_Weights.DEFAULT, transform_input=False).to(device)
    model.eval()
    
    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        print(f"Error: OpenCV could not open video {args.input}")
        sys.exit(1)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    output_fps = args.fps if args.fps is not None else input_fps
    if output_fps <= 0:
        output_fps = 30.0
    print(f"Opened {args.input}. Total frames: {frame_count}; output FPS: {output_fps:g}")

    current_frame = 1
    batch_start = 1
    dreamed_frames = []
    writer = None
    video_size = None

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            print(f"Dreaming frame {current_frame}/{frame_count}...")
            img_tensor = frame_to_tensor(frame)
            dream_tensor = run_octaves(img_tensor, model, args)

            result_img = deprocess(dream_tensor)
            dreamed_frame = cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR)

            if args.upscale_enabled:
                dreamed_frames.append(dreamed_frame)
            else:
                # With no upscaling there is no reason to retain a batch: write
                # each completed dream frame directly into the output video.
                writer, video_size = append_batch(
                    (dreamed_frame,), current_frame, writer, video_size, output_fps, args
                )

            del img_tensor
            del dream_tensor
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            if args.upscale_enabled and len(dreamed_frames) == args.batch_size:
                writer, video_size = append_batch(
                    dreamed_frames, batch_start, writer, video_size, output_fps, args
                )
                dreamed_frames.clear()
                batch_start = current_frame + 1

            current_frame += 1

        if dreamed_frames:
            writer, video_size = append_batch(
                dreamed_frames, batch_start, writer, video_size, output_fps, args
            )
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    finally:
        cap.release()
        if writer is not None:
            writer.release()

    if writer is None:
        print("Error: Input video contained no readable frames", file=sys.stderr)
        sys.exit(1)

    print(f"Video processing complete. Upscaled video saved to {args.output}")
