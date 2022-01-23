import os
import time

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver.chrome.service import Service


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    
    # Set the location of the webdriver
    s = Service('./chromedriver')
    driver = webdriver.Chrome(service=s)
    
    driver.get(url)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    # find image tag div
    all_divs = soup.find('div', {'id' : 'dgwt-jg-2'})
    
    job_profiles = all_divs.find_all('img')
    
    urls = []
    for job_profile in job_profiles:
        # find the width of image for finding 
        # same size of image url
        img_width = job_profile['width']
        # write here attribute of img tag which contains image url
        for tag in job_profile['data-jg-srcset'].split(","):
            if img_width in tag:
                img_url = tag.strip().split(" ")[0]
                # finally, if the url is valid
                if is_valid(img_url):
                    urls.append(img_url)

    return urls


def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", 
                    total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


def main(url, path):
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        # for each img, download it
        download(img, path)
    


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="This script downloads all images from a web page")
    parser.add_argument("url", help="The URL of the web page you want to download images")
    parser.add_argument("-p", "--path", help="The Directory you want to store your images, default is the domain of URL passed")
    
    args = parser.parse_args()
    url = args.url
    path = args.path
    
    if not path:
        # if path isn't specified, use the domain name of that url as the folder name
        path = urlparse(url).netloc
        
            
    main(url.split("=")[-1], path)