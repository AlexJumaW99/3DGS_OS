import subprocess
import sys

def run_command(command, shell=True):
    """Helper to run shell commands and handle errors."""
    try:
        print(f"Executing: {command}")
        subprocess.check_call(command, shell=shell)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing: {command}\n{e}")
        sys.exit(1)

def install_nerfstudio_prerequisites():
    print("--- Starting Nerfstudio Prerequisite Installation ---")

    # 1. Create and update Conda environment
    # Note: Using 'shell=True' to ensure conda commands are recognized
    run_command("conda create --name nerfstudio -y python=3.8")
    
    # Building the installation command sequence
    # We use 'conda run -n nerfstudio' to ensure commands execute inside the new env
    env_prefix = "conda run -n nerfstudio"

    print("--- Updating Pip ---")
    run_command(f"{env_prefix} pip install --upgrade pip")

    print("--- Installing PyTorch with CUDA 11.8 Support ---")
    # Reference:
    pytorch_cmd = (
        f"{env_prefix} pip install torch==2.1.2+cu118 torchvision==0.16.2+cu118 "
        "--extra-index-url https://download.pytorch.org/whl/cu118"
    )
    run_command(pytorch_cmd)

    print("--- Installing CUDA Toolkit 11.8 ---")
    # Reference:
    run_command(f"{env_prefix} conda install -c 'nvidia/label/cuda-11.8.0' cuda-toolkit -y")

    print("--- Installing tiny-cuda-nn ---")
    # Ninja is required for building tiny-cuda-nn
    run_command(f"{env_prefix} pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch")

    print("--- Installing Nerfstudio Core ---")
    # Installing the base package via pip
    run_command(f"{env_prefix} pip install nerfstudio")

    print("\n--- Installation Complete! ---")
    print("To start using the environment, run:")
    print("conda activate nerfstudio")

if __name__ == "__main__":
    install_nerfstudio_prerequisites()