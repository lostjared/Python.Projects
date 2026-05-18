import sys
import os
import subprocess
import glob

if len(sys.argv) < 3:
    print("Usage: python glitch_factory.py [path_to_style_image.jpg] [dataset_path] [final_onnx_path]")
    sys.exit(1)

style_image = sys.argv[1]
dataset_path = sys.argv[2]
final_onnx = sys.argv[3] if len(sys.argv) > 3 else "final_model.onnx"

model_dir = "./my_glitch_models"
temp_export = "temp_export.onnx"
venv_python = "glitch_env/bin/python"

#commented out, I use this to to keep my GPU cool while its training
#print("Setting GPU power limits and persistence mode...")
#subprocess.run(["sudo", "nvidia-smi", "-pm", "1"], check=True)
#subprocess.run(["sudo", "nvidia-smi", "-pl", "130"], check=True)

print(f"Starting training against {style_image}...")
subprocess.run([
    venv_python, "neural_style.py", "train",
    "--dataset", dataset_path,
    "--style-image", style_image,
    "--save-model-dir", model_dir,
    "--epochs", "2",
    "--accel",
    "--batch-size", "4",
    "--log-interval", "100"
], check=True)

models = glob.glob(os.path.join(model_dir, "*.model"))
if not models:
    print("Error: No models found after training.")
    sys.exit(1)

latest_model = max(models, key=os.path.getmtime)
print(f"Training complete. Using model: {latest_model}")

print("Exporting to ONNX...")
subprocess.run([
    venv_python, "neural_style.py", "eval",
    "--model", latest_model,
    "--content-image", "/home/jared/Pictures/jared-ai.jpg",
    "--output-image", "factory_test.jpg",
    "--export_onnx", temp_export,
    "--accel"
], check=True)

print("Simplifying ONNX model for ACMX2...")
onnxsim_check = subprocess.run([venv_python, "-m", "onnxsim", "-h"], capture_output=True)

if onnxsim_check.returncode == 0:
    subprocess.run([venv_python, "-m", "onnxsim", temp_export, final_onnx], check=True)
    os.remove(temp_export)
    print(f"Success! Final model ready at: {final_onnx}")
else:
    print(f"Warning: onnxsim not found. Move {temp_export} to your models folder.")

print("Pipeline finished. Check factory_test.jpg for style preview.")
