
import glob
#import logging
import os
from datetime import timedelta

query = "**/*.jpg"
folder_path = "cam"
limit = 300
#files_list = sorted(glob.glob(query), key=os.path.getmtime, reverse=True)
files_list = sorted(glob.glob(query, recursive=True), key=os.path.getmtime, reverse=True)

# fileList: /config/www/cam/eingang/2022-01-27/image22-01-27_18-53-42-62.jpg, /config/www/cam/eingang/2022-01-27/image22-01-27_18-50-11-70.jpg, /config/www/cam/eingang/2022-01-27/image22-01-27_18-46-32-75.jpg, /config/www/cam/eingang/2022-01-27/image22-01-27_18-45-40-67.jpg
#   folder: /config/www/cam

imageDicts = {}
# Files nun in die Struktur bringen
for pic in files_list[0:limit]:
    # folder aus url entfernen, dann startet die url mit der camera
    picUrl = pic[len(folder_path)+1:]
    # cam rausschälen
    parts = picUrl.split('/')
    camera = parts[0]
    # tag ermitteln
    day = parts[1]
    # datum ermitteln
    time = parts[2].split('_')[1][0:8].replace("-",":")
    hour = time[0:2] + ':00'
    # bild an die richtige reihe im objekt hinzufügen

    # imageDicts[day][camera][time] = picUrl

    if day in imageDicts.keys():
        if hour in imageDicts[day].keys():
            if camera in imageDicts[day][hour].keys():
                imageDicts[day][hour][camera][time] = picUrl
            else:
                imageDicts[day][hour][camera] = { time : picUrl}
        else:
            imageDicts[day][hour] = { camera : { time: picUrl} }
    else:
        imageDicts[day] = { hour: { camera: { time: picUrl} } }
    #picturefallery
    #   - tage
    #       - cam
    #           - picture
test = pic



