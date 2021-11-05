from input import get_lines
from copy import deepcopy as dc


class SimplexTable:
    def __init__(self, rows):
        self.__matrix = get_lines(rows)
        self.table = [list(i.values()) for i in self.__matrix]
        self.__free = [i for i in range(1, len(self.__matrix[0]))]
        self.__base = [len(self.__free) + i + 1 for i in range(len(self.__matrix) - 1)]

    def __status(self):
        if min([i[0] for i in self.table[:len(self.table) - 1]]) < 0:
            # опорное решение не найдено
            return 0
        elif min(self.table[len(self.table) - 1][1:]) < 0:
            # оптимальное решение не найдено
            return 1
        else:
            return 2

    # метод нахождения разрешающего столбца и строки для поиска оптимального решения
    def __find_pivot_optimise(self, flag):
        # flag - есть значение метода __status
        if flag == 1:
            max_abs, support_column = -1, -1
            for i in range(1, len(self.table[len(self.table) - 1])):
                if self.table[len(self.table) - 1][i] < 0 and abs(self.table[len(self.table) - 1][i]) > max_abs:
                    max_abs = abs(self.table[len(self.table) - 1][i])
                    support_column = i
            min_div, support_row = 10 ** 8, -1
            for j in range(len(self.table) - 1):
                if self.table[j][support_column] != 0:
                    if abs(self.table[j][0] / self.table[j][support_column]) < min_div:
                        min_div = abs(self.table[j][0] / self.table[j][support_column])
                        support_row = j
        else:
            support_row = [i[0] for i in self.table].index(-max([abs(i[0]) for i in self.table if i[0] < 0]))
            support_column = self.table[support_row].index(min(self.table[support_row][1:]))
        print(f'Pivot column: x{self.__free[support_column - 1]}\n'
              f'Pivot row: x{self.__base[support_row]}\n'
              f'Pivot element: {round(self.table[support_row][support_column], 3)}\n\n')
        self.__free[support_column - 1], self.__base[support_row] = self.__base[support_row], self.__free[
            support_column - 1]
        return support_row, support_column

    def __jordan_exception(self, pair_of_coord):
        support_row, support_column = pair_of_coord
        pivot = self.table[support_row][support_column]
        simplex_table_iter = dc(self.table)
        for i in range(len(simplex_table_iter)):  # rows
            for j in range(len(simplex_table_iter[0])):  # cols
                if i == support_row and j != support_column:
                    simplex_table_iter[i][j] = self.table[i][j] / pivot
                elif i != support_row and j == support_column:
                    simplex_table_iter[i][j] = -self.table[i][j] / pivot
                elif i == support_row and j == support_column:
                    simplex_table_iter[i][j] = 1 / pivot
                else:
                    simplex_table_iter[i][j] = self.table[i][j] - (
                            self.table[support_row][j] * self.table[i][support_column]) / pivot
        return simplex_table_iter

    def solve(self):
        iteration = 0
        while True:
            print(f'Iteration number {iteration}')
            iteration += 1
            print(self)
            status = self.__status()
            if status != 2:
                self.table = dc(self.__jordan_exception(self.__find_pivot_optimise(status)))
                continue
            else:
                return

    def __repr__(self):
        output = '\t\t\tC\t\t\t' + '\t\t\t'.join([f'x{i}' for i in self.__free]) + '\n'
        rows = [f'x{str(i)}' for i in self.__base] + ['F']
        for i in range(len(self.table)):
            output += f'{rows[i]}\t\t' + ('%8.3f\t' * len(self.table[i]) % tuple(self.table[i])) + '\n'
        return output
