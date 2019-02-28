from comp.out import Solution, Slide
from comp.input import Photo, Problem


def join_tags(p1: Photo, p2: Photo = None):
    if p2 is None:
        return p1.tags

    return p1.tags.union(p2.tags)


def score_of_interest(s1: Slide, s2: Slide):
    t1 = join_tags(s1.photo1, s1.photo2)
    t2 = join_tags(s2.photo1, s2.photo2)

    common_tags = len(t1.intersection(t2))
    d1 = len(t1.difference(t2))
    d2 = len(t2.difference(t1))

    return min(common_tags, d1, d2)


def score(p: Problem, s: Solution):
    sum = 0
    for s1, s2 in zip(s.slides[:-1], s.slides[1:]):
        sum += score_of_interest(
            Slide(p.photos[s1.photo1.id], p.photos[s1.photo2.id] if s1.photo2 is not None else None),
            Slide(p.photos[s2.photo1.id], p.photos[s2.photo2.id] if s2.photo2 is not None else None))

    return sum


if __name__ == "__main__":
    p = Problem("in/a_example.txt")
    s = Solution.from_file("out/a_example.txt")
    print("Score: ", score(p, s))
