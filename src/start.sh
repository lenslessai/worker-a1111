#!/bin/bash

echo "Worker Initiated"

echo "Starting WebUI API"
python /stable-diffusion-webui/webui.py --skip-python-version-check --skip-install --skip-torch-cuda-test --ckpt /model.safetensors --lowram --opt-sdp-attention --disable-safe-unpickle --port 3000 --api --nowebui --skip-version-check  --no-hashing --no-download-sd-model --lora-dir /runpod-volume/models/Lora  &

echo "Starting RunPod Handler"
python -u /rp_handler.py
