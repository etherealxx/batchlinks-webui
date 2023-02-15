#github.com/etherealxx
import os
from time import sleep
import gradio as gr
from modules import script_callbacks #,scripts
from modules.paths import script_path
from modules.shared import cmd_opts #check for gradio queue
import urllib.request, subprocess, contextlib #these handle mega.nz
import requests #this handle civit
from tqdm import tqdm
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

modelpath = os.path.join(script_path, "models/Stable-diffusion")
embedpath = os.path.join(script_path, "embeddings")
vaepath = os.path.join(script_path, "models/VAE")
lorapath = os.path.join(script_path, "models/Lora")
addnetlorapath = os.path.join(script_path, "extensions/sd-webui-additional-networks/models/lora")
hynetpath = os.path.join(script_path, "models/hypernetworks")

newlines = ['\n', '\r\n', '\r']
currentlink = ''
currentfolder = modelpath
finalwrite = []
currentcondition = ''
logging = False

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
        print('[1;32mInstalling MEGA ...')
        print('[0m')
        ocr.runSh('sudo apt-get -y update')
        ocr.runSh('sudo apt-get -y install libmms0 libc-ares2 libc6 libcrypto++6 libgcc1 libmediainfo0v5 libpcre3 libpcrecpp0v5 libssl1.1 libstdc++6 libzen0v5 zlib1g apt-transport-https')
        ocr.runSh('sudo curl -sL -o /var/cache/apt/archives/MEGAcmd.deb https://mega.nz/linux/MEGAsync/Debian_9.0/amd64/megacmd-Debian_9.0_amd64.deb', output=True)
        ocr.runSh('sudo dpkg -i /var/cache/apt/archives/MEGAcmd.deb', output=True)
        print('[1;32mMEGA is installed.')
        print('[0m')
        #clear_output()
#these code above handle mega.nz

# def updatetext(text):
#     return gr.update(value=text)

def civitdown(url, folder):
    filename = url.rsplit('/', 1)[-1] + ".bdgh"
    pathtodown = os.path.join(folder, filename)
    max_retries = 5
    retry_delay = 10

    while True:

        downloaded_size = 0
        headers = {}

        progress = tqdm(total=1000000000, unit="B", unit_scale=True, desc=f"Downloading {filename}. (will be renamed correctly after downloading)", initial=downloaded_size, leave=False)

        with open(pathtodown, "ab") as f:
            while True:
                try:
                    response = requests.get(url, headers=headers, stream=True)
                    total_size = int(response.headers.get("Content-Length", 0))
                    # if total_size == 0:
                    #     total_size = downloaded_size
                    # progress.total = total_size 

                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            progress.update(len(chunk))

                    downloaded_size = os.path.getsize(pathtodown)
                    break
                except ConnectionError as e:
                    max_retries -= 1

                    if max_retries == 0:
                        raise e

                    sleep(retry_delay)

        progress.close()
        actualfilename = response.headers['Content-Disposition'].split("filename=")[1].strip('"')
        #%cd {folder}
        actualpath = os.path.join(folder, actualfilename)
        os.rename(pathtodown, actualpath)
        downloaded_size = os.path.getsize(actualpath)
        # Check if the download was successful
        if downloaded_size >= total_size:
            print(f"{actualfilename} successfully downloaded.")
            break
        else:
            print(f"Error: File download failed. Retrying...")

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
    print(towritedict)
    global finalwrite
    finalwrite = []
    modelbox, vaebox, lorabox, addnetlorabox, embedbox, hynetbox = [], [], [], [], [], []
    for namefile, namedir in towritedict.items():
        if namedir == modelpath:
            modelbox.append(namefile)
        elif namedir == vaepath:
            vaebox.append(namefile)
        elif namedir == lorapath:
            lorabox.append(namefile)
        elif namedir == addnetlorapath:
            addnetlorabox.append(namefile)
        elif namedir == embedpath:
            embedbox.append(namefile)
        elif namedir == hynetbox:
            hynetbox.append(namefile)

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
    global finalwrite
    if len(box) > 0:
        finalwrite.append("⬇️" + path + "⬇️")
        for item in box:
            finalwrite.append(item)

def run(command, choosedowner):
    #out = getoutput(f"{command}")
    #newfiles = []
    newfilesdict = dict()
    currentfolder = modelpath
    totrack = os.listdir(currentfolder)
    usemega = False
    global currentcondition
    currentcondition = 'Extracting links...'
    links = extract_links(command)
    for item in links:
        if item.startswith('https://mega.nz'):
            usemega = True
            break
    if usemega == True:
        currentcondition = 'Installing Mega...'
        installmega()
    print('[1;32mBatchLinks Downloads starting...')
    print('[0m')
    tocompare, totrack = [], []
    for listpart in links:
        if listpart.startswith("https://mega.nz"):
            currentlink = listpart
            print()
            print(currentlink)
            currentcondition = f'Downloading {currentlink}...'
            transfare(currentlink, currentfolder)
            #sleep(2)
            s = set(totrack)
            trackcompare = [x for x in tocompare if x not in s]
            if len(trackcompare) > 0 and 0 in range(len(trackcompare)):
                newfilesdict[trackcompare[0]] = currentfolder
            totrack = tocompare

        if listpart.startswith("https://huggingface.co"):
            currentlink = listpart
            print()
            print(currentlink)
            currentcondition = f'Downloading {currentlink}...'
            hfdown(currentlink, currentfolder, choosedowner)
            tocompare = os.listdir(currentfolder)
            s = set(totrack)
            trackcompare = [x for x in tocompare if x not in s]
            if len(trackcompare) > 0 and 0 in range(len(trackcompare)):
                newfilesdict[trackcompare[0]] = currentfolder
            totrack = tocompare
            # for filename in tocompare:
            #     if filename not in totrack:
            #         #newfiles.append(filename)
            #         newfilesdict[filename] = currentfolder

        if listpart.startswith("https://civitai.com"):
            currentlink = listpart
            print()
            print(currentlink)
            currentcondition = f'Downloading {currentlink}...'
            civitdown(currentlink, currentfolder)
            tocompare = os.listdir(currentfolder)
            s = set(totrack)
            trackcompare = [x for x in tocompare if x not in s]
            if len(trackcompare) > 0 and 0 in range(len(trackcompare)):
                newfilesdict[trackcompare[0]] = currentfolder
            totrack = tocompare

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
                    #debug
                    #print("totrack")
                    #print(totrack)

    print(newfilesdict)
    currentcondition = 'Writing output...'
    downloadedfiles = writeall(newfilesdict)
    print('[1;32mBatchLinks Downloads finished!')
    print('[0m')
    currentcondition = 'Done!'
    return downloadedfiles

def extract_links(string):
    links = []
    lines = string.split('\n')
    for line in lines:
        line = line.split('##')[0].strip()
        if line.startswith("https://mega.nz") or line.startswith("https://huggingface.co") or line.startswith("https://civitai.com"):
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
                if line.startswith("https://mega.nz") or line.startswith("https://huggingface.co") or line.startswith("https://civitai.com"):
                    links.append(line.strip())
                else:
                    for prefix in typechecker:
                        # print("checking" + prefix) //debug
                        if line.startswith("#" + prefix):
                            links.append(line.strip())

        text = list_to_text(links)
        return text    

# def debug():
#     count = 0
#     while True:
#         print(os.listdir(lorapath))
#         print('time spent: ' + str(count))
#         count +=1
#         sleep(1)
count = 0
def debug():
    # global count
    # count +=1
    # return 'time spent: ' + str(count)
    #if ticked:
    global currentcondition
    global logging
    if logging == False:
        currentcondition = "Logging activated."
        logging = True
    return currentcondition

def empty():
  return ''

def on_ui_tabs():     
    with gr.Blocks() as batchlinks:
        with gr.Row():
          with gr.Column(scale=2):
            gr.Markdown(
            """
            ### ⬇️ Batchlinks Downloader
            This tool will read the textbox and download every links from top to bottom one by one<br/>
            Put your links down below. Supported link: Huggingface, CivitAI, MEGA<br/>
            Use hashtag to separate downloaded items based on their download location<br/>
            Valid hashtags: `#embed`, `#model`,  `#hypernet`, `#lora`, `#vae`, `#addnetlora`, etc.<br/>
            (For colab that uses sd-webui-additional-networks, use `#addnetlora`)<br/>
            Use double hashtag after links for comment
            """)
          with gr.Column(scale=1):
            gr.Markdown(
            """
            [Readme Page](https://github.com/etherealxx/batchlinks-webui)<br/>
            [Example](https://github.com/etherealxx/batchlinks-webui#example)<br/>
            [Syntax](https://github.com/etherealxx/batchlinks-webui#syntax)<br/>
            [Valid Hashtags](https://github.com/etherealxx/batchlinks-webui#valid-hashtags)<br/>
            [Here's how you can get the direct links](https://github.com/etherealxx/batchlinks-webui/blob/main/howtogetthedirectlinks.md)
            """)
        with gr.Group():
          command = gr.Textbox(label="Links", placeholder="type here", lines=5)
          debug_txt = gr.Textbox(label="Log", interactive=False)
          ##this giant mess is because i know nothing about gradio
          #with gr.Row():
            #with gr.Column(scale=1):
              #debug_check = gr.Checkbox(value=False, label="debug")
              #btn_startlog = gr.Button("Start Logging")
              #btn_startlog.click(debug, outputs=debug_txt, every=1)
              #debug_check.change(debug, inputs=debug_check, outputs=debug_txt, every=1)
              #btw_stoplog = gr.Button("Stop Logging")
              #btw_stoplog.click(empty, outputs=debug_txt, cancels=[btn_startlog])
            #debug_txt.blur(debug, outputs=debug_txt, every=1)
            #with gr.Column(scale=4):
              #dummy1 = gr.Textbox("", interactive=False, visible=False)
          with gr.Row():
            with gr.Box():
                #command = gr.Textbox(label="Links", placeholder="type here", lines=5)
                try:
                  if cmd_opts.gradio_queue:
                      logging = gr.Radio(["Turn On Logging"], show_label=False)
                      logging.change(debug, outputs=debug_txt, every=1)
                  else:
                    print("Batchlinks webui extension: (Optional) Use --gradio-queue args to enable logging on the extension")
                except AttributeError:
                  print("Batchlinks webui extension: Your webui fork is outdated, it doesn't support --gradio-queue yet. This extension would still runs fine.")
                  pass
                out_text = gr.Textbox(label="Output")
                choose_downloader = gr.Radio(["gdown", "wget", "curl"], value="gdown", label="Huggingface download method (ignore if you don't understand)")

                with gr.Row():
                    
                    btn_run = gr.Button("Download All!", variant="primary")
                    #btn_debug = gr.Button(debug, output=debug_txt, every=1)
                    btn_run.click(run, inputs=[command, choose_downloader], outputs=out_text)
                    #btn_debug.click(debug, outputs=debug_txt, every=1)
                    # btn_upload = gr.UploadButton("Upload .txt", file_types="text")
                    # btn_upload.upload(uploaded, btn_upload, file_output)
            file_output = gr.File(file_types=['.txt'], label="you can upload a .txt file containing links here")
            file_output.change(uploaded, file_output, command)
        #batchlinks.load(debug, output=debug_txt, every=1)
    return (batchlinks, "Batchlinks Downloader", "batchlinks"),
script_callbacks.on_ui_tabs(on_ui_tabs)
