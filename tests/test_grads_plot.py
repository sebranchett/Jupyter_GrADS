# coding: utf-8

# Test plotting GrADS files

import pytest
from os import path
import src.read_grads as rg
import src.grads_plot as gp
from unittest.mock import patch
import matplotlib.pyplot as plt

@patch("src.grads_plot.plt.show")
def test_grads_plot(mock_show):
    filename = path.join(path.dirname(__file__), "test_graph.ctl")
    metadata, varsKeys = rg.read_metadata(filename)
    filename = path.join(path.dirname(__file__), "test_graph.grd")
    data = rg.read_data(metadata, varsKeys, filename)
    time_step = 0
    result_index = 0
    result_type = varsKeys[result_index][0]
    result_zeds = varsKeys[result_index][1]
    altitude_step = 0
    assert gp.grads_plot(metadata, data, result_zeds, time_step, result_type, altitude_step) == None
