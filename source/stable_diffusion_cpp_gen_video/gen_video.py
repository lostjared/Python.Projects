#!/bin/env python3
import os
import cv2
import argparse
import numpy as np
from PIL import Image
from stable_diffusion_cpp import StableDiffusion

def process_video(video_in, video_out, frame_dir, model_path, prompt, neg_prompt, seed, end_seed, strength, target_width, target_height, sampler):
    os.makedirs(frame_dir, exist_ok=True)
    model = StableDiffusion(model_path=model_path,wtype="f16")
    cap = cv2.VideoCapture(video_in)
    if not cap.isOpened():
        raise RuntimeError(f"Error opening video file: {video_in}")

    orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = max(1, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

    new_w = max(64, round(target_width / 64) * 64)
    new_h = max(64, round(target_height / 64) * 64)
    
    print(f"Original video dimensions: {orig_w}x{orig_h}")
    print(f"Using sampler: {sampler}")
    print(f"Requested target: {target_width}x{target_height} -> Snapped for SD: {new_w}x{new_h}")
#   fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#   out = cv2.VideoWriter(video_out, fourcc, fps, (new_w, new_h))
    frame_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break 
            
            frame_count += 1
            frame_filename = os.path.join(frame_dir, f"frame_{frame_count:06d}.png")

            if os.path.exists(frame_filename):
                out_bgr = cv2.imread(frame_filename)
                out.write(out_bgr)
                print(f"Loaded existing frame {frame_count}/{total_frames}")
                continue

            resized_frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)

            if end_seed is not None and total_frames > 1:
                alpha = min(1.0, (frame_count - 1) / (total_frames - 1))
                
                # Pass width and height here
                res1 = model.generate_image(
                    prompt=prompt, negative_prompt=neg_prompt, init_image=pil_img,
                    strength=strength, seed=seed, sample_method=sampler,
                    width=new_w, height=new_h
                )
                res2 = model.generate_image(
                    prompt=prompt, negative_prompt=neg_prompt, init_image=pil_img,
                    strength=strength, seed=end_seed, sample_method=sampler,
                    width=new_w, height=new_h
                )
                
                out_rgb1 = np.array(res1[0])
                out_rgb2 = np.array(res2[0])
                out_rgb = cv2.addWeighted(out_rgb1, 1.0 - alpha, out_rgb2, alpha, 0)
            else:
                # And pass width and height here
                res = model.generate_image(
                    prompt=prompt, negative_prompt=neg_prompt, init_image=pil_img,
                    strength=strength, seed=seed, sample_method=sampler,
                    width=new_w, height=new_h
                )
                out_rgb = np.array(res[0])

            out_bgr = cv2.cvtColor(out_rgb, cv2.COLOR_RGB2BGR)
            cv2.imwrite(frame_filename, out_bgr)
  #          out.write(out_bgr)
            
            print(f"Processed frame {frame_count}/{total_frames}")

    except KeyboardInterrupt:
        print("\n[!] Ctrl+C detected. Halting processing safely...")

    finally:
        cap.release()
#       out.release()
        print(f"Cleanup finished. Progress saved to '{frame_dir}'. Partial video saved to '{video_out}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video frames via stable-diffusion-cpp")
    parser.add_argument("-vi", "--video_in", required=True)
    parser.add_argument("-vo", "--video_out", required=True)
    parser.add_argument("-fd", "--frame_dir", default="output_frames")
    parser.add_argument("-m", "--model", required=True)
    parser.add_argument("-p", "--prompt", required=True)
    parser.add_argument("-n", "--neg_prompt", default="")
    parser.add_argument("-s", "--seed", type=int, required=True)
    parser.add_argument("-es", "--end_seed", type=int, default=None)
    parser.add_argument("--strength", type=float, default=0.75)
    parser.add_argument("-W", "--width", type=int, default=640)
    parser.add_argument("-H", "--height", type=int, default=360)
    parser.add_argument("-sm", "--sampler", default="euler_a", choices=["euler", "euler_a", "heun", "dpm2", "dpm++2m", "dpm++2mv2", "lms"])

    args = parser.parse_args()
    process_video(
        args.video_in, 
        args.video_out, 
        args.frame_dir,
        args.model, 
        args.prompt, 
        args.neg_prompt, 
        args.seed, 
        args.end_seed,
        args.strength,
        args.width,
        args.height,
        args.sampler
    )
