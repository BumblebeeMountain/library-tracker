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

    dayIndexes = [log.timeToIndex("00:00", i) for i in range(7)]
    dayLabels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    fig, ax = plt.subplots()
    ax.plot(timeArr)
    plt.xlabel("Time")
    plt.ylabel("Occupancy")

    ax.set_xticks(dayIndexes)
    ax.set_xticklabels(dayLabels, rotation=30)
    plt.tight_layout()
    plt.show()

def plotDay(log, dayIndex):
    timeArr = log.getLog()
    res = log.getRes()

    dayIndexes = [log.timeToIndex("00:00", i) for i in [dayIndex, dayIndex+1]]
    dayLabels = np.array(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    fig, ax = plt.subplots()
    arrToPlot = timeArr[dayIndexes[0]: dayIndexes[1]]
    ax.plot(arrToPlot)
    plt.xlabel("Time")
    plt.ylabel("Occupancy")

    ax.set_xticks([0, len(arrToPlot)])
    ax.set_xticklabels(dayLabels[dayIndex: dayIndex+2], rotation=30)
    plt.tight_layout()
    plt.show()

def main():
    diaLogName = "diaLog.db"
    log = getLog(diaLogName)
    # plotLog(log)
    plotDay(log, 3)

if __name__ == "__main__":
    main()
