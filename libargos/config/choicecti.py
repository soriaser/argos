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

""" Some simple Config Tree Items
"""
import logging, copy

from libargos.config.abstractcti import AbstractCti, AbstractCtiEditor
from libargos.qt import  Qt, QtCore, QtGui, QtSlot
from libargos.utils.misc import NOT_SPECIFIED


logger = logging.getLogger(__name__)

# Use setIndexWidget()?
 


class ChoiceCti(AbstractCti):
    """ Config Tree Item to store a choice between strings.
    """
    def __init__(self, nodeName, data=NOT_SPECIFIED, defaultData=0, editable=False,  
                 configValues=None, displayValues=None):
        """ Constructor.
        
            The data and defaultData are integers that are used to store the currentIndex.
            The displayValues parameter must be a list of strings, which will be displayed in the 
            combo box. The _configValues should be a list of the same size with the _configValues
            that each 'choice' represents, e.g. choice 'dashed' maps to configValue Qt.DashLine.
            If displayValues is None, the configValues are used as displayValues.
                    
            For the (other) parameters see the AbstractCti constructor documentation.
        """
        self.editable = editable
        self._configValues = [] if configValues is None else configValues
        if displayValues is None:
            self._displayValues = copy.copy(self._configValues) 
        else:
            assert not editable, "No separate displayValues may be set if the CTI is editable"
            self._displayValues = displayValues
            
        assert len(self._configValues) == len(self._displayValues),\
            "If set, configValues must have the same length as displayValues."
        
        self._defaultConfigValues = copy.copy(self._configValues)
        
        # Set after self._displayValues are defined. The parent constructor call _enforceDataType
        super(ChoiceCti, self).__init__(nodeName, data=data, defaultData=defaultData)
        
    
    def _enforceDataType(self, data):
        """ Converts to int so that this CTI always stores that type. 
        """
        idx = int(data)
        assert 0 <= idx < len(self._displayValues), \
            "Index should be >= 0 and < {}. Got {}".format(len(self._displayValues), idx)
        return idx

    
    @property
    def configValue(self):
        """ The currently selected configValue
        """
        return self._configValues[self.data]
        
        
    def _dataToString(self, data):
        """ Conversion function used to convert the (default)data to the display value.
        """
        choices = self._displayValues
        return str(choices[data])


    def _nodeGetNonDefaultsDict(self):
        """ Retrieves this nodes` values as a dictionary to be used for persistence.
            Non-recursive auxiliary function for getNonDefaultsDict
        """
        dct = super(ChoiceCti, self)._nodeGetNonDefaultsDict()
        if self._configValues != self._defaultConfigValues:
            dct['choices'] = self._configValues
                        
        return dct
    
    
    def _nodeSetValuesFromDict(self, dct):
        """ Sets values from a dictionary in the current node. 
            Non-recursive auxiliary function for setValuesFromDict
        """
        if 'choices' in dct:
            self._configValues = list(dct['choices'])
            self._displayValues = list(dct['choices'])
        super(ChoiceCti, self)._nodeSetValuesFromDict(dct)
                     
            
    @property
    def debugInfo(self):
        """ Returns the string with debugging information
        """
        return repr(self._displayValues)
    
    
    def createEditor(self, delegate, parent, option):
        """ Creates a ChoiceCtiEditor. 
            For the parameters see the AbstractCti constructor documentation.
        """
        return ChoiceCtiEditor(self, delegate, parent=parent) 
    
    
    def insertValue(self, pos, configValue, displayValue=None):
        """ Will insert the configValue in the configValues and the displayValue in the 
            displayValues list. 
            If displayValue is None, the configValue is set in the displayValues as well
        """
        self._configValues.insert(pos, configValue)
        self._displayValues.insert(pos, displayValue if displayValue is not None else configValue)
    
        
        
        
class ChoiceCtiEditor(AbstractCtiEditor):
    """ A CtiEditor which contains a QCombobox for editing ChoiceCti objects. 
    """
    def __init__(self, cti, delegate, parent=None):
        """ See the AbstractCtiEditor for more info on the parameters 
        """
        super(ChoiceCtiEditor, self).__init__(cti, delegate, parent=parent)
        
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(cti.editable)
        comboBox.addItems(cti._displayValues)
        
        # Store the configValue in the combo box, although it's not currently used.
        for idx, configValue in enumerate(cti._configValues):
            comboBox.setItemData(idx, configValue, role=Qt.UserRole)

        comboBox.activated.connect(self.comboBoxActivated)
        comboBox.model().rowsInserted.connect(self.comboBoxRowsInserted)
        self.comboBox = self.addSubEditor(comboBox, isFocusProxy=True)


    def finalize(self):
        """ Is called when the editor is closed. Disconnect signals.
        """
        self.comboBox.model().rowsInserted.disconnect(self.comboBoxRowsInserted)
        self.comboBox.activated.disconnect(self.comboBoxActivated)
        super(ChoiceCtiEditor, self).finalize()   
        
    
    def setData(self, data):
        """ Provides the main editor widget with a data to manipulate.
        """
        self.comboBox.setCurrentIndex(data)    

        
    def getData(self):
        """ Gets data from the editor widget.
        """
        return self.comboBox.currentIndex()
    
    
    @QtSlot(int)
    def comboBoxActivated(self, index):
        """ Is called when the user chooses an item in the combo box. The item's index is passed. 
            Note that this signal is sent even when the choice is not changed. 
        """
        self.delegate.commitData.emit(self)        
    
        
    @QtSlot(QtCore.QModelIndex, int, int)
    def comboBoxRowsInserted(self, _parent, start, end):
        """ Called when the user has entered a new value in the combobox.
            Puts the combobox values back into the cti.
        """
        assert start == end, "Bug, please report: more than one row inserted"
        configValue = self.comboBox.itemText(start)
        logger.debug("Inserting {!r} at position {} in {}"
                     .format(configValue, start, self.cti.nodePath))
        self.cti.insertValue(start, configValue)
    
    