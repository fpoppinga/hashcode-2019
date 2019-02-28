from comp.input import Problem
from comp.out import Solution, Slide, zipdir
from comp.score import score_of_interest, score


def solve(problem: Problem) -> Solution:
    solution = Solution([])
    for id, photo in problem.photos.items():
        if photo.is_vertical:
            continue
        slide = Slide(photo)
        if len(solution.slides) == 0:
            solution.slides.append(slide)
            continue
        score = score_of_interest(solution.slides[-1], slide)
        if score > 0:
            solution.slides.append(slide)

    return solution


if __name__ == "__main__":

    for file in ["a_example.txt", "b_lovely_landscapes.txt", "c_memorable_moments.txt", "d_pet_pictures.txt",
                 "e_shiny_selfies.txt"]:
        p = Problem("in/{}".format(file))
        s = solve(p)
        print("{} → {}".format(file, score(p, s)))
        s.to_file("out/{}".format(file))
    zipdir(".", "../code.zip")
