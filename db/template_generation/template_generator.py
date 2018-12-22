import argparse
import json
import random
from names import names as names


def producer(fieldtype, fields, name):
    output = {}
    output['date'] = 'DATE'
    output['product_type'] = fieldtype
    output['product_id'] = "ID"
    quantity = []
    for i in range(0, fields):
        random.seed()
        number = int(random.randrange(1, 20))
        quantity.append(number)
    parameters = {}
    counter = 0
    for i in range(0, fields):
        subname = names[counter]
        parameters[subname] = {}
        counter = counter + 1
        for j in range(0, quantity[i]):
            if counter == len(names):
                counter = 0
            parameters[subname][names[counter]] = "VALUE"
            counter = counter + 1
            if counter == len(names):
                counter = 0
    output["parameters"] = parameters
    file = open(name, "w")
    json.dump(output, file, indent=4)
    file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', type=str)
    parser.add_argument('-f', '--fields', type=int)
    parser.add_argument('-n', '--name', type=str)
    args = parser.parse_args()
    producer(args.type, args.fields, args.name)
