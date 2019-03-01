from comp.input import Problem, Photo
from comp.out import Solution, Slide, zipdir
from comp.score import score_of_interest, score, join_tags


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
        idx = 0
        for t in sorted(self.children):
            for c in self.children[t].walk():
                if idx < len(self.photos):
                    yield self.photos[idx]
                yield c
                idx += 1

        yield from self.photos[idx:]


def index(p: Problem) -> Solution:
    root = Node("")

    for id, photo in p.photos.items():
        root.insert(photo)

    vertical = None
    slides = []
    for photo in root.walk():
        if photo.is_vertical:
            if vertical is None:
                vertical = photo
            else:
                t1 = vertical.tags
                t2 = photo.tags

                common_tags = len(t1.intersection(t2))
                d1 = len(t1.difference(t2))
                d2 = len(t2.difference(t1))

                if common_tags > min(d1, d2):
                    slides.append(Slide(vertical, photo))

                vertical = None
            continue

        slides.append(Slide(photo))

    return Solution(slides)


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
