#!/usr/bin/env python3
import argparse
import csv

import matplotlib.pyplot as plt


class Plotter:
    def plot(self, x, y, label):
        """Create a 2D Plot of x and y"""
        pass


class PyPlotPlotter:
    def plot(self, x, y, label):
        plt.plot(x, y, label=label)
        plt.legend()
        plt.show()


def plot_file(file, column, plotter):
    y = []

    r = csv.reader(file, delimiter=',')
    header = next(r, None)
    for row in r:
        y.append(float(row[column]))

    x = range(1, len(y) + 1)
    plotter.plot(x, y, header[column])


def run(args):
    with open(args.file, "r") as csvfile:
        plot_file(csvfile, int(args.column), PyPlotPlotter())


if __name__ == "__main__":
    desc = "Plots a column of a csv file."
    parser = argparse.ArgumentParser(
        description=desc)
    parser.add_argument(
        "--column",
        required=True,
        help="The 0 based index specifying the column to plot")
    parser.add_argument('--file', required=True, type=str,
                        help='The file to calculate complexity on')

    args = parser.parse_args()
    run(args)
