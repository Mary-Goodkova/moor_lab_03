# Copyright 2021 Peter p.makretskii@gmail.com
from init import SimplexTable, solve_in_integer
from input import print_answer

# точка входа в программу
if __name__ == '__main__':
    filename = 'input1.txt'
    # чтение данных из файла, запись их в список
    data = [line.replace('\n', '') for line in open(filename)]
    # вызов метода print_answer для печати решения задачи
    print_answer(SimplexTable(data).solve())
    # печать разделителя
    print(f"\n{'-' * 50}\n")
    # вызов метода, решающего задачу целочисленного программирования
    solve_in_integer(SimplexTable(data))
