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
                    slides.append(Slide(int(splitted[0]), int(splitted[1])))
                elif len(splitted) == 1:
                    slides.append(Slide(int(splitted[0])))
        return Solution(slides)


class Slide:
    def __init__(self, id1, id2=None):
        self.id1 = id1
        self.id2 = id2

    def __str__(self):
        if self.id2:
            return "{} {}".format(self.id1, self.id2)
        else:
            return "{}".format(self.id1)


if __name__ == "__main__":
    Solution.from_file("out/a_example.txt").to_file("out/a_example.out.txt")
