#tableofcontentmaker
intro = """
<details>
  <summary>Table of Contents</summary>
  <ol>
"""

outro = """
    </li>
  </ol>
</details>
"""

tableofcontents = """
- [Installation](#installation)
- [About](#about)
- [Example](#example)
- [Syntax](#syntax)
    - [Hashtag](#hashtag)
    - [Links](#links)
    - [Double Hashtag](#double-hashtag)
    - [Others](#others)
  - [Valid Hashtags](#valid-hashtags)
  - [How to get the direct links (Important!)](#how-to-get-the-direct-links-important)
  - [Huggingface's download method](#huggingfaces-download-method)
- [Additional Syntax](#additional-syntax)
  - [Rename Downloaded Files](#rename-downloaded-files)
  - [Running Shell Commands](#running-shell-commands)
  - [Extract Everyting (`@extract`)](#extract-everyting-extract)
  - [Custom Hashtag Path (`@new`)](#custom-hashtag-path-new)
  - [Custom Direct Link Download with `aria2` (`@aria2`)](#custom-direct-link-download-with-aria2-aria2)
- [Gradio Queue](#gradio-queue)
  - [Logging](#logging)
  - [Cancel](#cancel)
  - [Progress Bar](#progress-bar)
  - [Changes if `--gradio-queue` is off](#changes-if---gradio-queue-is-off)
- [Other Features](#other-features)
  - [Notification](#notification)
  - [Copy From Pastebin](#copy-from-pastebin)
  - [SDless mode](#sdless-mode)
  - [Local Installation Support](#local-installation-support)
  - [Debug Mode (Developer only)](#debug-mode-developer-only)
- [Release Notes](#release-notes)
- [Roadmap](#roadmap)
- [Known Bugs](#known-bugs)
  - [Known Fixed Bugs](#known-fixed-bugs)
- [Contributing](#contributing)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)
"""

def mlineprint(toprint):
    if toprint[-1] == '\n':
        toprint = toprint[:-1]
    print(toprint.replace('\n', '', 1))


def writehtmllist(space, namehead, hashtaghead):
    spaces = ""
    for _ in range(space):
        spaces += " "
    if initialspace >= 2:
        return spaces + f'<ul><li><a href="{hashtaghead}">{namehead}</a></li></ul>'
    else:
        return spaces + f'<li><a href="{hashtaghead}">{namehead}</a></li>'

if __name__ == "__main__":
    rows = tableofcontents.replace('\n', '', 1).splitlines()#split('\n')  # split into a list of rows
    mlineprint(intro)
    for row in rows:
        if not row == '':
            initialspace = 0
            for char in row:
                if char == ' ':
                    initialspace += 1
                else:
                    break
            extractedrow = row.split("[")
            cuttedrow = extractedrow[1].partition("](")
            headingname = cuttedrow[0]
            headinghashtag = cuttedrow[2].rstrip(")")
            print(writehtmllist(initialspace+4, headingname, headinghashtag))
            # print(cuttedrow[0])
            # print(cuttedrow[2].rstrip(")"))
            # hashtagrow = row.partit
    mlineprint(outro)
