"""
класс Matrix - класс для хранения имени матрийцы и самой матрицы
check_type - Принимает строку возвращает измененую по типу переменную, если она под него подходит(int, float, complex)
get_user_number - Принимает число до которого происходит выбор действи, возвращает корректный комер
get_matrix_name - Проверяет доступно ли имя для матрицы
get_matrix_id_from_name - Возвращает  id матрицы по ее названию
main - Главная функция, main loop
transpose - Функция по транспонированию матрицы
calculate_mathematical_expression - Функция для подсчета выражения
brackets_remover - Удаляет скобки, если все выражение заключено в них
get_matrix_from_name - Возвращает матрицы по имени
mult_mat(a, b) - Перемножение a*b
plus_mat(a, b) - Сложение a+b
calculate_it - Функция для подсчета выражения, используется переодически рекурсивно
find_determinant - Стартовая функция для нахождения определителя
find_det - Рекурсивная функция для нахождения определителя
read_matrix - Стартовая функция для ввода матрциы
get_matrix_via_input - Ввод матрицы ручками
get_matrix_from_templates - Ввод матрциы из шаблонов
get_matrix_from_csv - Ввод матрциы из csv
show_matrix - Показать матрицу
"""


import csv
import os
import math

matrix_list = []
temp_matrix_list = []
temp_counter = 1


class Matrix:
    def __init__(self, name, matrix):
        self.name = name
        self.matrix = matrix
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])

    def print_it(self, space_between=12):
        for i in self.matrix:
            for j in i:
                if space_between < len(str(j)):
                    space_between = len(str(j))

        for i in self.matrix:
            for j in i:
                el = str(j)
                prob = space_between - len(el)
                prob1 = prob // 2
                prob2 = prob - prob1
                print(" "*prob1, el, " "*prob2, sep="", end="")
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

    try:
        a = a.replace(" ", "")
        if "+" in a:
            if a[-1] != "j":
                a = a.split("+")[-1] + "+" + a.split("+")[0]
    except AttributeError:
        pass

    try:
        if a.isdigit():
            a = int(a)
        elif is_float(a):
            a = float(a)
        else:
            a = complex(a)
    except ValueError:
        return None
    except AttributeError:
        return None
    return a


def get_user_number(n):
    while True:
        a = input("Ввод(0-вернуться/выйти): ")
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


def get_matrix_name():
    while True:
        name = input("Введите название переменной для матрицы(только Латинские буквы) ")

        for i in matrix_list:
            if i.name == name:
                print("Это название уже занято")
                break
        else:
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
              "\n4) Посчитать выражение\n5) Вычислить определитель\n6) Вычисление нормы матрицы")
        user_input = get_user_number(6)

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
        elif user_input == 5:
            find_determinant()
        elif user_input == 6:
            find_norm()


    input("Введите что-нибудь для выхода ")


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
    global matrix_list, temp_matrix_list

    def brackets_remover(exp):
        bracket_count = 0
        for i, e in enumerate(exp):
            if e == "(":
                bracket_count += 1
            elif e == ")":
                bracket_count -= 1
                if not bracket_count:
                    if exp[0] == "(" and i == len(exp) - 1 and "+" not in exp and "*" not in exp:
                        exp = exp[1:-1]
                    else:
                        break

        return exp

    def get_matrix_from_name(name):
        for i, e in enumerate(matrix_list):
            if e.name == name:
                return matrix_list[i]

        for i, e in enumerate(temp_matrix_list):
            if e.name == name:
                return temp_matrix_list[i]
        return None

    def mult_mat(a, b):
        a = a.strip()
        b = b.strip()
        global temp_matrix_list, temp_counter
        if "(" in a:
            a = calculate_it(a)
        if "(" in b:
            b = calculate_it(b)

        a = brackets_remover(a)
        b = brackets_remover(b)
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

        temp_matrix_list.append(Matrix("Temp"+str(temp_counter), new_matrix))
        temp_counter += 1

        return "Temp"+str(temp_counter-1)

    def plus_mat(a, b):
        a = a.strip()
        b = b.strip()
        global temp_matrix_list, temp_counter
        if "(" in a:
            a = calculate_it(a)
        if "(" in b:
            b = calculate_it(b)

        a = brackets_remover(a)
        b = brackets_remover(b)

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

        temp_matrix_list.append(Matrix("Temp" + str(temp_counter), new_matrix))
        temp_counter += 1

        return "Temp" + str(temp_counter - 1)

    def calculate_it(expr):
        expr = brackets_remover(expr)

        while "*" in expr:
            for i, e in enumerate(expr):
                if e == "*":
                    value1, value2 = "", ""
                    is_in_brackets = 0
                    for j in range(i-1, -1, -1):
                        if expr[j] == ")":
                            is_in_brackets += 1
                        if expr[j] == "(":
                            is_in_brackets -= 1
                            if is_in_brackets == 0:
                                value1 = expr[j:i]
                                break
                            elif is_in_brackets == -1:
                                value1 = expr[j+1:i]
                                break

                        if (expr[j] == "+" or expr[j] == "-" or expr[j] == "*") and not is_in_brackets:
                            value1 = expr[j+1:i]
                            break
                    else:
                        value1 = expr[0:i]

                    is_in_brackets = 0
                    for j in range(i+1, len(expr)):
                        if expr[j] == "(":
                            is_in_brackets += 1
                        if expr[j] == ")":
                            is_in_brackets -= 1
                            if is_in_brackets == 0:
                                value2 = expr[i+1:j+1]
                                break
                            elif is_in_brackets == -1:
                                value2 = expr[i+1:j]
                                break
                        if (expr[j] == "+" or expr[j] == "-" or expr[j] == "*") and not is_in_brackets:
                            value2 = expr[i+1:j]
                            break
                    else:
                        value2 = expr[i+1:]
                    ed = mult_mat(value1, value2)
                    if not ed:
                        return None
                    expr = expr.replace(value1+"*"+value2, ed)
                    break

        while "+" in expr:
            for i, e in enumerate(expr):
                if e == "+":
                    value1, value2 = "", ""
                    is_in_brackets = 0
                    for j in range(i - 1, -1, -1):
                        if expr[j] == ")":
                            is_in_brackets += 1
                        if expr[j] == "(":
                            is_in_brackets -= 1
                            if is_in_brackets == 0:
                                value1 = expr[j:i]
                                break
                            elif is_in_brackets == -1:
                                value1 = expr[j + 1:i]
                                break
                        if (expr[j] == "+" or expr[j] == "-") and not is_in_brackets:
                            value1 = expr[j + 1:i]
                            break
                    else:
                        value1 = expr[0:i]

                    is_in_brackets = False
                    for j in range(i + 1, len(expr)):
                        if expr[j] == "(":
                            is_in_brackets += 1
                        if expr[j] == ")":
                            is_in_brackets -= 1
                            if is_in_brackets == 0:
                                value2 = expr[i + 1:j + 1]
                                break
                            elif is_in_brackets == -1:
                                value2 = expr[i + 1:j]
                                break
                        if (expr[j] == "+" or expr[j] == "-") and not is_in_brackets:
                            value2 = expr[i + 1:j]
                            break
                    else:
                        value2 = expr[i + 1:]
                    ed = plus_mat(value1, value2)
                    if not ed:
                        return None
                    expr = expr.replace(value1 + "+" + value2, ed)
                    break

        return expr

    print("Введите выражение, которое хотите посчитать")
    expression = input().replace(" ", "")
    mas_chis = []
    temp_matrix_list = []
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

    temp = get_matrix_from_name(calculate_it(expression))

    if temp is None:
        print("Something gone wrong")
    else:
        temp.print_it()
    return


def find_determinant():
    def find_det(matrix):
        try:
            if len(matrix) != len(matrix[-1]):
                return None
        except:
            print("Невозможно проверить является ли матрица квадратной")
        if len(matrix) > 2:
            s = 0
            for k, e in enumerate(matrix[0]):
                new_matrix = []
                for i in range(1, len(matrix)):
                    new_matrix.append([])
                    for j in range(len(matrix)):
                        if j != k:
                            new_matrix[-1].append(matrix[i][j])

                s += e * (-1)**k * find_det(new_matrix)
            return s
        else:
            return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

    print("Введите имя матрицы которую хотите транспонировать. Доступные имена:", end=" ")
    for i in matrix_list:
        print(i.name, end=" , ")
    name = input("Введите имя: ")
    temp_id = get_matrix_id_from_name(name)
    if temp_id is None:
        print("Такое имя не найдено")
    else:
        a = find_det(matrix_list[temp_id].matrix)
        if a is not None:
            print(a)
        else:
            print("Матрица не квадратная")


def read_matrix():

    def get_matrix_via_input():
        while True:
            name = get_matrix_name()
            try:
                row = int(input("Введите кол-во строк ").strip())
                column = int(input("Введите кол-во столбцов ").strip())
            except ValueError:
                print("Введены не числа, попробуйте снова")
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
                        print("Элемент невозможно распознать")
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
        return Matrix(name, matrix_templates[a-1])

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
                        print("Невозможно распознать элемент в csv файле:", el)
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
        print("Данное имя не найдено")
    else:
        matrix_list[temp_id].print_it()


def find_norm():
    def find_all_norms_for_matrix(matrix):
        sum_rows = [0 for i in range(len(matrix.matrix))]
        sum_cols = [0 for i in range(len(matrix.matrix[0]))]
        sec_norm = 0
        for i, e in enumerate(matrix.matrix):
            for j, ee in enumerate(e):
                print(ee, sum_rows, sum_cols, sec_norm)
                sum_rows[i] += abs(ee)
                sum_cols[j] += abs(ee)
                sec_norm += abs(ee)**2
        print("Бесокнечная норма для матрицы {} - {}".format(matrix.name, max(sum_rows)))
        print("1 норма для матрицы {} - {}".format(matrix.name, max(sum_cols)))
        print("2 норма для матрицы {} - {}".format(matrix.name, math.sqrt(sec_norm)))

    print("Введите имя матрицы которую хотите вывести. Доступные имена:", end=" ")
    for i in matrix_list:
        print(i.name, end=" , ")
    name = input("Введите имя: ")
    temp_id = get_matrix_id_from_name(name)
    if temp_id is None:
        print("Данное имя не найдено")
        return
    find_all_norms_for_matrix(matrix_list[temp_id])


if __name__ == "__main__":
    matrix_list.append(Matrix("A", [[2, 0, -1], [0, -2, 2]]))
    matrix_list.append(Matrix("B", [[4.3, 1, 0], [3, 2.7, 1], [6.7, 1, 7.8]]))
    matrix_list.append(Matrix("C", [[3, 0, 7], [13, -12, 11], [10, -9, 10]]))
    matrix_list.append(Matrix("D", [[2, 3, 0, 5], [4, -3, -1, 1], [2, 5, 1, 3], [2, 7, 2, -2]]))
    matrix_list.append(Matrix("F", [[5+6j, 5.7+7j, 8j], [1, 0.5, 5], [5+8j, 5.7+7.4j, 8j]]))
    matrix_list.append(Matrix("T", [[5555555555 + 66666j, 5.7 + 7j, 8j], [1, 0.5, 5], [5 + 8j, 5.7 + 7.4j, 8j]]))
    matrix_list.append(Matrix("E", [[10, -7, 0], [-3, 2, 6], [5, -1, 5]]))
    main()
