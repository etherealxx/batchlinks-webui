#github.com/etherealxx
import os
import time
import gradio as gr
from modules import script_callbacks #,scripts
from modules.paths import script_path
from modules.shared import cmd_opts #check for gradio queue
import urllib.request, subprocess, contextlib #these handle mega.nz
import http.client
import requests #this handle civit
from tqdm import tqdm
#from IPython.display import display, clear_output
import pathlib
import inspect
import platform
import shlex
import signal

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

# try:
#     global gradiostate
#     if cmd_opts.gradio_queue:
#         gradiostate = True
#     else:
#         gradiostate = False
# except AttributeError:
#     gradiostate = False
#     pass

typechecker = [
    "embedding", "embeddings", "embed", "embeds", "textualinversion", "ti",
    "model", "models", "checkpoint", "checkpoints",
    "vae", "vaes",
    "lora", "loras",
    "hypernetwork", "hypernetworks", "hypernet", "hypernets", "hynet", "hynets",
    "addnetlora", "loraaddnet", "additionalnetworks", "addnet",
    "aestheticembedding", "aestheticembed",
    "controlnet", "cnet",
    "extension", "extensions", "ext"
    ]

typemain = [
    "model", "vae", "embed",
    "hynet", "lora", "addnetlora",
    "aestheticembed", "cnet", "ext"
]

supportedlinks = [
    "https://mega.nz",
    "https://huggingface.co",
    "https://civitai.com/api/download/models/",
    "https://civitai.com/models/",
    "https://cdn.discordapp.com/attachments",
    "https://github.com",
    "https://raw.githubusercontent.com",
    "https://files.catbox.moe"
]

modelpath = os.path.join(script_path, "models/Stable-diffusion")
embedpath = os.path.join(script_path, "embeddings")
vaepath = os.path.join(script_path, "models/VAE")
lorapath = os.path.join(script_path, "models/Lora")
addnetlorapath = os.path.join(script_path, "extensions/sd-webui-additional-networks/models/lora")
hynetpath = os.path.join(script_path, "models/hypernetworks")
aestheticembedpath = os.path.join(script_path, "extensions/stable-diffusion-webui-aesthetic-gradients/aesthetic_embeddings")
cnetpath = os.path.join(script_path, "extensions/sd-webui-controlnet/models")
extpath = os.path.join(script_path, "extensions")

if platform.system() == "Windows":
    for x in typemain: 
        exec(f"{x}path = {x}path.replace('/', '\\\\')")
        #exec(f"print({x}path)")

newlines = ['\n', '\r\n', '\r']
currentlink = ''
currentfolder = modelpath
finalwrite = []
currentcondition = ''
currentsuboutput = ''
processid = ''
logging = False
#currentiterfolder = ''
prockilled = False
currentfoldertrack = []
everyprocessid = []

globaldebug = False #set this to true to activate every debug features

def stopwatch(func):
    """
    A function that acts as a stopwatch for another function.

    Args:
    func (function): The function to be timed.

    Returns:
    The return value of the timed function.
    """
    def wrapper(*args, **kwargs):
        if not globaldebug:
            return func(*args, **kwargs)
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        print(f"Time taken by {func.__name__}: {minutes:.0f}m {seconds:.2f}s")
        return result
    return wrapper

#debuggingpurpose{
    #Hello debuggers! This will track every files when the extension is launched, and
    #you can remove every downloaded files after with hashtag '#debugresetdownloads', for debugging purposes on colab
    #(Note: You need to fill the textbox with only a single line of #debugresetdownloads and nothing more)
    #There's also another feature, '#debugeverymethod', which will download a single link with all four possible methods available.
import shutil
snapshot = []
paths_to_scan = []

# take a snapshot of the directories
def take_snapshot():
    snapshotdir = os.path.join(script_path, 'snapshot.txt')
    global snapshot
    global paths_to_scan
    paths_to_scan = []
    for x in typemain:
        exec(f"paths_to_scan.append({x}path)")
    if os.path.exists(snapshotdir):
        with open(snapshotdir, 'r') as f:
            snapshot = [line.strip() for line in f.readlines()]
        print("Batchlinks extension: snapshot already exist.")
        return
    else:
        snapshot = []
        for path in paths_to_scan:
            if os.path.exists(path):
                pathtemp = os.listdir(path)
                for file in pathtemp:
                    pathoffile = os.path.join(path, file)
                    snapshot.append(pathoffile)
        with open(snapshotdir, 'w') as f:
            for item in snapshot:
                f.write(f"{item}\n")
        print("Batchlinks extension: snapshot taken.")

# rewind everything to a fresh state
def global_rewind():
    global paths_to_scan
    global path
    global currentsuboutput
    removedall, removed_files, removed_dirs, new_snapshot = [], [], [], []
    print('[1;32mDebug rewind initiated...')
    print('[0m')
    for path in paths_to_scan:
        if os.path.exists(path):
            pathtemp = os.listdir(path)
            for file in pathtemp:
                pathoffile = os.path.join(path, file)
                new_snapshot.append(pathoffile)
    toremoves = [x for x in new_snapshot if x not in snapshot]
    for fileordir in toremoves:
        if os.path.exists(fileordir):
            if os.path.isdir(fileordir):
                shutil.rmtree(fileordir)
                removed_dirs.append(fileordir)
            else:
                os.remove(fileordir)
                removed_files.append(fileordir)
    if removed_files or removed_dirs:
        print("Removed files:")
        removedall.append("Removed files:")
        for file in removed_files:
            print(file)
            removedall.append(file)
        print("Removed directories:")
        removedall.append("Removed directories:")
        for dir in removed_dirs:
            print(dir)
            removedall.append(dir)
    print('[1;32mrewind completed')
    print('[0m')
    return removedall

# Take a snapshot of the directories
if globaldebug == True:
    take_snapshot()
# }

def printdebug(toprint):
    if globaldebug == True:
        print(toprint)

def runwithsubprocess(rawcommand, folder=None):

    commandtorun = shlex.split(rawcommand) #construct_command(rawcommand)
    printdebug(f"raw command: {rawcommand}")
    printdebug(f"merged command: {commandtorun}")
    global prockilled
    global everyprocessid
    # if gradiostate == False and not rawcommand.startswith("aria"):
    #     subprocess.run(commandtorun, stderr=subprocess.STDOUT, universal_newlines=True)
    # else:
    if folder != None:
        printdebug("debug folderforsavestate: " + str(folder))
        savestate_folder(folder)
        printdebug("debug currentfoldertrack: " + str(currentfoldertrack))
    process = subprocess.Popen(commandtorun, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    global processid
    processid = process.pid
    everyprocessid.append(processid)
    printdebug("debug processid: " + str(processid))

    ariacomplete = False
    global currentsuboutput
    import re
    while True:
        # Read the output from the process
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        # Check if the line contains progress information
        if rawcommand.startswith("aria2"):
            if 'Download Results' in nextline:
                ariacomplete = True
                print('\n')
                print(nextline, end='')
            else:
                if not ariacomplete:
                    match = re.search(r'\[[^\]]+\]', nextline)
                    if match:
                        stripnext = match.group().strip()
                        print("\r", end="")
                        print(f"\r{stripnext}", end='')
                else:
                    print(nextline, end='')
        else:
            if "%" in nextline.strip() or rawcommand.startswith("curl"):
                stripnext = nextline.strip()
                print("\r", end="")
                print(f"\r{stripnext}", end='')
            else:
                print(nextline, end='')
        currentsuboutput = nextline

    process.wait()
    currentsuboutput = ''
    processid = ''
    if prockilled == True:
        rewind_folder(folder)
        print('[1;31mOperation Cancelled')
        print('[0m')
        global currentcondition
        currentcondition = 'Operation Cancelled'
        return

#these code below handle mega.nz
def unbuffered(proc, stream='stdout'):
    stream = getattr(proc, stream)
    with contextlib.closing(stream):
        while prockilled == False:
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
    todownload_s = shlex.quote(todownload)
    folder_s = shlex.quote(folder)
    if platform.system() == "Windows":
        localappdata = os.environ['LOCALAPPDATA']
        megagetloc = os.path.join(shlex.quote(localappdata), "MEGAcmd", "mega-get.bat")
        runwithsubprocess(f"{megagetloc} {todownload_s} {folder_s}", folder_s)
    else:
        cmd = ["mega-get", todownload_s, folder_s]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        global processid
        global everyprocessid
        processid = proc.pid
        everyprocessid.append(processid)

        global currentsuboutput
        for line in unbuffered(proc):
            if prockilled == False:
                if not line.startswith("Download"):
                    currentsuboutput = line
                    print(f"\r{line}", end="")
                else:
                    print(f"\n{line}")
            else:
                currentsuboutput = ''
                print('[1;31mOperation Cancelled')
                print('[0m')
                global currentcondition
                currentcondition = 'Operation Cancelled'
                return
        currentsuboutput = ''

def installmega():
    HOME = os.path.expanduser("~")
    ocr_file = pathlib.Path(f"{HOME}/.ipython/ocr.py")
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
    megagetloc = os.path.join(shlex.quote(localappdata), "MEGAcmd", "mega-get.bat")
    megacmdloc = os.path.join(shlex.quote(userprofile), "Downloads", "MEGAcmdSetup64.exe")
    if not os.path.exists(megagetloc):
        print('[1;32mInstalling MEGA ...')
        print('[0m')
        runwithsubprocess(f"curl -o {megacmdloc} https://mega.nz/MEGAcmdSetup64.exe")
        time.sleep(1)
        runwithsubprocess(f"{megacmdloc} /S")
        time.sleep(4)
        print('[1;32mMEGA is installed.')
        print('[0m')
        #clear_output()
#these code above handle mega.nz

def civitdown(url, folder):
    filename = url.split('?')[0].rsplit('/', 1)[-1] + ".bdgh"
    pathtodown = os.path.join(folder, filename)
    max_retries = 5
    retry_delay = 10
    # url_s = quote(url)

    while prockilled == False:

        downloaded_size = 0
        headers = {}

        progress = tqdm(total=1000000000, unit="B", unit_scale=True, desc=f"Downloading {filename}. (will be renamed correctly after downloading)", initial=downloaded_size, leave=False)
        global currentsuboutput
        global currentcondition        
        with open(pathtodown, "ab") as f:
            while prockilled == False:
                try:
                    response = requests.get(url, headers=headers, stream=True)
                    total_size = int(response.headers.get("Content-Length", 0))
                    # if total_size == 0:
                    #     total_size = downloaded_size
                    # progress.total = total_size 

                    
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk and prockilled == False:
                                f.write(chunk)
                                progress.update(len(chunk))
                                currentsuboutput = str(progress)
                        else:
                            break

                    downloaded_size = os.path.getsize(pathtodown)
                    currentsuboutput = ''
                    break
                except ConnectionError as e:
                    max_retries -= 1

                    if max_retries == 0:
                        raise e

                    time.sleep(retry_delay)

        progress.close()
        if prockilled == True:
            if os.path.exists(pathtodown):
                os.remove(pathtodown)
            print('[1;31mOperation Cancelled')
            print('[0m')
            currentcondition = 'Operation Cancelled'
            currentsuboutput = ''
            return "Operation Cancelled"
        
        
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

#thank you @rti7743 for this part {
def civitdown2_get_json(url):
  import re
  m = re.search(r'https://civitai.com/models/(\d+)', url)
  model_id = m.group(1)

  api_url = "https://civitai.com/api/v1/models/" + model_id

  import requests
  txt = requests.get(api_url).text

  import json
  return json.loads(txt)

def civitdown2_get_save_directory(model_type, default_folder):
  if model_type == "Checkpoint":
    return modelpath
  elif model_type == "Hypernetwork":
    return hynetpath
  elif model_type == "TextualInversion":
    return embedpath
  elif model_type == "AestheticGradient":
    return aestheticembedpath
  elif model_type == "VAE":
    return vaepath
  elif model_type == "LORA":
    return lorapath
  else:
    return default_folder

def civitdown2_convertimage(imagejpg_save_path, imagepng_save_path):
  from PIL import Image
  img = Image.open(imagejpg_save_path)
  img_resized = img.resize((img.width // 2, img.height // 2))
  img_resized.save(imagepng_save_path)
  os.remove(imagejpg_save_path)

def civitdown2(url, folder, downloader, isdebugevery):
  model = civitdown2_get_json(url)
  if model == {'error': 'Model not found'}:
    print('[1;31mModel ' + url + ' is not available anymore')
    print('[0m')
    return
  
  save_directory = civitdown2_get_save_directory(model['type'], folder)

  data_url = model['modelVersions'][0]['files'][0]['downloadUrl']
  data_filename = model['modelVersions'][0]['files'][0]['name']
  image_url = model['modelVersions'][0]['images'][0]['url']

  if model['type'] == "TextualInversion":
      image_filename_jpg = pathlib.PurePath(data_filename).stem + ".preview.jpg"
      image_filename_png = pathlib.PurePath(data_filename).stem + ".preview.png"
  else:
      image_filename_jpg = pathlib.PurePath(data_filename).stem + ".jpg"
      image_filename_png = pathlib.PurePath(data_filename).stem + ".png"

  data_save_path = os.path.join(save_directory, data_filename)
  imagejpg_save_path = os.path.join(save_directory, image_filename_jpg)
  imagepng_save_path = os.path.join(save_directory, image_filename_png)

  currentmode = 'civit'
  if isdebugevery:
      currentmode = 'civitdebugevery'

  printdebug(f"debug download_url({data_url}, {data_save_path}, {downloader})")
  if prockilled == False:
    hfdown(data_url, data_save_path, downloader, currentmode)
  if prockilled == False:
    hfdown(image_url, imagejpg_save_path, downloader, currentmode)

  if isdebugevery:
    additionalname = '-' + downloader

    if model['type'] == "TextualInversion":
      image_filename_jpg = pathlib.PurePath(data_filename).stem + additionalname + ".preview.jpg"
      image_filename_png = pathlib.PurePath(data_filename).stem + additionalname + ".preview.png"
    else:
      image_filename_jpg = pathlib.PurePath(data_filename).stem + additionalname + ".jpg"
      image_filename_png = pathlib.PurePath(data_filename).stem + additionalname + ".png"
    
    imagejpg_save_path = os.path.join(save_directory, image_filename_jpg)
    imagepng_save_path = os.path.join(save_directory, image_filename_png)

  if prockilled == False:
    civitdown2_convertimage(imagejpg_save_path, imagepng_save_path)
    print(f"{data_save_path} successfully downloaded.")
#}

def hfdown(todownload, folder, downloader, mode='default'):
    if mode=='civit' or mode=='civitdebugevery':
        filename = pathlib.Path(folder).name
        filename_s = shlex.quote(filename)
        filepath = shlex.quote(folder)
        todownload_s = todownload
        folder_s = pathlib.Path(folder).parent.resolve()
    else:
        filename = todownload.rsplit('/', 1)[-1]
        filename_s = shlex.quote(filename)
        filepath = shlex.quote(os.path.join(folder, filename))
        todownload_s = shlex.quote(todownload)
        folder_s = shlex.quote(folder)
    #savestate_folder(folder_s)
    if platform.system() == "Windows":
        if downloader=='gdown':
            import gdown
            gdown.download(todownload, filepath, quiet=False)
        elif downloader=='wget':
            #os.system("python -m wget -o " + os.path.join(folder, filename) + " " + todownload)
            import wget
            wget.download(todownload, filepath)
        elif downloader=='curl':
            runwithsubprocess(f"curl -Lo {filepath} {todownload_s}")
    else:
        if downloader=='gdown':
            printdebug(f"debug gdown {todownload_s} -O {filepath}")
            runwithsubprocess(f"gdown {todownload_s} -O {filepath}", folder_s)
        elif downloader=='wget':
            runwithsubprocess(f"wget -O {filepath} {todownload_s} --progress=bar:force", folder_s)
        elif downloader=='curl':
            runwithsubprocess(f"curl -Lo {filepath} {todownload_s}", folder_s)
            # curdir = os.getcwd()
            # os.rename(os.path.join(curdir, filename), filepath)
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
            runwithsubprocess(f"aria2c --console-log-level=info -c -x 16 -s 16 -k 1M {todownload_s} -d {folder_s} -o {filename_s}", folder_s)
        printdebug("\nmode: " + mode)
        if mode=='debugevery':
            time.sleep(2)
            try:
                os.rename(os.path.join(folder, filename), os.path.join(folder, f"{os.path.splitext(filename)[0]}-{downloader}{os.path.splitext(filename)[1]}"))
                printdebug("renamed to " + f"{os.path.splitext(filename)[0]}-{downloader}{os.path.splitext(filename)[1]}")
            except FileNotFoundError:
                printdebug("rename failed somehow")
                pass
        elif mode=='civitdebugevery':
            time.sleep(2)
            printdebug("debug filename: " + str(filename))
            printdebug("debug filename_s: " + str(filename_s))
            printdebug("debug filepath: " + str(filepath))
            printdebug("debug todownload_s: " + str(todownload_s))
            printdebug("debug folder_s: " + str(folder_s))
            try:
                os.rename(folder, os.path.join(folder_s, f"{os.path.splitext(filename)[0]}-{downloader}{os.path.splitext(filename)[1]}"))
                printdebug("renamed to " + f"{os.path.splitext(filename)[0]}-{downloader}{os.path.splitext(filename)[1]}")
            except FileNotFoundError:
                printdebug("rename failed somehow")
                pass

    # if prockilled == True:
    #     #rewind_folder(folder_s)
    #     pass

def savestate_folder(folder):
    global currentfoldertrack
    currentfoldertrack = []
    listfile = os.listdir(folder)
    for file in listfile:
        pathoffile = os.path.join(folder, file)
        currentfoldertrack.append(pathoffile)

def rewind_folder(folder):
    listfilenew = os.listdir(folder)
    newerfoldertrack = []
    for file in listfilenew:
        pathoffile = os.path.join(folder, file)
        newerfoldertrack.append(pathoffile)
    toremove = [x for x in newerfoldertrack if x not in currentfoldertrack]
    printdebug("debug toremove: " + str(toremove))
    for fileordir in toremove:
        if os.path.exists(fileordir):
            if os.path.isdir(fileordir):
                shutil.rmtree(fileordir)
                print("Removed incomplete download: " + fileordir)
            else:
                os.remove(fileordir)
            print("Removed incomplete download: " + fileordir)

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
    filesdict = dict()
    for x in typemain:
        exec(f"os.makedirs({x}path, exist_ok=True)")
        exec(f"filesdict['{x}'] = os.listdir({x}path)")
    return filesdict

@stopwatch
def run(command, choosedowner):
    global prockilled
    prockilled = False
    global everyprocessid
    everyprocessid = []
    everymethod = False
    global currentcondition

    if command.strip() == '#debugresetdownloads' and snapshot != {} and globaldebug == True:
        currentcondition = f'Removing downloaded files...'
        removed_files = global_rewind()
        texttowrite = ["⬇️Removed files⬇️"]
        for item in removed_files:
            texttowrite.append(item)
        writefinal = list_to_text(texttowrite)
        currentcondition = f'Removing done.'
        return writefinal
    
    oldfilesdict = trackall()
    currentfolder = modelpath
    usemega = False
    currentcondition = 'Extracting links...'
    links = extract_links(command)
    printdebug("links: " + str(links))
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
    printdebug('prockilled: ' + str(prockilled))
    
    downmethod = ['gdown', 'wget', 'curl', 'aria2']
    hfmethods = [
        "https://raw.githubusercontent.com",
        "https://huggingface.co",
        "https://cdn.discordapp.com/attachments"
    ]
    for listpart in links:
        if prockilled == False:
            if listpart.startswith("https://mega.nz"):
                currentlink = listpart
                print('\n')
                print(currentlink)
                currentcondition = f'Downloading {currentlink}...'
                transfare(currentlink, currentfolder)

            elif listpart.startswith(tuple(hfmethods)):
            # elif listpart.startswith("https://huggingface.co") or listpart.startswith("https://raw.githubusercontent.com") or listpart.startswith("https://cdn.discordapp.com/attachments"):
                currentlink = listpart
                print('\n')
                print(currentlink)
                currentcondition = f'Downloading {currentlink}...'
                if everymethod == False:
                    hfdown(currentlink, currentfolder, choosedowner)
                else:
                    for xmethod in downmethod:
                        if prockilled == False:
                            hfdown(currentlink, currentfolder, xmethod, 'debugevery')

            elif listpart.startswith("https://files.catbox.moe"):
                currentlink = listpart
                print('\n')
                print(currentlink)
                try:
                    urllib.request.urlopen(currentlink)
                except http.client.RemoteDisconnected:
                    print('[1;31mConnection to ' + currentlink + ' failed.')
                    print("This colab session's server might doesn't have access to catbox")
                    print('[0m')
                    continue
                except urllib.error.URLError as e:
                    print('[1;31mConnection to ' + currentlink + ' failed.')
                    print("This colab session's server might doesn't have access to catbox")
                    print('[0m')
                    continue
                print(currentlink)
                currentcondition = f'Downloading {currentlink}...'
                hfdown(currentlink, currentfolder, choosedowner)

            elif listpart.startswith("https://civitai.com/api/download/models/"):
                currentlink = listpart
                print('\n')
                print(currentlink)
                currentcondition = f'Downloading {currentlink}...'
                civitdown(currentlink, currentfolder)

            elif listpart.startswith("https://github.com"):
                print('\n')
                print(currentlink)
                if '/raw/' in listpart:
                    currentcondition = f'Downloading {currentlink}...'
                    if everymethod == False:
                        hfdown(currentlink, currentfolder, choosedowner)
                    else:
                        for xmethod in downmethod:
                            if prockilled == False:
                                hfdown(currentlink, currentfolder, xmethod, 'debugevery')
                else:
                    splits = listpart.split("/")
                    currentlink = "/".join(splits[:5])
                    foldername = shlex.quote(listpart.rsplit('/', 1)[-1])
                    folderpath = shlex.quote(os.path.join(extpath, foldername))
                    currentcondition = f'Cloning {currentlink}...'
                    runwithsubprocess(f"git clone {currentlink} {folderpath}")

            elif listpart.startswith("https://civitai.com/models/"):
                currentlink = listpart
                print('\n')
                print(currentlink)
                currentcondition = f'Downloading {currentlink}...'
                if everymethod == False:
                    civitdown2(currentlink, currentfolder, choosedowner, False)
                else:
                    for xmethod in downmethod:
                        if prockilled == False:
                            civitdown2(currentlink, currentfolder, xmethod, True)
            
            elif listpart.startswith("#debugeverymethod") and globaldebug == True:
                print('\n')
                everymethod = True
                print('[1;32mDebugEveryMethod activated!')
                print('[1;32mOne link will be downloaded with every possible download method.')
                print('[0m')

            elif listpart.startswith("#debugresetdownloads") and snapshot != {} and globaldebug == True:
                print('\n')
                currentcondition = f'Removing downloaded files...'
                removed_files = global_rewind()
                oldfilesdict = trackall()
                texttowrite = ["⬇️Removed files⬇️"]
                for item in removed_files:
                    texttowrite.append(item)
                writefinal = list_to_text(texttowrite)
                printdebug(str(writefinal))

            else:
                for prefix in typechecker:
                    if listpart.startswith("#" + prefix):
                        if prefix in ["embedding", "embeddings", "embed", "embeds","textualinversion", "ti"]:
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
                        elif prefix in ["aestheticembedding", "aestheticembed"]:
                            currentfolder = aestheticembedpath
                        os.makedirs(currentfolder, exist_ok=True)
                
        else:
            currentcondition = 'Operation cancelled'
            return "Operation cancelled"

    currentcondition = 'Writing output...'
    downloadedfiles = writeall(oldfilesdict)
    for tokill in everyprocessid:
        try:
            os.kill(tokill, signal.SIGTERM)
        except ProcessLookupError:
            pass
    print()
    print('[1;32mBatchLinks Downloads finished!')
    print('[0m')
    currentcondition = 'Done!'
    printdebug(f"this should be the output:\n" + str(downloadedfiles))
    return downloadedfiles

def extract_links(string):
    links = []
    lines = string.split('\n')
    for line in lines:
        line = line.split('##')[0].strip()
        if line.startswith(tuple(supportedlinks)):
            links.append(line)
        elif line.startswith("#debugeverymethod"):
            links.append(line)
        elif line.startswith("#debugresetdownloads"):
            links.append(line)
        else:
            for prefix in typechecker:
                if line.startswith("#" + prefix):
                    links.append(line)

    #print(f"links: {links}")
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
                if line.startswith(tuple(supportedlinks)):
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
        currentsuboutput = ''
        logging = True
        return [currentcondition, gr.Button.update(visible=True), gr.Button.update(visible=False)]
    if currentsuboutput == '':
        return [currentcondition, gr.Button.update(), gr.Button.update()]
    else:
        return [f"{currentcondition}\n{currentsuboutput}", gr.Button.update(), gr.Button.update()]

def offlog():
    global currentcondition
    global currentsuboutput
    global logging
    if logging == True:
        currentcondition = "Logging deactivated."
        currentsuboutput = ''
        logging = False
    return [f"{currentcondition}", gr.Button.update(visible=False), gr.Button.update(visible=True)]
    
def empty():
  return ''

def cancelrun():
    global processid
    global prockilled
    printdebug("debug processid: " + str(processid))
    if not processid == '':
      
      os.kill(processid, signal.SIGTERM)
        #os.killpg(os.getpgid(processid.pid), signal.SIGTERM)
    prockilled = True
    if prockilled == True and globaldebug == True:
        print()
        print("This should kill")
        print()
    return "Operation Cancelled"

def on_ui_tabs():     
    with gr.Blocks() as batchlinks:
        with gr.Row():
          with gr.Column(scale=2):
            gr.Markdown(
            f"""
            <h3 style="font-size: 22px;">⬇️ Batchlinks Downloader ({currentversion}) {latestversiontext}</h3>
            <p style="font-size: 14px;;">This tool will read the textbox and download every links from top to bottom one by one<br/>
            Put your links down below. Supported link: Huggingface, CivitAI, MEGA, Discord, Github<br/>
            Use hashtag to separate downloaded items based on their download location<br/>
            Valid hashtags: <code>#embed</code>, <code>#model</code>,  <code>#hypernet</code>, <code>#lora</code>, <code>#vae</code>, <code>#addnetlora</code>, etc.<br/>
            (For colab that uses sd-webui-additional-networks, use <code>#addnetlora</code>)<br/>
            Use double hashtag after links for comment</p>
            """)
          with gr.Column(scale=1):
            gr.Markdown(
            """
            <p style="font-size: 14px;">Click these links for more:<br/>
            <a href="https://github.com/etherealxx/batchlinks-webui">Readme Page</a><br/>
            <a href="https://github.com/etherealxx/batchlinks-webui#example">Example</a><br/>
            <a href="https://github.com/etherealxx/batchlinks-webui#syntax">Syntax</a><br/>
            <a href="https://github.com/etherealxx/batchlinks-webui#valid-hashtags">Valid Hashtags</a><br/>
            <a href="https://github.com/etherealxx/batchlinks-webui/blob/main/howtogetthedirectlinks.md">Here's how you can get the direct links</a></p>
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
          with gr.Row():
            with gr.Box():
                try:
                  if cmd_opts.gradio_queue:
                      with gr.Row():
                        #   gr.Textbox(value=None, interactive=False, show_label=False)
                          btn_onlog = gr.Button("Turn On Logging", variant="primary", visible=True)
                          btn_offlog = gr.Button("Turn Off Logging", visible=False)
                          loggingon = btn_onlog.click(keeplog, outputs=[logbox, btn_offlog, btn_onlog], every=1)
                          btn_offlog.click(offlog, outputs=[logbox, btn_offlog, btn_onlog], cancels=[loggingon])
                        #   gr.Textbox(value=None, interactive=False, show_label=False)
                    #   logging = gr.Radio(["Turn On Logging"], show_label=False)
                    #   logging.change(keeplog, outputs=logbox, every=1)
                  else:
                    print("Batchlinks webui extension: (Optional) Use --gradio-queue args to enable logging & cancel button on this extension")
                except AttributeError:
                  print("[1;31mBatchlinks webui extension: Your webui fork is outdated, it doesn't support --gradio-queue yet. This extension might runs into problems")
                  print('[0m')
                  pass
                out_text = gr.Textbox(label="Output")

                if platform.system() == "Windows":
                    choose_downloader = gr.Radio(["gdown", "wget", "curl"], value="gdown", label="Download method (don't understand? ignore.)")
                else:
                    choose_downloader = gr.Radio(["gdown", "wget", "curl", "aria2"], value="gdown", label="Download method (don't understand? ignore.)")

                with gr.Row():
                    try:
                        if cmd_opts.gradio_queue:
                            with gr.Column(scale=2, min_width=100):
                                btn_run = gr.Button("Download All!", variant="primary")
                            # btn_upload = gr.UploadButton("Upload .txt", file_types="text")
                            # btn_upload.upload(uploaded, btn_upload, file_output)
                            with gr.Column(scale=1, min_width=100):
                                btn_cancel = gr.Button("Cancel")
                        else:
                            raise AttributeError
                            #btn_run = gr.Button("Download All!", variant="primary")
                    except AttributeError:
                        btn_run = gr.Button("Download All!", variant="primary")

                try:
                    if cmd_opts.gradio_queue:
                        run_event = btn_run.click(run, inputs=[command, choose_downloader], outputs=out_text)
                        btn_cancel.click(cancelrun, None, outputs=out_text, cancels=[run_event])
                    else:
                        raise AttributeError
                except AttributeError:
                    btn_run.click(run, inputs=[command, choose_downloader], outputs=out_text)

            file_output = gr.File(file_types=['.txt'], label="you can upload a .txt file containing links here")
            file_output.change(uploaded, file_output, command)
            finish_audio = gr.Audio(interactive=False, value=os.path.join(extension_dir, "notification.mp3"), elem_id="finish_audio", visible=False)
        #batchlinks.load(debug, output=debug_txt, every=1)
    return (batchlinks, "Batchlinks Downloader", "batchlinks"),
script_callbacks.on_ui_tabs(on_ui_tabs)