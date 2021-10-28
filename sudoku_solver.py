from math import sqrt
import z3


def get_square(x, y, arr):
    side_of_square = int(sqrt(len(arr)))
    return [arr[i][j] for i in range(x * side_of_square, (x + 1) * side_of_square)
            for j in range(y * side_of_square, (y + 1) * side_of_square)]


def main():
    solver = z3.Solver()
    instance_of_sudoku = [[int(j) for j in input().split()] for _ in range(4)]
    sudoku = [[z3.Int(f'var_{i}_{j}') for i in range(4)] for j in range(4)]
    # Define borders of numbers
    constraints = [z3.And(sudoku[i][j] > 0, sudoku[i][j] < 5) for i in range(4) for j in range(4)]
    # Distinct digits in rows
    row = [z3.Distinct(sudoku[i]) for i in range(4)]
    # Distinct digits in columns
    cells = [z3.Distinct([sudoku[j][i] for j in range(4)]) for i in range(4)]
    # Distinct digits in squares
    squares = [z3.Distinct(get_square(i, j, sudoku)) for i in range(2) for j in range(2)]
    # Set known variables
    data = [sudoku[i][j] == instance_of_sudoku[i][j] for j in range(4)
            for i in range(4) if instance_of_sudoku[i][j] != 0]
    solver.add(constraints + row + cells + squares + data)
    print()
    if solver.check() == z3.sat:
        model = solver.model()
        print(*[' '.join([str(model.evaluate(j)) for j in i]) for i in sudoku], sep='\n')
    else:
        print("Can`t find solution.")


if __name__ == '__main__':
    main()
