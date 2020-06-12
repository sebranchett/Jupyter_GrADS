##!/usr/bin/env python
## coding: utf-8
#
## Simple viewer for Grads files
#
## Need to read this very carefully:
## https://ipywidgets.readthedocs.io/en/latest/user_install.html
## nodejs didn't install properly on my Windows 7 machine, so I installed it from internet.
## Now works on Jupyter Notebook, but not on Jupyter Lab.
#
#import ipywidgets as widgets
import numpy as np
#
from scipy.io import FortranFile
#
#import matplotlib.pyplot as plt
#import pandas as pd
#
#
## ### Select the grads control file by clicking on the 'Upload' button
#
## In[2]:
#
#
#uploader = widgets.FileUpload(accept=".ctl", multiple=False)
#display(uploader)
#
#
## In[3]:
#
#
#filename = "atdf101.ctl"
#uploaded_file = uploader.value
#if len(uploaded_file) != 1: print('!!! something unexpected happened', len(uploaded_file))
#for key in uploaded_file:
#    filename = key
#print('selected control file is',filename)
#
#
## In[4]:
#
#
#f = open(filename, "r")
#lines = f.read()
#f.close
#
#lines = lines.replace("\r", "")
#lines = lines.split("\n")
#
#
## ## Extract the metadata
#
## In[5]:
#
def read_metadata(filename):
    f = open(filename, "r")
    lines = f.read()
    f.close
    
    lines = lines.replace("\r", "")
    lines = lines.split("\n")
    metadata = {}
    varsKeys = []
    continuation = False
    for line in lines:
        if not continuation:
            try:
                key, value = line.split(None, 1)
            except:
                key = line
    
            key = key.strip()
            
            if key in ["DSET", "TITLE", "OPTIONS"]:
                metadata[key] = value.strip()
    
            elif key == "UNDEF":
                metadata[key] = float(value)
    
            elif key in ["XDEF", "YDEF", "ZDEF", "TDEF"]:
                fields = line.split(None)
                linlev = fields[2]
                if linlev == "LINEAR":
                    if key != "TDEF":
                        metadata[key] = np.arange(float(fields[3]), int(fields[1])*float(fields[4]), float(fields[4]))
                    else:
                        nfields = int(fields[1])
                        tags = []
                        for i in range(nfields):
                            tag = fields[3]+i*('+'+fields[4])
                            tags.append(tag)
                        metadata[key] = tags
                elif linlev == "LEVELS":
                    levels = list(map(float, fields[3:]))
                    nlevels = int(fields[1])
                    if len(levels) == nlevels:
                        metadata[key] = list(map(float, fields[3:]))
                    else:
                        continuation = True
                else:
                    print("Unknown data grid:", linlev)
    
            elif key == "VARS":
                metadata[key] = int(value)
    
            elif key != "ENDVARS" and key != "":
                fields = line.split(None, 3)
                metadata[key] = fields[3].strip()
                varsKeys.append([key,int(fields[1])])
                    
        else:  # continuation line
            fields = line.split(None)
            levels += list(map(float, fields))
            if len(levels) == nlevels:
                metadata[key] = levels
                continuation = False
    
    if len(varsKeys) != metadata["VARS"]:
        print("There is a problem with the VARS metadata")
        print("VARS is ",metadata["VARS"],"but found",len(varsKeys),"variables")
    
    # print(metadata)
    
    return(metadata, varsKeys)
#
## ## Now find the results file and extract the data
#
## In[6]:
#
#
#grads_filename = filename[:-4]+"_"+metadata["TDEF"][0][-4:]+".grd"
#print(grads_filename)
#
#
## In[7]:
#
def read_data(metadata, varsKeys, grads_filename):
    data = {}
    
    f = FortranFile(grads_filename, 'r', '>u4')
    for label, nzed in varsKeys:
        if nzed == 0:
            values = []
            for it in range(len(metadata["TDEF"])):
                values.append(f.read_reals('>f4'))
            data[label] = values
        elif nzed == len(metadata["ZDEF"]):
            values = []
            for it in range(len(metadata["TDEF"])):
                for ized in range(nzed):
                    values.append(f.read_reals('>f4'))
            data[label] = values
        else:
            print('Unexpected number of altitudes')
    f.close()
    return(data)
#
## ## Plot the data
#
## ### Choose result type and time step
#
## In[9]:
#
#
#date_options = list(zip(metadata["TDEF"], range(0, len(metadata["TDEF"]))))
#
#time_widget = widgets.Dropdown(
#    options=date_options,
#    value=0,
#    description='Date stamp:',
#)
#display(time_widget)
#
#result_options = list(zip([i[0] for i in varsKeys], range(0,len(varsKeys))))
#result_widget = widgets.Dropdown(
#    options=result_options,
#    value=0,
#    description='Result type:',
#)
#display(result_widget)
#
#
## ### Choose altitude
#
## In[10]:
#
#
#time_step = time_widget.value
#
#result_index = result_widget.value
#result_type = varsKeys[result_index][0]
#result_zeds = varsKeys[result_index][1]
#
#if result_zeds != 0:
#    altitudes = len(metadata["ZDEF"])
#    altitude_options = list(zip(metadata["ZDEF"], range(0, len(metadata["ZDEF"]))))
#
#    altitude_widget = widgets.Dropdown(
#        options=altitude_options,
#        value=0,
#        description='Altitude:',
#    )
#    display(altitude_widget)
#print(result_zeds)
#
#
## In[12]:
#
#
#if result_zeds != 0:
#    altitude_step = altitude_widget.value
#    altitude_string = " altitude "+str(metadata["ZDEF"][altitude_step])
#    zed_multiplier = result_zeds
#else:
#    altitude_step = 0
#    altitude_string = ""
#    zed_multiplier = 1
#
#heat = data[result_type][time_step*(zed_multiplier)+altitude_step].reshape(len(metadata["YDEF"]), len(metadata["XDEF"]))
#lenX = len(metadata["XDEF"])
#lenY = len(metadata["YDEF"])
#
#df = pd.DataFrame(heat, index= metadata["YDEF"], columns=metadata["XDEF"])
#
#plt.figure(0,(12.,5.))
#heatmap = plt.pcolor(df)
#plt.title(result_type+" "+metadata["TDEF"][time_step]+altitude_string)
#plt.yticks(np.arange(0, lenY, 5), df.index[0::5])
#plt.xticks(np.arange(0, lenX, 10), df.columns[0::10])
#plt.colorbar(heatmap)
#plt.show()
#
