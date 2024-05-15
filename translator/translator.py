# Copyright (c) 2024 Itz-fork

import os
import re

from tqdm import tqdm
from time import sleep
from playwright.sync_api import Page
from playwright.sync_api import sync_playwright


# vars
to_translate = "wodetudijuranshinudi-ziyuewenhua"  # manhua name
en_name = "My_apprentice_is_actually_the_empress"
save_translations = f"manhua/{en_name}/translated"

sleep_for = 3
manhua_loc = f"{os.getcwd()}/manhua/{to_translate}"
chp_to_tl = [
    f"{os.getcwd()}/manhua/{to_translate}/{i}"
    for i in sorted(os.listdir(manhua_loc), key=lambda chp: int(chp))
]


# start text
print(
    f"""
ManhuaMTL Server [Translator Plugin]

    Chapters to translate: {len(chp_to_tl)}
    Images are saved at: "{save_translations}"
    Running: Playwright[firefox]
    Using: translate.google.com
"""
)


# translate img
def tl_img(page: Page, origin_img: str, save_to: str):
    """
    Interacts with Google Translate to translate the image
    """
    # Select files
    page.get_by_role("textbox", name="Browse your files").set_input_files(origin_img)

    # Download translated file
    try:
        page.get_by_role("button", name="Download translation").click()
        page.on(
            "download",
            lambda download: download.save_as(save_to),
        )
    except:
        page.screenshot(path="tl_test.png")


def start_tl():
    for chp in chp_to_tl:
        # chapter number
        chp_no = os.path.basename(chp)

        # sort images in ascending order
        imgs_to_tl = sorted(
            [
                os.path.join(dpath, f)
                for (dpath, drnms, fnams) in os.walk(chp)
                for f in fnams
            ],
            key=lambda nums: int(
                re.search(rf"(?<=\{chp}\/)(.*?)(?=\.jpg)", nums).group(1)
            ),
        )

        with sync_playwright() as p:
            browser = p.firefox.launch()
            page = browser.new_page()
            # Go to google image translate page with chinese(simplified) to english selected
            page.goto("https://translate.google.com/?sl=zh-CN&tl=en&op=images")

            for img in tqdm(
                imgs_to_tl,
                desc=f"  >> Translating Chapter {chp_no}",
                bar_format="{desc} ({n_fmt}/{total_fmt})",
            ):
                save_path = f"{save_translations}/{chp_no}/{os.path.basename(img)}"

                # Check if the image has already been translated
                if os.path.exists(save_path):
                    print("pass")
                    pass
                else:
                    tl_img(page, img, save_path)
                    # I used to pray for times like this
                    # sleep(3)
                    # reloads the webpage to clear old image
                    page.reload()

            # page.screenshot(path="example.png")
            browser.close()


def translator():
    start_tl()

translator()