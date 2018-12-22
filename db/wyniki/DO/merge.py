import argparse
import csv
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-f', nargs='+')
parser.add_argument('-o')
args = parser.parse_args()
output = {}
for file in args.f:
    with open(file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if int(row['timestamp']) in output.keys():
                output[int(row['timestamp'])] += int(row['served'])
            else:
                output[int(row['timestamp'])] = int(row['served'])
lel = sorted(output.keys())
print(lel)
lel2 = []
for i in lel:
	lel2.append(output[i])

print(output)

with open(args.o, 'w') as outf:
    writer = csv.DictWriter(outf, fieldnames=["timestamp", "served"])
    writer.writeheader()
    for k in output.keys():
        writer.writerow({"timestamp": k, "served": output[k]})
plt.figure("Served")
plt.plot(lel, lel2)
plt.show()
