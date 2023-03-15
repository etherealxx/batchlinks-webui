#!/usr/bin/env bash
pip3 show virtualenv >/dev/null || pip3 install virtualenv
[ -d gradiovenv ] || virtualenv gradiovenv
git clone -b sdless https://github.com/etherealxx/batchlinks-webui \
$HOME/Downloads/stable-diffusion-webui/extensions/batchlinks-webui
source gradiovenv/bin/activate; \
pip3 show gradio >/dev/null || pip3 install gradio==3.16.2
source gradiovenv/bin/activate; \
python3 $HOME/Downloads/stable-diffusion-webui/extensions/batchlinks-webui/scripts/batchlinks-downloader.py