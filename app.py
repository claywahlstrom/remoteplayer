
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

"""
TODO (feature):
    add support for Vista
        - use sys.getwindowsversion().major to detect version (note: doesn't work on unix)

"""

import os
import re
import time
import webbrowser

from bs4 import BeautifulSoup as Soup
from flask import Flask, render_template, request, jsonify
import requests

from clay.shell import is_unix

app = Flask(__name__)
app.config['ENV'] = 'development'

BROWSER = 'chrome'
PRESERVE_WINDOW = True

class RemoteSong(object):

    def __init__(self, url=None):
        self.url = url
        if url is None:
            self.title = 'none'
            self.url = 'none'
            self.length = 0
        else:
            self.build()
            
    def __repr__(self):
        if not(self):
            return 'RemoteSong()'
        return 'RemoteSong(title={}, url={}, length={})' \
            .format(self.title, self.url, self.length)
            
    def build(self):
        soup = Soup(requests.get(self.url).content, 'html.parser')
        title = soup.select('#eow-title')
        if len(title) == 0:
            title = soup.select('title')
        self.title = title[0].get_text(strip=True)
        self.length = get_seconds(soup=soup)

class RemoteQueue(object):
    
    def __init__(self):
        self.queue = []
        
    def __repr__(self):
        if not(self):
            return 'RemoteQueue()'
        return 'RemoteQueue({' + (',\n' + ' ' * 13).join(str(s) for s in self.queue) + '})'
        
    def countoftitle(self, title):
        return len(list(song for song in self.queue if song.title == title))
        
    def dequeue(self, index=0):
        self.queue.pop(index)
        
    def enqueue(self, remote_song):
        self.queue.append(remote_song)
        
    def peek(self, index=0):
        return self.queue[index]
        
    def size(self):
        return len(self.queue)
    
queue = RemoteQueue()

for i in range(2):
    queue.enqueue(RemoteSong())

def get_seconds(vid=None, soup=None):
    if soup is None:
        soup = BS(requests.get('https://www.youtube.com/watch?v={}'.format(vid)).content, 'html.parser')
    seconds = re.findall('"length_seconds":"(\d+)"', soup.get_text())[0]
    return int(seconds)

def advanceQueue(add_url=None):
    global queue, advance
    if add_url is None:
        form = request.form
    else:
        form = dict(url=add_url)
    print('form', form)
    if not('next' in form): # don't combine these ifs
            print('  adding url:', form['url'])
            for i in range(queue.countoftitle('none')):
                queue.dequeue(-1) # remove the none-types
            if queue.size() == 0:
                advance = True
            queue.enqueue(RemoteSong(url=form['url']))
    else:
        print('  dequeuing the current song')
        queue.dequeue()
        advance = True
    if queue.peek().title == 'none':
        queue.dequeue(0) # remove none-types between songs
    while queue.size() < 2:
        print('  filling a void song with none')
        queue.enqueue(RemoteSong())
    print(queue)
    
@app.route('/background_process')
def background_process():
    advanceQueue(add_url=request.args.get('url', 0, type=str))
    return jsonify(title=queue.peek(1).title)
    
@app.route('/', methods = ['GET', 'POST'])
def main():
    global queue, advance
    advance = False
    if request.method == 'POST':
        # print('form', request.form)
        advanceQueue()
        if advance and queue.countoftitle('none') != 2:
            peek = queue.peek()
            print('  playing the next song:', peek.title)
            if not(PRESERVE_WINDOW):
                if  is_unix():
                    os.system('pkill {}'.format(BROWSER))
                else:
                    os.system('taskkill /im {}.exe'.format(BROWSER))
            print('    video length =', peek.length)
            time.sleep(0.25)
            webbrowser.open(peek.url)
            
    return render_template('index.html', current=queue.peek(), upnext=queue.peek(1))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, threaded=True)
    
