from comp.input import Problem, Photo
from comp.out import Solution, Slide, zipdir
from comp.score import score_of_interest, score, join_tags


class Node:
    def __init__(self, tag):
        self.tag = tag
        self.slides = []
        self.children = {}

    def insert(self, slide):
        tags = sorted(join_tags(slide.photo1, slide.photo2))
        current = self
        for t in tags:
            if t not in current.children:
                current.children[t] = Node(t)

            current = current.children[t]

        current.slides.append(slide)

    def walk(self):
        yield from self.slides

        for t in sorted(self.children):
            yield from self.children[t].walk()


def index(p: Problem) -> Solution:
    root = Node("")

    vertical = None
    for id, photo in p.photos.items():
        if photo.is_vertical:
            if vertical is None:
                vertical = photo
            else:
                root.insert(Slide(photo, vertical))
                vertical = None

            continue

        root.insert(Slide(photo))

    return Solution(list(root.walk()))


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
