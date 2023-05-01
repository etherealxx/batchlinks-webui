from modules.shared import cmd_opts
import os, inspect, re #, sys, shlex

script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
batchlinks_dir = os.path.join(script_dir, "batchlinks-downloader.py")

# remove the progress bar if queue off
with open(batchlinks_dir, 'r', encoding='utf-8') as f:
    contents = f.read()

gradio_queue_on = False

try:
  if cmd_opts.gradio_queue: #automatic1111
    gradio_queue_on = True
except AttributeError:
  if not cmd_opts.disable_queue: #vladmandic
    gradio_queue_on = True

if gradio_queue_on:
    #os.system(f"sed -i 's/def run(command, choosedowner):/def run(command, choosedowner, progress=gr.Progress()):/g' {batchlinks_dir}")
    # os.system(f"sed -i '/^#progress/s/^#//' {batchlinks_dir}")
    new_contents = re.sub(r'^(\s*)#progress\(', r'\1progress(', contents, flags=re.MULTILINE)
    contents = re.sub(r'civitvae\):', 'civitvae, progress=gr.Progress()):', new_contents, flags=re.MULTILINE)

    with open(batchlinks_dir, 'w', encoding='utf-8') as f:
        f.write(contents)

else:
    # os.system(f"sed -i 's/def run(command, choosedowner, progress=gr.Progress()):/def run(command, choosedowner):/g' {batchlinks_dir}")
    # os.system(f"sed -i '/^progress(/ s/^/#/' {batchlinks_dir}")
    new_contents = re.sub(r'^(\s*)progress\(', r'\1#progress(', contents, flags=re.MULTILINE)
    contents = re.sub(r'civitvae,\s*progress=gr\.Progress\(\)\):$', 'civitvae):', new_contents, flags=re.MULTILINE)

    with open(batchlinks_dir, 'w', encoding='utf-8') as f:
        f.write(contents)