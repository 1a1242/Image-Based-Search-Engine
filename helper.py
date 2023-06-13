import requests
import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import cv2
import face_detection
import base64
import warnings
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


warnings.filterwarnings("ignore")
print(face_detection.available_detectors)
detector = face_detection.build_detector("DSFDDetector", confidence_threshold=.5, 
                                         nms_iou_threshold=.3)#RetinaNetMobileNetV1


api_key = '6d207e02198a847aa98d0a2a901485a5'


def get_driver():
    driver_path = "chromedriver.exe"
    # brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    option = webdriver.ChromeOptions()
    # option.binary_location = brave_path
    # option.add_argument("--headless") 
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
    return driver

def face_detection(path,format):
    im = cv2.imread(path)[:, :, ::-1]
    detections = detector.detect(im)
    status = False
    if detections.shape[0] == 1:
        xmin, ymin, xmax, ymax, conf = tuple(detections[0])
        status = True
        # print((xmin, ymin, xmax, ymax))
        im = im[round(ymin)-1:round(ymax)-1,round(xmin)-1:round(xmax)-1]
    cv2.imwrite(f"capture.{format.lower()}", im[:, :, ::-1])
    return status,f"capture.{format.lower()}"

def get_img_url(img_path):
    with open(img_path, 'rb') as file:
        image_data = file.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    url = 'https://freeimage.host/api/1/upload'
    data = {'key': api_key,
            'action': 'upload',
            'source': image_base64,
            'format': 'json'}
    response = requests.post(url, data=data)
    img_url = response.json()['image']['file']['resource']['chain']['image']
    return img_url

def google_search_link(file_path):
    return get_img_url(file_path)


def links_scrape(driver,img_url):
    driver.get('https://www.google.com/imghp?hl=EN')
    driver.maximize_window()
    time.sleep(2)
    path = 'div.dRYYxd > div.nDcEnd > svg'
    driver.find_element(By.CSS_SELECTOR, path).click()
    time.sleep(2)  
    path = 'div.PXT6cd > input'
    driver.find_element(By.CSS_SELECTOR, path).send_keys(img_url)
    path = 'div.PXT6cd > div'
    driver.find_element(By.CSS_SELECTOR, path).click()
    time.sleep(2)
    path = 'div.Lyudef > div > div.z3qvzf > div:nth-child(2) > span > div.VfPpkd-dgl2Hf-ppHlrf-sM5MNb > button'
    driver.find_element(By.CSS_SELECTOR, path).click()
    time.sleep(5)
    links = []
    path = 'div.b57KQc > c-wiz > div > div > div > div.UJ8EBe > div.F0mDWe > div > div > div > ul > div > a'
    s = driver.find_elements(By.CSS_SELECTOR, path)
    for i in s:
        l = i.get_attribute('href')
        links.append(l)
    print(links)
    driver.close()
    driver.quit()
    return links[:10]

if __name__ == '__main__':
    import os
    file_path = os.path.join('test_images','download.jpg')
    img_url = google_search_link(file_path)
    print(img_url)
    print(links_scrape(img_url))
