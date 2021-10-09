import os
from PIL import Image


list_of_all_files = []


def file_finder(pat):
    global list_of_all_files
    list_of_files_paths = os.listdir(pat)
    for i in list_of_files_paths:
        if os.path.isdir(pat+"/"+i):
            if i == ".idea":
                continue
            print("Найдена папка", pat+"/"+i)
            file_finder(pat+"/"+i)
        else:
            list_of_all_files.append(pat+"/"+i)


def file_changer(list_of_files):
    all_files = len(list_of_files)
    for i, e in enumerate(list_of_files):
        try:
            if (i+1) % 500 == 0:
                print("Обработано {} из {}".format(i+1, all_files))
        except:
            print("Вообще хер знает, что произошло, счетчика не будет")

        coef = 1
        try:
            img = Image.open(e)
            width, height = img.size
            if width > 1920 and height > 1080:
                if width/1920 > height/1080:
                    coef = width/1920
                else:
                    coef = height/1080
        except:
            print("Невозможно открыть файд(Не картинка?)", e)
            continue

        try:
            if coef != 1:
                img = img.resize((int(width/coef), int(height/coef)))
            img.save(e+"NoneNoneNoneNoneNoneNone", "JPEG", quality=40)
            img.close()
            os.remove(e)
            os.rename(e+"NoneNoneNoneNoneNoneNone", e)
        except:
            print("Can't delete or save file", e)


def main():
    global list_of_all_files
    file_finder("test_images")
    print("Найдено", len(list_of_all_files), "файлов")
    input("Введи что-нибудь для продолжения(конвертации)")
    file_changer(list_of_all_files)


if __name__ == "__main__":
    main()
