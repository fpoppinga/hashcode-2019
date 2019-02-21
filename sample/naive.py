import argparse

import numpy as np
from sample.io import Problem, Solution, Piece, score


def valid(problem, piece):
    pizza_slice = piece.cut(problem.pizza)
    area = piece.area()
    mushroom_count = int(np.sum(pizza_slice))
    tomato_count = area - mushroom_count

    print(pizza_slice)
    print("shrooms:", mushroom_count)
    print("tomatos:", tomato_count)

    return area <= problem.max_cells and mushroom_count >= problem.min_ingredients and tomato_count >= problem.min_ingredients


def split(problem, piece):
    yy, xx = piece.cut(problem.pizza).shape

    border = int(piece.x2 - xx / 2)
    p1, p2 = Piece(piece.x1, piece.y1, border, piece.y2),\
           Piece(border + 1, piece.y1, piece.x2, piece.y2)

    return p1, p2


def dnc(problem, piece):
    if piece.area() == 0:
        return []

    if valid(problem, piece):
        return [piece]

    p1, p2 = split(problem, piece)

    if p1.area() == piece.area() or p2.area() == piece.area():
        return []

    return dnc(problem, p1) + dnc(problem, p2)


def solve(problem: Problem) -> Solution:
    pizza = problem.pizza
    yy, xx = pizza.shape
    piece = Piece(0, 0, xx - 1, yy - 1)

    return Solution(dnc(problem, piece))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", default="in/c_medium.in")
    parser.add_argument("--solution", default="out/c_medium.out")
    args = parser.parse_args()

    p = Problem(args.problem)
    s = solve(p)
    s.to_file(args.solution)

    score(p, s)
