from comp.input import Photo


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
                    photo1 = Photo(int(splitted[0], True, []))
                    photo2 = Photo(int(splitted[1], True, []))
                    slides.append(photo1, photo2)
                elif len(splitted) == 1:
                    slides.append(Slide(Photo(int(splitted[0]), False, [])))
        return Solution(slides)


class Slide:
    def __init__(self, photo1: Photo, photo2=None):
        self.photo1 = photo1
        self.photo2 = photo2

    def __str__(self):
        if self.photo2:
            return "{} {}".format(self.photo1.id, self.photo2.id)
        else:
            return "{}".format(self.photo1.id)


if __name__ == "__main__":
    Solution.from_file("out/a_example.txt").to_file("out/a_example.out.txt")
