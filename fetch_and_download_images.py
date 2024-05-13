import bs4
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import requests

#creating a directory to save images
folder_name = 'bird images'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)
    
def download_image(url, folder_name, search_query, num):
    """
    Downloads an image from the given URL and saves it in the specified folder.

    Args:
        url (str): The URL of the image to download.
        folder_name (str): The name of the folder to save the image in.
        search_query (str): The search query associated with the image.
        num (int): The number of the image.

    Returns:
        None
    """
    # create a new directory for each search_query under the bird images directory
    path = os.path.join(folder_name, search_query)
    if not os.path.isdir(path):
        os.makedirs(path)

    # write image to file
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(path, str(num) + ".jpg"), 'wb') as file:
            file.write(response.content)

keywords = pd.read_csv('birds.csv', sep=",")

def fetch_links_by_search(search_query, downloader):
                         
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"    # Setting the mode for the WebDriver
    options = Options()

    options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')         
    options.add_argument('start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--allow-cross-origin-auth-prompt')
    options.add_argument('window-size=1200x600') 

    driver = webdriver.Chrome(options=options) # Initialize Chrome WebDriver with options
    # Navigate to Google Images
    driver.get('https://www.google.com/imghp?hl=en')

    # Reject all cookies
    reject_all_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[text()='Reject all']")))
    time.sleep(2)  
    reject_all_button.click()

    # Find the search bar and input the search query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.submit()

    # Wait for search results to load (add any additional wait if required)
    driver.implicitly_wait(4)
    driver.execute_script("window.scrollTo(0, 0);")

    page_html = driver.page_source
    pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
    containers = pageSoup.findAll('div', {'class':"H8Rx8c"} ) # Establishing the amount of images loaded 

    len_containers = len(containers)

    # Iterating through all of loaded images
    for i in range(1, len_containers+1):    
        if i % 25 == 0:
            continue
        img_box = driver.find_element(By.XPATH, '//*[@id="rso"]/div/div/div[1]/div/div/div[%s]/div[2]/h3/a/div/div/div'%(i)) # Fetched through Inspect: right-click - copy XPATH 
        img_box_src = img_box.get_attribute("src")
        # Click on the thumbnail
        img_box.click()

        # XPath of the image display 
        time.sleep(4)
        time_started = time.time()
        img_src = None  # Initialize img_src here
        while True:
            fir_img = driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div/div/div/c-wiz/div/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]')
            img_src = fir_img.get_attribute('src')

            if img_src != img_box_src:
                break
            else:
                # Timeout if the full resolution image can't be loaded
                current_time = time.time()
                if current_time - time_started > 10:
                    print("Timeout! Will download a lower resolution image and move onto the next one")
                    break

        # Downloading image
        try:
            if img_src:  # Check if img_src is not None
                downloader(img_src, folder_name, search_query, i)
                print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, img_src))
        except:
            print("Couldn't download an image %s, continuing downloading the next one"%(i))

    
# Creating header for file containing image source link 
with open("img_src_links.csv", "w") as outfile:
    outfile.write("search_terms|src_link\n")

# Loops through the list of search input
for search_query in keywords['Scientific name']:
    try:
        link = fetch_links_by_search(search_query, download_image)
        search_query = search_query.replace(" ", "_")
        with open("img_src_links.csv", "a") as outfile:
            outfile.write(f"{search_query}|{link}\n")
    except Exception as e: 
        print(e)