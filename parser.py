from typing import Tuple

from classes import *


def parse(data: str) -> Tuple[Ship, List[Hit]]:
    data = data.splitlines()
    N, M, E, R = map(int, data[0].split())
    H, L, C = map(int, data[1].split())
    empties = []
    for i in range(2, 2 + E):
        x0, y0, x1, y1 = map(int, data[i].split())
        empties.append(Rectangle(Point(x0, y0), Point(x1 - 1, y1 - 1)))
    compartments = []
    for i in range(2 + E, 2 + E + R):
        line = data[i].split()
        name = line[0]
        x0, y0, x1, y1, damage_limit = int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5])
        compartments.append(Compartment(name, Point(x0, y0), Point(x1 - 1, y1 - 1), damage_limit))
    K = int(data[2 + E + R])
    hits = []
    for i in range(2 + E + R + 1, 2 + E + R + 1 + K):
        x0, y0, x1, y1, damage = map(int, data[i].split())
        hits.append(Hit(Point(x0, y0), Point(x1, y1), damage))
    return Ship(N, M, H, L, C, empties, compartments), hits
