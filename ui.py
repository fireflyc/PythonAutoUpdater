#coding=utf-8
from threading import Thread
from updater import Updater

__author__ = 'fireflyc'

import Tkinter
import ttk
import tkMessageBox


class TkUI:
    def __init__(self, download_path, url, title=u"自动更新"):
        self.download_path = download_path

        self.updater = Updater(url)
        self.win = Tkinter.Tk()
        self.win.title(title)
        self.win.geometry("600x400")
        self.btn = Tkinter.Button(self.win, text=u"检查更新", command=self.check_update)
        self.btn.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)

        self.total_progressbar = ttk.Progressbar(self.win, orient=Tkinter.HORIZONTAL, mode="determinate")
        self.total_progressbar.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)
        self.total_progressbar["maximum"] = None

        self.progressbar = ttk.Progressbar(self.win, orient=Tkinter.HORIZONTAL, mode="determinate")
        self.progressbar.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)
        self.progressbar["maximum"] = None

        self.info = Tkinter.Text(self.win)
        self.info.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)
        self.info.config()

    def next_file(self, remote_file):
        self.info.insert(Tkinter.END, u"开始下载%s\n" % remote_file)
        self.total_progressbar["value"] += 1

    def notify_process(self, read_size, total_size):
        self.progressbar["value"] = round(float(read_size) / total_size * 100)
        self.win.update()

    def download(self):
        self.updater.update(self.download_path, self.next_file, self.notify_process)
        self.info.insert(Tkinter.END, u"更新完毕\n")

    def check_update(self):
        self.info.insert(Tkinter.END, u"检查更新..\n")
        remote_file_list = self.updater.check()
        if len(remote_file_list) == 0:
            self.info.insert(Tkinter.END, u"所有文件都是最新的，您不需要更新\n")
            return
        self.info.insert(Tkinter.END, u"需要更新文件的列表\n")
        for remote_file in remote_file_list:
            self.info.insert(Tkinter.END, str(remote_file) + "\n")
        self.total_progressbar["maximum"] = len(remote_file_list)
        if tkMessageBox.askyesno(u"是否更新", u"发现新版本是否更新"):
            self.btn.config(state=Tkinter.DISABLED)
            thread = Thread(target=self.download)
            thread.start()

    def show(self):
        Tkinter.mainloop()
