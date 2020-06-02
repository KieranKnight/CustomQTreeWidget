#!/bin/env python
 
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 KieranKnight

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

------------------------------------------------------------------------------
Creating a CustomTreeWidget UI.

Description:
This module is an example of how to create a custom tree widget
using PySide2.

The module provides an example dictionary that you may see
in a professional environment. Typically, this data would be
stored within a class object but the data has been laid out so
it is easier to follow along.

To create your own "data" dictionary you will need another method or class
that performs tasks and returns a dictionary. Doing this may require slight
adjustments to the rest of the code.

The data explained:
The idea behind the data is that you've had a method that queries a file directory.
This then returns a dictionary with the following format:
    The first key : The folder that has been queried
        The value: A nested list in case multiple files are found.
            Files dict: Each file contains a dictionary of information.

"""

import sys
from PySide2 import QtWidgets, QtCore, QtGui
 

# EXAMPLE DICTIONARY DATA
_data ={
    '/folderOne': [
        [{'Sequence': 'zzz999', 'Shot': 'zzz_1234', 'Version': '01', 'Location': '/file/path'}]
    ],
    '/folderTwo': [
        [{'Sequence': 'zzz999', 'Shot': 'zzz999_000', 'Version': '01', 'Location': '/file/path'}], 
        [{'Sequence': 'zzz999', 'Shot': 'zzz999_000', 'Version': '02', 'Location': '/file/path'}]
    ],
    '/folderThree': [
        [{'Sequence': 'abc111', 'Shot': 'abc111_5678', 'Version': '01', 'Location': '/file/path'}], 
        [{'Sequence': 'abc111', 'Shot': 'abc111_5678', 'Version': '02', 'Location': '/file/path'}],
        [{'Sequence': 'abc111', 'Shot': 'abc111_5678', 'Version': '03', 'Location': '/file/path'}],
        [{'Sequence': 'abc111', 'Shot': 'abc111_5678', 'Version': '05', 'Location': '/file/path'}]
    ]
}


class UI(QtWidgets.QMainWindow):
    _OBJ_NAME = 'CustomTreeWidget'
    def __init__(self, parent=None):
        super(UI, self).__init__(parent=parent)
        # setting up the UI 
        self.setWindowTitle(self._OBJ_NAME)
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        # Creating the tree widget
        self.treeWidget = CustomTreeWidget(_data, parent=self.centralwidget)
        self.setCentralWidget(self.centralwidget)

        # Creating an example button to show how the data can be used.
        self._show_data_useage_btn = QtWidgets.QPushButton()
        self._show_data_useage_btn.setText('Select a row and see the printed data!')
        self._show_data_useage_btn.clicked.connect(self.show_data_useage)

        # adding the widgets to the layout
        self.verticalLayout.addWidget(self.treeWidget)
        self.verticalLayout.addWidget(self._show_data_useage_btn)

    def show_data_useage(self):
        """
        Example button connection to show the data from a selected item
        """
        _selected_items = self.treeWidget.selectedItems()
        if not _selected_items:
            print('Please select a row')
            return
        for selected in _selected_items:
            print('>> Sequence: {}'.format(selected.sequence.text()))
            print('>> Shot: {}'.format(selected.shot.text()))
            print('>> Version: {}'.format(selected.version.text()))
            print('>> Location: {}'.format(selected.location.text()))


class CustomTreeWidget(QtWidgets.QTreeWidget):
    """
    Creating the TreeWidget Object that will be used
    to hold the custom TreeWidgetItems.

    Arguments:
        QtWidgets {QTreeWidget} -- Inheriting the base QTreeWidget

    Returns:
        CustomTreeWidget -- Object linking to the widget and items created.
    """
    _HEADERS = ['Sequence', 'Shot', 'Version', 'Location']
    def __init__(self, data, parent=None):
        """
        Sorting through the data within the initial method
        as we want this to run as soon as the class is instantiated.

        Arguments:
            data {[type]} -- The dictionary data of what the items will created from.

        Keyword Arguments:
            parent {QMainWindow} -- The main application window to attach to(default: {None})
        """
        super(CustomTreeWidget, self).__init__(parent)
        
        self._data = data
        self.setColumnCount(len(self.headers))
        self.setHeaderLabels(self.headers)
        
        # Looping through the data items
        for key, value in self.data.items():
            _header = self  # setting a default header item
            # reversing the nested list to get the newest version of
            # the data that we are trying to show.
            for val in reversed(value):
                _item = CustomTreeItem(val[0], self, _header)
                # if the _item is an instance of the CustomTreeWidget
                # we now need to change the _header variable to the
                # newly created widget, so this will now be the parent
                # for the rest of the versions added.
                if isinstance(_header, CustomTreeWidget):
                    _header = _item                              
                
        ## Set Columns Width to match content:
        [self.resizeColumnToContents(50) for column in range(self.columnCount())]
            
    @property
    def headers(self):
        return self._HEADERS

    @property
    def data(self):
        return self._data
 

class CustomTreeItem( QtWidgets.QTreeWidgetItem ):
    """
    Overriding the QTreeWidgetItem to work with widgets.

    Arguments:
        QtWidgets {QTreeWidgetItem} -- Inheriting the base QTreeWidgetItem
    """
    def __init__( self, name, top_item, parent=None):
        """
        Buidling the widgets directly within the __init__ method
        so everytime the class is instantiated, the widgets will be built.

        Arguments:
            name {dict} -- A Dictionary containing all the needed file information.
            top_item {QMainWindow} -- The main application window.

        Keyword Arguments:
            parent {QMainWindow | CustomTreeWidget} -- The main parernt object.(default: {None})

        NOTE:
            A property has been added for each widget created.
            This means that when querying the selected row.
            Please see the method; show_data_useage_btn()
        """
        super( CustomTreeItem, self).__init__(parent)

        ## Column 0 - Sequence:
        self._sequence_widget = QtWidgets.QLabel()
        self._sequence_widget.setText(name['Sequence'])
        top_item.setItemWidget(self, 0, self._sequence_widget)
 
        ## Column 1 - Shot:
        self._shot_widget = QtWidgets.QLabel()
        self._shot_widget.setText(name['Shot'])
        top_item.setItemWidget( self, 1, self._shot_widget )
 
        ## Column 2 - Version:
        self._version_widget = QtWidgets.QLabel()
        self._version_widget.setText(name['Version'])
        top_item.setItemWidget( self, 2, self._version_widget )

        ## Column 3 - Location
        self._location_widget = QtWidgets.QLabel()
        self._location_widget.setText(name['Location'])
        top_item.setItemWidget( self, 3, self._location_widget )

    @property
    def sequence(self):
        return self._sequence_widget

    @property
    def shot(self):
        return self._shot_widget
    
    @property
    def version(self):
        return self._version_widget

    @property
    def location(self):
        return self._location_widget


def openUI():
    """
    Opening the UI and resizing the window
    """
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    ui.resize(500, 200)
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    openUI()