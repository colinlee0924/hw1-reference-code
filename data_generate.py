#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
##------------- [Tool] Data generator -------------
# * Author: CIMLab
# * Date: Sep 30th, 2021
# * Description:
#       This program is a tool to help you guys to
#       generate the data about inter-arrival times &
#       service times. Feel free to modify it as u like.
##-------------------------------------------------
#

import numpy as np
import pandas as pd

df = pd.DataFrame(columns = ['AV', 'PT'])

job_num = 10

for i in range(job_num):
    AV = np.random.exponential(30)
    PT = np.random.exponential(50)
    df.loc[len(df)] = [AV, PT]
    
# plot to check the shape of data
import matplotlib.pyplot as plt
plt.hist(df["AV"])
plt.show()
plt.hist(df["PT"])
plt.show()

#save file
df.loc[len(df)] = [-1, -1]
df.to_excel("data.xlsx")

