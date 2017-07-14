"""
Copyright (c) 2017, Clayton Wahlstrom
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import time
import webbrowser

from flask import Flask, render_template, request
from bs4 import BeautifulSoup as Soup
from requests import get

from pack import LINUX
from pack.web import openweb

app = Flask(__name__)

browser = 'chrome'
url = 'none'
title = 'none'

@app.route('/', methods = ['GET','POST'])
def main():
    global url, title
    if request.method == 'POST':
        url = request.form['url']
        if LINUX:
            os.system('pkill chrome')
        else:
            os.system('taskkill /im {}.exe'.format(browser))
        soup = Soup(get(url).content, 'html.parser')
        title = soup.select('#eow-title')[0].text.strip()
        time.sleep(0.5)
        webbrowser.open(url)
        #openweb(url, browser=browser)
    return render_template('index.html', url=url, title=title)

@app.route('/template')
def template():
    templatename = "Template Name"
    return render_template('template.html', templatename=templatename)

@app.route('/<path:path>')
def render(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    print('This template renders static files by default')
    app.run(host='0.0.0.0')
    
