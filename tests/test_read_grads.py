# coding: utf-8

# Test reading Grads control and data files

import pytest
from os import path
import src.read_grads as rg

def test_read_metadata():
    filename = path.join(path.dirname(__file__), "meta_test_file.ctl")
    metadata, varsKeys = rg.read_metadata(filename)
    assert len(metadata) == 50
    assert len(varsKeys) == 41
    assert metadata["TDEF"][2] == "1jan2000+1mo+1mo"
    assert varsKeys[6][0] == "OMEGA"
    assert varsKeys[4][1] == 8

def test_read_data():
    metadata = { 'TDEF': [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ] }
    varsKeys = [['SKT', 1]]
    filename = path.join(path.dirname(__file__), "data_test_file.grd")
    data = rg.read_data(metadata, varsKeys, filename)
    assert len(data) == 1
    assert len(data['SKT']) == 12
    assert data['SKT'][1][-1] < 233.
    assert data['SKT'][1][-1] > 232.
