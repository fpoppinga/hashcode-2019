import numpy as np


class ProblemFile:
    def __init__(self, path):
        with open(path, "r") as f:
            preamble = f.readline().split()
            [r, c, min_ingredients, max_cells] = map(int, preamble)

            self.rows = r
            self.cols = c
            self.min_ingredients = min_ingredients
            self.max_cells = max_cells

            lines = f.readlines()

            # We define:
            # T <=> 0
            # M <=> 1
            pizza = np.zeros((r, c), dtype=np.uint8)
            for rr, line in enumerate(lines):
                for cc, char in enumerate(line.strip()):
                    pizza[rr, cc] = 0 if char == "T" else 1

            print(pizza)
            self.pizza = pizza


if __name__ == "__main__":
    p = ProblemFile("in/a_example.in")
