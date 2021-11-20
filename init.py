# Copyright 2021 Peter p.makretskii@gmail.com
import math
from input import get_lines, print_answer
from copy import deepcopy as dc


# класс "симплекс таблица"
class SimplexTable:
    # в конструктор подается список строк, прочитанных из файла
    def __init__(self, rows):
        self.__rows = rows
        # симплекс-таблица, представляемая списком словарей
        self.__matrix = get_lines(self.__rows)
        # симплекс-таблица, представляемая списком списков
        self.__table = [list(i.values()) for i in self.__matrix]
        # число отрицательных значений в столбце свободных членов
        self.__minus_count = len(self.__matrix[0])
        # список индексов свободных переменных
        self.__free = [i for i in range(1, len(self.__matrix[0]))]
        # список индексов базисных переменных
        self.__base = [len(self.__free) + i + 1 for i in range(len(self.__matrix) - 1)]

    # геттер для симплекс таблицы
    def get_rows(self):
        return self.__rows

    # метод определяет, нужно оптимизировать решение или искать опорное
    def __status(self):
        s_minuses = [i[0] for i in self.__table[:-1] if i[0] < 0]  # минусы столбца свободных членов
        if s_minuses:
            # опорное решение не найдено
            if len(s_minuses) >= self.__minus_count:
                # решений нет
                return 4
            # запоминаем число отрицательных значений в столбце свободных членов
            self.__minus_count = len(s_minuses)
            return 0
        if min(self.__table[-1][1:]) < 0:
            # оптимальное решение не найдено
            return 1
        return 3

    # метод нахождения разрешающего столбца и строки для поиска оптимального решения
    def __find_pivot_optimise(self, flag, show=True):
        # show = True, когда нужно выводить на экран промежуточные симплекс таблицы
        # flag - значение метода __status
        if flag == 1:
            # случай, когда надо искать оптимальное решение
            max_abs, support_column = -1, -1
            for i in range(1, len(self.__table[-1])):
                if self.__table[-1][i] < 0 and abs(self.__table[-1][i]) > max_abs:
                    max_abs = abs(self.__table[-1][i])
                    support_column = i
            min_div, support_row = 10 ** 8, -1
            for j in range(len(self.__table) - 1):
                if self.__table[j][support_column] > 0:
                    if abs(self.__table[j][0] / self.__table[j][support_column]) < min_div:
                        min_div = abs(self.__table[j][0] / self.__table[j][support_column])
                        support_row = j
        else:
            # случай, когда надо искать опорное решение
            max_abs, support_row = -1, -1
            for i in range(len(self.__table) - 1):
                if self.__table[i][0] < 0 and abs(self.__table[i][0]) >= max_abs:
                    max_abs = abs(self.__table[i][0])
                    support_row = i
            min_div, support_column = 10 ** 8, -1
            for j in range(1, len(self.__table[-1])):
                if self.__table[support_row][j] != 0:
                    if abs(self.__table[-1][j] / self.__table[support_row][j]) <= min_div:
                        min_div = abs(self.__table[-1][j] / self.__table[support_row][j])
                        support_column = j
        if show:
            # печатаем результат
            print(f'Pivot column: x{self.__free[support_column - 1]}\n'
                  f'Pivot row: x{self.__base[support_row]}\n'
                  f'Pivot element: {round(self.__table[support_row][support_column], 3)}\n\n')
        self.__free[support_column - 1], self.__base[support_row] = self.__base[support_row], self.__free[
            support_column - 1]
        return support_row, support_column

    # метод, осуществляющий алгоритм Жорданова исключения
    def __jordan_exception(self, pair_of_coord):
        support_row, support_column = pair_of_coord
        pivot = self.__table[support_row][support_column]
        simplex_table_iter = dc(self.__table)
        for i in range(len(simplex_table_iter)):  # rows
            for j in range(len(simplex_table_iter[0])):  # cols
                if i == support_row and j != support_column:
                    simplex_table_iter[i][j] = self.__table[i][j] / pivot
                elif i != support_row and j == support_column:
                    simplex_table_iter[i][j] = -self.__table[i][j] / pivot
                elif i == support_row and j == support_column:
                    simplex_table_iter[i][j] = 1 / pivot
                else:
                    simplex_table_iter[i][j] = self.__table[i][j] - (
                            self.__table[support_row][j] * self.__table[i][support_column]) / pivot
        return simplex_table_iter

    # метод, осуществляющий решение задачи
    def solve(self, show=True):
        iteration = 0
        while True:
            if show:
                print(f'Iteration number {iteration}')
            iteration += 1
            if show:
                print(self)
            status = self.__status()  # определяем, нужно оптимизировать или искать опорное решение
            if status != 2 and status != 3 and status != 4:
                self.__table = dc(self.__jordan_exception(self.__find_pivot_optimise(status, show)))
                continue
            elif status == 3:
                # задача решена
                output_vars = [i for i in range(1, max(self.__matrix[0].keys()) + 1)]
                output = []
                for i in output_vars:  # собираем значения исходных переменных
                    if i in self.__base:
                        ind = self.__base.index(i)
                        output.append(round(self.__table[ind][0], 3))
                    else:
                        ind = self.__free.index(i)
                        output.append(round(self.__table[0][ind], 3))
                return output, round(self.__table[-1][0], 3)
            else:
                # решений нет
                return 'No solution'

    # метод печати симплекс-таблицы
    def __repr__(self):
        output = '\t\t\tC\t\t\t' + '\t\t\t'.join([f'x{i}' for i in self.__free]) + '\n'
        rows = [f'x{str(i)}' for i in self.__base] + ['F']
        for i in range(len(self.__table)):
            output += f'{rows[i]}\t\t' + \
                      ('%8.3f\t' * len(self.__table[i]) %
                       tuple(self.__table[i])) + '\n'
        return output


# функция, проверяющая, есть ли в результате решения задачи нецелые числа
def is_integer(answer):
    for i in answer[0]:
        if i != round(i):
            return False
    return True


# рекурсивная функция решения задачи ЦЛП
def solve_in_integer_recursion(rows):
    solution = SimplexTable(rows).solve(show=False)
    if type(solution) is tuple:
        if is_integer(solution):
            # условие выхода из рекурсии - нахождение целочисленного решения
            return solution
        collection = []
        for i in range(len(solution[0])):
            if solution[0][i] != round(solution[0][i]):
                rows_less = rows.copy()
                rows_less.insert(len(rows_less) - 1, f'x{i + 1}<={math.floor(solution[0][i])}')
                result = solve_in_integer_recursion(
                    rows_less)  # вход в рекурсию после добавления дополнительного ограничения
                if result is not None:
                    collection += result

                rows_more = rows.copy()
                rows_more.insert(len(rows_more) - 1, f'x{i + 1}>={math.ceil(solution[0][i])}')
                result = solve_in_integer_recursion(
                    rows_more)  # вход в рекурсию после добавления дополнительного ограничения
                if result is not None:
                    collection += result
        return collection
    else:
        # задача не имеет решений в нецелых числах
        return


def solve_in_integer(simplex_table):
    solution = simplex_table.solve(show=False)
    print('Original task:')
    if print_answer(solution):
        collection = solve_in_integer_recursion(simplex_table.get_rows())
        collection = [(collection[i], collection[i + 1]) for i in range(0, len(collection) - 1, 2)]

        to_out = []
        for _ in collection:
            if _ not in to_out:
                to_out.append(_)

        # оптимальное значение
        optimal_f, optimal_str = -10 ** 10, ''
        print('\nAll valid answers:')
        for answer in to_out:
            # вывод результата
            output = 'x%i =\t' * len(answer[0])
            output = output % tuple(i for i in range(1, len(answer[0]) + 1))
            output = output.replace('=\t', '= %5.3f\t')
            output %= tuple(answer[0])
            output += f'F = {answer[1]}'
            if answer[1] > optimal_f:
                optimal_str = output
            print(output)
        print(f'\nOptimal is:\n{optimal_str}')
    else:
        print('Can not find solution in integer')
