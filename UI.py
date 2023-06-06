import wx
import wx.grid
from drawChart import findall_db_data
from getDatas import getHTML


class MainWindow(wx.Frame):
    """主界面"""

    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, size=(400, 600), pos=(400, 100))

        panel = wx.Panel(self)
        button1 = wx.Button(panel, label="查询历史行情", size=(400, 40), id=1)
        button1.Bind(wx.EVT_BUTTON, self.on_button_click)
        button2 = wx.Button(panel, label="退出查询", size=(400, 40), id=2)
        button2.Bind(wx.EVT_BUTTON, self.on_button_click)
        # 更改按钮文字样式
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        button1.SetFont(font)
        button2.SetFont(font)
        # 创建一个位图对象，并从文件中加载一张图片
        bmp = wx.Bitmap('img/wx_Main.jpg', wx.BITMAP_TYPE_JPEG)
        # 创建 StaticBitmap 控件，并将位图赋值给它
        self.bitmap = wx.StaticBitmap(panel, bitmap=bmp)
        # 将 StaticBitmap 控件添加到窗口中
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bitmap, 3, wx.EXPAND)  # 占取3/4
        sizer.Add(button1, 0, wx.CENTER)  # 大小保持原样
        sizer.Add(button2, 0, wx.CENTER)

        panel.SetSizer(sizer)

    def on_button_click(self, event):
        event_id = event.GetId()
        if event_id == 1:
            frame2 = SecondWindow(None, "历史行情")
            frame2.Show()
            self.Close()

        if event_id == 2:
            self.Close()


class SecondWindow(wx.Frame):
    """副界面"""

    data = []
    column_names = []
    stack_Code = 0

    def __init__(self, parent, title):
        super(SecondWindow, self).__init__(parent, title=title, size=(750, 650))
        self.bitmap = None
        self.grid = None
        self.grid1 = None
        self.column_names = ['日期', '开盘价', '收盘价', '最高价', '最低价', '涨跌额', '成交金额', '成交量']
        panel = wx.Panel(self)
        btn1 = wx.Button(parent=panel, id=1, label='查询数据', pos=(640, 300), size=(90, 30))
        btn2 = wx.Button(parent=panel, id=2, label='更新数据', pos=(640, 350), size=(90, 30))
        btn3 = wx.Button(parent=panel, id=3, label='查询折线图', pos=(640, 400), size=(90, 30))
        btn4 = wx.Button(parent=panel, id=4, label='查询OHLC图', pos=(640, 450), size=(90, 30))
        btn5 = wx.Button(parent=panel, id=5, label='查询k线图', pos=(640, 500), size=(90, 30))
        btn6 = wx.Button(parent=panel, id=6, label='返回主界面', pos=(640, 550), size=(90, 30))

        btn1.Bind(wx.EVT_BUTTON, self.on_click)
        btn2.Bind(wx.EVT_BUTTON, self.on_click)
        btn3.Bind(wx.EVT_BUTTON, self.on_click)
        btn4.Bind(wx.EVT_BUTTON, self.on_click)
        btn5.Bind(wx.EVT_BUTTON, self.on_click)
        btn6.Bind(wx.EVT_BUTTON, self.on_click)

    def on_click(self, event):
        event_id = event.GetId()
        if event_id == 1:
            print('查询数据:')
            self.data = None
            data = []
            data_dict = findall_db_data('2023-01-03', '2023-05-01')
            for d in data_dict:
                values = [d['日期'], d['开盘价'], d['收盘价'], d['最高价'], d['最低价'], d['涨跌额'], d['成交金额'], d['成交量']]
                data.append(values)
            print(data)
            self.data = data
            if self.bitmap is not None:
                self.bitmap.Hide()
            if self.grid1 is not None:
                self.grid1.Hide()
            if self.grid is None:
                self.grid = wx.grid.Grid(self)
                self.grid.CreateGrid(len(self.data), len(self.data[0]))
                for row in range(len(self.data)):
                    for col in range(len(self.data[row])):
                        self.grid.SetColLabelValue(col, self.column_names[col])
                        self.grid.SetCellValue(row, col, str(self.data[row][col]))
                self.grid.AutoSize()
            else:
                self.grid.Show()
        elif event_id == 2:
            print('更新数据:')
            self.data = None
            monthData = getHTML('600887')
            data = []
            for item in monthData:
                tmp = list(item.values())
                data.append(tmp)
            print(data)
            self.data = data
            if self.bitmap is not None:
                self.bitmap.Hide()
            if self.grid is not None:
                self.grid.Hide()
            if self.grid1 is None:
                self.grid1 = wx.grid.Grid(self)
                self.grid1.CreateGrid(len(self.data), len(self.data[0]))
                for row in range(len(self.data)):
                    for col in range(len(self.data[row])):
                        self.grid1.SetColLabelValue(col, self.column_names[col])
                        self.grid1.SetCellValue(row, col, str(self.data[row][col]))
                self.grid1.AutoSize()
            else:
                self.grid1.Show()
        elif event_id == 3:
            print('查询折线图')
            if self.grid is not None:
                self.grid.Hide()
            if self.grid1 is not None:
                self.grid1.Hide()
            if self.bitmap is not None:
                self.bitmap.Hide()  # 最后将其销毁
            img = wx.Image('img/plot1.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, img)
            self.Show()
        elif event_id == 4:
            print('查询OHLC图')
            if self.grid is not None:
                self.grid.Hide()
            if self.grid1 is not None:
                self.grid1.Hide()
            if self.bitmap is not None:
                self.bitmap.Hide()
            img = wx.Image('img/plot2.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, img)
            self.Show()
        elif event_id == 5:
            print('查询k线图')
            if self.grid is not None:
                self.grid.Hide()
            if self.grid1 is not None:
                self.grid1.Hide()
            if self.bitmap is not None:
                self.bitmap.Hide()
            img = wx.Image('img/plot3.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, img)
            self.Show()
        else:
            mainFrame = MainWindow(None, "伊利股份600887")
            mainFrame.Show()
            self.Close()


if __name__ == '__main__':
    app = wx.App()
    frame1 = MainWindow(None, "伊利股份600887")
    frame1.Show()
    app.MainLoop()
