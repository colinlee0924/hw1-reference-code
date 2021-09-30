#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
##---- [Sample code] Single Queue Single Server ----
# * Author: CIMLab
# * Date: Sep 30th, 2021
# * Description:
#       This program is a reference for you guys
#       to finish your homework 1-b. Feel free to
#       modify it as u like.
##-------------------------------------------------
#

import pandas as pd


STOPT, TNOW, TOA, TOSC, TTLAS, BTime = [0, 0, 0, 0, 0, 0]

BUSY, INX1, INX2, LWL, LWLMAX, ETYPE = [0, 0, 0, 0, 0, 0]

DATA = []

trace_record = pd.DataFrame(columns = ['TOA', 'TOSC', 'TTLAS', 'BTime', 'BUSY', 'LWL', 'LWLMAX', 'ETYPE'])

VeryLarge = float('inf')

def MIN(A, B):
    global ETYPE
    Min_T = A
    ETYPE = 1
    if Min_T > B:
        Min_T = B
        ETYPE = 2
    return Min_T

def sample(code):
    global INX1, INX2
    if code == 1:
        if DATA.loc[INX1, 'AV'] < 0:
            value = VeryLarge
        else:
            value = DATA.loc[INX1, 'AV']
        INX1 += 1
    elif code == 2:
        if DATA.loc[INX2, 'PT'] < 0:
            value = VeryLarge
        else:
            value = DATA.loc[INX2, 'PT']
        INX2 += 1
    return value

def read_file():
    global DATA, STOPT
    print("Discrete Event Simulation Illustration")
    print("Single Queue Single Server Simulation")
    print("======================================")
    
# =============================================================================
#     #key in file name
#     file_name = input("Please Key in File name: ")
#     DATA = pd.read_excel(file_name)
# =============================================================================
    
    DATA = pd.read_excel("data_EXP.xlsx")
    
    STOPT = int(input("Please Key in Ending time: "))
    print("======================================")

def print_trace():
    if ETYPE == 1:
        print("TNOW: {}  SC".format(TNOW))
    elif ETYPE == 2:
        print("TNOW: {}  AV".format(TNOW))
    else:
        print("TNOW: {}".format(TNOW))
    print("TOA TOSC TTLAS BTime BUSY LWL LWLMAX ETYPE")
    print("------------------------------------------")
    print("{}   {}    {}    {}    {}    {}    {}    {}".format(TOA, TOSC, TTLAS, BTime, BUSY, LWL, LWLMAX, ETYPE))
    print("------------------------------------------")
    
    idx = len(trace_record)
    trace_record.loc[idx] = [TOA, TOSC, TTLAS, BTime, BUSY, LWL, LWLMAX, ETYPE]
    
    #tmp = input("")
    

def initial():
    global TNOW, TTLAS, BUSY, BTime, LWL, LWLMAX, INX1, INX2
    #Initial internal systemvariables
    TNOW, TTLAS = (0, 0)
    BUSY, BTime = (0, 0)
    LWL, LWLMAX = (0, 0)
    INX1, INX2 = (0, 0)
    
    global DATA, TOA, TOSC
    #Read input data
    read_file()
    #initialize the first event
    TOA = sample(1)
    TOSC = VeryLarge
    print_trace()

def compute_statistics():
    global BTime, LWLMAX
    BTime = BTime + BUSY * (TNOW - TTLAS)
    if LWL > LWLMAX:
        LWLMAX = LWL

def output():
    compute_statistics()
    print("Max waiting length is: {}".format(LWLMAX))
    print("Facility utilization is: {}".format(BTime/STOPT))

def arrival_event():
    global TOA, BUSY, TOSC, LWL
    TOA = TNOW + sample(1)
    if BUSY == 0:
        BUSY = 1
        TOSC = TNOW + sample(2)
    else:
        LWL = LWL + 1

def end_service_event():
    global TOSC, LWL, BUSY
    TOSC = VeryLarge
    if LWL != 0:
        LWL -= 1
        TOSC = TNOW + sample(2)
    else:
        BUSY = 0

def EVENT(Event_Type):
    if Event_Type == 1:
        end_service_event()
    elif Event_Type == 2:
        arrival_event()
    print_trace()
    
def next_event():
    global TNOW, TTLAS
    initial()
    TNOW = MIN(TOSC, TOA)
    while TNOW < STOPT:
        compute_statistics()
        EVENT(ETYPE)
        TTLAS = TNOW
        TNOW = MIN(TOSC, TOA)
    TNOW = STOPT
    output()

next_event()

#save trace
#trace_record.to_excel("trace.xlsx")