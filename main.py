# Copyright 2021 Peter p.makretskii@gmail.com
from init import SimplexTable

if __name__ == '__main__':
    filename = 'input1.txt'
    data = [line.replace('\n', '') for line in open(filename)]
    output = SimplexTable(data).solve()

    if type(output) is tuple:
        print('The answer is:')
        for i in range(len(output[0])):
            print(f'x{i + 1} = {output[0][i]}')
        print(f'F = {output[1]}')
    else:
        print(output)
