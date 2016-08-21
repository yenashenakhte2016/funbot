from __future__ import ( division, absolute_import, print_function, unicode_literals )
import telepot
import datetime
import time
import sys, os, tempfile, logging
if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse


def download_file(url, desc=None):
    u = urllib2.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = url.split('/')[-1]
    filename = filename.split('=')[-1]
    filename = filename.split('?')[-1]
    if not filename:
        filename = 'downloaded.file'
    if desc:
        filename = os.path.join(desc, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "[{0:6.2f}%]\n".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")

def handle(msg):
    chat_id = msg['chat']['id']
    from_id = msg['from']['id']
    command = msg['text']
    msg_id = msg['message_id']
    print ('Got command: ',command, '\tFrom: ',from_id,'\t',str(datetime.datetime.now()))
    stream = open('MSGlog.txt','a')
    stream.write(str(chat_id)+'\t'+str(command)+'\t'+str(datetime.datetime.now())+'\n')
    stream.close()

    if command == '/start':
        bot.sendChatAction(chat_id, 'typing')
        bot.sendMessage(chat_id,'Im HUNGRY to download...\nfeed me :)',)

    else:
        try:
            url = command
            download_file(url)
            bot.sendChatAction(chat_id, 'typing')
            bot.sendMessage(chat_id,'Download Completed :)',)
        except Exception as e:
            bot.sendChatAction(chat_id, 'typing')
            bot.sendMessage(chat_id,str(e))

##############     ENTER YOUR TOKEN BELOW
bot = telepot.Bot('Token')
bot
bot.message_loop(handle)
print ('\nDesigned by @Electrovirus \n\nI am listening ...')

while 1:
    time.sleep(10)
