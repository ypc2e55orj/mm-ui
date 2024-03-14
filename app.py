import wx


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY)


if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
