import subprocess
import sys
import shutil

def run_command(command, description):
    """
    Runs a shell command and prints status.
    """
    print(f"\n[INFO] Starting: {description}...")
    try:
        # shell=True is used to ensure conda commands are recognized if not in direct path,
        # though explicit executable paths or 'conda run' are safer.
        subprocess.check_call(command, shell=True)
        print(f"[SUCCESS] Completed: {description}")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Failed during: {description}")
        print(f"Error command: {e.cmd}")
        sys.exit(1)

def check_conda():
    """Checks if Conda is installed and reachable."""
    if shutil.which("conda") is None:
        print("[ERROR] Conda is not found in your PATH. Please install Anaconda or Miniconda first.")
        sys.exit(1)

def main():
    print("=== Nerfstudio Server Installer (Full Package) ===")
    check_conda()
    
    # 1. Get custom environment name
    env_name = input("Enter the name for your new Conda environment: ").strip()
    if not env_name:
        print("[ERROR] Environment name cannot be empty.")
        sys.exit(1)

    # 2. Create Conda Environment (Python 3.8 as per docs recommended for compatibility)
    # Using python 3.8 ensures maximum compatibility with nerfstudio dependencies
    create_env_cmd = f"conda create --name {env_name} -y python=3.8"
    run_command(create_env_cmd, f"Creating Conda environment '{env_name}'")

    # NOTE: We use 'conda run -n <env_name>' to execute commands inside the environment
    # without needing to activate it in the shell script context.

    # 3. Upgrade pip
    pip_upgrade_cmd = f"conda run -n {env_name} python -m pip install --upgrade pip"
    run_command(pip_upgrade_cmd, "Upgrading pip")

    # 4. Install CUDA Toolkit 11.8 (Heavy Requirement)
    # This is critical for building tiny-cuda-nn extensions on the server
    cuda_cmd = f"conda run -n {env_name} conda install -y -c \"nvidia/label/cuda-11.8.0\" cuda-toolkit"
    run_command(cuda_cmd, "Installing CUDA Toolkit 11.8")

    # 5. Install PyTorch 2.1.2 with CUDA 11.8 (Recommended Configuration)
    # This ensures the server's GPUs are fully utilized
    torch_cmd = (
        f"conda run -n {env_name} pip install "
        "torch==2.1.2+cu118 torchvision==0.16.2+cu118 "
        "--extra-index-url https://download.pytorch.org/whl/cu118"
    )
    run_command(torch_cmd, "Installing PyTorch 2.1.2 (CUDA 11.8 version)")

    # 6. Install tiny-cuda-nn (Heavy Requirement)
    # This compiles C++ extensions. It requires the CUDA toolkit installed above.
    # We install 'ninja' first to speed up the build.
    tcnn_cmd = (
        f"conda run -n {env_name} pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch"
    )
    run_command(tcnn_cmd, "Compiling and installing tiny-cuda-nn (this may take a few minutes)")

    # 7. Install Nerfstudio (Full Package)
    # This includes the core library and the Viewer (GUI)
    nerfstudio_cmd = f"conda run -n {env_name} pip install nerfstudio"
    run_command(nerfstudio_cmd, "Installing Nerfstudio and Viewer")

    print("\n" + "="*50)
    print(f"[COMPLETE] Nerfstudio has been installed in environment: '{env_name}'")
    print("="*50)
    print("To start using it, run the following in your terminal:")
    print(f"    conda activate {env_name}")
    print("    ns-train splatfacto --data <your_data_folder>")
    print("="*50)

if __name__ == "__main__":
    main()