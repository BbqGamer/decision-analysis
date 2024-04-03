import csv
import sys


def main():
    if len(sys.argv) <= 2:
        print("Supply a data and parameters files")
        exit()

    datafile = sys.argv[1]
    paramsfile = sys.argv[2]

    data = []
    with open(datafile, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data.append(row)

    with open(paramsfile, "r") as f:

        def read_list(f, func=float):
            return list(map(func, f.readline().split(": ")[1].split(",")))

        types = [0 if s == "G" else 1 for s in read_list(f, str)]
        indifferences = read_list(f)
        prefferences = read_list(f)
        vetos = read_list(f)
        weights = read_list(f)
        credibility_threshold = float(f.readline().split(":")[1])
        boundaries = []
        row = f.readline()
        while row:
            boundaries.append(list(map(float, row.split(": ")[1].split(","))))
            row = f.readline()

    print(
        data,
        types,
        indifferences,
        prefferences,
        vetos,
        weights,
        credibility_threshold,
        boundaries,
    )


if __name__ == "__main__":
    main()
