#!/usr/bin/env python3

"""
main.py

Program to track the occupancy in the library at various times and see if
busier than usual or not.
"""

from bs4 import BeautifulSoup as bs
from bs4 import Comment
import numpy as np
import requests
import sys
import pickle

from logStore import LogStore

def getOcc(loc="dmd"):
    """
    get the occupancy and the time of update
    params:
        loc - str - either dmd (diamond) or ic (information commons)
    returns:
        occupancy, time of update
    """
    page = requests.get(f"https://lib-wordpress.sheffield.ac.uk/occupancy/{loc}.htm?style=infoscreen")
    if page.ok:
        soup = bs(page.text, 'html.parser')
        vals = soup.findAll(class_="SENTRY_occupancy")
        if len(vals) > 0:
            comment = soup.findAll(text=lambda text:isinstance(text, Comment))
            occ = int(vals[0].text)
            time = comment[0][-7:-2]

            return occ, time
    raise Exception(f"Error fetching page: {page}")

if __name__ == "__main__":
    diaLogName = "diaLog.db"
    try:
        with open(diaLogName, "rb") as f:
            log = pickle.load(f)
    except Exception as e:
        print(e)
        log = LogStore(diaLogName, 10, 0.1)
        print("no log, so creating new log")

    try:
        occ, time = getOcc("dmd")
    except:
        print("ERROR: cannot get occupancy")
        sys.exit(1)

    log.addToLog(time, occ)
    log.save()
