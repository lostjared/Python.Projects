#!/usr/bin/env python3
"""Apply the Deep Dream processing from ddream_proc.py to one image."""

import argparse
import os
import sys

import cv2
import torch
from torchvision import models
from torchvision.models import Inception_V3_Weights

from ddream_proc import deprocess, frame_to_tensor, run_octaves


def parse_args():
    parser = argparse.ArgumentParser(description="Deep Dream a single image.")
    parser.add_argument('-i', '--input', required=True, help="Path to input image")
    parser.add_argument('-o', '--output', required=True, help="Path to output image")
    parser.add_argument('-l', '--layer', default='Mixed_6c', help="Target network layer")
    parser.add_argument(
        '-c', '--channel', type=int, default=None,
        help="Target a specific feature channel (for example, 138 for eyes)",
    )
    parser.add_argument(
        '-n', '--iters', type=int, default=10,
        help="Gradient ascent iterations per octave",
    )
    parser.add_argument('--lr', type=float, default=0.05, help="Gradient ascent learning rate")
    parser.add_argument('--octaves', type=int, default=4, help="Number of scales to process")
    parser.add_argument('--scale', type=float, default=1.4, help="Scale factor between octaves")
    parser.add_argument('--jitter', type=int, default=32, help="Maximum random pixel shift")
    return parser.parse_args()


def validate_args(args):
    if not os.path.isfile(args.input):
        raise ValueError(f"input image not found: {args.input}")
    if args.iters < 1:
        raise ValueError('--iters must be at least 1')
    if args.octaves < 1:
        raise ValueError('--octaves must be at least 1')
    if args.scale <= 1 and args.octaves > 1:
        raise ValueError('--scale must be greater than 1 when using multiple octaves')
    if args.jitter < 0:
        raise ValueError('--jitter cannot be negative')


def main():
    args = parse_args()

    try:
        validate_args(args)
    except ValueError as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2

    frame = cv2.imread(args.input, cv2.IMREAD_COLOR)
    if frame is None:
        print(f'Error: could not decode image: {args.input}', file=sys.stderr)
        return 1

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = models.inception_v3(
        weights=Inception_V3_Weights.DEFAULT,
        transform_input=False,
    ).to(device)
    model.eval()

    image_tensor = frame_to_tensor(frame)
    dream_tensor = run_octaves(image_tensor, model, args)
    result_rgb = deprocess(dream_tensor)
    result_bgr = cv2.cvtColor(result_rgb, cv2.COLOR_RGB2BGR)

    output_parent = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(output_parent, exist_ok=True)
    if not cv2.imwrite(args.output, result_bgr):
        print(f'Error: could not write image: {args.output}', file=sys.stderr)
        return 1

    print(f'Processed image saved to {args.output}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
