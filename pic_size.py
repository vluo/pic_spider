import os, sys
import time
from PIL import Image


imgRoot = '/home/python/pic_spy/albums/poco_album'
imgFormats = ('jpg', 'jpeg', 'png', 'gif')
folders = os.listdir(imgRoot)
imgNum = 0
limitSize = 1280

for folder in folders:
    imgFolder = os.path.join(imgRoot, folder)
    thumbFolder = os.path.join(imgFolder, 'thumbs')
    if os.path.isdir(imgFolder):
        images = os.listdir(imgFolder)
        for image in images:
            imagePath = os.path.join(imgFolder, image)
            if os.path.isfile(imagePath):
                ext = imagePath.split('.')[-1]
                if ext.lower() not in imgFormats:
                    continue
                #end if
                imageObj = Image.open(imagePath)
                (i_width, i_heitht) = imageObj.size
                imgNum = imgNum + 1
                minSize = min(i_width, i_heitht)
                if minSize > limitSize:
                    if not os.path.exists(thumbFolder):
                        os.makedirs(thumbFolder)
                    #end if
                    ratio = limitSize/minSize
                    newWith = int(i_width*ratio)
                    newHeight = int(i_heitht*ratio)
                    newFile = os.path.join(thumbFolder, image)+'.'+str(newWith)+'_'+str(newHeight)+'.'+ext
                    if os.path.isfile(newFile):
                        os.remove(newFile)
                    #end if
                    #imageObj.quality = 90
                    imageObj.resize((newWith, newHeight), Image.ANTIALIAS).save(newFile, quality=95)#Image.ANTIALIAS LANCZOS
                    print('save >>>'+newFile)
                    #break
                #end if
                #print('%.4d'%imgNum+' '+imagePath+' with={0}, heiht={1}'.format(i_width, i_heitht))
            #end if
        #end for
    #end fi
#end for

print('done  >>'+str(time.time()))

