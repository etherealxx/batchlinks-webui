import os
import time
import gradio as gr
from modules import scripts, script_callbacks
import urllib.request, subprocess, contextlib #these handle mega.nz
from IPython.display import clear_output #this also handle mega.nz

typechecker = [
    "embedding", "embeddings", "embed", "embeds",
    "model", "models", "checkpoint", "checkpoints",
    "vae", "vaes",
    "lora", "loras",
    "hypernetwork", "hypernetworks", "hypernet", "hypernets", "hynet", "hynets",
    "addnetlora", "loraaddnet", "additionalnetworks", "addnet"
    ]

newlines = ['\n', '\r\n', '\r']
currentlink = ''
currentfolder = '/content/stable-diffusion-webui/models/Stable-diffusion'

#these code below handle mega.nz
def unbuffered(proc, stream='stdout'):
    stream = getattr(proc, stream)
    with contextlib.closing(stream):
        while True:
            out = []
            last = stream.read(1)
            # Don't loop forever
            if last == '' and proc.poll() is not None:
                break
            while last not in newlines:
                # Don't loop forever
                if last == '' and proc.poll() is not None:
                    break
                out.append(last)
                last = stream.read(1)
            out = ''.join(out)
            yield out

def transfare(todownload, folder):
    import codecs
    decoder = codecs.getincrementaldecoder("UTF-8")()
    cmd = ["mega-get", todownload, folder]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    for line in unbuffered(proc):
      if not line.startswith("Download"):
        print(f"\r{line}", end="")
      else:
        print(f"\n{line}")


def installmega():
  HOME = os.path.expanduser("~")
  if not os.path.exists(f"{HOME}/.ipython/ocr.py"):
      hCode = "https://raw.githubusercontent.com/biplobsd/" \
                  "OneClickRun/master/res/ocr.py"
      urllib.request.urlretrieve(hCode, f"{HOME}/.ipython/ocr.py")

  from ocr import (
      runSh,
      loadingAn,
  )

  if not os.path.exists("/usr/bin/mega-cmd"):
      loadingAn()
      print("Installing MEGA ...")
      runSh('sudo apt-get -y update')
      runSh('sudo apt-get -y install libmms0 libc-ares2 libc6 libcrypto++6 libgcc1 libmediainfo0v5 libpcre3 libpcrecpp0v5 libssl1.1 libstdc++6 libzen0v5 zlib1g apt-transport-https')
      runSh('sudo curl -sL -o /var/cache/apt/archives/MEGAcmd.deb https://mega.nz/linux/MEGAsync/Debian_9.0/amd64/megacmd-Debian_9.0_amd64.deb', output=True)
      runSh('sudo dpkg -i /var/cache/apt/archives/MEGAcmd.deb', output=True)
      print("MEGA is installed.")
      clear_output()
#these code above handle mega.nz

# def updatetext(text):
#     return gr.update(value=text)

# def test():
#     updatetext("one")
#     time.sleep(3)
#     updatetext("two")
#     time.sleep(3)
#     updatetext("three")
#     time.sleep(3)
#     updatetext("four")
#     time.sleep(3)
#     return "done"

def run(command):
    #out = getoutput(f"{command}")
    currentfolder = '/content/stable-diffusion-webui/models/Stable-diffusion'
    links = extract_links(command)
    print(links)
    installmega()
    for listpart in links:
        if listpart.startswith("https://mega.nz") or listpart.startswith("mega.nz"):
            currentlink = listpart
            transfare(currentlink, currentfolder)

        else:
            for prefix in typechecker:
                if listpart.startswith("#" + prefix):
                    if prefix in ["embedding", "embeddings", "embed", "embeds"]:
                        currentfolder = '/content/stable-diffusion-webui/embeddings'
                    elif prefix in ["model", "models", "checkpoint", "checkpoints"]:
                        currentfolder = '/content/stable-diffusion-webui/models/Stable-diffusion'
                    elif prefix in ["vae", "vaes"]:
                        currentfolder = '/content/stable-diffusion-webui/models/VAE'
                    elif prefix in ["lora", "loras"]:
                        currentfolder = '/content/stable-diffusion-webui/models/Lora'
                    elif prefix in ["hypernetwork", "hypernetworks", "hypernet", "hypernets", "hynet", "hynets",]:
                        currentfolder = '/content/stable-diffusion-webui/models/hypernetworks'
                    elif prefix in ["addnetlora", "loraaddnet", "additionalnetworks", "addnet"]:
                        currentfolder = '/content/stable-diffusion-webui/extensions/sd-webui-additional-networks/models/lora'

    return links + "\nall done!"

def extract_links(string):
    links = []
    lines = string.lower().split('\n')
    for line in lines:
        line = line.split('##')[0].strip()
        if line.startswith("https://mega.nz") or line.startswith("mega.nz"):
            links.append(line)
        else:
            for prefix in typechecker:
                if line.startswith("#" + prefix):
                    links.append(line)
    return links

def list_to_text(lst):
    stripped_list = [item.strip(',').strip('\"') for item in lst]
    return '\n'.join(stripped_list)

def uploaded(textpath):
    if not textpath is None:
        print(textpath)
        file_paths = textpath.name
        print(file_paths)
        links = []

        with open(file_paths, 'r') as file:
            for line in file:
                if line.startswith("https://mega.nz") or line.startswith("mega.nz"):
                    links.append(line.strip())
                else:
                    for prefix in typechecker:
                        # print("checking" + prefix) //debug
                        if line.startswith("#" + prefix):
                            links.append(line.strip())

        text = list_to_text(links)
        return text    

def on_ui_tabs():     
    with gr.Blocks() as megalinks:
        gr.Markdown(
        """
        ### 🦒 Colab Run Command
        ```py
        model: wget https://huggingface.co/ckpt/anything-v4.5-vae-swapped/resolve/main/anything-v4.5-vae-swapped.safetensors -O /content/stable-diffusion-webui/models/Stable-diffusion/anything-v4.5-vae-swapped.safetensors
        lora:  wget https://huggingface.co/embed/Sakimi-Chan_LoRA/resolve/main/Sakimi-Chan_LoRA.safetensors -O /content/stable-diffusion-webui/extensions/sd-webui-additional-networks/models/lora/Sakimi-Chan_LoRA.safetensors
        embed: wget https://huggingface.co/embed/EasyNegative/resolve/main/EasyNegative.safetensors -O /content/stable-diffusion-webui/embeddings/EasyNegative.safetensors
        vae:   wget https://huggingface.co/ckpt/trinart_characters_19.2m_stable_diffusion_v1/resolve/main/autoencoder_fix_kl-f8-trinart_characters.ckpt -O /content/stable-diffusion-webui/models/VAE/autoencoder_fix_kl-f8-trinart_characters.vae.pt
        zip outputs folder: zip -r /content/outputs.zip /content/stable-diffusion-webui/outputs
        ```
        """)
        with gr.Group():
            file_output = gr.File(file_types=['text'])
            
            with gr.Box():
                command = gr.Textbox(show_label=False, placeholder="command")
                out_text = gr.Textbox(show_label=False)

                with gr.Row():
                    
                    btn_run = gr.Button("run command")
                    # btn_test = gr.Button("test")
                    btn_run.click(run, inputs=command, outputs=out_text)
                    # btn_test.click(test, outputs=out_text)
                    file_output.change(uploaded, file_output, command)
                    # btn_upload = gr.UploadButton("Upload .txt", file_types="text")
                    # btn_upload.upload(uploaded, btn_upload, file_output)
    return (megalinks, "Megalinks", "megalinks"),
script_callbacks.on_ui_tabs(on_ui_tabs)
