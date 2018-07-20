#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_time.py: game time and utility functions""" 

class GTime():
    time_delta = 0
    time = 0

    def set(new_time):
        GTime.time_delta = new_time - GTime.time
        GTime.time = new_time

    def reset():
        GTime.time_delta = 0
        GTime.time = 0


def str_time(time):
    time, ms = time//1000, time%1000
    time, s = time//60, time%60
    h, m = time//60, time%60
    if h:
        return str(h) +":" + str(m).zfill(2)+":"+ str(s).zfill(2)
    else:
        return str(h) +":" + str(m).zfill(2)+":"+ str(s).zfill(2)# str(m).zfill(2) +":"+ str(s).zfill(2) 

def str_idle(time):
    time, ms = time//1000, time%1000
    m, s = time//60, time%60
    if m:
        return str(m).zfill(2) +":"+ str(s).zfill(2)
    else:
        return str(s).zfill(2) +"."+ str(ms//10).zfill(2)
