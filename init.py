from input import get_lines


class SimplexTable:
    def __init__(self, rows):
        self.matrix = get_lines(rows)
        self.free = [i for i in range(1, len(self.matrix[0]))]
        self.base = [len(self.free) + i + 1 for i in range(len(self.matrix) - 1)]

    def solve(self):
        pass

    def __repr__(self):
        output = '\t\t\tC\t\t\t' + '\t\t\t'.join([f'x{i}' for i in self.free]) + '\n'
        rows = [f'x{str(i)}' for i in self.base] + ['F']
        for i in range(len(self.matrix)):
            output += f'{rows[i]}\t\t'
            for _ in self.matrix[i]:
                output += '%8.3f\t'
            output = output % tuple(self.matrix[i].values())
            output += '\n'
        return output
