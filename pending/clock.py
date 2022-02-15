#加入wx.Timer定时器
import wx
class myFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None,pos=[100,100],
                         size=[390,420],title="商贾三国")
        icon = wx.Icon(name=".\\icons\\V.ico", type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        # self.i=1
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour((220, 210, 0))
        poem = "步出夏门行·观沧海 \n作者：曹操  汉代 "
        font = wx.Font(20, wx.SCRIPT, wx.NORMAL, wx.NORMAL)
        self.mytext = wx.StaticText(parent=self.panel,
                                    pos=[30, 30], size=[330, 380], label=poem)
        self.mytext.SetFont(font)
        self.timer=wx.Timer(self)
        self.Show()
        self.Bind(wx.EVT_TIMER,self.onTimer,self.timer)
        self.timer.StartOnce(2000)
    def onTimer(self,event):
        poem = "步出夏门行·观沧海 \n作者：曹操  汉代 \n东临碣石，以观沧海。\n" \
               "水何澹澹，山岛竦峙。\n树木丛生，百草丰茂。\n秋风萧瑟，洪波涌起。\n" \
               "日月之行，若出其中。\n星汉灿烂，若出其里。\n幸甚至哉，歌以咏志。"
        # poem=str(self.i)
        self.mytext.SetLabel(poem)
        # self.i=self.i+1
        # print(self.i)
        # self.timer.Stop()
myapp=wx.App()
myframe=myFrame()
myapp.MainLoop()