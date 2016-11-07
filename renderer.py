# coding: utf-8

from flask import Flask, send_from_directory
import os
import time
import requests
import shutil
from selenium import webdriver

app = Flask(__name__)

project_path = '/path/to/project'
website = "http://website:8080"

@app.route("/")
@app.route("/<path:url>")
def prerender(url=''):
    url = "{}/{}".format(website, url)
    if ("." in url[-4:]):
        ext = ''
    else:
        ext = '.html'
    filename = '{}/{}{}'.format(project_path, url.replace("/", '_'), ext)
    if os.path.exists(filename):
        return send_from_directory(
            os.path.dirname(filename), os.path.basename(filename)
        )
    if ext == '.html':
        driver = webdriver.PhantomJS() # or add to your PATH
        driver.set_window_size(1024, 768) # optional
        driver.get(url)
        time.sleep(5)
        page_source = (driver.page_source).encode('ascii', 'ignore')
        target = open(filename, 'w')
        target.write(page_source)
        target.close()
        return page_source
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        del response
    return send_from_directory(
        os.path.dirname(filename), os.path.basename(filename)
    )

if __name__ == '__main__':
      app.run()
