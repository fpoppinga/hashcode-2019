import argparse

import numpy as np
from sample.io import Problem, Solution, Piece, score


def valid(problem, piece):
    pizza_slice = piece.cut(problem.pizza)
    area = piece.area()
    mushroom_count = int(np.sum(pizza_slice))
    tomato_count = area - mushroom_count

    return area <= problem.max_cells and mushroom_count >= problem.min_ingredients and tomato_count >= problem.min_ingredients


def cost(problem, piece):
    if valid(problem, piece):
        return 1
    return 0


def split(problem, piece):
    yy, xx = piece.cut(problem.pizza).shape

    border = int(piece.x2 - xx / 2)
    b1, b2 = Piece(piece.x1, piece.y1, border, piece.y2), \
             Piece(border + 1, piece.y1, piece.x2, piece.y2)
    max_score = cost(problem, b1) + cost(problem, b2)

    for border in range(piece.x1, piece.x2):
        p1, p2 = Piece(piece.x1, piece.y1, border, piece.y2), \
                 Piece(border + 1, piece.y1, piece.x2, piece.y2)
        the_score = cost(problem, p1) + cost(problem, p2)
        if the_score > max_score:
            max_score = the_score
            b1, b2 = p1, p2

    for border in range(piece.y1, piece.y2):
        p1, p2 = Piece(piece.x1, piece.y1, piece.x2, border), \
                 Piece(piece.x1, border + 1, piece.x2, piece.y2)
        the_score = cost(problem, p1) + cost(problem, p2)
        if the_score > max_score:
            max_score = the_score
            b1, b2 = p1, p2

    return b1, b2


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
    parser.add_argument("--problem", default="in/d_big.in")
    parser.add_argument("--solution", default="out/d_big.out")
    args = parser.parse_args()

    p = Problem(args.problem)
    s = solve(p)
    s.to_file(args.solution)

    score(p, s)
