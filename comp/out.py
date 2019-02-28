from comp.input import Photo
import zipfile
import os


def zipdir(path, ziph):
    # ziph is zipfile handle
    zipf = zipfile.ZipFile(ziph, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                zipf.write(os.path.join(root, file))


class Solution:
    def __init__(self, slides):
        self.slides = slides

    def to_file(self, path):
        with open(path, "w") as result_file:
            result_file.write("{}\n".format(len(self.slides)))
            for slide in self.slides:
                result_file.writelines("{}\n".format(slide))

    @staticmethod
    def from_file(path):
        slides = []
        with open(path, "r") as result_file:
            slide_count = int(result_file.readline())
            row_num = 0
            for line in result_file:
                row_num = row_num + 1
                if row_num > slide_count:
                    raise Exception("More piece-lines than defined in header: (>={})!".format(row_num))

                splitted = line.split(" ")
                if len(splitted) > 2:
                    raise Exception("More than two pieces in line {}: {}".format(row_num, line))
                elif len(splitted) == 2:
                    photo1 = Photo(int(splitted[0]), True, [])
                    photo2 = Photo(int(splitted[1]), True, [])
                    slides.append(Slide(photo1, photo2))
                elif len(splitted) == 1:
                    slides.append(Slide(Photo(int(splitted[0]), False, [])))
        return Solution(slides)


class Slide:
    def __init__(self, photo1: Photo, photo2=None):
        if photo1.is_vertical:
            if photo2 == None:
                raise Exception("Cannot create slide with single vertical photo: {}".format(photo1))
            elif not photo2.is_vertical:
                raise Exception("Tried to use a vertical photo with a horizontal one: ({},{})".format(photo1, photo2))
        else:
            if photo2 != None:
                raise Exception("Cannot use a horizontal photo in a pair: ({},{})".format(photo1, photo2))

        self.photo1 = photo1
        self.photo2 = photo2

    def __str__(self):
        if self.photo2:
            return "{} {}".format(self.photo1.id, self.photo2.id)
        else:
            return "{}".format(self.photo1.id)


if __name__ == "__main__":
    Solution.from_file("out/a_example.txt").to_file("out/a_example.out.txt")
