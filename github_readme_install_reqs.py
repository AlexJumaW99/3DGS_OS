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

    # PROMPT USER FOR ENVIRONMENT NAME
    env_name = input("Please enter a name for the new Conda environment: ").strip()
    
    if not env_name:
        print("Error: Environment name cannot be empty.")
        sys.exit(1)

    # 1. Create and update Conda environment using the chosen name
    # Note: Using 'shell=True' to ensure conda commands are recognized
    print(f"--- Creating Conda Environment '{env_name}' ---")
    run_command(f"conda create --name {env_name} -y python=3.8")
    
    # Building the installation command sequence
    # We use 'conda run -n {env_name}' to ensure commands execute inside the new env
    env_prefix = f"conda run -n {env_name}"

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
    print(f"To start using the environment, run:")
    print(f"conda activate {env_name}")

if __name__ == "__main__":
    install_nerfstudio_prerequisites()