import sys

import parser
from classes import Point, BIT2D, Ship


def solution(data: str) -> str:
    ship, hits = parser.parse(data)
    answer = ""
    exclude_sum = 0
    res = [[0 for _ in range(ship.N)] for _ in range(ship.M)]
    for empty in ship.empties:
        ship.update(empty.p1, empty.p2, 1)
        for i in range(ship.N):
            for j in range(ship.M):
                res[j][i] = ship.sum_square(Point(i - 1, j - 1), Point(i, j))

        for i in range(ship.M):
            print(res[i])
        print()
    # for compartment in ship.compartments:
    #     ship.update(compartment.p1, compartment.p2, 2)

    # for hit in hits:
    #     ship.update(hit.p1, hit.p2, hit.damage)
    #     print(ship.sum_square(hit.p1, hit.p2))
        # for empty in ship.empties:
        #     if empty.cross_square(hit.p1, hit.p2):
        #         exclude_sum += ship.sum_square(empty.p1, empty.p2)
        # for i in range(ship.N):
        #     for j in range(ship.M):
        #         res[j][i] = ship.sum_p(Point(i, j))
        # for i in range(5):
        #     print(res[i])
        # print()
        # print(ship.sum_p(Point(ship.N - 1, ship.M - 1)) - exclude_sum)
    # ship = Ship(5, 5, 3, 3, 3, [], [])
    # ship.update(Point(0, 0), Point(3, 3), 1)
    res = [[0 for _ in range(ship.N)] for _ in range(ship.M)]
    # print(ship.sum_square(Point(1, 1), Point(1, 1)))
    # for i in range(ship.N):
    #     for j in range(ship.M):
    #         res[j][i] = ship.sum_square(Point(i - 1, j - 1), Point(i, j))
    #
    # for i in range(5):
    #     print(res[i])
    # for hit in hits:
    #     ship.update(hit.p1, hit.p1, hit.damage)
    #     # print(ship.xy, ship.x, ship.y, ship.i, sep="\n")
    #     tmp = [[0 for _ in range(ship.N + 1)] for _ in range(ship.M + 1)]
    #     for i in range(ship.M + 1):
    #         for j in range(ship.N + 1):
    #             tmp[i][j] = ship.sum_p(Point(j, i))
    #     for i in range(ship.M + 1):
    #         print(tmp[i])
    #     input()
    #     answer += ship.get_message(hit) + "\n"
    return answer


def run():
    input_name, output_name = sys.argv[1], sys.argv[2]
    with open(input_name, "r") as inp:
        with open(output_name, "w") as out:
            data = inp.read()
            result = solution(data)
            out.write(result)


run()
