# Copyright 2021 Peter p.makretskii@gmail.com
from input import get_lines
from copy import deepcopy as dc


class SimplexTable:
    def __init__(self, rows):
        # симплекс-таблица, представляемая списком словарей
        self.__matrix = get_lines(rows)

        # симплекс-таблица, представляемая списком списков
        self.__table = [list(i.values()) for i in self.__matrix]
        #
        self.__buffer = []
        #
        self.__minus_pos = len(self.__matrix[0])
        # список индексов свободных переменных
        self.__free = [i for i in range(1, len(self.__matrix[0]))]
        # список индексов базисных переменных
        self.__base = [len(self.__free) + i + 1 for i in range(len(self.__matrix) - 1)]

    # метод определяет, нужно оптимизировать решение или искать опорное
    def __status(self):
        s_minuses = [i[0] for i in self.__table[:-1] if i[0] < 0]  # минусы столбца свободных членов
        if s_minuses:
            # опорное решение не найдено
            if len(s_minuses) >= self.__minus_pos:
                # решений нет
                return 4
            self.__minus_pos = len(s_minuses)
            return 0
        if min(self.__table[-1][1:]) < 0:
            # оптимальное решение не найдено
            return 1
        return 3

    # метод нахождения разрешающего столбца и строки для поиска оптимального решения
    def __find_pivot_optimise(self, flag):
        # flag - есть значение метода __status
        if flag == 1:
            max_abs, support_column = -1, -1
            for i in range(1, len(self.__table[-1])):
                if self.__table[-1][i] < 0 and abs(self.__table[-1][i]) > max_abs:
                    max_abs = abs(self.__table[-1][i])
                    support_column = i
            min_div, support_row = 10 ** 8, -1
            for j in range(len(self.__table) - 1):
                if self.__table[j][support_column] != 0:
                    if abs(self.__table[j][0] / self.__table[j][support_column]) < min_div:
                        min_div = abs(self.__table[j][0] / self.__table[j][support_column])
                        support_row = j
        else:
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
    def solve(self):
        iteration = 0
        while iteration < 5:
            print(f'Iteration number {iteration}')
            iteration += 1
            print(self)
            status = self.__status()
            if status != 2 and status != 3 and status != 4:
                self.__table = dc(self.__jordan_exception(self.__find_pivot_optimise(status)))
                continue
            elif status == 3:
                output_vars = [i for i in range(1, max(self.__matrix[0].keys()) + 1)]
                output = []
                for i in output_vars:
                    if i in self.__base:
                        ind = self.__base.index(i)
                        output.append(round(self.__table[ind][0], 3))
                    else:
                        ind = self.__free.index(i)
                        output.append(round(self.__table[0][ind], 3))
                return output, round(self.__table[-1][0], 3)
            else:
                return 'No solution'

    # метод, осуществляющий рекурсию для решения задачи в целых числах
    def __solve_in_integer_recursive(self, got_answers):
        for row in self.__table:
            if round(row[0]) != row[0]:
                if self.__table.index(row) not in got_answers:
                    got_answers[self.__table.index(row)] = {}
                # больше
                new_row = [int(row[0]) - row[0]]
                for value in row[1:]:
                    new_row.append(-value)
                self.__table.insert(len(self.__table) - 1, new_row)
                solution = self.solve()
                if solution == 'No solution':
                    return got_answers
                if not [val for val in solution[0] if val != round(val)]:
                    got_answers[self.__table.index(row)]['+'] = solution
                    return got_answers
                else:
                    print('didnt solved')

                # меньше
                new_row = [row[0] - int(row[0])]
                for value in row[1:]:
                    new_row.append(value)
                self.__table.insert(len(self.__table) - 1, new_row)
                solution = self.solve()
                if solution == 'No solution':
                    return got_answers
                if not [val for val in solution[0] if val != round(val)]:
                    got_answers[self.__table.index(row)]['-'] = solution
                    return got_answers
                else:
                    print('didnt solve')

    # метод, осуществляющий решение задачи в целых числах
    def solve_in_integer(self):
        solution = self.solve()
        if solution == 'No solution' or not [val for val in solution[0] if val != round(val)]:
            return solution
        answer = {}
        self.__buffer = dc(self.__table)
        print(self.__solve_in_integer_recursive(answer))

    def __repr__(self):
        output = '\t\t\tC\t\t\t' + '\t\t\t'.join([f'x{i}' for i in self.__free]) + '\n'
        rows = [f'x{str(i)}' for i in self.__base] + ['F']
        for i in range(len(self.__table)):
            output += f'{rows[i]}\t\t' + \
                      ('%8.3f\t' * len(self.__table[i]) %
                       tuple(self.__table[i])) + '\n'
        return output
