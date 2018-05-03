"""
This Program downloads images from a given url.
It can be parsed via command line or it can be
added manually.


@author Jorge Cardona
"""

import urllib2                     # url requests
import re                          # to get all images from url 
import os                          # to test for a directory
import sys                         # to parse from command line
from os.path import basename       
from urlparse import urlsplit
from urlparse import urlparse
from posixpath import basename 

class ImageScrapper(object):

    # Class member
    IMG_DIR='images/'

    def __init__(self):    
        pass

    # Replace all the spaces with '%20'
    def process_url(self, raw_url):
        if (' ' not in raw_url[-1]):
            processedURL = raw_url.replace(' ','%20')

            # Check if it is an complete url
            if(processedURL[0] == '/'):
                if(processedURL[1] == '/'):
                    processedURL = 'http:' + raw_url
            return processedURL
        
        elif (' ' in raw_url[-1]):
            processedURL = raw_url[:-1]
            processedURL = raw_url.replace(' ','%20')

            if(processedURL[0] == '/'):
                if(processedURL[1] == '/'):
                    processedURL = 'http:' + raw_url
                            
            return processedURL

    # End of process_url


    # Lets get the domain name...
    def getDomainName(self, url):

        self.DOMAIN = ''
        self.i =0
        self.flag = 0
        self.url_len = len(str(url))

        while(self.i < self.url_len):
            if(url[self.i] == '.'):
                self.flag = 1
                if(url[self.i+1] == 'c'):
                    self.flag = 2
                    if(url[self.i+2] == 'o'):
                        self.flag = 3
                        if(url[self.i+3] == 'm'):
                            self.flag = 4
                            
            if(self.flag == 4):
                self.DOMAIN += ".com"
                break
            else:
                self.flag = 0
                
                self.DOMAIN += url[self.i]
                self.i += 1
        # End of while

        return self.DOMAIN
    # End of getDomainName


    def fileUp(self, url, DOMAIN):
        
        # Parsing the URL
        self.parse_object=urlparse(url)
        print("\n\n parse_object: {}\n\n".format(self.parse_object));

        # Lets make a dir for our images:
        if not os.path.exists(ImageScrapper.IMG_DIR):
            os.mkdir(ImageScrapper.IMG_DIR)

        # Lets make a request, and store the HTML locally
        self.urlRequest = urllib2.urlopen(url).read()
        self.source = str(DOMAIN)+'.html'
        self.foo = open(self.source[8:], 'wb')
        self.foo.write(self.urlRequest)
        self.foo.close

        return self.urlRequest
    # End of fileUp



    def getImages(self, url, urlRequest, DOMAIN):
        
        # Lets use RE-X to find all the images in our urlRequested     
        self.imgurls = re.findall('img .*?src="(.*?)"',urlRequest)
        for self.imgurl in self.imgurls:

            # Lets try as is.
            try:
                # Lets clean the url
                print("\nAttempting: {}".format(imgurl))
                imgurl = self.process_url(self.imgurl)


                # Now it should work..
                print("Attempting as: {}".format(self.imgurl))
                self.imgData = urllib2.urlopen(self.imgurl).read()
                self.fileName = basename(urlsplit(self.imgurl)[2])
                self.output = open(self.IMG_DIR+self.fileName,'wb')
                self.output.write(self.imgData)
                self.output.close()
                print("YES!")


                # Let handle it another way...
            except:
                try:
                    print("\nSecond try: ")
                    print("RE-Attempting: {}".format(self.imgurl))
                    self.imgurl = self.process_url(self.imgurl)

                    print("RE-Attempting as: {}".format(imgurl))
                    self.imgData = urllib2.urlopen(self.imgurl).read()
                    self.fileName = basename(urlsplit(self.imgurl)[2])

                    self.output = open(self.IMG_DIR+self.fileName,'wb')
                    self.output.write(self.imgData)
                    self.output.close()
                    print("YES!")

                except:
                    print("\nSecond except: ")
                    print("RE-RE-Attempting: {}".format(self.imgurl))
                    
                    if(self.imgurl[0] == '/'):
                        self.imgurl = self.getDomainName(url)+self.imgurl
                    
                    print("RE-RE-Attempting as: {}".format(self.imgurl))
                    self.imgdata = urllib2.urlopen(self.imgurl).read()
                    self.fileName = basename(urlsplit(self.imgurl)[2])

                    self.temp = self.IMG_DIR+self.fileName
                    
                    if(self.temp == self.IMG_DIR):
                        # THIS IS THE END??
                        return
                    
                    self.output  = open(self.temp,'wb')
                    self.output.write(self.imgdata)
                    self.output.close()
                    print("YES!")
                    
                    pass

    #End of getImage()

if __name__ == '__main__':

    #url = 'https://www.reddit.com/r/Pictures/'
    #url = 'https://imgur.com'
    #url= 'https://www.google.com'
    url='https://www.worldatlas.com/webimage/countrys/samerica/fk.htm'
    
    if(len(sys.argv) > 1):
        url = sys.argv[1]

    pics = ImageScrapper();

    DOMAIN = pics.getDomainName(url)
    requestURL = pics.fileUp(url, DOMAIN)

    pics.getImages(url, requestURL, DOMAIN)
    print("\n\nDONE...\n")