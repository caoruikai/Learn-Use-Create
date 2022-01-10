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

## Add & Prioritize NVIDIA Repository
1. Download the pin file to prioritize the nvidia source when install packages: `wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin`
2. Move the pin file to `apt` preference folder to make it effective: `sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600`
3. Add nvidia apt repository: `sudo apt-add-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"`
4. Update `apt` source list: `sudo apt update`

## Install NVIDIA driver
1. Check graphic card & available drivers: `ubuntu-drivers devices`
2. For GeForce GTX 970, install the recommended driver: `sudo apt install nvidia-driver-495`.
3. Reboot after installation: `sudo reboot`.
4. Check the status after the reboot: `nvidia-smi`.

## Install CUDA
1. Check `GCC` version: `gcc --version`. (CUDA 11.0 requires `GCC` 9.x on Ubuntu 20.04) It should already be handled when the driver was installed.
2. Check kernels: `uname -r`. Make sure the kernels header and the development packages are installed. Every time the linux kernel is updated, it is good practice to run `sudo apt install linux-headers-$(uname -r)` to install those for the current kernel. Otherwise CUDA may break.
3. Download machine learning deb: `wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/nvidia-machine-learning-repo-ubuntu2004_1.0.0-1_amd64.deb`
4. Install `.deb` package: `sudo apt install ./nvidia-machine-learning-repo-ubuntu2004_1.0.0-1_amd64.deb`.
5. Update `apt` list: `sudo apt update`.
6. Install CUDA 11.0 & cuDNN SDK 8.0: `sudo apt install --no-install-recommends cuda-11-0=11.0.3-1 libcudnn8=8.0.5.39-1+cuda11.0 libcudnn8-dev=8.0.5.39-1+cuda11.0`.
7. Reboot
8. (Optional) Install TensorRT to reduce latency: `sudo apt install --no-install-recommends libnvinfer8=8.0.0-1+cuda11.0 libnvinfer-dev=8.0.0-1+cuda11.0 libnvinfer-plugin8=8.0.0-1+cuda11.0`.

## Drop the NVIDIA Repo from the APT list (To prevent version changes)
1. Move the pin file out of the preference folder: `sudo mv /etc/apt/preferences.d/cuda-repository-pin-600 ~/backups/cuda-repository-pin-600`
2. Drop the NVIDIA repo from the source list: `sudo apt-add-repository --remove "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"`
3. Drop the NVIDIA ML repo from the source list: `sudo apt-add-repository --remove "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64 /"`
3. Update the list: `sudo apt update`



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
