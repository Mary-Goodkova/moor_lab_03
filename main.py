from init import SimplexTable

if __name__ == '__main__':
    filename = 'input.txt'
    data = [line.replace('\n', '') for line in open(filename)]
    s_t = SimplexTable(data)
    print(s_t)
