# Text-presenter

## Demo

https://github.com/bruehldev/text-presenter/assets/15344369/cd66171d-5974-4b13-b46f-2e738ffd05e2



## Requirements
- Conda for package management
- Ensure you have an NVIDIA GPU with the required drivers:
  ```
  nvidia-smi
  ```
- Install the build-essential packages:
  ```
  sudo apt update
  sudo apt install build-essential
  ```

## Usage

1. Install the required packages by running the following command:
  - Create:
    ```
    conda env create --name textpresenter --file environment.yml
    ```
  - Activate:
    ```
    conda activate textpresenter
    ```

2. For Windows OS:
  - Ensure cuda is installed:
    ```
    nvcc --version
    ```
  - Uninstall the existing torch package: 
    ```
    pip uninstall torch
    ```
  - Visit the [PyTorch website](https://pytorch.org/get-started/locally/) to get the command for installing the latest version of PyTorch with CUDA support
    
    CUDA 11.8:
    ```
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```
    CUDA 12.1:
    ```
    pip3 install torch torchvision torchaudio
    ```

3. Start application
  - Run:
    ```
    python app.py
    ```






