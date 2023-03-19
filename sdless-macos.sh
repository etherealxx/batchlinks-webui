#!/usr/bin/env bash
pip3 show virtualenv >/dev/null || pip3 install -q virtualenv
[ -d gradiovenv ] || virtualenv gradiovenv
source gradiovenv/bin/activate; \
pip3 show gradio >/dev/null || pip3 install -q gradio==3.16.2
source gradiovenv/bin/activate; \
python3 scripts/batchlinks-downloader.py