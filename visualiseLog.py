#!/usr/bin/env python3

"""
visualiseLog.py
"""

import numpy as np
import matplotlib.pyplot as plt
from logStore import LogStore
from datetime import datetime
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

def rotateArr(arr):
    arr.append(arr.pop(0))

def plotDay(log, dayIndex):
    timeArr = log.getLog()
    res = log.getRes()

    dayIndexes = [log.timeToIndex("06:00", i) for i in [dayIndex, dayIndex+1]]

    dayLabels = np.array(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    arrToPlot = timeArr[dayIndexes[0]: dayIndexes[1]]
    if dayIndex+1 > 6:
        arrToPlot = np.append(arrToPlot, timeArr[:log.timeToIndex("06:00", 0)])

    xTicks = [i for i in range(0, len(arrToPlot)+1, int(60/log.getRes()*2))]
    xTickLabels = [f"0{c}:00" for c in range(0, 9, 2)] + [f"{c}:00" for c in range(10, 23, 2)]
    for i in range(3):
        rotateArr(xTickLabels)
    xTickLabels.append("06:00")
    xTickLabels[0] = dayLabels[dayIndex]
    xTickLabels[-1] = dayLabels[(dayIndex+1)%7]

    title = f"Occupancy in Diamond for {dayLabels[dayIndex]}"
    plotGraph(arrToPlot, xTicks, xTickLabels, title)

def plotGraph(arrToPlot, xTicks=None, xTickLabels=None, title=None, xLabel="Time", yLabel="Occupancy", grid=True):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(arrToPlot)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    if xTicks is not None and xTickLabels is not None:
        ax.set_xticks(xTicks)
        ax.set_xticklabels(xTickLabels, rotation=30)

    if grid:
        ax.grid(b=True, which='major', ls='--')

    if title:
        plt.title(title)

    plt.tight_layout()
    plt.show()

def compDay(log):
    index = log.timeToIndex("06:00", 0)
    timeLog = log.getLog()

    timeArr = np.array(timeLog[index:])
    timeArr = np.append(timeArr, timeLog[:index])

    timeArr = timeArr.reshape((7,-1))

    xTicks = [i for i in range(0, timeArr.shape[1]+1, int(60/log.getRes()*2))]
    xTickLabels = [f"0{c}:00" for c in range(0, 9, 2)] + [f"{c}:00" for c in range(10, 24, 2)]
    for i in range(3):
        rotateArr(xTickLabels)
    xTickLabels.append("06:00")

    fig, ax = plt.subplots(figsize=(12,6))
    dayLabels = np.array(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    plt.xlabel("Time")
    plt.ylabel("Occupancy")
    plt.title("Inter-day comparison of occupancy in The Diamond")
    ax.set_xticks(xTicks)
    ax.set_xticklabels(xTickLabels, rotation=30)

    for i, day in enumerate(timeArr):
        ax.plot(day, label=dayLabels[i])
    ax.grid(b=True, which='major', ls='--')
    plt.legend()
    plt.tight_layout()
    plt.show()

def avgDay(log):
    index = log.timeToIndex("06:00", 0)
    timeLog = log.getLog()

    timeArr = np.array(timeLog[index:])
    timeArr = np.append(timeArr, timeLog[:index])

    timeArr = timeArr.reshape((7,-1))

    avg = np.mean(timeArr, axis=0)

    xTicks = [i for i in range(0, len(avg)+1, int(60/log.getRes()*2))]
    xTickLabels = [f"0{c}:00" for c in range(0, 9, 2)] + [f"{c}:00" for c in range(10, 24, 2)]
    for i in range(3):
        rotateArr(xTickLabels)
    xTickLabels.append("06:00")
    plotGraph(avg, xTicks, xTickLabels, yLabel="Average Occupancy", title="Average day")

def main():
    diaLogName = "diaLog.db"
    dayDict = {"mon":0, "tue":1, "wed":2, "thur":3, "fri":4, "sat":5, "sun":6}

    log = getLog(diaLogName)
    # plotLog(log)
    # plotDay(log, int(datetime.today().weekday()))
    avgDay(log)
    compDay(log)


if __name__ == "__main__":
    main()
