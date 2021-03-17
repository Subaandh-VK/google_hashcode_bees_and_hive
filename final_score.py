# Author:Subaandh

import argparse
import os
import math
import bee_hive_main

class Hive():
    def __init__(self, i, j, id, req_pollen, size):
        self.i = i
        self.j = j
        self.id = id
        self.req_pollen = req_pollen  # HashMap {"pollen_id": "required pollens"}
        self.size = size


class Flower():
    def __init__(self, i, j, id, pollen, size):
        self.i = i
        self.j = j
        self.id = id
        self.pollen = pollen
        self.size = size


class Bees():
    def __init__(self, i, j, id, avail_weight, max_weight, flag):
        self.i = i
        self.j = j
        self.id = id
        self.avail_weight = avail_weight
        self.max_weight = max_weight
        self.flag = flag


class Pollen():
    def __init__(self, avail_pollen, pollen_id, weight):
        self.avail_pollen = avail_pollen
        self.pollen_id = pollen_id
        self.weight = weight

class Scorer():
    def __init__(self, bee_id, command, flower_id, pollen_id, count):
        self.bee_id = bee_id
        self.command = command
        self.flower_id = flower_id
        self.pollen_id = pollen_id
        self.count = count

def parse_input(path):
    global info_list, rows, cols, map, bees, time, weight, filename, min_pollen_weight, requirement, pollen_weights
    # Open File
    filename = os.path.basename(os.path.normpath(path))
    print("Filename is: ", filename)
    print("Path is:", path)
    f = open(path)

    line = f.readline()
    rows = int(line.split(" ")[0])
    cols = int(line.split(" ")[1])
    bees = int(line.split(" ")[2])
    time = int(line.split(" ")[3])
    max_weight = int(line.split(" ")[4])

    print(rows, cols, bees, time, max_weight)
    map = [[None for i in range(cols)] for j in range(rows)]
    bees_list = []
    flower_list = []
    hive_list = []
    pollen_weights = []

    # Initialise Painting list object for input size
    # Line 2 store size of the pollen
    # Read pollen weights
    if len(pollen_weights) == 0:
        # Line 3 Weight
        f.readline()
        weights = f.readline()
        # print("Weights", weights)
        pollen_weights = [int(x.strip()) for x in weights.split(" ")]
        # print("Pollen Weights", pollen_weights)
        min_pollen_weight = min(pollen_weights)

    # Read and Fill Flowers data
    if len(flower_list) == 0:
        # Line 4 Number of flowers
        lines = f.readline()
        for index in range(int(lines.strip())):
            indexes = f.readline()
            # Line 5 Flower Indexes
            i = int(indexes.split()[0].strip())
            j = int(indexes.split()[1].strip())

            # Line 6 Available pollen
            pollen_data = f.readline()
            pollen_list = []

            for pollen in range(0, len(pollen_weights)):
                avail_pollen = int(pollen_data.split(" ")[pollen])
                pollen_id = int(pollen)
                weight = int(pollen_weights[pollen])

                pollen_list.append(Pollen(avail_pollen, pollen_id, weight))

            flower_list.append(Flower(i, j, index, pollen_list, len(pollen_list)))
            map[i][j] = Flower(i, j, index, pollen_list, len(pollen_list))

    # Read and Fill hive
    if len(hive_list) == 0:
        # Getting the number of hives
        lines = f.readline()
        # print("hives", lines)
        for index in range(0, int(lines)):
            value = f.readline()
            i = int(value.split()[0].strip())
            j = int(value.split()[1].strip())

            # The Number of pollens required
            count_line = f.readline().strip()
            req_pollen_count = int(count_line)

            req_pollen_type = f.readline()
            req_dict = {}
            size = 0
            for x in range(0, req_pollen_count):
                requirement_list = req_pollen_type.split(" ")
                p_id = int(req_pollen_type.split(" ")[x].strip())
                if (p_id in req_dict.keys()):
                    req_dict[p_id] = req_dict.get(p_id) + 1
                    requirement += 1
                    size += 1
                else:
                    req_dict.update({p_id: 1})
                    requirement += 1
                    size += 1
            hive_list.append(Hive(i, j, index, req_dict, size))
            map[i][j] = hive_list[len(hive_list) - 1]
            # print("Req dict:", req_dict)

        for i in range(bees):
            bees_list.append(Bees(hive_list[0].i, hive_list[0].j, i, max_weight, max_weight, 0))
            map[hive_list[0].i][hive_list[0].i] = Bees(hive_list[0].i, hive_list[0].j, i, max_weight, max_weight, 0)

    return map, hive_list, flower_list, bees_list

def parse_output(path):
    f = open(path)

    cmd_list = []
    line = f.readline()
    size = int(line.strip())

    for line in f.readlines():
        bee = int(line.split(" ")[0])
        cmd = line.split(" ")[1].strip()
        flower = int(line.split(" ")[2])
        pollen = int(line.split(" ")[3])
        count = int(line.split(" ")[4])

        print(bee, cmd , flower, pollen, count)
        cmd_list.append(Scorer(bee, cmd , flower, pollen, count))

    return cmd_list

def find_distance(x1, x2, y1, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

def check_gather(bee_list, flower_list, bee_id, flower_id, pollen_id, count):
    global turn

    b = bee_list[bee_id]
    flower = flower_list[flower_id]
    pollen = flower.pollen[pollen_id]

    pollen.avail_pollen -= count
    if pollen.avail_pollen < 0:
        print("Collecting more pollens than available")
        return None

    b.avail_weight -= (pollen.weight * count)
    if b.avail_weight < 0:
        print("Overload for the bees")
        return None

    if turn > time:
        print("Maximum Time limit exceeded")
        return None

    if (math.floor(find_distance(b.i, flower.i, b.j, flower.j)) == 0):
        turn += 0
    else:
        turn += 1

    b.i = flower.i
    b.j = flower.j

    return True

def check_empty(hive):
    for key, value in hive.req_pollen.items():
        if value != 0:
            return False

    return True

def check_feed(hive_list, bee_list, bee_id, hive_id, pollen_id, count):
    global turn, time, final_score

    b = bee_list[bee_id]
    hive = hive_list[hive_id]


    hive.req_pollen[pollen_id] -= count
    b.avail_weight += pollen_weights[pollen_id] * count
    if hive.req_pollen.get(pollen_id) < 0:
        print("Heavy load for the hive")
        return None

    if math.floor(find_distance(b.i, hive.i, b.j, hive.j)) == 0:
        turn += 0
    else:
        turn += 1

    b.i = hive.i
    b.j = hive.j

    if turn > time:
        print("Maximum Time limit exceeded")
        return None

    # print('After Req', hive.req_pollen)
    if (check_empty(hive)):
        final_score += (((time - turn) / time) * 100)

    return True

def calculate_score(cmd_list, hive_list, flower_list, bee_list):
    print("Calculating Score")
    for cmd in cmd_list:
        bee = cmd.bee_id
        command = cmd.command
        flower_id = cmd.flower_id
        pollen_id = cmd.pollen_id
        count = cmd.count

        # print("Command", command, command == 'G', command == 'F')
        if (command == 'G'):
            ret = check_gather(bee_list, flower_list, bee, flower_id, pollen_id, count)
            if ret is None:
                return ret

        elif (command == 'F'):
            check_feed(hive_list, bee_list, bee, flower_id, pollen_id, count)
            if ret is None:
                return ret

    return True

def main():
    global info_list, rows, cols, map, bees, time, weight, filename, min_pollen_weight
    global requirement
    global final_score, turn
    final_score = 0
    turn = 0

    path_list = ["small_in.txt", "problem1.txt", "problem2.txt", "problem3.txt"]
    out_list = ["output_small_in.txt", "output_problem1.txt", "output_problem2.txt", "output_problem3.txt"]
    requirement = 0

    for path in range(len(path_list)):
        map, hive_list, flower_list, bees_list = parse_input(path_list[path])
        bee_hive_main.main(path_list[path])


        cmd_list = parse_output(out_list[path])
        print(len(cmd_list))
        calculate_score(cmd_list, hive_list, flower_list, bees_list)

    print("**************************** Final Score is:", math.ceil(final_score), "*****************************")

if __name__ == "__main__":
    main()







