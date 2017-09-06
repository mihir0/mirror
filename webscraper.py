# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 15:14:54 2017

@code based off https://www.quora.com/How-do-I-download-all-images-from-a-website-using-Python
@scrapes google image search for pics
"""

#code based off of https://www.quora.com/How-do-I-download-all-images-from-a-website-using-Python
from bs4 import BeautifulSoup
import urllib2
import json
import io
from PIL import Image

class webscraper():
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    def __init__(self):
        pass
        
    def getImageList(self, query, maxImages):  # cannot get more than 100 images
        query =  '+'.join(query.split())  #this will make the query terminator+3
        url="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"
        print url
       
        req = urllib2.Request(url, headers = self.header)
        soup= urllib2.urlopen(req)
        soup = BeautifulSoup(soup)
        imageList = [] # contains the link for Large original images, type of  image
        count = 0;
        for a in soup.find_all("div",{"class":"rg_meta"}):
            if (count >= maxImages):
                break
            else:
                link , Type =json.loads(a.text)["ou"], json.loads(a.text)["ity"]
                imageList.append((link,Type))
                count += 1
        return imageList
    def getImageFromURL(self, url):
        '''
        *NOTE : PIL has a glitch where it struggles to load jpegs.
        @descrip : gets images from a URL
        @param url : (imgurl, type)
        @returns a file containing the image '''
        print url[0]
        try:
            req = urllib2.Request(url[0], headers = {'User-Agent' : self.header})
            return io.BytesIO(urllib2.urlopen(req).read())
        except Exception as e:
            print "could not load : " + str(url)
            print e
            return None

if __name__ == "__main__":
    scrap = webscraper()
    listImg = scrap.getImageList("georgia tech memes", 100)
    print listImg
    for i in listImg:
        try: #PIL has a glitch where it may not load JPEGs
            img = Image.open(scrap.getImageFromURL(i))
            img.show()
        except Exception as e:
            print "Error" + str(e)

#
#query= "michael jackson memes"
#query=  '+'.join(query.split())  #this will make the query terminator+3
#url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
#header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
#req = urllib2.Request(url,headers=header)
#soup= urllib2.urlopen(req)
#soup = BeautifulSoup(soup)
#
#ActualImages=[] # contains the link for Large original images, type of  image
#for a in soup.find_all("div",{"class":"rg_meta"}):
#    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
#    ActualImages.append((link,Type))
#    
#print ActualImages
#print len(ActualImages)
#
#
#for i, (img, Type) in enumerate(ActualImages):
#    try:
#        print img
#        req = urllib2.Request(img, headers={'User-Agent' : header})
#        #raw_img = urllib2.urlopen(req).read()
#        f = io.BytesIO(urllib2.urlopen(req).read())
#        img = Image.open(f)
#        img.show()
#        '''
#        if not os.path.exists(DIR):
#            os.mkdir(DIR)
#        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
#        print cntr
#        if len(Type)==0:
#            f = open(DIR + image_type + "_"+ str(cntr)+".jpg", 'wb')
#        else :
#            f = open(DIR + image_type + "_"+ str(cntr)+"."+Type, 'wb')
# 
#        f.write(raw_img)
#        f.close()
#        '''
#    except Exception as e:
#        print "could not load : " + str(img)
#        print e