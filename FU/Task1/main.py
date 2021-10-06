import unittest
import numpy
import csv
import os


matrix_list = []


class Matrix:
    def __init__(self, name, matrix):
        self.name = name
        self.matrix = matrix
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])

    def print_it(self):
        for i in self.matrix:
            for j in i:
                print(j, end=" ")
            print()

    def transpose(self):
        new_matrix = [[] for i in range(self.columns)]

        for i in range(self.rows):
            for j in range(self.columns):
                new_matrix[j].append(self.matrix[i][j])

        self.matrix = new_matrix
        self.rows, self.columns = self.columns, self.rows


def check_type(a):
    def is_float(potential_float):
        try:
            float(potential_float)
        except ValueError:
            return False
        return True

    a = a.replace(" ", "")
    try:
        if a.isdigit():
            a = int(a)
        elif is_float(a):
            a = float(a)
        else:
            a = complex(a)
    except ValueError:
        return None
    return a


def get_user_number(n):
    while True:
        a = input("Ввод(0-вернуться/выйти): ")
        try:
            a = int(a)
        except TypeError:
            print("Попробуйте снова, это не число")
        else:
            if 0 <= a <= n:
                break
            else:
                print("Попробуйте снова, число вне интервала")
    return a


def get_matrix_name():
    while True:
        name = input("Введите название переменной для матрицы(только Латинские буквы) ")

        for i in matrix_list:
            if i.name == name:
                print("Это название уже занято")

        for i in name:
            if not(65 <= ord(i) <= 90 or 97 <= ord(i) <= 122) or ord(i) == 106:
                print("В названии сожержится не латинская буква:", i)
                break
        else:
            break
    return name


def get_matrix_id_from_name(name):
    for i, e in enumerate(matrix_list):
        if e.name == name:
            return i
    return None


def main():

    while True:
        print("Выберите действие: \n1) Ввести матрицу \n2) Показать матрицы \n3) Транспонировать матрицу"
              "\n4) Посчитать выражение")
        user_input = get_user_number(4)

        if user_input == 0:
            break
        elif user_input == 1:
            read_matrix()
        elif user_input == 2:
            show_matrix()
        elif user_input == 3:
            transpose()
        elif user_input == 4:
            calculate_mathematical_expression()

    input("Введите что-нибудь для выхода")


def transpose():
    print("Введите имя матрицы которую хотите транспонировать. Доступные имена:", end=" ")
    for i in matrix_list:
        print(i.name, end=" , ")
    name = input("Введите имя: ")
    temp_id = get_matrix_id_from_name(name)
    if temp_id is None:
        print("Такое имя не найдено")
    else:
        matrix_list[temp_id].transpose()
        print("Матрица {} теперь транспонированная".format(name))


def calculate_mathematical_expression():
    temp_matrix = []
    temp_counter = 1

    def get_matrix_from_name(name):
        for i, e in enumerate(matrix_list):
            if e.name == name:
                return matrix_list[i]
        return None

    def mult_mat(a, b):
        a = a.strip()
        b = b.strip()
        new_matrix = []

        if check_type(a):
            a = check_type(a)
            b = get_matrix_from_name(b)
            if b is None:
                return None

            for i in b.matrix:
                new_matrix.append([])
                for j in i:
                    new_matrix[-1].append(j*a)

        elif check_type(b):
            b = check_type(b)
            a = get_matrix_from_name(b)
            if a is None:
                return None

            for i in a.matrix:
                new_matrix.append([])
                for j in i:
                    new_matrix[-1].append(j * b)
        else:
            a = get_matrix_from_name(a)
            b = get_matrix_from_name(b)
            if a is None or b is None:
                return None
            if a.columns != b.rows:
                return None

            for i in range(a.rows):
                new_matrix.append([])
                for j in range(b.columns):
                    s = 0
                    for k in range(a.columns):
                        s += a.matrix[i][k] * b.matrix[k][j]
                    new_matrix[-1].append(s)

        return new_matrix

    def plus_mat(a, b):
        a = get_matrix_from_name(a)
        b = get_matrix_from_name(b)
        if a is None or b is None:
            return None
        if a.rows != b.rows or a.columns != b.columns:
            return None

        new_matrix = []
        for i in range(a.rows):
            new_matrix.append([])
            for j in range(a.columns):
                new_matrix[-1].append(a.matrix[i][j] + b.matrix[i][j])
        return new_matrix

    def calculate_it(expr):
        while "*" in expr:
            for i, e in enumerate(expr):
                if e == "*":
                    value1, value2 = "", ""
                    for j in range(i-1, 0, -1):
                        if expr[j] == "+" or expr[j] == "-" or expr[j] == "*":
                            value1 = expr[j+1:i]
                            break
                    else:
                        value1 = expr[0:i]

                    for j in range(i+1, len(expr)):
                        if expr[j] == "+" or expr[j] == "-" or expr[j] == "*":
                            value2 = expr[i+1:j]
                            break
                    else:
                        value2 = expr[i+1:]

                    print(value1, value2)
                    print(mult_mat(value1, value2))
            break

        while "+" in expr:
            for i, e in enumerate(expr):
                if e == "+":
                    value1, value2 = "", ""
                    for j in range(i-1, 0, -1):
                        if expr[j] == "+" or expr[j] == "-":
                            value1 = expr[j+1:i]
                            break
                    else:
                        value1 = expr[0:i]

                    for j in range(i+1, len(expr)):
                        if expr[j] == "+" or expr[j] == "-":
                            value2 = expr[i+1:j]
                            break
                    else:
                        value2 = expr[i+1:]

                    print(value1, value2)
                    print(plus_mat(value1, value2))
            break

    print("Введите выражение, которое хотите посчитать")
    expression = input().replace(" ", "")
    mas_chis = []
    temp1 = None
    for i, e in enumerate(expression):
        if e.isdigit() or e == "." or e == "j":
            if temp1 is None:
                temp1 = i
        else:
            if e == "*":
                temp1 = None
            if temp1 is not None:
                mas_chis.append([temp1, i])
                temp1 = None

    new_expression = ""
    pr_end = 0
    for i in mas_chis:
        new_expression += expression[pr_end: i[-1]]
        new_expression += "*"
        pr_end = i[-1]
    new_expression += expression[pr_end:]
    expression = new_expression

    print(expression)

    calculate_it(expression)


def read_matrix():

    def get_matrix_via_input():
        while True:
            name = get_matrix_name()
            try:
                row = int(input("Введите кол-во строк ").strip())
                column = int(input("Введите кол-во столбцов ").strip())
            except ValueError:
                print("Попробуйте снова")
            else:
                break

        matrix = []

        for i in range(row):
            matrix.append([])
            print("Введите строку №", i + 1, " поэлементно", sep="")
            for j in range(column):
                while True:
                    a = input("Введите элемент ({} {}) ".format(i + 1, j + 1))
                    a = check_type(a)
                    if a is None:
                        print("НЕВЕРНО")
                    else:
                        matrix[i].append(a)
                        break

        return Matrix(name, matrix)

    def get_matrix_from_templates():
        matrix_templates = [[[1, 2, 3], [1 + 3j, 2, 5.5], [4 + 6j, 6, 5]],
                            [[3, 4, 5], [1 + 6j, 2, 8.5], [4 + 6j, 6, 5]]]

        for i, e in enumerate(matrix_templates):
            print("Матрица", i+1)
            for j in e:
                for k in j:
                    print(k, end=" ")
                print()

        a = get_user_number(len(matrix_templates))
        if a == 0:
            return None

        name = get_matrix_name()
        return Matrix(name, matrix_templates[a])

    def get_matrix_from_csv():
        print("Выберите .csv файл(разделитель: ','):")
        files_in_directory = os.listdir()
        available_files = []
        temp_con = 0
        for i in files_in_directory:
            if i[-4:] == ".csv":
                temp_con += 1
                available_files.append(i)
                print("{}) {}".format(temp_con, i))

        a = get_user_number(temp_con)
        if not a:
            return None

        matrix = []
        with open(available_files[a-1], 'r') as csv_file:
            csv_data = csv.reader(csv_file)
            for row in csv_data:
                matrix.append([])
                for el in row:
                    a = check_type(el)
                    if a is None:
                        print("Невозможно распознать:", el)
                        return None
                    else:
                        matrix[-1].append(el)

        name = get_matrix_name()
        return Matrix(name, matrix)

    print("Как ввести матрицу:\n1)Забить поэлементно\n2)Взять из шаблонов\n3)Забить из csv файла")

    user_input = get_user_number(3)
    temp_matrix = []

    if user_input == 0:
        return
    elif user_input == 1:
        temp_matrix = get_matrix_via_input()
    elif user_input == 2:
        temp_matrix = get_matrix_from_templates()
    elif user_input == 3:
        temp_matrix = get_matrix_from_csv()

    if temp_matrix is not None:
        matrix_list.append(temp_matrix)


def show_matrix():
    print("Введите имя матрицы которую хотите вывести. Доступные имена:", end=" ")
    for i in matrix_list:
        print(i.name, end=" , ")
    name = input("Введите имя: ")
    temp_id = get_matrix_id_from_name(name)
    if temp_id is None:
        print("Такое имя не найдено")
    else:
        matrix_list[temp_id].print_it()


if __name__ == "__main__":
    matrix_list.append(Matrix("A", [[2, 0, -1], [0, -2, 2]]))
    matrix_list.append(Matrix("B", [[4, 1, 0], [3, 2, 1], [0, 1, 0]]))
    matrix_list.append(Matrix("C", [[3, 0, 7], [13, -12, 11], [10, -9, 10]]))
    main()
