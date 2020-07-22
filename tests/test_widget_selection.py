# coding: utf-8

# Test widget selection tools

import pytest
import src.widget_selection as ws

def test_results_and_time_widget():
    metadata = { 'TDEF': ['1jan2000', '1jan2000+1mo', '1jan2000+1mo+1mo'],
                 'ZDEF': [925.0, 850.0, 700.0, 500.0, 300.0, 200.0, 90.0, 30.0],
                 'GH':    'geopotential height               [m]',
                 'TEMP':  'abs. temperature               [degK]',
                 'U':     'zonal (u) wind                  [m/s]',
                 'V':     'meridional (v) wind             [m/s]',
                 'Q':     'specific humidity              [g/Kg]',
                 'RH':    'relative humidity                 [%]',
                 'OMEGA': 'pressure vertical velocity     [Pa/s]',
                 'PSI':   'streamfunction           [10^6 m^2/s]',
                 'CHI':   'velocity potential       [10^6 m^2/s]'
               }
    varsKeys = [['GH', 8], ['TEMP', 8], ['U', 8], ['V', 8], ['Q', 8],
                ['RH', 8], ['OMEGA', 8], ['PSI', 8], ['CHI', 8]]
    time_widget, result_widget = ws.result_and_time_options(metadata, varsKeys)
    assert time_widget.options[2][0] == "1jan2000+1mo+1mo"
    assert result_widget.options[6][0][:6] == "OMEGA:"
    assert result_widget.options[6][1] == 6

def test_altitude_options():
    metadata = { 'TDEF': ['1jan2000', '1jan2000+1mo', '1jan2000+1mo+1mo'],
                 'ZDEF': [925.0, 850.0, 700.0, 500.0, 300.0, 200.0, 90.0, 30.0],
                 'GH':    'geopotential height               [m]' }
    altitude_widget = ws.altitude_options(metadata)
    assert altitude_widget.options[3][0] == 500.
    assert altitude_widget.options[7][1] == 7
