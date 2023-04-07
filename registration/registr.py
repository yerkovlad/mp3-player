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
        self.btn_registr = QtWidgets.QPushButton(Form)
        self.btn_registr.setGeometry(QtCore.QRect(140, 100, 91, 41))
        self.btn_registr.setObjectName("btn_registr")
        self.btn_registr.released.connect(self.registration_btn_func)
        self.btn_registr.setStyleSheet(btn_style)
        self.textpassword = QtWidgets.QLineEdit(Form)
        self.textpassword.setGeometry(QtCore.QRect(100, 30, 181, 31))
        self.textpassword.setObjectName("textusername")
        self.textusername = QtWidgets.QLineEdit(Form)
        self.textusername.setGeometry(QtCore.QRect(100, 0, 181, 31))
        self.textusername.setObjectName("textpassword")
        self.text_complete = QLabel('You have been registered')
        self.text_complete.setWindowTitle('Registration')
        self.text_complete.setGeometry(850, 250, 370, 100)
        

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        """
        In this function sets text and widget titles
        """
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Registration", "Registration"))
        self.btn_registr.setText(_translate("Form", "Sign up"))

    def registration_btn_func(self):
        """
        When button 'Registration' clicked, program return or from incorrect information or that you registered
        """
        if read_from_mndb(self.textusername.text(), self.textpassword.text()) != None:
            self.text_complete.setText('Such a user is already registered, if this is you, log in to your account')
        elif self.textusername.text() == '' and self.textpassword.text() == '':
            self.text_complete.setText('Please, create your username and password')
        elif self.textusername.text() == '':
            self.text_complete.setText('Please, create your username')
        elif self.textpassword.text() == '':
            self.text_complete.setText('Please, create your password')
        else:
            write_to_mndb(self.textusername.text(), self.textpassword.text())
            write_ac_inf_to_database(self.textusername.text(), self.textpassword.text())
            write_to_mndb(self.textusername.text(), self.textpassword.text(), read_from_mus_table())
        self.text_complete.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())