# -*- coding: utf-8 -*-

# This file is part of Argos.
#
# Argos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Argos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Argos. If not, see <http://www.gnu.org/licenses/>.

""" Healpix plot
"""
from __future__ import division, print_function

import logging

import healpy as hp
import matplotlib
import numpy as np

from argos.inspector.abstract import AbstractInspector, InvalidDataError
from argos.utils.cls import (array_has_real_numbers)

matplotlib.use("QT5Agg")

import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

logger = logging.getLogger(__name__)


class Healpix(AbstractInspector):
    """ Inspector that contains a PyQtGraph Healpix
    """
    def __init__(self, collector, parent=None):
        """ Constructor. See AbstractInspector constructor for parameters.
        """
        super(Healpix, self).__init__(collector, parent=parent)

        # The sliced array is kept in memory. This may be different per inspector, e.g. 3D
        # inspectors may decide that this uses to much memory. The slice is therefor not stored
        # in the collector.
        self.slicedArray = None

        self.fig = plt.figure(0, figsize=(12, 8))
        self.plotWidget = FigureCanvas(self.fig)
        self.contentsLayout.addWidget(self.plotWidget)


    @classmethod
    def axesNames(cls):
        """ The names of the axes that this inspector visualizes.
            See the parent class documentation for a more detailed explanation.
        """
        return tuple(['X'])


    def _hasValidData(self):
        """ Returns True if the inspector has data that can be plotted.
        """
        return self.slicedArray is not None and array_has_real_numbers(self.slicedArray.data)


    def _clearContents(self):
        """ Clears the  the inspector widget when no valid input is available.
        """
        plt.clf()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def _drawContents(self, reason=None, initiator=None):
        """ Draws the plot contents from the sliced array of the collected repo tree item.

            The reason parameter is used to determine if the axes will be reset (the initiator
            parameter is ignored). See AbstractInspector.updateContents for their description.
        """
        self.slicedArray = self.collector.getSlicedArray()

        if not self._hasValidData():
            self._clearContents()
            raise InvalidDataError("No data available or it does not contain real numbers")

        datas = self.slicedArray.data
        if datas.dtype == np.float64:
            datas[np.isnan(datas)] = hp.UNSEEN

        cmap = plt.cm.Spectral_r
        cmap.set_over(cmap(1.0))
        cmap.set_under('white')
        cmap.set_bad('gray')

        plt.clf()

        hp.mollview(map=datas, nest=True, coord=['C', 'G'], cmap=cmap, notext=True, fig=0)
        hp.graticule(verbose=False)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
