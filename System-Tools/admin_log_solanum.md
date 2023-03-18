# System Configuration
1. Update hostname
    1. `sudo hostnamectl set-hostname <hostname>`
    2. Update the file `/etc/hosts` to match the new hostname.
2. Assign a fixed IP address in the DHCP(router)




# Install & Configure Useful Packages
- vim: `sudo apt install vim`
- htop: `sudo apt install htop` 2022-01-09
- OpenSSH: client and server. See "OpenSSH" section in linux_ubuntu_note.md for details.
- git: `sudo apt install git` 2022-01-09
    - Config: `git config --global user.name "tsaork"`; `git config --global user.email tsaork@gmail.com`
    - Key pairs to push to github: `ssh-keygen -t ed25519 -C "tsaork@gmail.com"` and copy the `.pub` content to github.com




# Install packages from NVIDIA 2022-01-08
- Versions:
    - TensorFlow 2.4
    - CUDA 11.0
    - cuDNN 8.0
    - TensorRT 8

## References
- [TensorFlow Documentation Page](https://www.tensorflow.org/install/gpu#install_cuda_with_apt)
- [TensorFlow Tested GPU Build Configuration](https://www.tensorflow.org/install/source#gpu)
- [CUDA Toolkit 11.0 Documentation](https://docs.nvidia.com/cuda/archive/11.0/)
- [CUDA Toolkit 11.0 Installation Guide](https://docs.nvidia.com/cuda/archive/11.0/cuda-installation-guide-linux/index.html)
- [NVIDIA CUDA Repository for Ubuntu 20.04 x86_64](https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/)
- [NVIDIA Machine Learning Repository for Ubuntu 20.04 x86_64](https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/)

## Preparations
1. Check which graphic card was installed: `lspci | grep -i nvidia`
2. Check system info: `uname -m && cat /etc/*release`

## ~~Add & Prioritize NVIDIA Repository~~
1. ~~Download the pin file to prioritize the nvidia source when install packages: `wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin`~~
2. ~~Move the pin file to `apt` preference folder to make it effective: `sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600`~~
3. ~~Add nvidia apt repository: `sudo apt-add-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"`~~
4. ~~Update `apt` source list: `sudo apt update`~~

## Install NVIDIA driver
1. Check graphic card & available drivers: `ubuntu-drivers devices`
2. For GeForce GTX 970, install the recommended driver: `sudo apt install nvidia-driver-495`.
3. Reboot after installation: `sudo reboot`.
4. Check the status after the reboot: `nvidia-smi`.

## ~~Install CUDA~~
1. ~~Check `GCC` version: `gcc --version`. (CUDA 11.0 requires `GCC` 9.x on Ubuntu 20.04) It should already be handled when the driver was installed.~~
2. ~~Check kernels: `uname -r`. Make sure the kernels header and the development packages are installed. Every time the linux kernel is updated, it is good practice to run `sudo apt install linux-headers-$(uname -r)` to install those for the current kernel. Otherwise CUDA may break.~~
3. ~~Download machine learning deb: `wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/nvidia-machine-learning-repo-ubuntu2004_1.0.0-1_amd64.deb`~~
4. ~~Install `.deb` package: `sudo apt install ./nvidia-machine-learning-repo-ubuntu2004_1.0.0-1_amd64.deb`.~~
5. ~~Update `apt` list: `sudo apt update`.~~
6. ~~Install CUDA 11.0 & cuDNN SDK 8.0: `sudo apt install --no-install-recommends cuda-11-0=11.0.3-1 libcudnn8=8.0.5.39-1+cuda11.0 libcudnn8-dev=8.0.5.39-1+cuda11.0`.~~
7. ~~Reboot~~
8. ~~(Optional) Install TensorRT to reduce latency: `sudo apt install --no-install-recommends libnvinfer8=8.0.0-1+cuda11.0 libnvinfer-dev=8.0.0-1+cuda11.0 libnvinfer-plugin8=8.0.0-1+cuda11.0`.~~

## ~~Drop the NVIDIA Repo from the APT list (To prevent version changes)~~
1. ~~Move the pin file out of the preference folder: `sudo mv /etc/apt/preferences.d/cuda-repository-pin-600 ~/backups/cuda-repository-pin-600`~~
2. ~~Drop the NVIDIA repo from the source list: `sudo apt-add-repository --remove "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"`~~
3. ~~Drop the NVIDIA ML repo from the source list: `sudo apt-add-repository --remove "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64 /"`~~
3. ~~~~



# Install Data Science & Machine Learning Packages 2022-01-09

## Install and create a `virtualenv` for Python 3.8 on Ubuntu 20.04
1. Add `universe` apt repository: `sudo apt-add-repository universe` (DO NOT change the `/etc/apt/source.list` file directly).
2. Install `python3.8-venv`: `sudo apt install python3.8-venv`.
3. Create a virtualenv: `python3 -m venv ds-ml`
4. Activate virtualenv: `source ~/ds-ml/bin/activate`.
5. Use `pip` to install packages: `python -m pip install -U <packages>`
6. Deactivate the virtualenv: `deactivate`.

## Install Packages
1. Activate the virtualenv: `source ~/ds-ml/bin/activate`
2. Check the installed packages: `pip list`
3. Install `wheel` package: `python -m pip install -U pip setuptools wheel`
4. Install the packages: `python -m pip install -U tensorflow==2.4 xgboost scikit-learn numpy==1.19.2 scipy pandas matplotlib seaborn spacy[cuda110,transformers,lookups] gensim jupyterlab`
5. Install spaCy models: `python -m spacy download en_core_web_trf`, `python -m spacy download zh_core_web_trf`
6. Configurate and access JupyterLab
    1. `jupyter lab --generate-config`
    2. `vim ~/.jupyter/jupyter_lab_config.py`
    3. Add a line: `c.NotebookApp.port = <jupyter-port-number>`
    4. Run the jupyter lab: `jupyter lab`
    5. Open another terminal on local client, and use SSH to tunnel: `ssh -L <local-port-number>:localhost:<jupyter-port-number> tsaork@solanum`
    6. Copy the JupyterLab url and past in in a brower.

# CUDA: Uninstall & Upgrade for PyTorch 2.0 2023-03-16

## Uninstall CUDA

### 2 Versions of CUDA
- `nvidia-smi` shows the CUDA installed with the driver.
- `nvcc --version` shows the CUDA runtime installed.
- The 2 CUDAs above are irrelavent, however, the following way of upgrading will upgrade both.
- To use CUDA 11.7 or 11.8 with PyTorch 2.0, correct version of `nvcc` needs to be installed.

### Uninstall previous CUDA runtime `nvcc`
1. Check installed package by `apt-cache search <package-name>`
2. Unistall CUDA related packages by `sudo apt-get --purge remove "*cublas*" "cuda*" "nsight*"`
3. Clean up the remaining files by `sudo rm -rf /usr/local/cuda*`
4. Remove unnecessary package files by `sudo apt autoremove`

## Install NVIDIA driver (if not installed)
1. Check graphic card & available drivers: `ubuntu-drivers devices`
2. For GeForce GTX 970, install the recommended driver: `sudo apt install nvidia-driver-495`.
3. Reboot after installation: `sudo reboot`.
4. Check the status after the reboot: `nvidia-smi`.

## Install newer version of CUDA
- Adding `.pin` file is unnecessary because the two packages `nsight-compute` and `nsight-system` suppressed in the `.pin` file are NOT found in the Ubuntu apt repository.
1. Download CUDA 11.7 and cuDNN with compatible version (and all dependencies)
    ```bash
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcudnn8-dev_8.5.0.96-1+cuda11.7_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcudnn8_8.5.0.96-1+cuda11.7_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-runtime-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-toolkit-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-demo-suite-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-libraries-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-libraries-dev-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-compiler-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-tools-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-documentation-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nvml-dev-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-cuobjdump-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-cuxxfilt-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nvcc-11-7_11.7.99-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nvprune-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-cudart-11-7_11.7.99-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-cudart-dev-11-7_11.7.99-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nvrtc-11-7_11.7.99-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nvrtc-dev-11-7_11.7.99-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcublas-11-7_11.10.3.66-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcublas-dev-11-7_11.10.3.66-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcufft-11-7_10.7.2.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcufft-dev-11-7_10.7.2.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcufile-11-7_1.3.1.18-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcufile-dev-11-7_1.3.1.18-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcurand-11-7_10.2.10.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcurand-dev-11-7_10.2.10.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcusolver-11-7_11.4.0.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcusolver-dev-11-7_11.4.0.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcusparse-11-7_11.7.4.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcusparse-dev-11-7_11.7.4.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnpp-11-7_11.7.4.75-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnpp-dev-11-7_11.7.4.75-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnvjpeg-11-7_11.8.0.2-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnvjpeg-dev-11-7_11.8.0.2-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-cccl-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-driver-dev-11-7_11.7.99-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-command-line-tools-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-visual-tools-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/gds-tools-11-7_1.3.1.18-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-cupti-11-7_11.7.101-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-cupti-dev-11-7_11.7.101-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-gdb-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-memcheck-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nvdisasm-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nvprof-11-7_11.7.101-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nvtx-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-sanitizer-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-toolkit-config-common_11.7.99-1_all.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-toolkit-11-7-config-common_11.7.99-1_all.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-toolkit-11-config-common_11.7.99-1_all.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nsight-compute-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nsight-11-7_11.7.91-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nvvp-11-7_11.7.101-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-nsight-systems-11-7_11.7.1-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-drivers-515_515.65.01-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/nsight-compute-2022.2.1_2022.2.1.3-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnvidia-common-515_515.65.01-0ubuntu1_all.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnvidia-compute-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnvidia-decode-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnvidia-encode-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnvidia-fbc1-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnvidia-gl-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/nvidia-compute-utils-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/nvidia-dkms-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/nvidia-driver-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/nvidia-kernel-common-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/nvidia-kernel-source-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/nvidia-modprobe_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/nvidia-settings_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/nvidia-utils-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/xserver-xorg-video-nvidia-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/nsight-systems-2022.1.3_2022.1.3.3-1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnvidia-extra-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnvidia-cfg1-515_515.65.01-0ubuntu1_amd64.deb
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-drivers_515.65.01-1_amd64.deb
    ```
2. Install `libtinfo5`
    ```bash
    sudo add-apt-repository universe
    sudo apt install libtinfo5
    sudo add-apt-repository --remove universe
    ```
3. Install CUDA and all dependencies: `sudo apt install --no-install-recommends ~/Downloads/CUDA-11-7-install/*.deb`
4. Reboot `sudo shutdown`

## Install PyTorch
1. Create a virtualenv: `python3 -m venv pytorch-venv`
2. Activate the venv: `source ~/pytorch-venv/bin/activate`
3. Install `wheel`: `pip install wheel`
3. Install packages `python -m pip install -U torch torchvision torchaudio torchtext xgboost scikit-learn numpy pandas scipy matplotlib seaborn spacy[cuda-autodetect] jupyterlab`