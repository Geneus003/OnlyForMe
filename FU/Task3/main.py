import csv
import os


class ApproximationMethods:
    def __init__(self):
        print("Введите название csv файла")


def main():
    print(read_data())


def read_data():
    available_csv = []
    con = 1
    for i, e in enumerate(os.listdir()):
        if e[-4:] == ".csv":
            print(f"{con}) {e}")
            con += 1
            available_csv.append(e)
    print("Введите номер файла")
    csv_shoose = get_user_number(len(available_csv))
    if csv_shoose == 0:
        return False
    matrix = []
    with open(available_csv[csv_shoose-1], 'r') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        for row in csv_data:
            matrix.append([])
            for el in row:
                a = check_type(el)
                if a is None:
                    print("Невозможно распознать элемент в csv файле(возможно указан неверный разделитель):", el)
                    return None
                else:
                    matrix[-1].append(a)

    return matrix


def get_user_number(n):
    while True:
        a = input("Ввод(0-выйти): ")
        try:
            a = int(a)
        except ValueError:
            print("Попробуйте снова, это не число")
        else:
            if 0 <= a <= n:
                break
            else:
                print("Попробуйте снова, число вне интервала")
    return a


def check_type(a):
    def is_float(potential_float):
        try:
            float(potential_float)
        except ValueError:
            return False
        return True

    try:
        a = a.replace(" ", "")
    except AttributeError:
        pass
    try:
        if a.isdigit():
            a = int(a)
        elif is_float(a):
            a = float(a)
        else:
            return None
    except:
        return None
    return a


if __name__ == "__main__":
    main()

