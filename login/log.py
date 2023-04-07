from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from global_database.con_to_mon_db_serv import *

class Ui_Form(object):
    """
    The main class for this widget, where is all code
    """
    def setupUi(self, Form):
        """
        The function, where is all parametrs for this widget
        """
        btn_style = '''QPushButton{background-color: skyblue;}
                       QPushButton:hover{background-color: lightskyblue; color: dodgerblue; \
                       font-weight: bold;}'''
        Form.setObjectName("Search music")
        Form.resize(400, 300)
        self.btn_login = QtWidgets.QPushButton(Form)
        self.btn_login.setGeometry(QtCore.QRect(140, 100, 91, 41))
        self.btn_login.setObjectName("btn_login")
        self.btn_login.released.connect(self.login_btn_func)
        self.btn_login.setStyleSheet(btn_style)
        self.textpassword = QtWidgets.QLineEdit(Form)
        self.textpassword.setGeometry(QtCore.QRect(100, 30, 181, 31))
        self.textpassword.setObjectName("textusername")
        self.textusername = QtWidgets.QLineEdit(Form)
        self.textusername.setGeometry(QtCore.QRect(100, 0, 181, 31))
        self.textusername.setObjectName("textpassword")
        self.text_complete = QLabel()
        self.text_complete.setWindowTitle('Login')
        self.text_complete.setGeometry(850, 250, 370, 100)
        

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        """
        In this function sets text and widget titles
        """
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Login", "Login"))
        self.btn_login.setText(_translate("Form", "Login"))

    def login_btn_func(self):
        """
        When button 'Login' clicked, program return or from incorrect information or that you logined
        """
        if self.textusername.text() == '' and self.textpassword.text() == '':
            self.text_complete.setText('Please, write your username and password')
        elif self.textusername.text() == '':
            self.text_complete.setText('Please, write your username')
        elif self.textpassword.text() == '':
            self.text_complete.setText('Please, write your password')
        elif read_from_mndb(self.textusername.text(), self.textpassword.text()) == None:
            self.text_complete.setText('You entered an incorrect username or password')
        else:
            self.text_complete.setText('You have been logined')
            write_ac_inf_to_database(self.textusername.text(), self.textpassword.text())
            read_from_mndb(self.textusername.text(), self.textpassword.text(), True)
        self.text_complete.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())