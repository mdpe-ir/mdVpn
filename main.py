import os
from datetime import datetime
from time import sleep

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication, pyqtSignal, Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton

from MdVpn import mdVersion, mdCopyrightYear, rootPasswordEmptyMessage, baseDir


class Message(QWidget):
    def __init__(self, title, message, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QGridLayout())
        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet(
            "font-family: 'Roboto', sans-serif; font-size: 14px; font-weight: bold; padding: 0;")
        self.messageLabel = QLabel(message, self)
        self.messageLabel.setStyleSheet(
            "font-family: 'Roboto', sans-serif; font-size: 12px; font-weight: normal; padding: 0;")
        self.buttonClose = QPushButton(self)
        self.buttonClose.setIcon(QIcon(f"{baseDir}/res/close.png"))
        self.buttonClose.setFixedSize(14, 14)
        self.layout().addWidget(self.titleLabel, 0, 0)
        self.layout().addWidget(self.messageLabel, 1, 0)
        self.layout().addWidget(self.buttonClose, 0, 1, 2, 1)


class Notification(QWidget):
    signNotifyClose = pyqtSignal(str)

    def __init__(self, parent=None):
        time = datetime.now()
        currentTime = str(time.hour) + ":" + str(time.minute) + "_"
        self.LOG_TAG = currentTime + self.__class__.__name__ + ": "
        super(QWidget, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        resolution = QDesktopWidget().screenGeometry(-1)
        screenWidth = resolution.width()
        screenHeight = resolution.height()
        # print(self.LOG_TAG + "width: " + str(resolution.width()) + " height: " + str(resolution.height()))
        self.nMessages = 0
        self.mainLayout = QVBoxLayout(self)
        w = (int(screenWidth / 1.3))

        self.move(QPoint(w, 0))

    def setNotify(self, title, message):
        m = Message(title, message, self)
        self.mainLayout.addWidget(m)
        m.buttonClose.clicked.connect(self.onClicked)
        self.nMessages += 1
        self.show()

    def onClicked(self):
        # self.mainLayout.removeWidget(self.sender().parent())
        self.sender().parent().deleteLater()
        self.nMessages -= 1
        self.adjustSize()
        if self.nMessages == 0:
            self.close()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(552, 344)
        MainWindow.setMaximumSize(552, 344)
        MainWindow.setMinimumSize(552, 344)
        font = QtGui.QFont()
        font.setFamily("IRANSans")
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(f"{baseDir}/res/md-vpn-icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(f"/opt/mdVpn/res/md-vpn-icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 100, 531, 211))
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 531, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.disconnectBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.disconnectBtn.setObjectName("disconnectBtn")
        self.horizontalLayout.addWidget(self.disconnectBtn)
        self.connectTofastesServerButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.connectTofastesServerButton.setObjectName("connectTofastesServerButton")
        self.horizontalLayout.addWidget(self.connectTofastesServerButton)

        self.reconnectServerButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.reconnectServerButton.setObjectName("reconnectServerButton")
        self.horizontalLayout.addWidget(self.reconnectServerButton)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(3, 320, 331, 20))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.horizontalLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 530, 30))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.InputHorizantalPassword = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.InputHorizantalPassword.setContentsMargins(0, 0, 0, 0)
        self.InputHorizantalPassword.setObjectName("InputHorizantalPassword")
        self.sudoPasswordLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.sudoPasswordLabel.setObjectName("sudoPasswordLabel")
        self.InputHorizantalPassword.addWidget(self.sudoPasswordLabel)
        self.passwordInput = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.passwordInput.setObjectName("passwordInput")
        self.InputHorizantalPassword.addWidget(self.passwordInput)

        qtRectangle = MainWindow.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        MainWindow.move(qtRectangle.topLeft())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.notification = Notification()

    def sudoPasswordNotFoundNotify(self):
        self.notification.setNotify("{}".format('Oh No!'),
                                    "{}".format(rootPasswordEmptyMessage))

    def QPushButtonClicked(self):
        self.connectTofastesServerButton.clicked.connect(self.connect)
        self.disconnectBtn.clicked.connect(self.disconnect)
        self.reconnectServerButton.clicked.connect(self.reconnect)
        self.generate_status()

    def connect(self):
        sudo_password = self.passwordInput.toPlainText()
        if sudo_password == "":
            self.sudoPasswordNotFoundNotify()
            self.label.setText(rootPasswordEmptyMessage)
        else:
            self.label.setText('Connecting ...')
            QCoreApplication.processEvents()
            command = '-S protonvpn connect --fast'
            p = os.popen("sudo -S %s" % (command), 'w').write(sudo_password)
            QCoreApplication.processEvents()
            self.label.setText(f'Connected !')
            sleep(10)
            self.generate_status()

    def reconnect(self):
        sudo_password = self.passwordInput.toPlainText()
        if sudo_password == "":
            self.sudoPasswordNotFoundNotify()
            self.label.setText(rootPasswordEmptyMessage)
        else:
            self.label.setText('Reconnecting ...')
            QCoreApplication.processEvents()

            command = '-S   protonvpn reconnect'
            p = os.popen("sudo -S %s" % (command), 'w').write(sudo_password)

            self.label.setText(f'Connected !')
            sleep(10)
            self.generate_status()

    def disconnect(self):
        sudo_password = self.passwordInput.toPlainText()
        if sudo_password == "":
            self.sudoPasswordNotFoundNotify()
            self.label.setText(rootPasswordEmptyMessage)
        else:
            self.label.setText('Disconnecting ...')
            QCoreApplication.processEvents()
            command = '-S protonvpn disconnect'
            p = os.popen("sudo -S %s" % (command), 'w').write(sudo_password)
            self.label.setText(f'Disconnected !')
            sleep(5)
            self.generate_status()

    def generate_status(self):
        QCoreApplication.processEvents()
        stream = os.popen('protonvpn status')
        result = '\n' + stream.read()
        self.label.setText(f' {result}')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Md Vpn"))
        self.label.setText(_translate("MainWindow", " "))
        self.disconnectBtn.setText(_translate("MainWindow", "Disconnect"))
        self.connectTofastesServerButton.setText(_translate("MainWindow", "Connect To Fastest server "))
        self.reconnectServerButton.setText(_translate("MainWindow", "Reconnect"))
        self.label_2.setText(
            _translate("MainWindow",
                       f"CopyRight {mdCopyrightYear} |  mdpe.ir | Based On ProtonVpn | {mdVersion}"))
        self.sudoPasswordLabel.setText(_translate("Dialog", "Sudo Password : "))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.QPushButtonClicked()
    sys.exit(app.exec_())
