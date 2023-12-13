# Text-presenter

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
    conda env create --name textpresentor --file environment.yml
    ```
  - Activate:
    ```
    conda activate textpresentor
    ```

2. Start main.py
  - Run:
    ```
    python main.py
    ```