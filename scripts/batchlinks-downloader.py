import os
import time
import gradio as gr
from modules import scripts, script_callbacks
import urllib.request, subprocess, contextlib #these handle mega.nz
#from IPython.display import display, clear_output
from pathlib import Path

typechecker = [
    "embedding", "embeddings", "embed", "embeds",
    "model", "models", "checkpoint", "checkpoints",
    "vae", "vaes",
    "lora", "loras",
    "hypernetwork", "hypernetworks", "hypernet", "hypernets", "hynet", "hynets",
    "addnetlora", "loraaddnet", "additionalnetworks", "addnet"
    ]

modelpath = "/content/stable-diffusion-webui/models/Stable-diffusion"
embedpath = "/content/stable-diffusion-webui/embeddings"
vaepath = "/content/stable-diffusion-webui/models/VAE"
lorapath = "/content/stable-diffusion-webui/models/Lora"
addnetlorapath = "/content/stable-diffusion-webui/extensions/sd-webui-additional-networks/models/lora"
hynetpath = "/content/stable-diffusion-webui/models/hypernetworks"

newlines = ['\n', '\r\n', '\r']
currentlink = ''
currentfolder = modelpath
finalwrite = []

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
    ocr_file = Path(f"{HOME}/.ipython/ocr.py")
    if not ocr_file.exists():
        hCode = "https://raw.githubusercontent.com/biplobsd/" \
                    "OneClickRun/master/res/ocr.py"
        urllib.request.urlretrieve(hCode, str(ocr_file))

    from importlib.util import module_from_spec, spec_from_file_location
    ocr_spec = spec_from_file_location("ocr", str(ocr_file))
    ocr = module_from_spec(ocr_spec)
    ocr_spec.loader.exec_module(ocr)

    if not os.path.exists("/usr/bin/mega-cmd"):
        #ocr.loadingAn()
        print("Installing MEGA ...")
        ocr.runSh('sudo apt-get -y update')
        ocr.runSh('sudo apt-get -y install libmms0 libc-ares2 libc6 libcrypto++6 libgcc1 libmediainfo0v5 libpcre3 libpcrecpp0v5 libssl1.1 libstdc++6 libzen0v5 zlib1g apt-transport-https')
        ocr.runSh('sudo curl -sL -o /var/cache/apt/archives/MEGAcmd.deb https://mega.nz/linux/MEGAsync/Debian_9.0/amd64/megacmd-Debian_9.0_amd64.deb', output=True)
        ocr.runSh('sudo dpkg -i /var/cache/apt/archives/MEGAcmd.deb', output=True)
        print("MEGA is installed.")
        #clear_output()
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
def hfdown(todownload, folder, downloader):
    filename = todownload.rsplit('/', 1)[-1]
    if downloader=='gdown':
        os.system(f"gdown {todownload} -O " + os.path.join(folder, filename))
    elif downloader=='wget':
        os.system(f"wget {todownload} -P {folder}")
    elif downloader=='curl':
        os.system(f"curl -Lo {filename} {todownload}")
        curdir = os.getcwd()
        os.rename(os.path.join(curdir, filename), os.path.join(folder, filename))

def writeall(towritedict):
    finalwrite = []
    modelbox, vaebox, lorabox, addnetlorabox, embedbox, hynetbox = [], [], [], [], [], []
    for file, dir in towritedict.items():
        if dir == modelpath:
            modelbox.append(file)
        elif dir == vaepath:
            vaebox.append(file)
        elif dir == lorapath:
            lorabox.append(file)
        elif dir == addnetlorapath:
            addnetlorabox.append(file)
        elif dir == embedpath:
            embedbox.append(file)
        elif dir == hynetbox:
            hynetbox.append(file)

    finalwrite.append("All done!")
    finalwrite.append("Downloaded files: ")

    writepart(modelbox, modelpath)
    writepart(vaebox, vaepath)
    writepart(lorabox, lorapath)
    writepart(addnetlorabox, addnetlorapath)
    writepart(embedbox, embedpath)
    writepart(hynetbox, hynetbox)

    finaloutput = list_to_text(finalwrite)
    finalwrite = []
    return finaloutput

def writepart(box, path):
    if len(box) > 0:
        finalwrite.append("⬇️" + path + "⬇️")
        for item in box:
            finalwrite.append(item)

def run(command, choosedowner):
    #out = getoutput(f"{command}")
    newfiles = []
    newfilesdict = dict()
    currentfolder = modelpath
    totrack = os.listdir(currentfolder)
    links = extract_links(command)
    installmega()
    for listpart in links:
        if listpart.startswith("https://mega.nz"):
            currentlink = listpart
            print()
            print(currentlink)
            transfare(currentlink, currentfolder)
            tocompare = os.listdir(currentfolder)
            for filename in tocompare:
                if filename not in totrack:
                    #newfiles.append(filename)
                    newfilesdict[filename] = currentfolder

        if listpart.startswith("https://huggingface.co"):
            currentlink = listpart
            print()
            print(currentlink)
            hfdown(currentlink, currentfolder, choosedowner)
            for filename in tocompare:
                if filename not in totrack:
                    #newfiles.append(filename)
                    newfilesdict[filename] = currentfolder

        else:
            for prefix in typechecker:
                if listpart.startswith("#" + prefix):
                    if prefix in ["embedding", "embeddings", "embed", "embeds"]:
                        currentfolder = embedpath
                    elif prefix in ["model", "models", "checkpoint", "checkpoints"]:
                        currentfolder = modelpath
                    elif prefix in ["vae", "vaes"]:
                        currentfolder = vaepath
                    elif prefix in ["lora", "loras"]:
                        currentfolder = lorapath
                    elif prefix in ["hypernetwork", "hypernetworks", "hypernet", "hypernets", "hynet", "hynets",]:
                        currentfolder = hynetpath
                    elif prefix in ["addnetlora", "loraaddnet", "additionalnetworks", "addnet"]:
                        currentfolder = addnetlorapath
                    os.makedirs(currentfolder, exist_ok=True)
                    print(currentfolder)
                    totrack = os.listdir(currentfolder)
    
    downloadedfiles = writeall(newfilesdict)

    return downloadedfiles

def extract_links(string):
    links = []
    lines = string.split('\n')
    for line in lines:
        line = line.split('##')[0].strip()
        if line.startswith("https://mega.nz"):
            links.append(line)
        if line.startswith("https://huggingface.co"):
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
    with gr.Blocks() as batchlinks:
        gr.Markdown(
        """
        ### ⬇️ Batchlinks Downloader
        this tool will read the textbox and download every links from top to bottom one by one<br/>
        put your links down below. Supported link: MEGA, Huggingface<br/>
        use hashtag to separate downloaded items based on their download location<br/>
        valid hashtags: `#embed`, `#model`,  `#hypernet`, `#lora`, `#vae`, `#addnetlora`, etc.<br/>
        (For colab that uses sd-webui-additional-networks, use `#addnetlora`)<br/>
        use double hashtag after links for comment
        """)
        with gr.Group():
          with gr.Row():
            with gr.Box():
                command = gr.Textbox(label="Links", placeholder="type here", lines=5)
                out_text = gr.Textbox(label="Output")
                choose_downloader = gr.Radio(["gdown", "wget", "curl"], value="gdown", label="Huggingface download method (ignore if you don't understand)")

                with gr.Row():
                    
                    btn_run = gr.Button("Download All!")
                    # btn_test = gr.Button("test")
                    btn_run.click(run, inputs=[command, choose_downloader], outputs=out_text)
                    # btn_test.click(test, outputs=out_text)
                    # btn_upload = gr.UploadButton("Upload .txt", file_types="text")
                    # btn_upload.upload(uploaded, btn_upload, file_output)
            file_output = gr.File(file_types=['.txt'], label="you can upload a .txt file containing links here")
            file_output.change(uploaded, file_output, command)
    return (batchlinks, "Batchlinks Downloader", "batchlinks"),
script_callbacks.on_ui_tabs(on_ui_tabs)
