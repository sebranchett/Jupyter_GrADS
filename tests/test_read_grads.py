# coding: utf-8

# Test reading Grads control and data files

import pytest
from os import path
from read_grads import read_metadata, read_data

def test_read_metadata():
    filename = path.join(path.dirname(__file__), "test_file.ctl")
    metadata, varsKeys = read_metadata(filename)
    assert len(metadata) == 50
    assert len(varsKeys) == 41
    assert metadata["TDEF"][2] == "1jan2000+1mo+1mo"
    assert varsKeys[6][0] == "OMEGA"
    assert varsKeys[4][1] == 8