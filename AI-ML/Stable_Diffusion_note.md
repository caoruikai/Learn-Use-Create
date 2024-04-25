# Stable Diffusion Learning & Working Notes

# Install Automatic 1111 WebUI on Windows with Nvidia Card
1. Launch the Git bash. In the created Stable Diffusion folder: `git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git`
2. Launch the Anaconda prompt, go to the Stable Diffusion folder, then create a conda environment: `conda create -n StableDiffusion python=3.10.6`
3. Activate the conda environment: `conda activate StableDiffusion`
4. Update the line in `webui-user.bat`: `set COMMANDLINE_ARGS=--xformers`.
4. Configurate and launch webui: `webui-user.bat`

# Update Automatic 1111 WebUI on Windows
1. Launch a bash terminal from Windows terminal app
2. Navigate to the webui folder
3. `git pull`

# WebUI

# Checkpoints

# Loras

# Extensions
- infinite image browsing
- Booru tag autocompletion
- Tagger, for prompts inference
- Ultimate SD upscale

# Image2Image
### Inpaining
- Mask should be larger than the potential replacement.

# Tips
- Shape of the images influence the content. For example, width 512 x height 1024 is stand up one person while 1024x512 is bent over. 1024x640 might generate two persons.
- Popular nagative embeddings improve image quality a lot.
- CFG scale not only effect how strongly the image conform to prompts, but also the image quality. Too high CFG may lead to "over-exposed" images.
- More sampling steps == more realistic image
- Most face loras works best for front faces. Lower the weight of the lora for "looking back" view. Do not add glasses.
- Fewer prompting words describing views and poses leads to better quality (easier to generate, less errors?)

# Questions
- Automatic 1111: how to save other parameters than prompts
- Automatic 1111: how to save and view meta data (base model, etc) for models