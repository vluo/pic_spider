import os, sys, shutil
import time
from PIL import Image

imgFormats = ('jpg', 'jpeg', 'png', 'gif')
imgNum = 0
limitSize = 1280
imgRoot = '/home/python/pic_spy/albums'
albums = ['poco_album', 'lofter_album', 'tuchong_album']

def resizer(album):
    global imgNum
    albumDir = os.path.join(imgRoot, album)
    authFolders = os.listdir(albumDir)
    for folder in authFolders:
        imgFolder = os.path.join(albumDir, folder)
        if os.path.isdir(imgFolder):
            images = os.listdir(imgFolder)
            thumbFolder = os.path.join(imgFolder, 'thumbs')
            if not os.path.exists(thumbFolder):
                os.makedirs(thumbFolder)
            # end if
            for image in images:
                imagePath = os.path.join(imgFolder, image)
                if os.path.isfile(imagePath):
                    ext = imagePath.split('.')[-1]
                    if ext.lower() not in imgFormats:
                        continue
                    #end if
                    thumbFile = os.path.join(thumbFolder, image)
                    fileSize = int(os.path.getsize(imagePath) / 1024)
                    try:
                        imageObj = Image.open(imagePath)
                    except OSError:
                        pass
                    #end try

                    action = '';
                    imgNum = imgNum + 1

                    if fileSize > 1000:
                        (i_width, i_heitht) = imageObj.size
                        minSize = min(i_width, i_heitht)
                        action = 'RESIZE'
                        ratio = limitSize/minSize
                        if ratio < 1:
                            newWith = int(i_width*ratio)
                            newHeight = int(i_heitht*ratio)
                        else:
                            if os.path.isfile(thumbFile):
                                os.remove(thumbFile)
                            #end if
                            newWith = i_width
                            newHeight = i_heitht
                        #end if
                        newFile = os.path.join(thumbFolder, image)+'.'+str(newWith)+'_'+str(newHeight)+'.'+ext
                        if os.path.isfile(newFile):
                            continue #os.remove(newFile)
                        #end if
                        #imageObj.quality = 90
                        imageObj.resize((newWith, newHeight), Image.ANTIALIAS).save(newFile, quality=95)#Image.ANTIALIAS LANCZOS
                        print('save >>>'+newFile)
                        #break
                    else:
                        resize = 'COPY'
                        if not os.path.isfile(thumbFile):
                            shutil.copyfile(imagePath, thumbFile)
                        #end if
                    #end if
                    print('%.4d'%imgNum+' '+action+' image : '+imagePath)
                #end if
            #end for
        #end fi
    #end for
#end def

startTime = time.time()
for album in albums:
    resizer(album)
#end for

print('done  >>'+str(time.time()-startTime))

