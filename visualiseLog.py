#!/usr/bin/env python3

"""
visualiseLog.py
"""

import numpy as np
import matplotlib.pyplot as plt
from logStore import LogStore
import pickle

def getLog(logName):
    with open (logName, "rb") as f:
        log = pickle.load(f)
        return log

def plotLog(log):
    timeArr = log.getLog()
    res = log.getRes()

    dayIndexes = [log.timeToIndex("00:00", i) for i in range(8)]
    dayLabels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday"]

    plotGraph(timeArr, dayIndexes, dayLabels, grid=True)

def plotDay(log, dayIndex):
    timeArr = log.getLog()
    res = log.getRes()

    dayIndexes = [log.timeToIndex("00:00", i) for i in [dayIndex, dayIndex+1]]
    dayLabels = np.array(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    arrToPlot = timeArr[dayIndexes[0]: dayIndexes[1]]

    xTicks = [i for i in range(0, len(arrToPlot)+1, int(60/log.getRes()*2))]
    xTickLabels = [f"0{c}:00" for c in range(0, 9, 2)] + [f"{c}:00" for c in range(10, 25, 2)]
    xTickLabels[0] = dayLabels[dayIndex]
    xTickLabels[-1] = dayLabels[(dayIndex+1)%8]

    plotGraph(arrToPlot, xTicks, xTickLabels)

def plotGraph(arrToPlot, xTicks=None, xTickLabels=None, xLabel="Time", yLabel="Occupancy", grid=True):
    fig, ax = plt.subplots()
    ax.plot(arrToPlot)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    if xTicks is not None and xTickLabels is not None:
        ax.set_xticks(xTicks)
        ax.set_xticklabels(xTickLabels, rotation=30)

    if grid:
        ax.grid(b=True, which='major', ls='--')

    plt.tight_layout()
    plt.show()


def avgDay(log):
    timeArr = np.array(log.getLog()).reshape((7,-1))
    avg = np.mean(timeArr, axis=0)
    plotGraph(avg, grid=False)

def main():
    diaLogName = "diaLog.db"
    log = getLog(diaLogName)
    plotLog(log)
    # plotDay(log, 4)
    # avgDay(log)

if __name__ == "__main__":
    main()
