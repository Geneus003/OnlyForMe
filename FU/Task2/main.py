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


def main():
    # matrix = get_matrix_via_input()
    # vector_ot = get_matrix_via_input(len(matrix))
    matrix = [[5, -3, 1], [-0.5, 3, 2], [1, -2, 5]]
    vector_ot = [3, 0.5, 4]
    print(matrix, vector_ot)
    yakobi(matrix, vector_ot)


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


def yakobi(matrix, vector_ot, iter_count=200):
    vector_sol = [0 for i in range(len(matrix))]
    for k in range(iter_count):
        vector_sol_n = [0 for i in range(len(matrix))]
        print(k, vector_sol)
        for i in range(len(matrix)):
            t = 0
            for j in range(len(matrix)):
                if j == i:
                    continue
                t += (-1 * matrix[i][j])/matrix[i][i] * vector_sol[j]
            t += vector_ot[i] / matrix[i][i]
            vector_sol_n[i] = t
        for i in range(len(vector_sol)):
            if abs(vector_sol[i] - vector_sol_n[i]) > 0.001:
                break
        else:
            vector_sol = vector_sol_n
            break
        vector_sol = vector_sol_n

    print(vector_sol)


if __name__ == "__main__":
    main()
