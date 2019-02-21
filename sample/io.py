import numpy as np
import argparse


class Piece:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def area(self):
        return (abs(self.x2 - self.x1) + 1) * (abs(self.y2 - self.y1) + 1)

    def cut(self, pizza):
        return pizza[self.y1:(self.y2 + 1), self.x1:(self.x2 + 1)]

    def __str__(self):
        return "{} {} {} {}".format(self.y1, self.x1, self.y2, self.x2, self.area())


class Solution:
    def __init__(self, pieces):
        self.max_rows = len(pieces)
        self.pieces = pieces

    def to_file(self, path):
        with open(path, "w") as result_file:
            result_file.write("{}\n".format(self.max_rows))
            for piece in self.pieces:
                result_file.writelines("{}\n".format(piece))

    @staticmethod
    def from_file(path):
        pieces = []
        with open(path, "r") as result_file:
            max_rows = int(result_file.readline())
            row_num = 0
            for line in result_file:
                row_num = row_num + 1
                if row_num > max_rows:
                    raise Exception("More piece-lines than defined in header: (>={})!".format(row_num))
                piece = Piece(*map(int, line.split(" ")))
                print("piece: {} → {}".format(piece, piece.area()))
                pieces.append(piece)
        return Solution(pieces)


class Problem:
    def __init__(self, path):
        with open(path, "r") as f:
            preamble = f.readline().split()
            [r, c, min_ingredients, max_cells] = map(int, preamble)

            self.rows = r
            self.cols = c
            self.min_ingredients = min_ingredients
            self.max_cells = max_cells

            lines = f.readlines()

            # We define:
            # T <=> 0
            # M <=> 1
            pizza = np.zeros((r, c), dtype=np.uint8)
            for rr, line in enumerate(lines):
                for cc, char in enumerate(line.strip()):
                    pizza[rr, cc] = 0 if char == "T" else 1

            print(pizza)
            self.pizza = pizza


def score(problem: Problem, solution: Solution):
    occupied = np.zeros((problem.rows, problem.cols))
    score = 0
    for piece in solution.pieces:
        score = score + piece.area()
        occupied[piece.x1: piece.x2 + 1, piece.y1: piece.y2 + 1] += 1
    if occupied.max() > 1:
        raise Exception("Double occupation: ", occupied)
    print("final score: {}".format(score))
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", default="in/a_example.in")
    parser.add_argument("--solution", default="out/a_example.out")
    args = parser.parse_args()

    p = Problem(args.problem)
    s = Solution.from_file(args.solution)

    score(p, s)
