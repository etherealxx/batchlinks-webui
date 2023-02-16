<br />
<div align="center">
  <a href="https://github.com/etherealxx/batchlinks-downloader">
    <img src="images/batchlinks_logo.png" alt="Logo" height="150">
  </a>

<h3 align="center">BatchLinks Downloader</h3>

<p align="center">
    Batch-downloading models in SD webui colab made simple.
    <br />
    <a href="https://github.com/etherealxx/batchlinks-downloader"><strong></strong></a>
    <br />
    <br />
    <a href="https://github.com/etherealxx/etherportal-webui-colab/issues">Report Bug</a>
    ·
    <a href="https://github.com/etherealxx/etherportal-webui-colab/discussions/new?category=ideas">Request Feature</a>
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
!git clone https://github.com/etherealxx/batchlinks-webui /content/stable-diffusion-webui/extensions/batchlinks-webui
```

<!--
or, if your colab use the newer version of webui (gradio version above 3.16.0) you can use this instead (it adds a little progress bar)

```
!git clone -b gradio-v3-16-2 https://github.com/etherealxx/batchlinks-webui /content/stable-diffusion-webui/extensions/batchlinks-webui
```
-->

**Keep in mind that this extension wont work on your local Windows installation!** (atleast for now, this is just for colab).

## About

This extension will streamline your downloads on your [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) colab session. Paste the links you need to download (or you can upload a txt file containing the links), use the hashstag syntax to choose the download location (see below), and hit the `Download All` button to download them!

## Example

Look at this example<br/>
<img src="images/example.jpg" alt="Logo" height="500"><br/>

```
#model
https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix2/AbyssOrangeMix2_hard.safetensors
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
```

This piece of lines will be read from top to bottom. Every hashtag, it will change the current output directory to said directory (see below). So what this example do is it will download `AOM2` model to the model folder, then it will download the vae and put it to the Vae folder. Next it will download two embed, `bad prompt` and `bad artist`. Next it will download several LoRAs from CivitAI and MEGA, and put it to the Lora folder.

You can also copy that example and paste it to a `.txt` file to use later. You can load a `.txt` file containing that piece of lines directly from the UI.

When the items is downloading, you can inspect the running code on the colab cell, or just take a coffee and chill☕

When the download is complete, the downloaded file will be listed<br/>
<img src="images/downloaded.jpg" alt="Logo" height="300"><br/>

## Syntax

**Hashtag** - Hashtag means change current output directory to this directory. `#model` means every links below this hashtag, will be downloaded to */content/stable-diffusion-webui/models/Stable-diffusion*, until it hits another hashtag, which will change the output directory again. See below for valid hashtags.

Additional note: If you use some colab that doesn't support native LoRA on webui (that means, using `sd-webui-additional-networks` extension in order to work), like [camenduru](https://github.com/camenduru/stable-diffusion-webui-colab)'s colab, use `#addnetlora` instead of `#lora`. It will download the lora to where it supposed to be.

**Links** - Links are the main things you wants to be downloaded. Current supported links are from [Huggingface](https://huggingface.co/), [MEGA](https://mega.nz/), and [CivitAI](https://civitai.com/). Every links other than that will be ignored.  Keep in mind the only supported links are direct download links (see below). For Huggingface, there will be three different method of downloading offered (see below). For MEGA, it will use `mega-cmd` to download. For CivitAI, it will use `requests`.

**Double Hashtag** - Double hashtag means comment. You can put double hashtag in the same line of the link and it will be ignored (keep in mind to put the link first then the double hashtag)

**Others** - Other than that will be ignored.

### Valid Hashtags

`#model`, `#models`, `#checkpoint`, or `#checkpoints` will put the downloaded file to */content/stable-diffusion-webui/models/Stable-diffusion*

`#embedding`, `#embeddings`, `#embed`, or `#embeds` will put the downloaded file to */content/stable-diffusion-webui/embeddings*

`#vae` or `#vaes` will put the downloaded file to */content/stable-diffusion-webui/models/VAE*

`#hypernetwork`, `#hypernetworks`, `#hypernet`, `#hypernets`, `#hynet`, or `#hynets` will put the downloaded file to */content/stable-diffusion-webui/models/hypernetworks*

`#lora` or `#loras` will put the downloaded file to */content/stable-diffusion-webui/models/Lora*

`#addnetlora`, `#loraaddnet`, `#additionalnetworks`, or `#addnet` will put the downloaded file to */content/stable-diffusion-webui/extensions/sd-webui-additional-networks/models/lora*

### How to get the direct links

See [here](https://github.com/etherealxx/batchlinks-downloader/blob/main/howtogetthedirectlinks.md)

### Huggingface's download method

So there's three supported method: `gdown`, `wget`, and `curl`. Use whatever, really. The difference between them are actually very little. Myself love using gdown since the output is cleaner than the others.

<!-- 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

## Logging

If you use latest version of [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), or webui forks that supports `--gradio-queue` args on launch.py, use it and you will be able to enable logging by pressing the `Turn On Logging` radio button. Logging will tell you what are you actually downloading right now on the webui.<br/>
<img src="images/logging.jpg" alt="Log" height="160"><br/>

## Roadmap

- [ ] Add checker for downloaded models (so that it won't download again after the model is downloaded)
- [ ] Progress bar (the only thing preventing me to make a progress bar is some webui colab use gradio 3.9, which doesn't support progress bar.)
- [ ] Supports Windows local installation
- [ ] Support customizable hashtag from the UI
- [ ] aria2 for huggingface download method
- [ ] Using threading/subprocess instead of os.system to download files
- [ ] completed download will use the webui's notification.mp3

## Known Bugs

- ~~File downloaded from MEGA will not listed on the output, as it use different download method. There is some delay between the transfare() function complete until it writes the file. I don't know how long the delay is.~~ Fixed in [v1.1.0](fe6feafc07fbbe3efd2883b33855f8d66b5f89ea)
- Progress bar (the yellow bar) doesn't progress as expected (v3-16-2 branch)
- The delay between file is downloaded and the output shows is really long (1min+) on [camenduru's v1.6 colab](https://github.com/camenduru/stable-diffusion-webui-colab) (Gradio related?)

<!-- CONTRIBUTING -->

## Contributing

I just learned python few months ago, by just looking at other peoples project and sometimes asking ChatGPT. Gradio is new for me. I literally just learn it in one day to make this extension, so expect some bugs.

However, if you have a suggestion or code-fixing that would make this better, please fork the repo and create a pull request. Don't forget to explain the solution you provided on the commit comment, so we can learn together!😁
Don't forget to give the project a star! Thanks again!

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

* [Camenduru's Webui Huggingface](https://github.com/camenduru/stable-diffusion-webui-huggingface) - I use his extension as my base (my gradio skill sucks T.T)
* [SD Civitai Browser](https://github.com/Vetchems/sd-civitai-browser) - Civit download script
* [Mega-to-Google-Drive](https://github.com/menukaonline/Mega-to-Google-Drive) - MEGA download script
