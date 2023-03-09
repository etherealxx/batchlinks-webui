<br />

<div align="center">
  <a href="https://github.com/etherealxx/batchlinks-downloader">
    <img src="images/batchlinks_logo.png" alt="Logo" width="528">
  </a>

<h3 align="center">BatchLinks Downloader</h3>

<p align="center">
    Batch-downloading models in SD webui colab made simple.
    <br />
    <a href="https://github.com/etherealxx/batchlinks-downloader"><strong></strong></a>
    <br />
    <a href="https://github.com/etherealxx/batchlinks-downloader/issues">Report Bug</a>
    ·
    <a href="https://github.com/etherealxx/batchlinks-downloader/discussions/new?category=ideas">Request Feature</a>
  </p>

</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#example">Example</a></li>
    <li>
      <a href="#syntax">Syntax</a>
      <ul>
        <li><a href="#valid-hashtags">Valid Hastags</a></li>
        <li><a href="https://github.com/etherealxx/batchlinks-downloader/blob/main/howtogetthedirectlinks.md">How to get the direct links (Important!)</a></li>
        <li><a href="#huggingfaces-download-method">Huggingface's download method</a></li>
        <li><a href="#civitais-download-method">CivitAI's download method</a></li>
        <li><a href="#rename-downloaded-files">Rename-Downloaded-Files</a></li>
        <li><a href="#running-shell-command">Running-Shell-Commands</a></li>
      </ul>
    </li>
    <li>
      <a href="#gradio-queue">Gradio Queue</a>
      <ul>
        <li><a href="#logging">Logging</a></li>
        <li><a href="#cancel">Cancel</a></li>
        <li><a href="#progress-bar">Progress Bar</a></li>
      </ul>
    </li>
    <li>
      <a href="#other-features">Other Features</a>
      <ul>
        <li><a href="#notification">Notification</a></li>
        <li><a href="#local-installation-support">Local Installation Support</a></li>
        <li><a href="#latest-release-v210">Latest Release: v2.1.0</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#known-bugs">Known Bugs</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgements</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->

# SDless branch
Run this on a new colab cell:
```
!pip install gradio==3.16.2
!git clone -b sdless https://github.com/etherealxx/batchlinks-webui /content/stable-diffusion-webui/extensions/batchlinks-webui
!python /content/stable-diffusion-webui/extensions/batchlinks-webui/scripts/batchlinks-downloader.py
```

## Installation

Copy this line into your colab installation cell. Or into a new cell if you already launched the webui.

```
!git clone https://github.com/etherealxx/batchlinks-webui /content/stable-diffusion-webui/extensions/batchlinks-webui
```

or, you can copy the url of this repo and install it via webui and restart the UI.<br/>
<img src="images/ext_installer.jpg" alt="Logo" width="362"><br/>
(If `gradio no interface is running` or `bad gateway` shows up when restarting the UI, that means you need to restart the cell anyway 😅)

<!--
or, if your colab use the newer version of webui (gradio version above 3.16.0) you can use this instead (it adds a little progress bar)

```
!git clone -b gradio-v3-16-2 https://github.com/etherealxx/batchlinks-webui /content/stable-diffusion-webui/extensions/batchlinks-webui
```
-->

Using `--gradio-queue` on the launch.py argument is highly recommended, as it enables this extension to show download progress bar on the UI and a cancel button. The option itself has no negative effect on the webui. [Read more here.](https://github.com/etherealxx/batchlinks-webui#gradio-queue)<br/>
<img src="images/queue.jpg" alt="Logo" width="300"><br/>

While it's not recommended to use this extension on your local installation, you can use this extension on Windows. [More here](https://github.com/etherealxx/batchlinks-webui#local-installation-support)

## About

This extension will streamline your downloads on your [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) colab session. Paste the links you need to download (or you can upload a txt file containing the links), use the hashstag syntax to choose the download location (see below), and hit the `Download All` button to download them!

## Example

Look at this example<br/>
<img src="images/example.jpg" alt="Logo" width="738"><br/>

```
#model
https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix3/AOM3.safetensors
#vae
https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/vae/kl-f8-anime2.ckpt
#embed
https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt_version2.pt
https://huggingface.co/NiXXerHATTER59/bad-artist/resolve/main/bad-artist.pt
#lora
https://civitai.com/api/download/models/8840 ##1-mb-lora-trained-in-5-mins-that-does-the-same-thing-as-25-gb-model-but-better
https://civitai.com/api/download/models/6891 ##sans undertale
https://mega.nz/file/gAxTWBAI#uL7EZay-OND5G6ELJlGfUNG0s7Q4TynZKqFdvs0v0tc ##agent8-finetune
https://mega.nz/file/oU43FSTY#vwAfsAb7RKJ4xtsSP7uzrKpWhh1y8BdpIBFurwsVP2o ##agent8-dreambooth
#hypernet
https://cdn.discordapp.com/attachments/1070489470127841381/1070489471964954684/MomopocoV3.pt
```

This piece of lines will be read from top to bottom. Every hashtag, it will change the current output directory to said directory (see below). So what this example do is it will download `AOM3` model to the model folder, then it will download the vae and put it to the Vae folder. Next it will download two embed, `bad prompt` and `bad artist`. Next it will download several LoRAs from CivitAI and MEGA, and put it to the Lora folder. Lastly, it changes the directory to hypernet directory, then 

You can also copy that example and paste it to a `.txt` file to use later. You can load a `.txt` file containing that piece of lines directly from the UI.

When the items is downloading, you can inspect the running code on the colab cell, or just take a coffee and chill☕. If you activate logging, you can inspect the download progress from the UI, more [here](https://github.com/etherealxx/batchlinks-webui#logging)

When the download is complete, the downloaded file will be listed<br/>
<img src="images/downloaded.jpg" alt="Logo" width="745"><br/>

## Syntax

**Hashtag** - Hashtag means change current output directory to this directory. `#model` means every links below this hashtag, will be downloaded to _/content/stable-diffusion-webui/models/Stable-diffusion_, until it hits another hashtag, which will change the output directory again. See below for valid hashtags.

Note: If you use some colab that doesn't support native LoRA on webui (that means, using `sd-webui-additional-networks` extension in order to work), like [camenduru's v1.6](https://github.com/camenduru/stable-diffusion-webui-colab) colab, use `#addnetlora` instead of `#lora`. It will download the lora to where it supposed to be.

**Links** - Links are the main things you wants to be downloaded. Current supported links are from [Huggingface](https://huggingface.co/), [MEGA](https://mega.nz/), [CivitAI](https://civitai.com/), Discord attachments (https://cdn.discordapp.com/attachments/), [catbox](https://files.catbox.moe), and Github (https://github.com or https://raw.githubusercontent.com). Every links other than that will be ignored. Keep in mind the only supported links are direct download links (see [here](https://github.com/etherealxx/batchlinks-downloader/blob/main/howtogetthedirectlinks.md)). For Huggingface, Civitai (model link method), and Discord attachments, there will be three different method of downloading offered (see [below](https://github.com/etherealxx/batchlinks-webui#huggingfaces-download-method)). For MEGA, it will use `mega-cmd` to download. For Github, if, the link is a raw file, it will download the file. Else, it will use `git clone`, useful to clone extension repo into the webui extension folder.

More about CivitAI download method [here](https://github.com/etherealxx/batchlinks-webui#civitais-download-method).

**Double Hashtag** - Double hashtag means comment. You can put double hashtag in the same line of the link and it will be ignored (keep in mind to put the link first then the double hashtag)

**Others** - Other texts will be ignored.

### Valid Hashtags

`#model`, `#models`, `#checkpoint`, or `#checkpoints` will put the downloaded file to _/content/stable-diffusion-webui/models/Stable-diffusion_

`#embedding`, `#embeddings`, `#embed`, `#embeds`, `#textualinversion`, or `#ti` will put the downloaded file to _/content/stable-diffusion-webui/embeddings_

`#vae` or `#vaes` will put the downloaded file to _/content/stable-diffusion-webui/models/VAE_

`#hypernetwork`, `#hypernetworks`, `#hypernet`, `#hypernets`, `#hynet`, or `#hynets` will put the downloaded file to _/content/stable-diffusion-webui/models/hypernetworks_

`#lora` or `#loras` will put the downloaded file to _/content/stable-diffusion-webui/models/Lora_

`#addnetlora`, `#loraaddnet`, `#additionalnetworks`, or `#addnet` will put the downloaded file to _/content/stable-diffusion-webui/extensions/sd-webui-additional-networks/models/lora_

`#aestheticembedding` or `#aestheticembed` will put the downloaded file to _content/stable-diffusion-webui/extensions/stable-diffusion-webui-aesthetic-gradients/aesthetic_embeddings_

`#controlnet` or `#cnet` will put the downloaded file to _/content/stable-diffusion-webui/extensions/sd-webui-controlnet/models_

Github links (if it does not contain `/raw/` in it) doesn't need hashtag. It will always considered as webui extension, and the repository will be cloned to _/content/stable-diffusion-webui/extensions/(reponame)_

### How to get the direct links (Important!)

See [here](https://github.com/etherealxx/batchlinks-downloader/blob/main/howtogetthedirectlinks.md)

### Huggingface's download method

So there's four supported method: `gdown`, `wget`, `curl` and `aria2`. Use whatever, really. The difference between them are actually little. Myself love using `gdown` since the output is cleaner than the others. Some says `aria2` has the fastest download speed.

### Civitai's download method

There are two ways to download links from Civit. The `model link` method, and the `direct link` method.

The `model link` method **will automatically** choose the directory of the saved model without even using hashtag. It will download the default model of a model page. The advantage of this method is you will also get the model preview images that can shows up on the latest version of [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui). This method will also uses the same download protocol as huggingface's (see above). <br/>The `model link` method's link starts with **https://civitai.com/models/**

The `direct link` method is the old method, which needs hashtag for the downloaded model to be properly placed, and uses `request` module to download. The advantage of this method is you can choose what model variation you want to download by grabbing the right url. See [here](https://github.com/etherealxx/batchlinks-downloader/blob/main/howtogetthedirectlinks.md) for more.<br/>The `direct link` method's link starts with **https://civitai.com/api/download/models/**

Here's the difference of syntax between two methods:

Model link:
```
https://civitai.com/models/4823/deliberate
```
Direct link:
```
#model
https://civitai.com/api/download/models/5616
```

Check [this page](https://github.com/etherealxx/batchlinks-downloader/blob/main/howtogetthedirectlinks.md) to learn more on how to get the links for each methods.

### Rename Downloaded Files
Using `>` symbol, you can rename files. Take this for example<br/>
<img src="images/rename.jpg" alt="Log" width="407"><br/>
Mostly catbox file has random name, by using `>` symbol after the link, you can type the desired name on the right. (Don't forget the extension)

### Running Shell Commands
You can run shell commands by using `!` in front of the command you want, just like in google colab cells. Then press the `Download All!` button. (Sure, it doesn't download anything, but, well😅)<br/>
<img src="images/shell1.jpg" alt="Log" width="200">
<img src="images/shell2.jpg" alt="Log" width="200"><br/>
You can run many lines at once too!

<!--

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

## Gradio Queue

If you use --gradio-queue argument on `launch.py`, some feature will be activated.
### Logging

<!-- If you use latest version of [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), or webui forks that supports `--gradio-queue` args on launch.py, use it and you will be able to -->
Enable logging by pressing the `Turn On Logging` radio button, and wait till `Logging activated` shows up and the box is blinking with orange border. Logging will tell you what are you actually downloading right now on the webui. After your download session is completed, it's recommended to turn back off the feature.<br/>
<img src="images/logging.jpg" alt="Log" width="407"><br/>

### Cancel 
Pressing `cancel` button while download in progress will stops the current session. Useful when at one time the download speeds is too slow. If you're currently downloading a single item, that item will be cancelled, but the other downloaded one will remain intact.<br/>
<img src="images/cancel.jpg" alt="Log" width="500"><br/>

### Progress Bar
There will be an additional progress bar that tells you the current activities.<br/>
<img src="images/progress.jpg" alt="Log" width="500"><br/>

### Changes if `--gradio-queue` is off
Feature listed above will dissapear, and your only option for download is just `aria2` (speed is priority).<br/>Note that when you pressed the `Download All!` button, **nothing will shows up on the UI**. You need to check the colab console.<br/>
<img src="images/checkconsole1.jpg" alt="check" width="407"><img src="images/checkconsole2.jpg" alt="off" width="407"><br/>
Another thing to note is your download session will always be cutted every 70 seconds (to prevent hangs/desync).<br/>
<img src="images/gradiooff1.jpg" alt="off" width="407"><br/>
Don't worry, you can continue your session by pressing the `Resume Download` button. It will refresh the links with the one you haven't downloaded yet, then pressing `Download All!` will download the remaining links.<br/>
<img src="images/gradiooff2.jpg" alt="off" width="407"><br/>

## Other Features

### Notification

~~If there's `notification.mp3` on your webui installation folder (the one who plays when image generation is complete), this extension will also use that sound file to notify completed batch download.~~

I'm now integrating the notifiction audio to the extension itself!😊

### Local Installation Support

This extension is tested to work on Windows 11. Maybe works on Debian-based linux (but you better inspect the source code first).
On Windows, this extension will install [MEGAcmd](https://github.com/meganz/MEGAcmd) for MEGA file download.
MacOS is not supported.

## Latest release: v2.1.0

#### Release v2.1.2
- CivitAI direct link now use curl to get the filename, and use the chosen download method to download. `requests` is no longer needed.

#### Release v2.1.1
- Partial Windows support is back

Changes:
- wget disabled on windows currently, until it fixed

Fixes:
- gdown & curl bug fixed
- utf-8 as default encoding for queue checker (fix bug in Windows)

### Release v2.1.0
Features:
- Supports renaming downloaded file with `>` (for example: `https://files.catbox.moe/uarze8.safetensors > neurosama.safetensors`)
- Supports extension usage without `--gradio-queue` (ported from [onedotsix](https://github.com/etherealxx/batchlinks-webui/tree/onedotsix))
- Supports running shell command from the UI with `!` (for example: type `!pip freeze`, then hit the `Download all!` button and see the colab console)
- Progress bar for `--gradio-queue`

Changes:
- `aria2` as *the only* download method when using without `--gradio-queue`
- Download session will be cut every 80 seconds on when using without `--gradio-queue` (just like [onedotsix](https://github.com/etherealxx/batchlinks-webui/tree/onedotsix))
- _Debug stopwatch (decorator)_ won't run automatically when `globaldebug = True`, must be uncommented manually (it disrupt the progress bar)
- Dropped support for webui based on Gradio 3.9 (update your installation, or use [onedotsix](https://github.com/etherealxx/batchlinks-webui/tree/onedotsix) instead)
- UI tweak (Smaller font size)

### Release v2.0.0
Features:
- `aria2` as download method.
- Cancel button for cancelling download process (`--gradio-queue` required)
- Detection if a CivitAI links no longer exist
- New hashtags: `#textualinversion`, `#ti`, `#aestheticembedding`, `#aestheticembed`, `#controlnet`, and `#cnet`
- Toggle logging on/off
- `shlex.quote` to properly quote links (Thanks **[@rti7743](https://github.com/rti7743)**!)
- Supports cloning webui extensions
- Supports download from catbox.moe
- Supports download from CivitAI model links (Thanks **[@rti7743](https://github.com/rti7743)**!)
- Supports download from Github (repository and raw files)
- Supports for aesthetic gradients, controlnet model, and extensions path.
- UI font scaled down
- Uses `subprocess.Popen` instead of `os.system`
<br/>_
- _Debug snapshot_<br/>
When `globaldebug = True`, the moment this extension launch, it saves the current state of the webui on various location (into `snapshot.txt`), and when you type `#debugresetdownloads` on the textbox, it will compare the current state and the last saved state, and removes every new file/folder. This will be useful for debugging and testing.
- _Debug every download method_<br/>
When `globaldebug = True` and you type `#debugevery method` on the textbox, every link that has 4 different method of download (Huggingface etc.) will be downloaded with every method, regardless of the radio button choice. The result is 4 file being downloaded.
- _Debug stopwatch_<br/>
When `globaldebug = True`, it will give an output for how long a single download session lasts

## Roadmap

- [ ] Add checker for downloaded models (so that it won't download again after the model is downloaded)
- [ ] Different UI for mobile
- [ ] Gradio progress bar
- [ ] Logo change
- [ ] Moving most of the content of this Readme.md to Wiki instead
- [ ] Other download sites (s-ul.eu, gitgud, Google Drive)
- [ ] Support customizable hashtag from the UI
- [ ] UI overhaul
- [ ] (Windows) wget & aria2 support
<br/>_
- [x] aria2 for huggingface download method
- [x] Cleaning the code from unnecesarry comments
- [x] Completed download will use the webui's notification.mp3
- [x] Supports Windows local installation
- [x] Using threading/subprocess instead of os.system to download files

## Known Bugs

- Progress bar (the yellow bar) doesn't progress as expected
- Sometimes colab cannot be shut down with a single click on the stop button. Hitting the button several times will raise a KeyboardInterrupt and forcely stopping the cell.
- Sometimes notification sound doesn't play when downloading same file twice in a row
- Sometimes notification sound shows up when starting download, instead of when the download process is completed.
- There's still a chance that the UI of non `--gradio-queue` session and/or onedotsix freezes after a download session
- Windows: The delay between file is downloaded and the output shows is pretty long, and even sometimes the notification comes at the wrong time.
<br/>_
- ~~Links that has bracket in it needs to be 'escaped' (For example, `Baka-DiffusionV1(Fp16).safetensors` must be typed `Baka-DiffusionV1\(Fp16\).safetensors`)~~ Fixed in [v2.0.0](dbb2adb3d07e41654244076b8ef4e851c3bb1f0c)
- ~~The delay between file is downloaded and the output shows is really long (1min+) on [camenduru's v1.6 colab](https://github.com/camenduru/stable-diffusion-webui-colab) (Gradio related?)~~ Seems like fixed in [v1.1.0](fe6feafc07fbbe3efd2883b33855f8d66b5f89ea)
- ~~File downloaded from MEGA will not listed on the output, as it use different download method. There is some delay between the transfare() function complete until it writes the file. I don't know how long the delay is.~~ Fixed in [v1.1.0](fe6feafc07fbbe3efd2883b33855f8d66b5f89ea)

## Contributing

I just learned python few months ago, by just looking at other peoples project and sometimes asking ChatGPT. Gradio is new for me. I literally just learn it in one day to make this extension, so expect some bugs.

However, if you have a suggestion or code-fixing that would make this better, please notify me in the issue tab, fork the repo and create a pull request. Don't forget to explain the solution you provided on the commit comment, so we can learn together!😁<br/>
A star on this project would be nice! Thanks again!

<!--
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->

## Contact

My Email - gwathon3@gmail.com <br/>
My Youtube - [MJ Devlog](https://www.youtube.com/@mjdevlog)

## Acknowledgments

- [Camenduru's Webui Huggingface](https://github.com/camenduru/stable-diffusion-webui-huggingface) - I use his extension as my base (my gradio skill sucks T.T)
- [SD Civitai Browser](https://github.com/Vetchems/sd-civitai-browser) - Civit download script (Obsolete)
- [Mega-to-Google-Drive](https://github.com/menukaonline/Mega-to-Google-Drive) - MEGA download script
- [MEGAcmd](https://github.com/meganz/MEGAcmd)
