import copy
import fractions
import decimal
import csv
import os


def main():
    def calculate_solutions(matrix, vector_ot, target_value=100):
        reverse_matrix = find_reverse_matrix(matrix)
        reverse_vector_ot = find_reverse_matrix(vector_ot)

        yakobi_solutions = yakobi(matrix, vector_ot)
        yakobi_solutions_rev = yakobi(reverse_matrix, vector_ot)

        temp_matrix = solve_eq(matrix, yakobi_solutions)
        temp_matrix_reverse = find_reverse_matrix(temp_matrix)

        print_matrix(temp_matrix_reverse, False)

        coef_obusl = find_norm(temp_matrix) * find_norm(temp_matrix_reverse)

        if coef_obusl < target_value:
            print("Матрица обусловленна хорошо для метода Якоби:", coef_obusl)
            return yakobi_solutions, reverse_matrix
        else:
            print("Матрица обусловлена плохо для метода Якоби:", coef_obusl)
            print("Решения для метода Якоби")
            print_matrix(yakobi_solutions, True)

        print()

        gaus_solution_first = gaus_jourdan(matrix, vector_ot)
        gaus_solution_first_reverse = gaus_jourdan(reverse_matrix, vector_ot)

        new_gaus_solutions_first = []
        for i in range(len(gaus_solution_first)):
            new_gaus_solutions_first.append([])
            for j in range(len(gaus_solution_first[0])):
                if j >= len(matrix[0]):
                    new_gaus_solutions_first[i].append(gaus_solution_first[i][j])
        gaus_solution_first = new_gaus_solutions_first


        temp_matrix = solve_eq(matrix, gaus_solution_first)
        temp_matrix_reverse = find_reverse_matrix(temp_matrix)
        print_matrix(matrix, False)
        print_matrix(gaus_solution_first, True)
        print()
        print_matrix(temp_matrix, False)
        print_matrix(temp_matrix_reverse, False)
        coef_obusl = find_norm(temp_matrix) * find_norm(temp_matrix_reverse)

        if coef_obusl < target_value:
            print("Матрица обусловленна хорошо для метода Жордана-Гаусса:", coef_obusl)
            return gaus_solution_first, reverse_matrix
        else:
            print("Матрица обусловленна плохо для метода Жордана-Гаусса:", coef_obusl)
            print("Решения для метода Жордана-Гаусса")
            print_matrix(gaus_solution_first, True)

        print()
        matrix_fraction = convert_matrix_to_fraction(copy.deepcopy(matrix))
        vector_ot_fraction = convert_matrix_to_fraction(copy.deepcopy(vector_ot))

        gaus_solution_second = gaus_jourdan(matrix_fraction, vector_ot_fraction)
        gaus_solution_second = convert_matrix_to_float(gaus_solution_second)

        new_gaus_solution_second = []

        for i in range(len(gaus_solution_second)):
            new_gaus_solution_second.append([])
            for j in range(len(gaus_solution_second[0])):
                if j >= len(matrix[0]):
                    new_gaus_solution_second[i].append(gaus_solution_second[i][j])

        return new_gaus_solution_second, reverse_matrix

    """
    print("ВВОД ИСХОДНОЙ МАТРИЦЫ")
    matrix = read_matrix()
    if matrix is None:
        return
    print("ВВОД ВЕКТОРА СВОБОДНЫХ ЧЛЕНОВ")
    vector_ot = read_matrix(size=len(matrix))
    if vector_ot is None:
        return
    """
    matrix = [[1, 2], [1, 1.9999]]
    vector_ot = [[3.01], [3]]

    deter = find_det(matrix)
    if deter is None:
        print("Матрица не является квадратной")
        return
    elif deter == 0:
        print("Матрица является вырожденной. Определитель равен 0")
        return

    solutions, reverse_matrix = calculate_solutions(matrix, vector_ot)
    print("Исходная матрица:")
    print_matrix(matrix, False)
    print("Вектор свободных членов")
    print_matrix(vector_ot, True)
    print("Обратная матрица")
    print_matrix(reverse_matrix, False)
    print("Вектор переменных")
    print_matrix(solutions, True)


def solve_eq(matrix, resh):
    new_matrix = []
    for i, e in enumerate(matrix):
        new_matrix.append([])
        for j, ee in enumerate(e):
            new_matrix[i].append(ee*resh[j][0])
    return new_matrix



def yakobi(matrix, vector_ot, iter_count=300):
    vector_sol = [0 for i in range(len(matrix))]
    for k in range(iter_count):
        vector_sol_n = [0 for i in range(len(matrix))]
        for i in range(len(matrix)):
            t = 0
            for j in range(len(matrix)):
                if j == i:
                    continue
                t += (-1 * matrix[i][j])/matrix[i][i] * vector_sol[j]
            t += vector_ot[i][0] / matrix[i][i]
            vector_sol_n[i] = t
        for i in range(len(vector_sol)):
            if abs(vector_sol[i] - vector_sol_n[i]) > 0.001:
                break
        else:
            vector_sol = vector_sol_n
            break
        vector_sol = vector_sol_n

    for i in range(len(vector_sol)):
        vector_sol[i] = [vector_sol[i]]

    return vector_sol


def gaus_jourdan(matrixs, vector_ot):
    matrix = copy.deepcopy(matrixs)
    for i in range(len(matrix)):
        if isinstance(vector_ot[i], list):
            for j in vector_ot[i]:
                matrix[i].append(j)
        else:
            matrix[i].append(vector_ot[i])

    for i in range(len(matrix)):
        temp_matrix = []
        for j in range(len(matrix[0])):
            if matrix[i][i] == 0:
                temp_matrix.append(matrix[i][j] / 0.0000000001)
            else:
                temp_matrix.append(matrix[i][j] / matrix[i][i])
        matrix[i] = temp_matrix
        for j in range(len(matrix)):
            temp_matrix = []
            if j == i:
                continue
            for k in range(len(matrix[0])):
                temp_matrix.append(matrix[j][k]-matrix[i][k]*matrix[j][i])
            matrix[j] = temp_matrix

    return matrix


def convert_matrix_to_fraction(matrixs):
    matrix = copy.deepcopy(matrixs)
    for i in range(len(matrix)):
        if isinstance(matrix[i], list):
            for j in range(len(matrix[i])):
                matrix[i][j] = fractions.Fraction(matrix[i][j])
        else:
            matrix[i] = fractions.Fraction(matrix[i])
    return matrix


def convert_matrix_to_float(matrixs):

    def decimal_from_fraction(frac):
        return frac.numerator / decimal.Decimal(frac.denominator)

    matrix = copy.deepcopy(matrixs)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = decimal_from_fraction(matrix[i][j])
    return matrix


def find_reverse_matrix(matrix):
    matrix_size = len(matrix)
    new_matrix = []
    for i in range(matrix_size):
        new_matrix.append([])
        for j in range(matrix_size):
            if i == j:
                new_matrix[-1].append(1)
            else:
                new_matrix[-1].append(0)

    matrix = gaus_jourdan(matrix, new_matrix)
    new_matrix = []
    for i in range(len(matrix)):
        new_matrix.append([])
        for j in range(len(matrix[0])):
            if j >= matrix_size:
                new_matrix[i].append(matrix[i][j])

    return new_matrix


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


def find_norm(matrix):
    sum_rows = [0 for i in range(len(matrix))]
    for i, e in enumerate(matrix):
        for j, ee in enumerate(e):
            sum_rows[i] += abs(ee)
    return max(sum_rows)


def print_matrix(matrix, is_solutions):
    space_between = 12
    for i in matrix:
        for j in i:
            if space_between < len(str(j)):
                space_between = len(str(j)) + 1

    for i in matrix:
        for j in i:
            el = str(j)
            prob = space_between - len(el)
            prob1 = prob // 2
            prob2 = prob - prob1
            print(" " * prob1, el, " " * prob2, sep="", end="")
        if not is_solutions:
            print()
    if is_solutions:
        print()


def read_matrix(size=None):
    def get_matrix_via_input(size=None):
        row, column = 0, 0
        if size:
            print("Введите вектор свободных членов")
            row = size
            column = 1
        else:
            print("Введите матрицу")

        while not size:
            try:
                row = int(input("Введите кол-во строк ").strip())
                column = int(input("Введите кол-во столбцов ").strip())
            except ValueError:
                print("Введены не числа, попробуйте снова")
            else:
                if row <= 0 or column <= 0:
                    print("Одно из чисел меньше или равно 0")
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
        return matrix

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

    print("Как ввести матрицу:\n1)Забить поэлементно\n2)Забить из csv файла")

    user_input = get_user_number(2)
    temp_matrix = []

    if user_input == 0:
        return
    elif user_input == 1:
        if size:
            temp_matrix = get_matrix_via_input(size=size)
        else:
            temp_matrix = get_matrix_via_input()
    elif user_input == 2:
        temp_matrix = get_matrix_from_csv()
        if temp_matrix is None:
            return None
        if size:
            if len(temp_matrix) != size:
                print("Размер матрицы свободных членов не сходится с размером исходной матрицы")
                return None
            for i in temp_matrix:
                if len(i) != 1:
                    print("В одной строке не может быть больше одного числа")
                    return None

    return temp_matrix


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
    input("Введите что-нибудь для выхода ")
