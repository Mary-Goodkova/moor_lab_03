import re


def check_validation(line):
    if 'F' in line:
        if 'max' in line or 'min' in line:
            if line.find('->') < line.find('m'):
                return
    else:
        if '<=' in line or '>=' in line:
            return
    raise Exception('wrong format of input data')


def parse(line):
    check_validation(line)
    if 'F' in line:
        line = line.replace('F=', '')
        if 'max' in line:
            line = line.replace('->max', '>=0')
        else:
            line = line.replace('->min', '<=0')
    flag = 1 - 2 * int('>=' in line)
    target = float(line[line.find('=') + 1:]) * flag
    line = line[:line.find('=') - 1]
    terms = re.split('-|\+', line)
    terms = ['-' + i if line[line.find(i) - 1] == '-' else i for i in terms]
    if '' in terms:
        terms.remove('')
    vec = []
    for term in terms:
        split_term = term.split('x')
        split_term[0], split_term[1] = int(split_term[1]), split_term[0]
        for i in range(len(split_term)):
            if not split_term[i]:
                split_term[i] = '1'
            elif split_term[i] == '-':
                split_term[i] = '-1'
        vec.append([i for i in split_term])
    vec.append([-1, target])
    vec = dict(vec)
    for ind in vec:
        vec[ind] = float(vec[ind]) * flag
    return dict(sorted(vec.items(), key=lambda i: i[0]))


def get_lines(rows):
    rows = [parse(row) for row in rows]
    variables = max([max(i.keys()) for i in rows])
    for row in rows:
        for var in range(1, variables + 1):
            if var not in row.keys():
                row[var] = 0
    return rows
