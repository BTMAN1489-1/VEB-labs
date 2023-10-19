import wx
import logging
from client_socket import ClientSocket


class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        self.sb = self.CreateStatusBar()

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        host_text = wx.StaticText(panel, label="Хост: ")
        self.enter_host = wx.TextCtrl(panel)
        hbox.Add(host_text, flag=wx.TOP | wx.LEFT, border=10)
        hbox.Add(self.enter_host, flag=wx.RIGHT | wx.TOP | wx.LEFT, border=10, proportion=1)

        port_text = wx.StaticText(panel, label="Порт: ")
        self.enter_port = wx.TextCtrl(panel)
        hbox.Add(port_text, flag=wx.TOP | wx.LEFT, border=10)
        hbox.Add(self.enter_port, flag=wx.RIGHT | wx.TOP | wx.LEFT, border=10, proportion=1)

        connect_button = wx.Button(panel, label="Установить соединение")

        vbox.Add(hbox, flag=wx.EXPAND | wx.RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM, proportion=1, border=10)
        vbox.Add(wx.StaticLine(panel), flag=wx.EXPAND | wx.RIGHT | wx.LEFT, border=10)
        vbox.Add(connect_button, flag=wx.ALIGN_CENTER | wx.RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM, border=10)

        self.Bind(wx.EVT_BUTTON, self.on_create_connection,connect_button)

        panel.SetSizer(vbox)

    def on_create_connection(self, event):
        port = self.enter_port
        host = self.enter_host
        try:
            conn = ClientSocket(host.GetValue(), int(port.GetValue()))
            conn.create_connection()

            logging.info(f"Successful connection to <{host}:{port}>")

            self.sb.SetStatusText("Подключение выполнено")
            dialog = wx.FileDialog(self, "Выберите файл для отправки")
            res = dialog.ShowModal()
            path = dialog.GetPath()
            dialog.Destroy()
            if res == wx.ID_OK:
                self.sb.SetStatusText("Файл отправляется")
                conn.send_file(path)
                self.sb.SetStatusText("Файл отправлен")
            else:
                self.sb.SetStatusText("Соединение сброшено")

        except Exception as e:
            logging.exception(e)
            self.sb.SetStatusText("Ошибка подключения")
            port.Clear()
            host.Clear()

