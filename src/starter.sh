#!/bin/bash

echo "Starting starter.sh"
pip install boto3 rich ultralytics

mkdir /VAE
wget -q -O /stable-diffusion-webui/models/VAE/sdxl_vae.safetensors https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors
cd /stable-diffusion-webui/extensions && git clone https://github.com/Bing-su/adetailer
echo "Starting WebUI API"
python /stable-diffusion-webui/webui.py --no-half-vae --skip-python-version-check --skip-install --skip-torch-cuda-test --ckpt /sd_xl_base_1.0.safetensors --vae-path /stable-diffusion-webui/models/VAE/sdxl_vae.safetensors --lowram --opt-sdp-attention --disable-safe-unpickle --port 3000 --api --nowebui --skip-version-check  --no-hashing --no-download-sd-model --lora-dir /runpod-volume/models/Lora  &

cd /
curl https://raw.githubusercontent.com/lenslessai/worker-a1111/lensless/src/my_utils.py > my_utils.py 
curl https://raw.githubusercontent.com/lenslessai/worker-a1111/lensless/src/rp_handler.py > rp_handler.py  

echo "Starting RunPod Handler"
python -u /rp_handler.py