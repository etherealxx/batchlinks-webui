# Release Notes

### Latest Patch: v3.2.1
- Changed "pruned" option to "fp precision" due to CivitAI API changes
- Fixed bug: No matter when the download process is cancelled or not, CivitAI download will give print out notification that the download process is successful
- Fixed bug: Preventing the UI errored out when storage is full and trying to convert jpg image while downloading civitai stuff (PIL.UnidentifiedImageError)
- UI overhaul

#### Patch: v3.2.0a
- Added support for [vladmandic's fork of automatic1111's webui](https://github.com/vladmandic/automatic)

## Latest Release: v3.2.0
- Bug fixed when downloading with aria2 on Windows
- Bug fixed on gradio update checker on sdless batch file for windows
- CivitAi error prevention (when the website is down)
- Cleaned the code of the hashtag system
- `Copy from Pastebin` feature
- Custom aria command with `@aria`
- Making sure custom hashtag doesn't start with number
- New calmer notification sound
- Readme page cleanup
- Some help link changed to link into wiki instead
- UI fix to adapt with latest gradio (v3.23.0)
- Various bug fixes related to CivitAI download

#### Release v3.1.1b
- Hotfix: Fixed CivitAI link refuses to be downloaded properly. Seems like CivitAI changes its API.
- Fixed several bugs on Windows, especially SDless

#### Release v3.1.1a
- Hotfix: Fixed CivitAI 'model type chooser' bug and fixed `@extract` bug on colab

#### Release v3.1.1
- Added some fix in case CivitAI website is down
- Added message when user pressed "Download All!" but the textbox is empty
- Fixed bug where Lycoris folder always shows on downloaded files the first time user download something

#### Release v3.1.0a
- Hotfix: Indented block on line 1497 fix

### Release v3.1.0
- New hashtag: `#altmodel`, when you use `--ckptdir` argument on `launch.py` line, this hashtag will points to that directory. Otherwise, it'll point to the same directory as `#model`
- New hashtag: `#lycoris`, change current save directory to _/content/stable-diffusion-webui/extensions/sd-webui-additional-networks/models/lora/lycoris_<br/>(Side note: _Lycoris/Locon/Loha_ will works just fine if you use `#addnetlora` instead, as long as you have both [addnet extension](https://github.com/kohya-ss/sd-webui-additional-networks) and [locon extension](https://github.com/KohakuBlueleaf/a1111-sd-webui-locon) installed)
- New hashtag: `#upscaler`, change current save directory to _/content/stable-diffusion-webui/models/ESRGAN_ (This was added few commits ago, but i forgot to write it on the release notes)

Fixes:
- Fixed bug when installing wget/aria2 on Windows
- Fixed sdless scripts so that it also installs `tqdm`
- Fixed bug where custom paths doesn't put CivitAi download (Model Path method) when custom hashtag is used
- Ongoing downloads will correctly stops when Cancel button is pressed on Windows
- CivitAi (Model Path method) now will not download training dataset by accident

#### Release v3.0.2
- Hotfix: removed a comment that messed up the non queue mode. Now the extension works again without `--gradio-queue`.

#### Release v3.0.1
- Hotfix: using `urllib.request` instead of `curl -sI` to get the model name on CivitAI direct link method, since it's more reliable (and the curl method always fails somehow). The `requests` method is returned as a fallback.

### Release v3.0.0
- Added `@extract` syntax
- (Almost) Full Windows support
- Auto-download config file if available when downloading from CivitAI (SD 2.0+)
- Auto-renaming for downloading ckpt/safetensors and pruned model from CivitAI using direct link method
- CivitAI direct link now use `curl` to get the filename, and use the chosen download method (from the four) to download. Huge download speed boost. `requests` is no longer needed.
- Supports download from Anonfiles, Dropbox, Google Drive, Mediafire, Pixeldrain
- Supports download from Github (raw and release files)
- Supports for custom hashtags with `@new` syntax
- Supports for SDless mode (read more [here](https://github.com/etherealxx/batchlinks-webui#sdless-mode))
- UI overhaul:
  - Now there's a table that shows where does the hashtags points into
  - Option to stretch the UI, if your monitor is small, or using colab on mobile
  - Option to hide help text
  - Option to choose preferred CivitAI models. This will works if you download the model via model page link (https://civitai.com/models/)
  - Upload txt now use a little button instead of covering half of the screen

Fixes:
- CivitAI `model page link` no longer randomly download the first model on the json list.
- Most of Windows bugs
- Renaming problem when using CivitAI model page link method
- Warning message when CivitAI download isn't possible (server down)

### Older Release
<details>
  <summary>👈v2.0.0 - v2.1.1</summary>
  <ol>
    <h3>Release v2.1.1</h3>
    Partial Windows support is back
    Changes:
    <ul>
      <li><code>wget</code> disabled on windows currently, until it fixed
    </ul>
    Fixes:
    <ul>
      <li><code>gdown</code> & <code>curl</code> bug fixed
      <li><code>utf-8</code> as default encoding for queue checker (fix bug in Windows)
    </ul>
    <h3>Release v2.1.0</h3>
    Features:
    <ul>
      <li>Supports renaming downloaded file with <code>></code> (for example: <code>https://files.catbox.moe/uarze8.safetensors > neurosama.safetensors</code>)
      <li>Supports extension usage without <code>--gradio-queue</code> (ported from <a href="https://github.com/etherealxx/batchlinks-webui/tree/onedotsix">onedotsix</a>)
      <li>Supports running shell command from the UI with <code>!</code> (for example: type <code>!pip freeze</code>, then hit the <code>Download all!</code> button and see the colab console)
      <li>Progress bar for <code>--gradio-queue</code>
    </ul>
    Changes:
    <ul>
      <li><code>aria2</code> as <em>the only</em> download method when using without <code>--gradio-queue</code>
      <li>Download session will be cut every 80 seconds on when using without <code>--gradio-queue</code> (just like <a href="https://github.com/etherealxx/batchlinks-webui/tree/onedotsix">onedotsix</a>)
      <li><em>Debug stopwatch (decorator)</em> won't run automatically when <code>globaldebug = True</code>, must be uncommented manually (it disrupt the progress bar)
      <li>Dropped support for webui based on Gradio 3.9 (update your installation, or use <a href="https://github.com/etherealxx/batchlinks-webui/tree/onedotsix">onedotsix</a> instead)
      <li>UI tweak (Smaller font size)
    </ul>
    <h3>Release v2.0.0</h3>
    Features:
    <ul>
      <li><code>aria2</code> as download method.
      <li>Cancel button for cancelling download process (<code>--gradio-queue</code> required)
      <li>Detection if a CivitAI links no longer exist
      <li>New hashtags: <code>#textualinversion</code>, <code>#ti</code>, <code>#aestheticembedding</code>, <code>#aestheticembed</code>, <code>#controlnet</code>, and <code>#cnet</code>
      <li>Toggle logging on/off
      <li><code>shlex.quote</code> to properly quote links (Thanks <strong><a href="https://github.com/rti7743">@rti7743</a></strong>!)
      <li>Supports cloning webui extensions
      <li>Supports download from catbox.moe
      <li>Supports download from CivitAI model links (Thanks <strong><a href="https://github.com/rti7743">@rti7743</a></strong>!)
      <li>Supports download from Github (repository and raw files)
      <li>Supports for aesthetic gradients, controlnet model, and extensions path.
      <li>UI font scaled down
      <li>Uses <code>subprocess.Popen</code> instead of <code>os.system</code>
      <br/>_
      <li><em>Debug snapshot</em><br/>
      When <code>globaldebug = True</code>, the moment this extension launch, it saves the current state of the webui on various location (into <code>snapshot.txt</code>), and when you type <code>#debugresetdownloads</code> on the textbox, it will compare the current state and the last saved state, and removes every new file/folder. This will be useful for debugging and testing.
      <li><em>Debug every download method</em><br/>
      When <code>globaldebug = True</code> and you type <code>#debugevery method</code> on the textbox, every link that has 4 different method of download (Huggingface etc.) will be downloaded with every method, regardless of the radio button choice. The result is 4 file being downloaded.
      <li><em>Debug stopwatch</em><br/>
      When <code>globaldebug = True</code>, it will give an output for how long a single download session lasts
    </ul>
  </ol>
</details>