import os
from PIL import Image


list_of_all_files = []


def file_finder(pat):
    global list_of_all_files
    list_of_files_paths = os.listdir(pat)
    for i in list_of_files_paths:
        if os.path.isdir(pat+"/"+i):
            print("found folder", pat+"/"+i)
            file_finder(pat+"/"+i)
        else:
            list_of_all_files.append(pat+"/"+i)


def file_changer(list_of_files):
    all_files = len(list_of_files)
    for i, e in enumerate(list_of_files):
        coef = 1
        try:
            img = Image.open(e)
            width, height = img.size
            if width > 1920 and height > 1080:
                if width/1920 > height/1080:
                    coef = int(width/1920)
                else:
                    coef = int(height/1080)
        except:
            print("Can't open file", e)
            continue

        try:
            print(e)
            os.remove(e)
            if coef != 1:
                img = img.resize((width/coef, height/coef))
            img.save(e, "JPEG", quality=50)
        except:
            print("Can't delete or save file", e)


def main():
    global list_of_all_files
    file_finder("test_images")
    print(list_of_all_files)
    file_changer(list_of_all_files)



if __name__ == "__main__":
    main()
