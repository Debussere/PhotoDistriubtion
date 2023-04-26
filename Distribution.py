import os
import glob
from pathlib import Path
from PIL import Image
import re
import pandas as pd
import time


mydir = Path("E:/36d Reinhard")

while True:
    file_station = input("File selection(ALL/IN/OUT): ")
    if file_station == "ALL" or file_station == "IN" or file_station == "OUT": break

print("Loading data")
# getting car information out of the image
def cars_list(imagename):
    try:
        image = Image.open(imagename)
        image_dict = image.info
        try:
            description = image_dict['photoshop'][1028]
            labels = description.decode("ascii", errors ='ignore')
        except:
            exif = image_dict['exif']
            labels = exif.decode("ascii", errors ='ignore')
        car = re.findall('Car\s[0-9]*?\.', labels)
        if car == []: 
            car = ["Car 00."]
        car = set(car)
    except:
        car = ["Car 00."]
    return(car)

def beautify_car_name(car):
    l = car.split()
    number = l[1].replace(".", "").zfill(3)
    car = l[0] + " " + number
    return car

# all folders in 36 days
folders = list()
folders.append('D (-1)')
for i in range(0, 37):
    folders.append("D " + str(i).zfill(2))


types = ('.jpg', '.jpeg', '.png','.heic')

df = pd.DataFrame(None)
# selectfolder
for folder in folders:
    if file_station == "IN":
        path = mydir / folder / "IN" 
    elif file_station == "ALL":
        path = mydir / folder
    elif file_station == "OUT":
        path = mydir / folder / "OUT"
    os.chdir(path)
    # create list of all img files in selected folder
    files_img = []
    for type in types:
        if file_station == "IN" or file_station == "OUT":
            files_img.extend(glob.glob('**/*' + type, recursive=True))
        elif file_station == "ALL":
            files_img.extend(glob.glob(type))
    files = files_img
    # loop over all files
    for image in files:
        image_path = path / image
        cars = cars_list(image_path)
        if cars == []:
            df = df.append(pd.DataFrame([[folder, "car 000", image, 1]], columns=['Folder', 'Car', 'image', 'Count']))
        for car in cars:
            # create dataframe
            car = beautify_car_name(car)
            df = df.append(pd.DataFrame([[folder, car, image, 1]], columns=['Folder', 'Car', 'image', 'Count']))

print("Data read")
time.sleep(1)

csv_name = "Distribution" + file_station + ".csv"

df.to_csv(mydir / csv_name, index= False, header= True)

print("Saved!")
time.sleep(1)