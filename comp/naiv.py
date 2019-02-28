from comp.input import Problem, Photo
from comp.out import Solution, Slide, zipdir
from comp.score import score_of_interest, score


class Node:
    def __init__(self, tag):
        self.tag = tag
        self.photos = []
        self.children = {}

    def insert(self, photo):
        tags = sorted(photo.tags)
        current = self
        for t in tags:
            if t not in current.children:
                current.children[t] = Node(t)

            current = current.children[t]

        current.photos.append(photo)

    def walk(self):
        yield from self.photos

        for t in sorted(self.children):
            yield from self.children[t].walk()


def index(p: Problem) -> Solution:
    root = Node("")

    for id, photo in p.photos.items():
        if photo.is_vertical:
            continue

        root.insert(photo)

    return Solution([Slide(p) for p in root.walk()])


def naiv(problem: Problem) -> Solution:
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
        s = index(p)
        print("{} → {}".format(file, score(p, s)))
        s.to_file("out/{}".format(file))
    zipdir(".", "../code.zip")
