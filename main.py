from init import SimplexTable

if __name__ == '__main__':
    filename = 'input1.txt'
    data = [line.replace('\n', '') for line in open(filename)]
    s_t = SimplexTable(data)
    s_t.solve()
    # print(s_t)
