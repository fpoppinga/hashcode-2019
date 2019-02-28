from os import walk


class Photo:
    def __init__(self, id, is_vertical, tags):
        self.id = id
        self.is_vertical = is_vertical
        self.tags = tags

    def __str__(self):
        return "id: {}, {}, [{}]".format(self.id, self.is_vertical, self.tags)


class Problem:
    def __init__(self, path):
        self.photos = {}
        with open(path, "r") as f:
            count = int(f.readline())

            id = 0
            while id < count:
                [orientation, tag_count, *tags] = f.readline().split()
                self.photos[id] = Photo(id, orientation == "V", set(tags))
                id += 1


if __name__ == "__main__":
    for (dirpath, _, files) in walk("./in"):
        for file in files:
            p = Problem(dirpath + "/" + file)

            for id, photo in p.photos.items():
                print(photo)