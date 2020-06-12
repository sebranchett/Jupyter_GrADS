#!/usr/bin/env python
# coding: utf-8

# Create plot from grads files

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def grads_plot(metadata, data, zeds, time_step, result_type, altitude_step):
    if zeds != 0:
        altitude_string = " - altitude "+str(metadata["ZDEF"][altitude_step])
        zed_multiplier = zeds
    else:
        altitude_string = ""
        zed_multiplier = 1

    heat = data[result_type][time_step*(zed_multiplier)+altitude_step].reshape(len(metadata["YDEF"]), len(metadata["XDEF"]))
    lenX = len(metadata["XDEF"])
    lenY = len(metadata["YDEF"])

    df = pd.DataFrame(heat, index= metadata["YDEF"], columns=metadata["XDEF"])

    plt.figure(0,(12.,5.))
    heatmap = plt.pcolor(df)
    plt.title(" ".join(metadata[result_type].split())+" - "+metadata["TDEF"][time_step]+altitude_string)
    plt.yticks(np.arange(0, lenY, 5), df.index[0::5])
    plt.xticks(np.arange(0, lenX, 10), df.columns[0::10])
    plt.colorbar(heatmap)

    return(plt)
