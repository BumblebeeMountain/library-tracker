#!/usr/bin/env python3

import pickle
from main import getOcc

diaLogName = "diaLog.db"
with open (diaLogName, "rb") as f:
    log = pickle.load(f)

start = log.timeToIndex("00:00", 3)
end = log.timeToIndex("00:00", 4)

# occ, time = getOcc()
# print(f"occ: {occ}")
# print(f"time: {time}")

# index = log.timeToIndex(time)
# print(index)

print(log.getLog()[start:end])
