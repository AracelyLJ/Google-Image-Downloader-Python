import time
import base64
from io import BytesIO
import re
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from PIL import Image

cwd = os.getcwd()
IMAGE_FOLDER = 'download'
os.makedirs(
    name=f'{cwd}/{IMAGE_FOLDER}',
    exist_ok=True
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service
)

SLEEP_TIME = 1

def download_google_images(search_query: str, number_of_images: int) -> str:
    '''Download google images with this function\n
       Takes -> search_query, number_of_images\n
       Returns -> None
    '''

    def scroll_to_bottom():
        '''Scroll to the bottom of the page
        '''
        last_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(SLEEP_TIME)

            new_height = driver.execute_script('return document.body.scrollHeight')
            try:
                element = driver.find_element(
                    by=By.CSS_SELECTOR,
                    value='.YstHxe input'
                )
                element.click()
                time.sleep(SLEEP_TIME)
            except:
                pass

            if new_height == last_height:
                break

            last_height = new_height

    url = 'https://images.google.com/'

    driver.get(
        url=url
    )

    box = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea"
    )

    box.send_keys(search_query)
    box.send_keys(Keys.ENTER)
    time.sleep(SLEEP_TIME)

    scroll_to_bottom()
    time.sleep(SLEEP_TIME)

    img_results = driver.find_elements(
        by=By.XPATH,
        value="//img[contains(@class,'rg_i Q4LuWd')]"
        # value="/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]"
    )

    total_images = len(img_results)
    print(img_results[0])

    print(f'Total images - {total_images}')

    count = 0

    for i in range(1, 100):
        # range(1, 50) will capture images 1 to 49 of the search results
        # You can change the range as per your need.
        try:
    
        # XPath of each image
            img = driver.find_element_by_xpath(
                '//*[@id="islrg"]/div[1]/div[' +
            str(i) + ']/a[1]/div[1]/img')
    
            # Enter the location of folder in which
            # the images will be saved
            img.screenshot('Download-Location' + 
                        tag + ' (' + str(i) + ').png')
            # Each new screenshot will automatically
            # have its name updated
    
            # Just to avoid unwanted errors
            time.sleep(0.2)
    
        except:
            
            # if we can't find the XPath of an image,
            # we skip to the next image
            continue

    # for img_result in img_results:
        try:
            WebDriverWait(
                driver,
                15
            ).until(
                EC.element_to_be_clickable(
                    img_result
                )
            )
            print(img_result)
            img_result.click()
            time.sleep(SLEEP_TIME)

            actual_imgs = driver.find_elements(
                by=By.XPATH,
                value="//img[contains(@class,'n3VNCb')]"
            )

    #         src = ''

    #         for actual_img in actual_imgs:
    #             if 'https://encrypted' in actual_img.get_attribute('src'):
    #                 pass
    #             elif 'http' in actual_img.get_attribute('src'):
    #                 src += actual_img.get_attribute('src')
    #                 break
    #             else:
    #                 pass

    #         for actual_img in actual_imgs:
    #             if src == '' and 'base' in actual_img.get_attribute('src'):
    #                 src += actual_img.get_attribute('src')

    #         if 'https://' in src:
    #             image_name = search_query.replace('/', ' ')
    #             image_name = re.sub(pattern=" ", repl="_", string=image_name)
    #             file_path = f'{IMAGE_FOLDER}/{count}_{image_name}.jpeg'
    #             try:
    #                 result = requests.get(src, allow_redirects=True, timeout=10)
    #                 open(file_path, 'wb').write(result.content)
    #                 img = Image.open(file_path)
    #                 img = img.convert('RGB')
    #                 img.save(file_path, 'JPEG')
    #                 print(f'Count - {count} - Image saved from https.')
    #             except:
    #                 print('Bad image. https://')
    #                 try:
    #                     os.unlink(file_path)
    #                 except:
    #                     pass
    #                 count -= 1
    #         else:
    #             img_data = src.split(',')
    #             image_name = search_query.replace('/', ' ')
    #             image_name = re.sub(pattern=" ", repl="_", string=image_name)
    #             file_path = f'{IMAGE_FOLDER}/{count}_{image_name}.jpeg'
    #             print("-------------------")
    #             print(img_data)
    #             print(image_name)
    #             print(file_path)
    #             try:
    #                 img = Image.open(BytesIO(base64.b64decode(img_data[1])))
    #                 img = img.convert('RGB')
    #                 img.save(file_path, 'JPEG')
    #                 print(f'Count - {count} - Image saved from Base64.')
    #             except:
    #                 print('Bad image. no https://')
    #                 count -= 1
        except ElementClickInterceptedException as e:
            count -= 1
            print(e)
            print('Image is not clickable.')
            driver.quit()

        count += 1

    #     if count >= total_images:
    #         print('No more images to download.')
    #         break
    #     if count == number_of_images:
    #         break

tags = [
    'traje tipico china',
    'traje tipico india',
    'traje tipico mexico',
]

for tag in tags:
    print(f'{"="*10} Downloding for the tag - {tag} {"="*10}')
    download_google_images(
        tag,
        5
    )
    print(f'{"="*10} Finished downloding for the tag - {tag} {"="*10}')

# driver.quit()