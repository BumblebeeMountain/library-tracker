#!/usr/bin/env python3

"""
logStore.py

Used to store the average estimate of the logs
"""

import numpy as np
import pickle
from datetime import datetime

class LogStore():
    def __init__(self, logName, resolution, lr, defaultVal=600):
        self.__logName = logName
        self.__resolution = resolution # i.e. 10 for every 10 mins
        self.__defaultVal = defaultVal
        self.__lr = lr
        self.__n = int((7 * 24 * 60) / self.__resolution)
        self.__log = np.zeros(self.__n) + self.__defaultVal

    def timeToIndex(self, time, dayIndex=None):
        """
        time: str - XX:YY
        """

        time = time.split(":")
        hr = int(time[0])
        minute = int(time[1])

        if dayIndex is None:
            dayIndex = int(datetime.today().weekday() * 24 * 60)
        else:
            dayIndex *= 24 * 60

        dayIndex = int(dayIndex / self.__resolution)
        hrIndex = int(hr * 60 / self.__resolution)
        minIndex = int(minute / self.__resolution)

        return dayIndex + hrIndex + minIndex

    def addToLog(self, time, occ):
        print(time)
        index = self.timeToIndex(time)
        dQ = self.__lr * (occ - self.__log[index])
        self.__log[index] += dQ

    def getLog(self):
        return self.__log.copy()

    def getN(self):
        return self.__n

    def getRes(self):
        return self.__resolution

    def save(self):
        with open(self.__logName, "wb") as f:
            pickle.dump(self, f)

