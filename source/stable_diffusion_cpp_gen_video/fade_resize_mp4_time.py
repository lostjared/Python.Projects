#!/usr/bin/env python3

import cv2
import numpy as np
import sys
import os

# --- Configuration ---
OUTPUT_FILE = "output_video.mp4"
FPS = 60.0
PAUSE_SECONDS = 0.05
FADE_SECONDS = 0.1

def load_image_list(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    with open(filepath, 'r') as f:
        paths = [line.strip() for line in f if line.strip()]
    return paths

def parse_resolution(res_str):
    """Parses a string like '480x480' into (width, height)."""
    try:
        w_str, h_str = res_str.lower().split('x')
        return int(w_str), int(h_str)
    except ValueError:
        print(f"Error: Invalid resolution format '{res_str}'. Use format 'WIDTHxHEIGHT' (e.g., 640x480).")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python video_fader.py <image_list.txt> [WIDTHxHEIGHT]")
        print("Example: python video_fader.py list.txt 480x480")
        return

    list_file = sys.argv[1]
    image_paths = load_image_list(list_file)

    if not image_paths:
        print("No images found in the text file.")
        return

    # 1. Determine Target Resolution
    target_size = None
    
    # Check if user provided the optional resolution argument
    if len(sys.argv) >= 3:
        target_size = parse_resolution(sys.argv[2])
        print(f"Forcing output resolution to: {target_size[0]}x{target_size[1]}")

    # 2. Load First Image
    first_img = cv2.imread(image_paths[0])
    if first_img is None:
        print(f"Error loading first image: {image_paths[0]}")
        return

    # If no target size provided, use the first image's size
    if target_size is None:
        h, w, _ = first_img.shape
        target_size = (w, h)
        print(f"No resolution specified. Using first image size: {w}x{h}")

    # Explicitly unpack width and height for readability
    video_w, video_h = target_size

    # Resize the first image if it doesn't match the target
    if first_img.shape[1] != video_w or first_img.shape[0] != video_h:
        first_img = cv2.resize(first_img, (video_w, video_h))

    # 3. Initialize VideoWriter
    # Note: VideoWriter expects size as (Width, Height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (video_w, video_h))

    if not out.isOpened():
        print("Error: Could not open video writer.")
        return

    # Calculate frame counts
    pause_frames = int(PAUSE_SECONDS * FPS)
    fade_frames = int(FADE_SECONDS * FPS)

    # Initialize loop with the prepared first image
    current_img = first_img

    # --- Processing Loop ---
    for i in range(1, len(image_paths)):
        next_path = image_paths[i]
        next_img = cv2.imread(next_path)

        if next_img is None:
            print(f"Skipping unreadable: {next_path}")
            continue

        # Resize next_img to match the video dimensions exactly
        if next_img.shape[1] != video_w or next_img.shape[0] != video_h:
            next_img = cv2.resize(next_img, (video_w, video_h))

        print(f"Processing transition: Image {i} -> Image {i+1}...")

        # A. Write Static Frames (Pause)
        for _ in range(pause_frames):
            out.write(current_img)

        # B. Write Fade Frames (Transition)
        for step in range(fade_frames):
            alpha = step / float(fade_frames)
            beta = 1.0 - alpha
            
            blended = cv2.addWeighted(next_img, alpha, current_img, beta, 0.0)
            out.write(blended)

        # Update current image
        current_img = next_img

    # Write the final static sequence
    print("Writing final frame sequence...")
    for _ in range(pause_frames):
        out.write(current_img)

    out.release()
    print(f"Done! Video saved to: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    main()
