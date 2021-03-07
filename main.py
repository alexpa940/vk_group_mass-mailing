# This Python file uses the following encoding: utf-8
import sys
import vk_api
import time
import random

from PySide2 import QtCore, QtGui, QtXml
from PySide2.QtGui import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtCore import QFile, QObject
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])

def loadDialog(file_name):
    loader = QUiLoader()
    the_file = QFile(file_name)
    the_file.open(QFile.ReadOnly)
    ret_val = loader.load(the_file)
    the_file.close()
    return ret_val

class Main(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._ui = loadDialog(r'mainwindow.ui')
        self.session = None
        self.API = None
        self._ui.logEdit.setReadOnly(True)
        self._ui.dialogEdit.setReadOnly(True)
        self._ui.testButton.clicked.connect(lambda: self.auth())
        self._ui.cleanButton.clicked.connect(lambda: self.cleanlogs())
        self._ui.sendButton.clicked.connect(lambda: self.send())

    def show(self, cancellable=False):
        self._ui.show()

    def cleanlogs(self):
        self._ui.logEdit.clear()

    def auth(self):
        self._ui.dialogEdit.clear()
        self._ui.logEdit.append(time.ctime() + " [VK] Trying to auth ")

        if not self._ui.lineEdit.text():
            self._ui.logEdit.append(time.ctime() + " [VK] Enter token ")
            return

        try:
            session = vk_api.VkApi(token=self._ui.lineEdit.text())
        except vk_api.ApiError:
            self._ui.logEdit.append(time.ctime() + " [VK] False to auth ")
            return
        self.session = session

        try:

            if self.session is None: return
            self.API = self.session.get_api()
            self._ui.logEdit.append(time.ctime() + " [VK] API is availible ")

            dialogs_list = self.session.method("messages.getConversations", {"offset": 0, "count": 20, "filter":'all'})
            for dialog in dialogs_list['items']:
                dialog_id = dialog['conversation']['peer']['local_id']
                self._ui.dialogEdit.append(str(dialog_id))
        except vk_api.ApiError:
            self._ui.logEdit.append(time.ctime() + " [VK] Check token. ")

    def send(self):
        if not self._ui.lineEdit.text():
            self._ui.logEdit.append(time.ctime() + " [VK] Enter token ")
            return
        if self.API is None:
            self._ui.logEdit.append(time.ctime() + " [VK] No auth. ")
            return
        if not self._ui.textEdit.toPlainText():
            self._ui.logEdit.append(time.ctime() + " [VK] Enter message ")
            return
        try:
            dialogs_list = self.session.method("messages.getConversations", {"offset": 0, "count": 20, "filter":'all'})
            for dialog in dialogs_list['items']:
                dialog_id = dialog['conversation']['peer']['local_id']
                self.API.messages.send(random_id=get_random_id(), peer_id=dialog_id, message=self._ui.textEdit.toPlainText())
            self._ui.logEdit.append(time.ctime() + " [VK] Message was sended ")
        except vk_api.ApiError:
            self._ui.logEdit.append(time.ctime() + " [VK] Check token. ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()

    sys.exit(app.exec_())





