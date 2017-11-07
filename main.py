# Version 0.05
# Fetarures:
# 1. Download MP3 from youtube
# 2. Uploads audio to server
# 3. Updates the xml file in the server.

from __future__ import unicode_literals
import youtube_dl

from subprocess import call
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import ftplib

import xml.etree.ElementTree
import time



# Functional Code

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


   

folder = "/Users/juangf/Desktop/python/poddy/%(title)s.%(ext)s" 

def updateXml():
    
    # FileData
    dateNow = time.strftime("%d-%m-%Y %H:%M")
    fileUrl = 'http://labx.cz/podcast/files/' + video_id + '.mp3'
    
    # Open original file and parse
    tree = xml.etree.ElementTree.parse('feed.xml')
    root = tree.getroot()
    
    channelTag = tree.find("channel") 
    pubDate = tree.find("channel/pubDate") 
    
    # Append new tags
    itemTag = xml.etree.ElementTree.SubElement(channelTag, 'item')
    titleTag = xml.etree.ElementTree.SubElement(itemTag, 'title')
    titleTag.text = video_title
    
    linkTag = xml.etree.ElementTree.SubElement(itemTag, 'link')
    linkTag.text = fileUrl
    
    guidTag = xml.etree.ElementTree.SubElement(itemTag, 'guid')
    guidTag.text = fileUrl
    
    descriptionTag = xml.etree.ElementTree.SubElement(itemTag, 'description')
    descriptionTag.text = 'Esta es la descripcion'
    
    enclosureTag = xml.etree.ElementTree.SubElement(itemTag, 'enclosure')
    enclosureTag.attrib['length'] = '1'
    enclosureTag.attrib['type'] = 'audio/mpeg'
    enclosureTag.attrib['url'] = fileUrl
    categoryTag = xml.etree.ElementTree.SubElement(itemTag, 'category')
    categoryTag.text = 'Esta es la categoria'
    
    pubDateTag = xml.etree.ElementTree.SubElement(itemTag, 'pubDate')
    pubDateTag.text = dateNow
    
    #nice formatting

    def indent(elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    indent(root)

    # Write back to file
    tree.write('feed.xml')



def uploadFile():
       
        newVideo_title = video_id + ".mp3"
        filename = newVideo_title
        
        xmlFile = "feed.xml"
        
        ftp = ftplib.FTP('31.15.10.77')
        ftp.login('labxcz', 'w6kvBGUquT')
        ftp.cwd('www/podcast/files')
        for archivo in [filename, xmlFile]:
            myfile = open(archivo, 'rb')
            ftp.storbinary('STOR ' + archivo, myfile)
        ftp.quit()




def callEmb():
    global video_id
    global video_title
    
    urlTarget = url.get()
    
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
    
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',
        'restrictfilenames': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(urlTarget, download=False)
        video_url = info_dict.get("url", None)
        video_id = info_dict.get("id", None)
        video_title = info_dict.get('title', None)
        ydl.download([urlTarget])
    

def ejecuta():
    callEmb()
    updateXml()
    done.grid()
    uploadFile()
    quit()
    





# Visual Layout

root = Tk()

address = Label(root, text="Youtube Address")
address.grid(row=0, column=0, sticky=E)

url = Entry(root)
url.grid(row=0, column=1)

boton1 = Button(root, text="Download Audio", command=ejecuta)
boton1.grid(row=1, column=1)

statusBar = Label(root, text="Downloading...", bd=1, relief=SUNKEN, anchor=W)
done = Label(root, text="Audio downloaded!")




    

root.mainloop()