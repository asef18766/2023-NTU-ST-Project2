from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from time import sleep
options = Options()
options.add_argument("--disable-notifications")
chrome = webdriver.Chrome(options=options, service=Service('chromedriver.exe'))
chrome.get("https://flat.io/")

lang_idx = 0
lang = [
    '',
    'es',
    'fr',
    'ja',
    'en-GB'
]

page_idx = 0
page = [
    '',
    'collaboration',
    'product-overview',
]

def change_lang():
    change_lang_btn = chrome.find_element(By.XPATH, '//button[@aria-label="Change language"]')
    change_lang_btn.click()

    lang_btn = chrome.find_element(By.XPATH, f'//a[@role="menuitem" and @href=\"/{"/".join([i for i in [ lang[lang_idx], page[page_idx] ] if len(i)])}\"]')
    lang_btn.click()

def change_page():
    chrome.get(f"https://flat.io/{page[page_idx]}")

def download_hero_wrapper()->str:
    #with open(fname, "wb") as fp:
    #    fp.write(chrome.find_element(By.CLASS_NAME, "hero-wrapper").screenshot_as_png)
    return chrome.find_element(By.CLASS_NAME, "hero-wrapper").text

def get_navbar()->str:
    return chrome.find_element(By.XPATH, '//div[@data-cy="header"]').text
    #with open(fname, "wb") as fp:
    #    fp.write(chrome.find_element(By.XPATH, '//div[@data-cy="header"]'))

def get_title()->str:
    return chrome.find_element(By.TAG_NAME, "title").get_attribute("innerHTML")

def craweler():
    global page_idx
    global lang_idx

    for i in range(len(lang)):
        for j in range(len(page)):
            page_idx = j
            lang_idx = i
            change_page()
            change_lang()
            #print(f"{page[page_idx]}-{lang[lang_idx]}")
            
            # prevent race condition, adjust it according to your computer & network performance
            sleep(2)
            
            with open(f"title-{lang[lang_idx]}-{page[page_idx]}.txt", "w", encoding='utf-8') as fp:
                fp.write(get_title())
            with open(f"navbar-{lang[lang_idx]}-{page[page_idx]}.txt", "w", encoding='utf-8') as fp:
                fp.write(get_navbar())
            with open(f"hero_wrapper-{lang[lang_idx]}-{page[page_idx]}.txt", "w", encoding='utf-8') as fp:
                fp.write(download_hero_wrapper())
        
        #download_hero_wrapper(f"{page[page_idx]}-{lang[lang_idx]}.png")

def main():
    global page_idx
    global lang_idx
    
    for i in range(len(lang)):
        for j in range(len(page)):
            page_idx = j
            lang_idx = i

            change_page()
            change_lang()

            # prevent race condition, adjust it according to your computer & network performance
            sleep(2)
            
            with open(f"title-{lang[lang_idx]}-{page[page_idx]}.txt", "r", encoding='utf-8') as fp:
                assert fp.read() == get_title()
            
            with open(f"navbar-{lang[lang_idx]}-{page[page_idx]}.txt", "r", encoding='utf-8') as fp:
                assert fp.read() == get_navbar()
            
            with open(f"hero_wrapper-{lang[lang_idx]}-{page[page_idx]}.txt", "r", encoding='utf-8') as fp:
                assert fp.read() == download_hero_wrapper()

if __name__ == "__main__":
    main()