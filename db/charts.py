import argparse
import csv
from process.process import *
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default="output.csv")
    parser.add_argument('--filters', nargs='+',
                        default=["create", "delete",
                                 "update", "f_read", "t_read"])
    parser.add_argument('--split', action='store_true')
    parser.add_argument('--only-general', action='store_true')
    parser.add_argument('--generalise', type=int)
    parser.add_argument('--average', default=0, type=int)
    args = parser.parse_args()
    with open(args.input, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append(row)
    data = sorted(data, key=lambda x: x["start_time"])
    start = data[0]["start_time"]
    for i in data:
        i["time_delta"] = round(float(i["start_time"]) - float(start), 6)
    if not args.average == 0:
        data = average_set(data, args.average)
    if args.generalise:
        data = generalise(data, args.generalise)
    if args.only_general:
        make_all_splited(data)
    else:
        for operation in args.filters:
            make_operation_plot(data, operation=operation, split=args.split)
    # stats
    false_counter = 0
    mean_counter = 0.0
    for entry in data:
        mean_counter = mean_counter + float(entry["o_time"])
        if entry["status"] == "False":
            false_counter = false_counter + 1
    end_time = time.gmtime(float(data[-1]["time_delta"]) +
                           float(data[-1]["o_time"]) +
                           float(data[-1]["r_time"]))
    print("MEAN: {}\nFAILS: {}\nFAIL RATE: {}\
           \nTOTAL OPERATIONS: {}\
           \nTOTAL TIME: {}\n".format(mean_counter / len(data),
                                      false_counter,
                                      false_counter / len(data) * 100,
                                      len(data),
                                      time.strftime("%H:%M:%S",
                                                    end_time)))
    plt.show()
