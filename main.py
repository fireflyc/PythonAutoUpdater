#coding=utf-8
import os
import subprocess
import shutil
import sys

from threading import Thread
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QDialog, QApplication, QMessageBox
from ui.main_ui import Ui_Dialog
from updater import Updater


class QtUI(QDialog, Ui_Dialog):
    update_progressbar_signal = pyqtSignal(int)
    finish_update_signal = pyqtSignal(list)

    def __init__(self, download_path, url, title=u"自动更新", kill_process_name="MyClient.exe"):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(title)

        self.download_path = os.path.join(download_path, "update")
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)
        self.download_files = []

        self.updater = Updater(url)
        self.kill_process_name = kill_process_name
        self.total_progressbar.setValue(0)
        self.total_progressbar.setMaximum(100)

        self.progressbar.setValue(0)
        self.progressbar.setMaximum(100)

        self.btn.clicked.connect(self.check_update)

        self.update_progressbar_signal.connect(self.on_update_progressbar)
        self.finish_update_signal.connect(self.on_finish_update)

    def next_file(self, remote_file):
        self.info.appendPlainText(u"开始下载%s\n" % remote_file)
        self.total_progressbar.setValue(self.total_progressbar.value() + 1)

    def on_update_progressbar(self, value):
        self.progressbar.setValue(value)

    def on_finish_update(self, download_files):
        self.download_files = download_files
        self.info.appendPlainText(u"更新完毕\n")
        if QMessageBox.question(self, u"是否重启", u"更新完毕是否重启应用？", QMessageBox.Yes,
                                QMessageBox.No) == QMessageBox.Yes:
            self.kill_process()
            self.copy_to_new()
            self.info.appendPlainText(u"应用新文件")
            sys.exit(0)

    def notify_process(self, read_size, total_size):
        self.update_progressbar_signal.emit(round(float(read_size) / total_size * 100))

    def download(self):
        download_files = self.updater.update(self.download_path, self.next_file, self.notify_process)
        self.finish_update_signal.emit(download_files)


    def check_update(self):
        self.info.appendPlainText(u"检查更新..\n")
        remote_file_list = self.updater.check()

        if len(remote_file_list) == 0:
            self.info.appendPlainText(u"所有文件都是最新的，您不需要更新\n")
            return
        self.info.appendPlainText(u"需要更新文件的列表\n")
        for remote_file in remote_file_list:
            self.info.appendPlainText(str(remote_file) + "\n")
        self.total_progressbar.setMaximum(len(remote_file_list))
        if QMessageBox.question(self, u"是否更新", u"发现新版本是否更新", QMessageBox.Yes,
                                QMessageBox.No) == QMessageBox.Yes:
            self.btn.setEnabled(False)
            Thread(target=self.download).start()

    def kill_process(self):
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.call("taskkill /F /IM " + self.kill_process_name, startupinfo=startupinfo, shell=True)

    def copy_to_new(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        for download_file in self.download_files:
            shutil.copy(download_file, cur_dir)
        shutil.rmtree(self.download_path)


cur_dir = os.path.dirname(os.path.abspath(__file__))

app = QApplication(sys.argv)
mainDlg = QtUI(cur_dir, sys.argv[1], kill_process_name=sys.argv[2])
mainDlg.showNormal()
app.exec_()