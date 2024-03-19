# This program is the property of Chukun Leo Gao. 
# Before you use the program, create the folder "JamCams_Auto" in your C drive.

import requests
from datetime import datetime
import pandas as pd
import json
import numpy as np
import os

jamcam_list = ['Camera A', 'Camera B', 'Camera C'] #Fill those in with camera names from https://www.tfljamcams.net or https://api.tfl.gov.uk/Place/Type/JamCam/. The key to look for is commonName. 
# The TfL website outputs a JSON file. If you want to read it, JSON formatter is a great tool.  
save_list = ['Camera_A', 'Camera_B', 'Camera_C'] #Anything you want, but should not have spaces, and should have the same length as jamcam_list

save_count = 0 
save_max = 300 #Total number of minutes to save. This can be altered.
time_update = np.array(['a'*50]*len(jamcam_list))
last_minute = 0
date = 'YOUR_DATE_HERE' #Put today's date in here in the format of "20240319_"

while save_count <= save_max:
    t = str(datetime.today())
    minute = int(t[14:16]) #get current minute

    if minute % 1 == 0 and minute != last_minute:
        print(minute, last_minute)
        url = 'https://api.tfl.gov.uk/Place/Type/JamCam/'
        r = requests.get(url)
        with open("jamcam_data.json", "wb") as f:
            f.write(r.content)

        df1 = pd.read_json('jamcam_data.json')
        with open('jamcam_data.json') as data_file:
            data = json.load(data_file)
        for i in range(df1.shape[0]):
            df2 = pd.json_normalize(data[i]['additionalProperties'])
            jamcam_num = -1
            for j in range(len(jamcam_list)):
                if jamcam_list[j] == df1.iloc[i]['commonName']:
                    jamcam_num = j
            if jamcam_num != -1:
                t2 = t[0:4] + t[5:7] + t[8:10] + '_' + save_list[jamcam_num] + '_' + t[11:13] + t[14:16]
                vid_link = df2.iloc[2]['value']
                r = requests.get(vid_link)
                vid_path = 'C:/JamCams_Auto/' + save_list[jamcam_num] + '/' + t2 + '.mp4'
                with open(vid_path, "wb") as f:
                    f.write(r.content)
                vid_size = os.path.getsize(vid_path)
                if save_count != 0:
                    last_vid_path = 'C:/JamCams_Auto/' + save_list[jamcam_num] + '/' + time_update[jamcam_num] + '.mp4'
                    last_vid_size = os.path.getsize(last_vid_path)
                    if vid_size == last_vid_size:
                        os.remove(vid_path) #If the video has the same size as the last saved one, it gets removed. This ensures that the same files are only saved once.
                    else:
                        time_update[jamcam_num] = t2
                elif save_count == 0:
                    time_update[jamcam_num] = t2
        save_count += 1
        print(save_count)
        print(time_update)
        last_minute = minute
        print('last minute updated:', last_minute)