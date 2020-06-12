#!/usr/bin/env python
# coding: utf-8

# Widget selection for Grads files

import ipywidgets as widgets

def result_and_time_options(metadata, varsKeys):

    date_options = list(zip(metadata["TDEF"], range(0, len(metadata["TDEF"]))))
    
    time_widget = widgets.Dropdown(
        options=date_options,
        value=0,
        description='Date stamp:',
    )
    
    labels = [row[0]+":  "+" ".join(metadata[row[0]].split())
              for row in varsKeys]
    result_options = list(zip(labels, range(0,len(varsKeys))))
    result_widget = widgets.Dropdown(
        options=result_options,
        value=0,
        description='Result type:',
    )

    return(time_widget, result_widget)


def altitude_options(metadata):
    altitudes = len(metadata["ZDEF"])
    z_options = list(zip(metadata["ZDEF"], range(0, len(metadata["ZDEF"]))))

    altitude_widget = widgets.Dropdown(
        options=z_options,
        value=0,
        description='Altitude:',
    )

    return(altitude_widget)
