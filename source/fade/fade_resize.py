import cv2
import numpy as np
import sys
import os

OUTPUT_FILE = "fade_output_video.mp4"
FPS = 30.0
PAUSE_SECONDS = 0.5
FADE_SECONDS = 0.5

def load_image_list(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    with open(filepath, 'r') as f:
        paths = [line.strip() for line in f if line.strip()]
    return paths

def parse_resolution(res_str):
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

    target_size = None
    
    if len(sys.argv) >= 3:
        target_size = parse_resolution(sys.argv[2])
        print(f"Forcing output resolution to: {target_size[0]}x{target_size[1]}")

    first_img = cv2.imread(image_paths[0])
    if first_img is None:
        print(f"Error loading first image: {image_paths[0]}")
        return

    if target_size is None:
        h, w, _ = first_img.shape
        target_size = (w, h)
        print(f"No resolution specified. Using first image size: {w}x{h}")

    video_w, video_h = target_size

    if first_img.shape[1] != video_w or first_img.shape[0] != video_h:
        first_img = cv2.resize(first_img, (video_w, video_h))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (video_w, video_h))

    if not out.isOpened():
        print("Error: Could not open video writer.")
        return

    pause_frames = int(PAUSE_SECONDS * FPS)
    fade_frames = int(FADE_SECONDS * FPS)

    current_img = first_img

    for i in range(1, len(image_paths)):
        next_path = image_paths[i]
        next_img = cv2.imread(next_path)

        if next_img is None:
            print(f"Skipping unreadable: {next_path}")
            continue

        if next_img.shape[1] != video_w or next_img.shape[0] != video_h:
            next_img = cv2.resize(next_img, (video_w, video_h))

        print(f"Processing transition: Image {i} -> Image {i+1}...")

        for _ in range(pause_frames):
            out.write(current_img)

        for step in range(fade_frames):
            alpha = step / float(fade_frames)
            beta = 1.0 - alpha
            
            blended = cv2.addWeighted(next_img, alpha, current_img, beta, 0.0)
            out.write(blended)

        current_img = next_img

    print("Writing final frame sequence...")
    for _ in range(pause_frames):
        out.write(current_img)

    out.release()
    print(f"Done! Video saved to: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    main()
