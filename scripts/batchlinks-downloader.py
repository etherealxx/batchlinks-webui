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
import inspect
import platform
from shlex import quote

script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
extension_dir = os.path.abspath(os.path.join(script_dir, "../"))
#Version checking{
version_dir = os.path.join(extension_dir, "version.txt")
with open(version_dir, 'r', encoding='utf-8') as file:
    curverall = file.readlines()
currentversion = curverall[0].strip()

try:
    versionurl = "https://raw.githubusercontent.com/etherealxx/batchlinks-webui/main/version.txt"
    versionresp = requests.get(versionurl)
    version_lines = versionresp.text.splitlines()
    latestversion = version_lines[0].strip()
except requests.exceptions.RequestException:
    latestversion = '??'

if latestversion != '??':
    if currentversion == latestversion:
        latestversiontext = ""
    else:
        latestversiontext = f"[Latest version: {latestversion}]"
else:
    latestversiontext = ""
#}

try:
    global gradiostate
    if cmd_opts.gradio_queue:
        gradiostate = True
    else:
        gradiostate = False
except AttributeError:
    gradiostate = False
    pass

typechecker = [
    "embedding", "embeddings", "embed", "embeds",
    "model", "models", "checkpoint", "checkpoints",
    "vae", "vaes",
    "lora", "loras",
    "hypernetwork", "hypernetworks", "hypernet", "hypernets", "hynet", "hynets",
    "addnetlora", "loraaddnet", "additionalnetworks", "addnet",
    "controlnet", "cnet",
    "extension", "extensions", "ext"
    ]

modelpath = os.path.join(script_path, "models/Stable-diffusion")
embedpath = os.path.join(script_path, "embeddings")
vaepath = os.path.join(script_path, "models/VAE")
lorapath = os.path.join(script_path, "models/Lora")
addnetlorapath = os.path.join(script_path, "extensions/sd-webui-additional-networks/models/lora")
hynetpath = os.path.join(script_path, "models/hypernetworks")
cnetpath = os.path.join(script_path, "extensions/sd-webui-controlnet/models")
extpath = os.path.join(script_path, "extensions")

if platform.system() == "Windows":
    typemain = ["model", "vae", "embed", "hynet", "lora", "addnetlora", "cnet", "ext"]
    for x in typemain:
        exec(f"{x}path = {x}path.replace('/', '\\\\')")
        #exec(f"print({x}path)")

newlines = ['\n', '\r\n', '\r']
currentlink = ''
currentfolder = modelpath
finalwrite = []
currentcondition = ''
currentsuboutput = ''
logging = False

def runwithsubprocess(rawcommand):
    def construct_command(command_string):
        # Split the command string into a list of arguments
        command_parts = command_string.split()

        # Loop through the list of arguments and convert any quoted strings into single arguments
        # This allows arguments with spaces to be correctly split into separate arguments
        new_command_parts = []
        quote_started = False
        for part in command_parts:
            if part.startswith('"'):
                quote_started = True
                new_part = part[1:]
            elif part.endswith('"'):
                quote_started = False
                new_part = new_command_parts[-1] + " " + part[:-1]
                new_command_parts[-1] = new_part
            elif quote_started:
                new_part = new_command_parts[-1] + " " + part
                new_command_parts[-1] = new_part
            else:
                new_command_parts.append(part)

        # Return the list of arguments as a command and arguments list
        return new_command_parts

    currentprocess = ''

    commandtorun = construct_command(rawcommand)
    if gradiostate == False and not rawcommand.startswith("aria"):
        subprocess.run(commandtorun, stderr=subprocess.STDOUT, universal_newlines=True)
    else:
        process = subprocess.Popen(commandtorun, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        ariacomplete = False
        global currentsuboutput
        while True:
            # Read the output from the process
            nextline = process.stdout.readline()
            if nextline == '' and process.poll() is not None:
                break
            # Check if the line contains progress information
            if "%" in nextline.strip() or rawcommand.startswith("curl"):#"INFO" in nextline.strip() or "NOTICE" in nextline.strip():
            # if loadingprogress == False:
                #     print('[1;32mThe progress bar is on the logging box in the UI')
                #     print('[0m')
                # loadingprogress = True
                #print(nextline, end='\r')
                # sys.stdout.write('\r' + nextline)
                # sys.stdout.flush()
                stripnext = nextline.strip()
                print("\r", end="")
                print(f"\r{stripnext}", end='')
            elif rawcommand.startswith("aria2"):
                if "Download complete" in nextline.strip():
                    ariacomplete = True
                    print(nextline, end='')
                else:
                    if ariacomplete == False:
                        stripnext = nextline.strip()
                        print("\r", end="")
                        print(f"\r{stripnext}", end='')
                    else:
                        print(nextline, end='')
            else:
                # loadingprogress = False
                print(nextline, end='')
            currentsuboutput = nextline

        process.wait()
        currentsuboutput = ''

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
    #import codecs
    #decoder = codecs.getincrementaldecoder("UTF-8")()
    todownload_s = quote(todownload)
    folder_s = quote(folder)
    if platform.system() == "Windows":
        localappdata = os.environ['LOCALAPPDATA']
        megagetloc = os.path.join(quote(localappdata), "MEGAcmd", "mega-get.bat")
        runwithsubprocess(f"{megagetloc} {todownload_s} {folder_s}")
    else:
        cmd = ["mega-get", todownload_s, folder_s]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        global currentsuboutput
        for line in unbuffered(proc):
            if not line.startswith("Download"):
                currentsuboutput = line
                print(f"\r{line}", end="")
            else:
                print(f"\n{line}")
        currentsuboutput = ''

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

def installmegawin():
    userprofile = os.environ['USERPROFILE']
    localappdata = os.environ['LOCALAPPDATA']
    megagetloc = os.path.join(quote(localappdata), "MEGAcmd", "mega-get.bat")
    megacmdloc = os.path.join(quote(userprofile), "Downloads", "MEGAcmdSetup64.exe")
    if not os.path.exists(megagetloc):
        print('[1;32mInstalling MEGA ...')
        print('[0m')
        runwithsubprocess(f"curl -o {megacmdloc} https://mega.nz/MEGAcmdSetup64.exe")
        sleep(1)
        runwithsubprocess(f"{megacmdloc} /S")
        sleep(4)
        print('[1;32mMEGA is installed.')
        print('[0m')
        #clear_output()
#these code above handle mega.nz

def civitdown(url, folder):
    filename = url.rsplit('/', 1)[-1] + ".bdgh"
    pathtodown = os.path.join(folder, filename)
    max_retries = 5
    retry_delay = 10
    url_s = quote(url)

    while True:

        downloaded_size = 0
        headers = {}

        progress = tqdm(total=1000000000, unit="B", unit_scale=True, desc=f"Downloading {filename}. (will be renamed correctly after downloading)", initial=downloaded_size, leave=False)
        global currentsuboutput
                
        with open(pathtodown, "ab") as f:
            while True:
                try:
                    response = requests.get(url_s, headers=headers, stream=True)
                    total_size = int(response.headers.get("Content-Length", 0))
                    # if total_size == 0:
                    #     total_size = downloaded_size
                    # progress.total = total_size 

                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            progress.update(len(chunk))
                            currentsuboutput = str(progress)

                    downloaded_size = os.path.getsize(pathtodown)
                    currentsuboutput = ''
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
    filename = quote(todownload.rsplit('/', 1)[-1])
    filepath = quote(os.path.join(folder, filename))
    todownload_s = quote(todownload)
    folder_s = quote(folder)
    if platform.system() == "Windows":
        if downloader=='gdown':
            import gdown
            gdown.download(todownload_s, filepath, quiet=False)
        elif downloader=='wget':
            #os.system("python -m wget -o " + os.path.join(folder, filename) + " " + todownload)
            import wget
            wget.download(todownload_s, filepath)
        elif downloader=='curl':
            runwithsubprocess(f"curl -Lo {filepath} {todownload_s}")
    else:
        if downloader=='gdown':
            runwithsubprocess(f"gdown {todownload_s} -O {filepath}")
        elif downloader=='wget':
            runwithsubprocess(f"wget {todownload_s} -P {folder_s}")
        elif downloader=='curl':
            runwithsubprocess(f"curl -Lo {filename} {todownload_s}")
            curdir = os.getcwd()
            os.rename(os.path.join(curdir, filename), filepath)
        elif downloader=='aria2':
            ariachecker = "dpkg-query -W -f='${Status}' aria2"
            checkaria = subprocess.getoutput(ariachecker)
            if "no packages found matching aria2" in checkaria:
                global currentcondition
                tempcondition = currentcondition
                currentcondition = "Installing aria2..."
                print('[1;32mInstalling aria2 ...')
                print('[0m')
                runwithsubprocess(f"apt-get -y install -qq aria2")
                print('[1;32maria2 installed!')
                print('[0m')
                currentcondition = tempcondition
            runwithsubprocess(f"aria2c --console-log-level=info -c -x 16 -s 16 -k 1M {todownload_s} -d {folder_s} -o {filename}")

def writeall(olddict):
    newdict = trackall()
    global finalwrite
    finalwrite = []

    finalwrite.append("All done!")
    finalwrite.append("Downloaded files: ")
    for oldtype, olddir in olddict.items():
        for newtype, newdir in newdict.items():
            if newtype == oldtype:
                s = set(olddir)
                trackcompare = [x for x in newdir if x not in s]
                if len(trackcompare) > 0:
                    exec(f"finalwrite.append('⬇️' + {newtype}path + '⬇️')")
                    for item in trackcompare:
                        finalwrite.append(item)

    finaloutput = list_to_text(finalwrite)
    finalwrite = []
    return finaloutput

def writepart(box, path):
    global finalwrite
    if len(box) > 0:
        finalwrite.append("⬇️" + path + "⬇️")
        for item in box:
            finalwrite.append(item)

def trackall():
    typemain = ["model", "vae", "embed", "hynet", "lora", "addnetlora", "cnet", "ext"]
    filesdict = dict()
    for x in typemain:
        exec(f"os.makedirs({x}path, exist_ok=True)")
        exec(f"filesdict['{x}'] = os.listdir({x}path)")
    return filesdict

def run(command, choosedowner):
    oldfilesdict = trackall()
    currentfolder = modelpath
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
        if platform.system() == "Windows":
            installmegawin()
        else:
            installmega()
    print('[1;32mBatchLinks Downloads starting...')
    print('[0m')
    for listpart in links:
        if listpart.startswith("https://mega.nz"):
            currentlink = listpart
            print()
            print(currentlink)
            currentcondition = f'Downloading {currentlink}...'
            transfare(currentlink, currentfolder)

        if listpart.startswith("https://huggingface.co") or listpart.startswith("https://cdn.discordapp.com/attachments"):
            currentlink = listpart
            print()
            print(currentlink)
            currentcondition = f'Downloading {currentlink}...'
            hfdown(currentlink, currentfolder, choosedowner)

        if listpart.startswith("https://civitai.com/api/download/models/"):
            currentlink = listpart
            print()
            print(currentlink)
            currentcondition = f'Downloading {currentlink}...'
            civitdown(currentlink, currentfolder)

        if listpart.startswith("https://github.com"):
            splits = listpart.split("/")
            currentlink = "/".join(splits[:5])
            foldername = quote(listpart.rsplit('/', 1)[-1])
            folderpath = quote(os.path.join(extpath, foldername))
            print()
            print(currentlink)
            currentcondition = f'Cloning {currentlink}...'
            runwithsubprocess(f"git clone {currentlink} {folderpath}")

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
                    elif prefix in ["controlnet", "cnet"]:
                        currentfolder = cnetpath
                    os.makedirs(currentfolder, exist_ok=True)

    currentcondition = 'Writing output...'
    downloadedfiles = writeall(oldfilesdict)
    print()
    print('[1;32mBatchLinks Downloads finished!')
    print('[0m')
    currentcondition = 'Done!'
    return downloadedfiles

def extract_links(string):
    links = []
    lines = string.split('\n')
    for line in lines:
        line = line.split('##')[0].strip()
        if line.startswith("https://mega.nz") or line.startswith("https://huggingface.co") or line.startswith("https://civitai.com/api/download/models/") or line.startswith("https://cdn.discordapp.com/attachments") or line.startswith("https://github.com"):
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
                if line.startswith("https://mega.nz") or line.startswith("https://huggingface.co") or line.startswith("https://civitai.com/api/download/models/") or line.startswith("https://cdn.discordapp.com/attachments") or line.startswith("https://github.com"):
                    links.append(line.strip())
                else:
                    for prefix in typechecker:
                        if line.startswith("#" + prefix):
                            links.append(line.strip())

        text = list_to_text(links)
        return text    

count = 0
def keeplog():
    global currentcondition
    global currentsuboutput
    global logging
    if logging == False:
        currentcondition = "Logging activated."
        logging = True
    if currentsuboutput == '':
        return currentcondition
    else:
        return f"{currentcondition}\n{currentsuboutput}"

def empty():
  return ''

def on_ui_tabs():     
    with gr.Blocks() as batchlinks:
        with gr.Row():
          with gr.Column(scale=2):
            gr.Markdown(
            f"""
            ### ⬇️ Batchlinks Downloader ({currentversion}) {latestversiontext}
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
          try:
            if cmd_opts.gradio_queue:
                logbox = gr.Textbox(label="Log", interactive=False)
            else:
                logbox = gr.Textbox("(use --gradio-queue args on launch.py to enable optional logging)", label="Log", interactive=False)
          except AttributeError:
            pass
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
                      logging.change(keeplog, outputs=logbox, every=1)
                  else:
                    print("Batchlinks webui extension: (Optional) Use --gradio-queue args to enable logging on the extension")
                except AttributeError:
                  print("Batchlinks webui extension: Your webui fork is outdated, it doesn't support --gradio-queue yet. This extension would still runs fine.")
                  pass
                out_text = gr.Textbox(label="Output")

                if platform.system() == "Windows":
                    choose_downloader = gr.Radio(["gdown", "wget", "curl"], value="gdown", label="Huggingface/Discord download method (don't understand? ignore.)")
                else:
                    choose_downloader = gr.Radio(["gdown", "wget", "curl", "aria2"], value="gdown", label="Huggingface/Discord download method (don't understand? ignore.)")

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
