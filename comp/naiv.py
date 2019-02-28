from comp.input import Problem
from comp.out import Solution, Slide, zipdir


def solve(problem: Problem) -> Solution:
    return Solution([Slide(problem.photos[0])])


if __name__ == "__main__":

    for file in ["a_example.txt", "b_lovely_landscapes.txt", "c_memorable_moments.txt", "d_pet_pictures.txt", "e_shiny_selfies.txt"]:
        p = Problem("in/{}".format(file))
        s = solve(p)
        s.to_file("out/{}".format(file))
    zipdir(".", "../code.zip")