import os
import re
import requests
import urllib.request

from pathlib import Path
from bs4 import BeautifulSoup


######## Helper functions ########
def extract_keys(url):
    pattern = r"comic_id=([^&]*)&section_slot=([^&]*)&chapter_slot=([^&]*)"
    matched = re.findall(pattern, url)
    return matched[0]

def download_chapter(url: str, bpath: str):
    # create folders
    print(url, bpath)
    Path(bpath).mkdir(parents=True, exist_ok=True)
    
    chap = requests.get(url)
    parsed = BeautifulSoup(chap.content, "html.parser")
    for img in parsed.select("#layout > div > div.chapter-main.scroll-mode > ul img"):
        img_url = img["src"]
        path = f"{bpath}/{os.path.basename(img_url)}"
        urllib.request.urlretrieve(img_url, path)


######## Main functions ########
def get_chapters(manhua_name: str, dl_to: str):
    chapter_list = []
    manhua = requests.get(f"https://www.baozimh.com/comic/{manhua_name}")
    parsed = BeautifulSoup(manhua.content, "html.parser")
    itm1 = parsed.select("#chapter-items a")
    itm2 = parsed.select("#chapters_other_list a")
    chapters = itm1 + itm2

    for chap in chapters:
        # get chapter url
        comic_id, section_slot, chapter_slot = extract_keys(chap["href"])
        chapter_url = f"https://www.baozimh.com/comic/chapter/{comic_id}/{section_slot}_{chapter_slot}.html"
        
        # download the chapter
        base_path = f"{dl_to}/{comic_id}/{chapter_slot}"
        download_chapter(chapter_url, base_path)
        
        chapter_list.append(base_path)

    return chapter_list


def main():
    manhua_name = "wodetudijuranshinudi-ziyuewenhua"
    download_to = f"{os.getcwd()}/manhua/{manhua_name}"
    chapters = get_chapters(manhua_name, download_to)

main()