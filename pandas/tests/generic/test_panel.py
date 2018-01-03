# -*- coding: utf-8 -*-
# pylint: disable-msg=E1101,W0612

from warnings import catch_warnings

from pandas import Panel
from pandas.util.testing import (assert_panel_equal,
                                 assert_almost_equal)

import pandas.util.testing as tm
import pandas.util._test_decorators as td
from .test_generic import Generic


class TestPanel(Generic):
    _typ = Panel
    _comparator = lambda self, x, y: assert_panel_equal(x, y, by_blocks=True)

    @td.skip_if_no('xarray', min_version='0.7.0')
    def test_to_xarray(self):
        from xarray import DataArray

        with catch_warnings(record=True):
            p = tm.makePanel()

            result = p.to_xarray()
            assert isinstance(result, DataArray)
            assert len(result.coords) == 3
            assert_almost_equal(list(result.coords.keys()),
                                ['items', 'major_axis', 'minor_axis'])
            assert len(result.dims) == 3

            # idempotency
            assert_panel_equal(result.to_pandas(), p)
