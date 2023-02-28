<br />

<div align="center">
  <a href="https://github.com/etherealxx/batchlinks-downloader">
    <img src="images/batchlinks_logo.png" alt="Logo" height="150" width="528">
  </a>

<h3 align="center">BatchLinks Downloader (onedotsix branch)</h3>

<p align="center">
    Batch-downloading models in SD webui colab made simple.<br />Made for camenduru's v1.6 colab notebook.
    <br />
    <a href="https://github.com/etherealxx/batchlinks-downloader"><strong></strong></a>
    <br />
    <a href="https://github.com/etherealxx/batchlinks-downloader/issues">Report Bug</a>
    ·
    <a href="https://github.com/etherealxx/batchlinks-downloader/discussions/new?category=ideas">Request Feature</a>
  </p>

</div>

<!-- TABLE OF CONTENTS -->

<!--
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>
-->

<!-- ABOUT THE PROJECT -->

## Installation

Copy this line into your colab installation cell. Or into a new cell if you already launched the webui.

```
!git clone -b onedotsix https://github.com/etherealxx/batchlinks-webui /content/stable-diffusion-webui/extensions/batchlinks-webui
```

Made just for [camenduru](https://github.com/camenduru)'s main branch of [stable-diffusion-webui-colab](https://github.com/camenduru/stable-diffusion-webui-colab) The [main branch of this extension](https://github.com/etherealxx/batchlinks-webui) is more superior for newer webui version. 

Windows installation is not supported at all.

<!--
or, if your colab use the newer version of webui (gradio version above 3.16.0) you can use this instead (it adds a little progress bar)

```
!git clone -b gradio-v3-16-2 https://github.com/etherealxx/batchlinks-webui /content/stable-diffusion-webui/extensions/batchlinks-webui
```
-->

## About

This extension will streamline your downloads on your [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) colab session. Paste the links you need to download (or you can upload a txt file containing the links), use the hashstag syntax to choose the download location (see below), and hit the `Download All` button to download them!

## Example

Look at this example<br/>
<img src="images/example.jpg" alt="Logo" height="500" width="738"><br/>

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
<img src="images/downloaded.jpg" alt="Logo" height="300" width="745"><br/>

## Syntax

**Hashtag** - Hashtag means change current output directory to this directory. `#model` means every links below this hashtag, will be downloaded to _/content/stable-diffusion-webui/models/Stable-diffusion_, until it hits another hashtag, which will change the output directory again. See below for valid hashtags.

Note 2: If you use some colab that doesn't support native LoRA on webui (that means, using `sd-webui-additional-networks` extension in order to work), like [camenduru](https://github.com/camenduru/stable-diffusion-webui-colab)'s colab, use `#addnetlora` instead of `#lora`. It will download the lora to where it supposed to be.

**Links** - Links are the main things you wants to be downloaded. Current supported links are from [Huggingface](https://huggingface.co/), [MEGA](https://mega.nz/), [CivitAI](https://civitai.com/), Discord attachments (https://cdn.discordapp.com/attachments/), and [Github](https://github.com). Every links other than that will be ignored. Keep in mind the only supported links are direct download links (see [here](https://github.com/etherealxx/batchlinks-downloader/blob/main/howtogetthedirectlinks.md)). For Huggingface, Civitai (model link method), and Discord attachments, there will be three different method of downloading offered (see [below](https://github.com/etherealxx/batchlinks-webui#huggingfaces-download-method)). For MEGA, it will use `mega-cmd` to download. For CivitAI (direct link method), it will use `requests`. For Github, currently it only supports `git clone`, useful to clone extension repo into the webui extension folder.

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

Github links doesn't need hashtag. It will always cloned to _/content/stable-diffusion-webui/extensions/(reponame)_

### How to get the direct links (Important!)

See [here](https://github.com/etherealxx/batchlinks-downloader/blob/main/howtogetthedirectlinks.md)

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

<!--

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

<!-- ### Logging

If you use latest version of [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), or webui forks that supports `--gradio-queue` args on launch.py, use it and you will be able to enable logging by pressing the `Turn On Logging` radio button. Logging will tell you what are you actually downloading right now on the webui.<br/>
<img src="images/logging.jpg" alt="Log" height="160" width="223"><br/> -->

### Notification

If there's `notification.mp3` on your webui installation folder (the one who plays when image generation is complete), this extension will also use that sound file to notify completed batch download.

## Latest release: v2.0.0+onedotsix
Features:
- (onedotsix) `aria2` as **the only** download method.
- (onedotsix) Downloading session will automatically stopped (cutted) every 2 minutes to prevent UI desync (Gradio error)
- (onedotsix) Resume button to continue cutted session by profiding links that aren't downloaded yet
- Cancel button for cancelling download process
- Debug snapshot.<br/>
When `take_snapshot()` is uncommented, it saves the current state of the webui on various location (into `snapshot.txt`), and when you type `#debugresetdownload` on the textbox, it will compare the current state and the last saved state, and removes every new file/folder. This will be useful for debugging and testing.
- New hashtags: `#textualinversion`, `#ti`, `#aestheticembedding`, `#aestheticembed`, `#controlnet`, and `#cnet`
- `shlex.quote` to properly quote links (Thanks **[@rti7743](https://github.com/rti7743)**!)
- Supports cloning webui extensions
- Supports download from CivitAI model links (Thanks **[@rti7743](https://github.com/rti7743)**!)
- Supports for aesthetic gradients, controlnet model, and extensions path.
- Uses `subprocess.Popen` instead of `os.system`

## Roadmap

- [ ] Add checker for downloaded models (so that it won't download again after the model is downloaded)
- [x] aria2 for huggingface download method
- [ ] Cleaning the code from unnecesarry comments
- [x] Completed download will use the webui's notification.mp3
- [ ] Logo change
- [ ] Other download sites (s-ul.eu, github, gitgud, catbox)
- [ ] ~~Progress bar (the only thing preventing me to make a progress bar is some webui colab use gradio 3.9, which doesn't support progress bar.)~~
- [ ] ~~Supports Windows local installation~~
- [ ] Support customizable hashtag from the UI
- [ ] UI overhaul
- [x] Using threading/subprocess instead of os.system to download files

## Known Bugs


- Sometimes notification sound doesn't play when downloading same file twice in a row
- Sometimes colab cannot be shut down with a single click on the stop button. Hitting the button several times will raise a KeyboardInterrupt and forcely stopping the cell.
- ~~Links that has bracket in it needs to be 'escaped' (For example, `Baka-DiffusionV1(Fp16).safetensors` must be typed `Baka-DiffusionV1\(Fp16\).safetensors`)~~ Fixed in v2.0.0+onedotsix
- ~~The delay between file is downloaded and the output shows is really long (1min+) on [camenduru's v1.6 colab](https://github.com/camenduru/stable-diffusion-webui-colab) (Gradio related?)~~ Seems like fixed in [v1.1.0](fe6feafc07fbbe3efd2883b33855f8d66b5f89ea)
- ~~File downloaded from MEGA will not listed on the output, as it use different download method. There is some delay between the transfare() function complete until it writes the file. I don't know how long the delay is.~~ Fixed in [v1.1.0](fe6feafc07fbbe3efd2883b33855f8d66b5f89ea)

<!-- CONTRIBUTING -->

## Contributing

I just learned python few months ago, by just looking at other peoples project and sometimes asking ChatGPT. Gradio is new for me. I literally just learn it in one day to make this extension, so expect some bugs.

However, if you have a suggestion or code-fixing that would make this better, please inform me in the issue page, fork the repo and create a pull request. Don't forget to explain the solution you provided on the commit comment, so we can learn together!😁<br/>
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
My Youtube - [MJ Devlog](youtube.com/@mjdevlog)

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Camenduru's Webui Huggingface](https://github.com/camenduru/stable-diffusion-webui-huggingface) - I use his extension as my base (my gradio skill sucks T.T)
- [SD Civitai Browser](https://github.com/Vetchems/sd-civitai-browser) - Civit download script
- [Mega-to-Google-Drive](https://github.com/menukaonline/Mega-to-Google-Drive) - MEGA download script
- [MEGAcmd](https://github.com/meganz/MEGAcmd)
