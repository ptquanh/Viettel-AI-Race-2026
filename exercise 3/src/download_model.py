import os
from pathlib import Path
from huggingface_hub import login, snapshot_download

def load_env():
    """Manually parse .env files to load environment variables."""
    # Look for .env in current, parent, or subdirectory 'exercise 3'
    env_paths = [Path(".env"), Path("../.env"), Path("exercise 3/.env")]
    for path in env_paths:
        if path.exists():
            print(f"Loading environment variables from {path.resolve()}")
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            val = parts[1].strip().strip('"').strip("'")
                            os.environ[key] = val
            break

def main():
    load_env()
    
    # Retrieve HF token
    token = os.getenv("HF_TOKEN")
    if token:
        print("HF_TOKEN detected. Logging into Hugging Face...")
        login(token=token)
    else:
        print("Warning: HF_TOKEN not found in environment or .env file.")
        print("Attempting to download repository without authentication (public access required)...")

    # Determine local directory path
    # If run from root and 'exercise 3' folder exists, download to 'exercise 3/Qwen3.5-2B-BTC'
    # Otherwise, download to './Qwen3.5-2B-BTC' relative to current directory.
    local_dir = Path("./Qwen3.5-2B-BTC")
    if Path("exercise 3").exists() and not Path(".").resolve().name == "exercise 3":
        local_dir = Path("exercise 3/Qwen3.5-2B-BTC")
        
    print(f"Target directory for model weights: {local_dir.resolve()}")
    
    # Download model weights
    try:
        snapshot_download(
            repo_id="Qwen/Qwen3.5-2B",
            local_dir=str(local_dir),
            local_dir_use_symlinks=False
        )
        print("SUCCESS: Model weights downloaded and verified successfully!")
    except Exception as e:
        print(f"ERROR: Failed to download model. Details: {e}")
        print("\nPlease check your internet connection, HF_TOKEN, or repository access.")

if __name__ == "__main__":
    main()
