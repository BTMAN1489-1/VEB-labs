import wx
from GUI import MyFrame


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "GUI")
    frame.Show()
    app.MainLoop()


