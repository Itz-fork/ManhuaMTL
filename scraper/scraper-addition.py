# Copyright (c) 2024 Itz-fork

import os
import re
import requests
import urllib.request

from pathlib import Path
from bs4 import BeautifulSoup


def extract_keys(url):
    pattern = r"comic_id=([^&]*)&section_slot=([^&]*)&chapter_slot=([^&]*)"
    matched = re.findall(pattern, url)
    return matched[0]


def download_chapter(url: str, bpath: str, chapter_number: int):
    # extract imgs
    chap = requests.get(url)
    parsed = BeautifulSoup(chap.content, "html.parser")
    img_to_dl = parsed.select("#layout > div > div.chapter-main.scroll-mode > ul img")
    ttl_imgs = len(img_to_dl)

    # check if chapter has already been downloaded
    if os.path.exists(bpath) and len(os.listdir(bpath)) == ttl_imgs:
        print(f"    - Chapter already downloaded ({bpath})")
        return

    # create folders
    Path(bpath).mkdir(parents=True, exist_ok=True)

    c = 0
    for img in img_to_dl:
        img_url = img["src"]
        ipath = f"{bpath}/{os.path.basename(img_url)}"

        # check if image already exists
        if os.path.exists(ipath):
            pass
        else:
            urllib.request.urlretrieve(img_url, ipath)
            c += 1
            print(f"    - Downloading image of chapter {chapter_number} ({c} of {len(img_to_dl)})")
    if c < ttl_imgs:
        print(f"    - Continued to download from {ttl_imgs - c} image from ({c}/{ttl_imgs})")
    else:
        print(f"    - Downloaded {c} images of {ttl_imgs}")


######## Main functions ########
def get_chapters(manhua_name: str, dl_to: str, chapter_from=None, chapter_to=None):
    chapter_list = []
    manhua = requests.get(f"https://www.baozimh.com/comic/{manhua_name}")
    parsed = BeautifulSoup(manhua.content, "html.parser")
    itm1 = parsed.select("#chapter-items a")
    itm2 = parsed.select("#chapters_other_list a")
    chapters = itm1 + itm2
    ch_to = chapter_to
    for chap in chapters:
        # get chapter url
        comic_id, section_slot, chapter_slot = extract_keys(chap["href"])
        if chapter_from is None:
            chapter_from = int(chapter_slot)
        if ch_to is None:
            chapter_to = int(chapter_slot)
        chapter_url = f"https://www.baozimh.com/comic/chapter/{comic_id}/{section_slot}_{chapter_slot}.html"
        base_path = f"{dl_to}/{comic_id}/{chapter_slot}"
        if chapter_to >= int(chapter_slot) >= chapter_from:
            # download the chapter
            print(f"  > Downloading chapter {chapter_slot}...")
            download_chapter(chapter_url, base_path, int(chapter_slot))

        chapter_list.append(base_path)

    return chapter_list


def main():
    manhua_name = "chaojishenjiyin-yuewenmanhua"
    download_to = f"{os.getcwd()}/manhua"
    chapter_from = 219
    chapter_to = None
    chapters = get_chapters(manhua_name=manhua_name, dl_to=download_to, chapter_from=chapter_from, chapter_to=chapter_to)
    print(chapters)


main()
