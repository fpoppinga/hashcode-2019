from comp.input import Problem, Photo
from comp.out import Solution, Slide, zipdir
from comp.score import score_of_interest, score
import sqlite3

db = sqlite3.connect(':memory:')

def init():
    db.execute("create table tags(photo_id, tag)")
    db.execute("create table photo(id number(19), vert boolean)")


def delete_photos(photos):
    db.execute("delete from photo where id in ('{}')".format("', '".format([p.id for p in photos])))
    db.execute("delete from tags where photo_id in ('{}')".format("', '".format([p.id for p in photos])))

def clear():
    db.execute("drop table photo")
    db.execute("drop table tags")
    init()

def get_photos_by_tag(p: Problem, tags, negatives=[], vertical=None, excludes = []):
    stmt1 = "select photo_id from tags where tag in ('{}')".format("', '".join(tags))
    stmt = "select id from photo where id in ({})".format(stmt1)
    if len(excludes) > 0:
        stmt += " and id not in ('{}')".format("', '".join(map(str,excludes)))
    if len(negatives) > 0:
        stmt2 = "select photo_id from tags where tag in ('{}')".format("', '".join(negatives))
        stmt += " and id not in ({})".format(stmt2)
    if vertical is not None:
        stmt += " and vert = {}".format(int(vertical))

    for fetch in db.execute(stmt):
        id = fetch[0]
        yield p.photos[id]


def index(p: Problem) -> Solution:
    for id, photo in p.photos.items():
        db.execute("insert into photo(id, vert) values (?,?)", [id, photo.is_vertical])
        db.executemany("insert into tags(photo_id, tag) values (?,?)", [(id, tag) for tag in photo.tags])

    slides = []
    used = set()
    for id, photo in p.photos.items():
        print(id)
        slide = None
        if photo.is_vertical:
            for other in get_photos_by_tag(p, photo.tags, vertical=True, excludes=used.union([photo.id])):
                if other.id in used:
                    continue
                used.add(other.id)
                slide = Slide(photo, other)
                break
        else:
            slide = Slide(photo)
        if slide is None:
            continue
        used.add(photo.id)
        slides.append(slide)

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
    init()
    for file in ["a_example.txt", "b_lovely_landscapes.txt", "c_memorable_moments.txt", "d_pet_pictures.txt",
                 "e_shiny_selfies.txt"]:
        p = Problem("in/{}".format(file))
        s = index(p)
        print("{} → {}".format(file, score(p, s)))
        s.to_file("out/{}".format(file))
        clear()
    zipdir(".", "../code.zip")
