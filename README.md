<br />
<div align="center">
  <a href="https://github.com/etherealxx/batchlinks-downloader">
    <img src="images/batchlinks_logo.png" alt="Logo" height="150">
  </a>

<h3 align="center">BatchLinks Downloader</h3>

<p align="center">
    Batch-downloading models in colab made simple.
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
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
-->

<!-- ABOUT THE PROJECT -->

## Installation

Copy this line into your colab installation cell, **before the launch.py line*.

```
`!git clone https://github.com/etherealxx/batchlinks-downloader /content/stable-diffusion-webui/extensions/batchlinks-downloader
```

**Keep in mind that this extension wont work on your local Windows installation!** (atleast for now, this is just for colab).

## About

<!--
[![Product Name Screen Shot][product-screenshot]](https://example.com)
-->

This extension will streamline your downloads session on your colab session.

## Example

Look at this example

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

This piece of line will be read from top to bottom. Every hashtag, it will change the current output directory to said directory (see below). So what this example do is it will download `AOM2` model to the model folder, then it will download the vae and put it to the Vae folder. Next it will download two embed, `bad prompt` and `bad artist`. Next it will download several LoRAs from CivitAI and MEGA, and put it to the Lora folder.

## Syntax

**Hashtag** - Hashtag means change current output directory to this directory. `#model` means every links below this hashtag, will be downloaded to `/content/stable-diffusion-webui/models/Stable-diffusion`, until it hits another hashtag, which will change the output directory again. See below for valid hashtags.

Additional note: If you use some colab that doesn't support native LoRA on webui (that means, using `sd-webui-additional-networks` extension in order to work), like [camenduru](https://github.com/camenduru/stable-diffusion-webui-colab)'s colab, use `#addnetlora` instead of `#lora`. It will download the lora to where it supposed to be.

**Links** - Links are the main things you wants to be downloaded. Current supported links are from [Huggingface](https://huggingface.co/), [MEGA](https://mega.nz/), and [CivitAI](https://civitai.com/). Every links other than that will be ignored.  Keep in mind the only supported links are direct download links (see below). For Huggingface, there will be three different method of downloading offered (see below). For MEGA, it will use `mega-cmd` to download. For CivitAI, it will use `requests`.

**Double Hashtag** - Double hashtag means comment. You can put double hashtag in the same line of the link and it will be ignored (keep in mind to put the link first then the double hashtag)

**Others** - Other than that will be ignored.

### Valid Hashtags

`#model`, `#models`, `#checkpoint`, or `#checkpoints` will put the downloaded file to `/content/stable-diffusion-webui/models/Stable-diffusion`

`#embedding`, `#embeddings`, `#embed`, or `#embeds` will put the downloaded file to `/content/stable-diffusion-webui/embeddings`

`#vae` or `#vaes` will put the downloaded file to `/content/stable-diffusion-webui/models/VAE`

`#hypernetwork`, `#hypernetworks`, `#hypernet`, `#hypernets`, `#hynet`, or `#hynets` will put the downloaded file to `/content/stable-diffusion-webui/models/hypernetworks`

`#lora` or `#loras` will put the downloaded file to `/content/stable-diffusion-webui/models/Lora`

`#addnetlora`, `#loraaddnet`, `#additionalnetworks`, or `#addnet` will put the downloaded file to `/content/stable-diffusion-webui/extensions/sd-webui-additional-networks/models/lora`

### How to get the direct links

See [here]()

### Huggingface's download method

So there's three supported method: `gdown`, `wget`, and `curl`. Use whatever, really. The difference between them are actually very little. Myself love using gdown since the output is cleaner than the others.

<!-- 
### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

<!-- GETTING STARTED -->

<!-- 
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* npm

  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)

2. Clone the repo

   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```

3. Install NPM packages

   ```sh
   npm install
   ```

4. Enter your API in `config.js`

   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

<!--
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>
 -->

<!-- ROADMAP -->

## Roadmap

- [ ] Add checker for downloaded models (so that it won't download again after the model is downloaded)
- [ ] Progress bar (the only thing preventing me to make a progress bar is some webui colab use gradio 3.6, which doesn't support progress bar.)
- [ ] Supports Winddows local installation
- [ ] Support customizable hashtag from the UI
- [ ] aria2 for huggingface download method

<!-- CONTRIBUTING -->

<!-- 
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

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
