#!/usr/bin/env python
# coding: utf-8

# Routines to read Grads control and data files

import numpy as np
from scipy.io import FortranFile


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
            except Exception:
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
                        metadata[key] = np.arange(float(fields[3]),
                                        int(fields[1])*float(fields[4]),
                                        float(fields[4]))
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
                varsKeys.append([key, int(fields[1])])

        else:  # continuation line
            fields = line.split(None)
            levels += list(map(float, fields))
            if len(levels) == nlevels:
                metadata[key] = levels
                continuation = False

    if len(varsKeys) != metadata["VARS"]:
        print("There is a problem with the VARS metadata")
        print("VARS is ", metadata["VARS"], "but found", len(varsKeys),
              "variables")

    return(metadata, varsKeys)


def read_data(metadata, varsKeys, grads_filename):
    data = {}

    f = FortranFile(grads_filename, 'r', '>u4')
    for label, nzed in varsKeys:
        if nzed == 0:
            values = []
            for it in range(len(metadata["TDEF"])):
                values.append(f.read_reals('>f4'))
            data[label] = values
        else:
            values = []
            for it in range(len(metadata["TDEF"])):
                for ized in range(nzed):
                    values.append(f.read_reals('>f4'))
            data[label] = values
    f.close()
    return(data)
