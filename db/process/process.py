import matplotlib.pyplot as plt
from math import floor


def make_operation_plot(dataset, operation=None, split=False):
    if operation is None:
        plt.figure("All operations")
        if split is False:
            plt.plot([i["time_delta"] for i in dataset],
                     [round(float(i["o_time"]), 5) for i in dataset])
            plt.draw()
        else:
            threads = {}
            for i in dataset:
                if i["thread"] in threads.keys():
                    threads[i["thread"]].append(i)
                else:
                    threads[i["thread"]] = []
                    threads[i["thread"]].append(i)
            for thread in threads.keys():
                plt.plot([i["time_delta"] for i in threads[thread]],
                         [round(float(i["o_time"]), 5)
                          for i in threads[thread]],
                         label=thread)
                plt.draw()
                plt.tight_layout()
                plt.legend(bbox_to_anchor=(1, 1))
    else:
        plt.figure("Only {}".format(operation))
        if split is False:
            plt.plot([i["time_delta"] for i in dataset
                      if operation in i["operation"]],
                     [round(float(i["o_time"]), 5) for i in dataset
                      if operation in i["operation"]])
            plt.draw()
        else:
            threads = {}
            for i in dataset:
                if i["operation"] == operation:
                    if i["thread"] in threads.keys():
                        threads[i["thread"]].append(i)
                    else:
                        threads[i["thread"]] = []
                        threads[i["thread"]].append(i)
            for thread in threads.keys():
                plt.plot([i["time_delta"] for i in threads[thread]],
                         [round(float(i["o_time"]), 5)
                          for i in threads[thread]],
                         label=thread)
                plt.draw()
                plt.tight_layout()
                plt.legend(bbox_to_anchor=(1, 1))


def make_all_splited(dataset):
    operations = {}
    for op in dataset:
        if op["operation"] in operations.keys():
            operations[op["operation"]].append(op)
        else:
            operations[op["operation"]] = []
            operations[op["operation"]].append(op)
    for op in operations.keys():
        plt.plot([i["time_delta"] for i in operations[op]],
                 [round(float(i["o_time"]), 5)
                  for i in operations[op]],
                 label=op)
        plt.draw()
        plt.tight_layout()
        plt.legend(bbox_to_anchor=(1, 1))


def average_set(dataset, window):
    start = floor(window / 2)
    stop = len(dataset) - floor(window / 2)
    new_set = []
    for i in range(start, stop):
        tmp = 0.0
        for j in range(i - start, i + start):
            tmp = tmp + float(dataset[j]["o_time"])
        tmp = tmp / window
        entry = dataset[i]
        entry["o_time"] = tmp
        new_set.append(entry)
    return new_set


def generalise(dataset, window):
    new_set = []
    start = floor(window / 2)
    stop = len(dataset) - floor(window / 2)
    tmp = 0.0
    for i in range(start, stop):
        for j in range(i - start, i + start):
            tmp = tmp + float(dataset[j]["o_time"])
        tmp = tmp / window
        entry = dataset[i]
        entry["o_time"] = tmp
        new_set.append(entry)
        i = i + start
    return new_set
