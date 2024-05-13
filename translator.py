from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://translate.google.com/?sl=zh-CN&tl=en&op=images")
    print(page.title())
    # switch to img
    # page.get_by_text("Images").click()
    # tweak translations
    # page.get_by_text("Detect language").click()
    # page.get_by_text("English").click()
    # page.screenshot(path="example.png")
    # page.get_by_label("Browse your files").set_input_files("imgs/4.jpg")
    
    page.get_by_role("textbox", name="Browse your files").set_input_files("imgs/11.jpg")

    download_info = page.get_by_role("button", name="Download translation").click()
    page.on("download", lambda download: download.save_as(f"translated/tled.jpg"))
    # download = download_info.value
    # download.save_as("translated/" + download.suggested_filename)
    page.screenshot(path="example.png")
    browser.close()