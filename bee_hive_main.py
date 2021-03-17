# Author: Subaandh

import os
import random
import math
import operator


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


class Result():
    def __init__(self, bee, command, flower_id, pollen_id, count):
        self.bee = bee
        self.command = command
        self.flower_id = flower_id
        self.pollen_id = pollen_id
        self.count = count


class Carry():
    def __init__(self, f_id, p_id, count):
        self.f_id = f_id
        self.p_id = p_id
        self.count = count


def write_output(result):
    output = open("output_" + filename, "w")

    output.write(str(len(result)))
    output.write("\n")

    for i in result:
        cmd = str(i.bee) + " " + str(i.command) + " " + str(i.flower_id) + " " + str(i.pollen_id) + " " + str(i.count)
        output.write(cmd)
        output.writelines("\n")

    output.close()


def gather(flower, pollen, req_dict, bee, result_list, count):
    bee_id = bee.id
    command = 'G'
    flower_index = flower.id
    pollen_index = pollen.pollen_id
    pollen.avail_pollen -= count

    bee.avail_weight -= (pollen.weight * count)
    result_list.append(Result(bee_id, command, flower_index, pollen_index, count))


def feed(hive, flower, pollen, req_dict, bee, result_list, count):
    bee_id = bee.id
    command = 'F'
    hive_index = hive.id
    pollen_index = pollen.pollen_id
    req_dict[pollen.pollen_id] = req_dict.get(pollen.pollen_id) - count

    result_list.append(Result(bee_id, command, hive_index, pollen_index, count))
    bee.avail_weight = bee.max_weight


def new_gather(req_dict, bee, result_list, carry_list):
    for carry in carry_list:
        bee_id = bee.id
        command = 'G'
        flower_index = carry.f_id.id
        pollen_index = carry.p_id.pollen_id
        carry.p_id.avail_pollen -= carry.count
        bee.avail_weight -= (carry.p_id.weight * carry.count)
        bee.i = carry.f_id.i
        bee.j = carry.f_id.j
        result_list.append(Result(bee_id, command, flower_index, pollen_index, carry.count))


def new_feed(hive, req_dict, bee, result_list, carry_list):
    global supplied
    for carry in carry_list:
        bee_id = bee.id
        command = 'F'
        hive_index = hive.id
        pollen_index = carry.p_id.pollen_id

        req_dict[carry.p_id.pollen_id] = req_dict.get(carry.p_id.pollen_id) - carry.count

        supplied += carry.count
        bee.i = hive.i
        bee.j = hive.j
        result_list.append(Result(bee_id, command, hive_index, pollen_index, carry.count))
        bee.avail_weight = bee.max_weight


def find_closest_bee(bees_list, hive):
    max_val = 999999
    best_id = -1

    for x in range(0, len(bees_list)):
        dist = find_distance(hive.i, bees_list[x].i, hive.j, bees_list[x].j)
        dist = math.ceil(dist)

        if dist <= max_val:
            max_val = dist
            best_id = x

    return best_id


def find_unused_bees(bees_list):
    idx = -1
    for bees in range(len(bees_list)):
        if bees_list[bees].flag == 0:
            return bees

    return idx


def find_closest_between(hive, flower, bees_list):
    best_id = -1
    max_val = 0

    for b in range(len(bees_list)):
        h_dist = math.ceil(find_distance(hive.i, bees_list[b].i, hive.j, bees_list[b].j))
        f_dist = math.ceil(find_distance(flower.i, bees_list[b].i, flower.j, bees_list[b].j))
        dist = h_dist + f_dist

        if dist >= max_val:
            max_val = dist
            best_id = b

    return best_id


def find_pollen2(hive, flower_list, bees_list, req_dict, result_list):
    for flower in flower_list:
        carry_list = []
        bee_id = random.randint(0, len(bees_list) - 1)
        bee = bees_list[bee_id]
        wt = bee.avail_weight
        req_copy = req_dict.copy()
        if (all(value <= 0 for value in req_copy.values())):
            break

        if (wt < min_pollen_weight):
            break

        for pollen in flower.pollen:
            avail = pollen.avail_pollen
            if (wt < min_pollen_weight):
                break

            if req_copy.get(pollen.pollen_id) is None:
                continue

            if pollen.pollen_id in req_copy.keys() and req_copy.get(pollen.pollen_id) > 0 and avail > 0:
                if ((wt - pollen.weight) < 0):
                    break

                wt -= pollen.weight
                req_copy[pollen.pollen_id] = req_copy.get(pollen.pollen_id) - 1
                avail -= 1

                if len(carry_list) == 0:
                    val = 1
                    carry_list.append(Carry(flower, pollen, val))
                    continue

                for carry in carry_list:
                    if carry.f_id.id == flower.id and carry.p_id.pollen_id == pollen.pollen_id:
                        carry.count += 1
                        break
                    else:
                        val = 1
                        carry_list.append(Carry(flower, pollen, val))
                        break

        new_gather(req_dict, bee, result_list, carry_list)
        new_feed(hive, req_dict, bee, result_list, carry_list)


def find_pollen(hive, flower_list, bees_list, req_dict, result_list):
    for flower in flower_list:
        carry_list = []
        bee_id = 0

        if len(pollen_weights) < 500:
            bee_id = random.randint(0, len(bees_list) - 1)
        else:
            unused_idx = find_unused_bees(bees_list)
            if unused_idx == -1:
                close_id = find_closest_between(hive, flower, bees_list)
                if close_id != -1:
                    bee_id = close_id
            else:
                bee_id = unused_idx

        bee = bees_list[bee_id]
        bee.flag += 1
        wt = bee.avail_weight
        req_copy = req_dict.copy()

        if all(value == 0 for value in req_copy.values()):
            break

        if wt < min_pollen_weight:
            break

        for pollen in flower.pollen:
            avail = pollen.avail_pollen
            if wt < min_pollen_weight:
                break

            if req_copy.get(pollen.pollen_id) is None:
                continue

            if pollen.pollen_id in req_copy.keys() and req_copy.get(pollen.pollen_id) > 0 and avail > 0:
                if ((wt - pollen.weight) < 0):
                    break

                wt -= pollen.weight
                req_copy[pollen.pollen_id] = req_copy.get(pollen.pollen_id) - 1
                avail -= 1

                if len(carry_list) == 0:
                    val = 1
                    carry_list.append(Carry(flower, pollen, val))
                    continue

                for carry in carry_list:
                    if carry.f_id.id == flower.id and carry.p_id.pollen_id == pollen.pollen_id:
                        carry.count += 1
                        break
                    else:
                        val = 1
                        carry_list.append(Carry(flower, pollen, val))
                        break

        new_gather(req_dict, bee, result_list, carry_list)
        new_feed(hive, req_dict, bee, result_list, carry_list)


def find_distance(x1, x2, y1, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

def calculate(map, hive_list, flower_list, bees_list):
    result_list = []

    for hive in hive_list:
        print("Filling Hive:", hive.id)
        while True:
            req_dict = hive.req_pollen

            # Solution 2
            # find_pollen(hive, flower_list, bees_list, req_dict, result_list)

            # Solution 1
            find_pollen2(hive, flower_list, bees_list, req_dict, result_list)

            if (all(value == 0 for value in req_dict.values())):
                break

    print("All Hives are full writing to output file")
    write_output(result_list)


def main(path):
    global rows, cols, map, bees, time, weight, filename, min_pollen_weight, supplied, pollen_weights
    supplied = 0

    requirement = 0

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
        print("Weights", weights)
        pollen_weights = [int(x.strip()) for x in weights.split(" ")]
        print("Pollen Weights", pollen_weights)
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

    calculate(map, hive_list, flower_list, bees_list)
    # calculate_value(map, hive_list, flower_list, bees_list)
    print("Requirement", requirement)
    print("Supplied", supplied)

if __name__ == "__main__":
    main()
