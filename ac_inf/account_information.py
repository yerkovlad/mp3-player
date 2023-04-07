from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from database_fl.connect_to_database import *

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
        Form.setObjectName("Form")
        Form.resize(296, 123)
        self.see_password_btn = QtWidgets.QPushButton(Form)
        self.see_password_btn.setGeometry(QtCore.QRect(20, 80, 91, 21))
        self.see_password_btn.setStyleSheet(btn_style)
        self.see_password_btn.setObjectName("see_password_btn")
        self.see_password_btn.released.connect(self.see_password)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 20, 271, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 271, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        """
        In this function sets text and widget titles
        """
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Account"))
        self.see_password_btn.setText(_translate("Form", "See password"))
        self.label.setText(_translate("Form", f"Username: {read_from_ac_inf_to_database()[0]}"))
        self.label_2.setText(_translate("Form", f"Password: {len(read_from_ac_inf_to_database()[1])*'*'}"))

    def see_password(self):
        """
        It's a function that see or no password
        """
        if self.see_password_btn.text() == 'See password':
            self.label_2.setText(f"Password: {read_from_ac_inf_to_database()[1]}")
            self.see_password_btn.setText('Hide password')
        else:
            self.label_2.setText(f"Password: {len(read_from_ac_inf_to_database()[1])*'*'}")
            self.see_password_btn.setText('See password')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())