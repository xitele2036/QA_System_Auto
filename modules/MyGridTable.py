
import  wx
import  wx.grid as gridlib
from memory_profiler import profile

#---------------------------------------------------------------------------

class CustomDataTable(gridlib.GridTableBase):
    def __init__(self, log, data, rowLabels=None, colLabels=None, dataTypes=None):
        gridlib.GridTableBase.__init__(self)
        self.log = log

        self.data = data
        self.rowLabels = rowLabels
        self.colLabels = colLabels
        self.dataTypes = dataTypes
        '''
        self.colLabels = ['Module', 'SubModule', 'CaseID', 'Name', 'Func',
                          'argc', 'arg1', 'arg2', 'arg3', 'arg4', 'Avail', 'Result', 'Comment']

        self.dataTypes = [gridlib.GRID_VALUE_STRING, 
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_BOOL,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          ]

        self.data = [
            ['', '', '', '', '', '', '', '', '', '', '', '', '']          

            ]
        '''

    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface

    def GetNumberRows(self):
        if self.data is None:
            return 0
        return len(self.data) # + 1

    def GetNumberCols(self):
        if self.colLabels is None or len(self.colLabels) == 0:
            return 0
        return len(self.colLabels)

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    # Get/Set values in the table.  The Python version of these
    # methods can handle any data-type, (as long as the Editor and
    # Renderer understands the type too,) not just strings as in the
    # C++ version.
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)

                # tell the grid we've added a row
                msg = gridlib.GridTableMessage(self,            # The table
                        gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                        1                                       # how many
                        )

                self.GetView().ProcessTableMessage(msg)
        innerSetValue(row, col, value) 

    def SetRowValue(self, row, value):
        def innerSetRowValue(row, value):
            try:
                lackcol = self.GetNumberCols() - len(value)
                if lackcol > 0:
                    for i in range(lackcol):
                        value.append('')                    
                self.data[row] = value                
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetRowValue(row, value)

                # tell the grid we've added a row
                msg = gridlib.GridTableMessage(self,            # The table
                        gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                        1                                       # how many
                        )
                self.GetView().ProcessTableMessage(msg)
        innerSetRowValue(row, value)
    
    def GetRowValue(self, row):
        try:
            return self.data[row]
        except IndexError:
            return ''
        
        #GRIDTABLE_REQUEST_VIEW_SEND_VALUES = _grid.GRIDTABLE_REQUEST_VIEW_SEND_VALUES
    #--------------------------------------------------
    # Some optional methods

    # Called when the grid needs to display labels
    def GetColLabelValue(self, col):
        return self.colLabels[col]
    
    # Called when the grid needs to display labels
    def GetRowLabelValue(self, row):
        if self.rowLabels is None:
            return str(row+1)
        try:
            return self.rowLabels[row]
        except IndexError:
            return ''

    # Called to determine the kind of editor/renderer to use by
    # default, doesn't necessarily have to be the same type used
    # natively by the editor/renderer if they know how to convert.
    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    # Called to determine how the data can be fetched and stored by the
    # editor and renderer.  This allows you to enforce some type-safety
    # in the grid.
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)

    #----------------------------------------------------------------------
    def InsertRows(self,pos=0,numRows=1):
        """"""
        for num in range(0,numRows):
            self.data.insert(pos,[''] * self.GetNumberCols())

        gridView = self.GetView()
        gridView.BeginBatch()
        insertMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED,pos,numRows)
        gridView.ProcessTableMessage(insertMsg)
        gridView.EndBatch()
        getValueMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        gridView.ProcessTableMessage(getValueMsg)                
               
        return True
   
    def AppendRows(self,numRows=1):
        """"""
        for num in range(0,numRows):
            self.data.append([''] * self.GetNumberCols())         
            
        gridView = self.GetView()
        gridView.BeginBatch()
        appendMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,numRows)
        gridView.ProcessTableMessage(appendMsg)
        gridView.EndBatch()
        getValueMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        gridView.ProcessTableMessage(getValueMsg)
        
        return True
    
    def DeleteRows(self,pos=0,numRows=1):
        if self.data is None or len(self.data) == 0:
            return False

        for rowNum in range(0,numRows):
            del self.data[pos:pos+numRows]
        
        gridView = self.GetView()
        gridView.BeginBatch()
        deleteMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,pos,numRows)
        gridView.ProcessTableMessage(deleteMsg)
        gridView.EndBatch()
        getValueMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        gridView.ProcessTableMessage(getValueMsg)
            
        return True
        
    def DeleteAll(self):                   
        return self.DeleteRows(numRows=len(self.data))
    

#---------------------------------------------------------------------------



class CustTableGrid(wx.grid.Grid):
    def __init__(self, parent, log, colLabels=None, dataTypes=None):
        wx.grid.Grid.__init__(self, parent, -1)

        '''
        colLabels = ['Module', 'SubModule', 'CaseID', 'Name', 'Func',
                          'argc', 'arg1', 'arg2', 'arg3', 'arg4', 'Avail', 'Result', 'Comment']

        dataTypes = [wx.grid.GRID_VALUE_STRING, 
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_BOOL,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          ]
        '''
        data = [ ]
        '''
            ['', '', '', '', '', '', '', '', '', '', '', '', '']          

            ]
        '''    
        self.table = CustomDataTable(log, data, colLabels=colLabels, dataTypes=dataTypes)

        # The second parameter means that the grid is to take ownership of the
        # table and will destroy it when done.  Otherwise you would need to keep
        # a reference to it and call it's Destroy method later.
        self.SetTable(self.table, True)

        self.SetRowLabelSize(50)
        #self.SetMargins(0,0)
        self.AutoSizeColumns(True)
                
        # wx.grid.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)
        # wx.grid.EVT_GRID_LABEL_LEFT_DCLICK(self, self.OnLabelLeftDClick)

    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
        print("OnLeftDClick")
            
    def OnLabelLeftDClick(self, evt):
        colNumber=evt.GetCol()
        #print "columm number is:",evt.GetCol()
        #print 'column %s label is %s:'%(colNumber,self.table.colLabels[colNumber])
        RowsData= sorted(self.table.data,key=lambda x:x[colNumber])
        rowNumber = self.table.GetNumberRows()
        row=0
        
        for row in range(rowNumber):
            self.table.SetRowValue(row,RowsData[row])         
        
        print("OnLabelLeftDoubleClick")
      
    
    def AddRowsToTable(self, row, data):
        for i in range(len(data)):
            self.table.InsertRows(row+i)
            self.table.SetRowValue(row+i,data[i])
            
    def AppendRowsToTable(self, data):
        existedRows = self.table.GetNumberRows()
        self.AddRowsToTable(existedRows, data)
    
    def DeleteRowsFromTable(self, pos, numRows=1):
        self.table.DeleteRows(pos, numRows)
    
    def DeleteAllFromTable(self):
        self.table.DeleteAll()
        
    def GetSelectedRowsFromTable(self):
        #return self.GetSelectedRows()
        rows = []
        for row in range(self.table.GetNumberRows()):
            if self.IsInSelection(row, 0):
                rows.append(row)
        print('select-->',rows)
        return rows
       
    def MoveToNextRow(self):
        Rows = sorted(self.GetSelectedRowsFromTable())
        try:        
            next_row = Rows[0] + 1
            # loop to the first row
            if next_row == self.table.GetNumberRows():
                next_row = 0
        except IndexError:
            return
            
        self.SelectRow(next_row)
        return next_row
    
    def GetRowValueFromTable(self, row):
        return self.table.GetRowValue(row)

    def SetRowValueToTable(self,row, value):
        return self.table.SetRowValue(row,value)
    
    def GetTableRows(self):
        return self.GetNumberRows()
    
    def OnLabelRightClick(self,evt):
        print("OnLabelRightClick")
        evt.Skip()
        



#---------------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, parent, log):

        wx.Frame.__init__(
            self, parent, -1, "Custom Table, data driven Grid  Demo", size=(640,480)
            )

        p = wx.Panel(self, -1, style=0)
        
        colLabels = ['Price', 'NumBuy', 'NumStack', 'numSell', 'Cost', 'Profit']
        
        dataTypes = [wx.grid.GRID_VALUE_STRING, 
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,                         
                          ]
        
        grid = CustTableGrid(p, log,colLabels=colLabels, dataTypes=dataTypes)
        b = wx.Button(p, -1, "Another Control...")
        b.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
        b.Bind(wx.EVT_SET_FOCUS, self.OnButtonFocus)
        bs = wx.BoxSizer(wx.VERTICAL)
        bs.Add(grid, 1, wx.GROW|wx.ALL, 5)
        bs.Add(b)
        p.SetSizer(bs)

    def OnButton(self, evt):
        print("button selected")

    def OnButtonFocus(self, evt):
        print("button focus")


#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.App(False)

    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()


#---------------------------------------------------------------------------
