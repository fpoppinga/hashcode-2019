import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

score = 0
with open(args.file, "r") as result_file:
    header = result_file.readline()
    for line in result_file:
        x1, y1, x2, y2 = map(int, line.split(" "))
        piece_size = abs(x2 - x1 + 1) * abs(y2 - y1 + 1)
        print("piece from ({},{}) to ({},{}) → {}".format(x1, y1, x2, y2, piece_size))
        score = score + piece_size

print("final score: ", score)
