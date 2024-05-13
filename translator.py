import os
import re

from time import sleep
from playwright.sync_api import Page
from playwright.sync_api import sync_playwright


# vars
save_translations = "translated"
imgs_to_tl = sorted(
    [os.path.join(dpath, f) for (dpath, drnms, fnams) in os.walk("imgs/") for f in fnams],
    key=lambda nums: int(re.search(r"(?<=\/)(.*?)(?=\.jpg)", nums).group(1))
    )
counter = 1

# start text
print(f"""
ManhuaMTL Server [Translator Plugin]

      Images to translate: {len(imgs_to_tl)}
      Images are saved at: "{save_translations}"
      Running: Playwright[firefox]
      Using: translate.google.com
""")


# translate img
def tl_img(page: Page, img: str):
    """
    Interacts with Google Translate to translate the image
    """
    # Select files
    page.screenshot(path="tl_out.png")
    page.get_by_role("textbox", name="Browse your files").set_input_files(img)

    # Download translated file
    download_info = page.get_by_role("button", name="Download translation").click()
    page.on("download", lambda download: download.save_as(f"{save_translations}/{counter}.jpg"))


with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()
    # Go to google image translate page with chinese(simplified) to english selected
    page.goto("https://translate.google.com/?sl=zh-CN&tl=en&op=images")

    for img in imgs_to_tl:
        print(f"   > Translting: {img} ...")
        tl_img(page, img)
        # sleep for 5sec (try not to get banned)
        sleep(5)
        # reloads the webpage to clear old image
        page.reload()
        counter += 1


    # page.screenshot(path="example.png")
    browser.close()