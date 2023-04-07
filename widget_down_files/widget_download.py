from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import bs4
import json
import os
import sys
import shutil
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
        Form.setObjectName("Search music")
        Form.resize(400, 300)
        self.btn_download = QtWidgets.QPushButton(Form)
        self.btn_download.setGeometry(QtCore.QRect(140, 100, 91, 41))
        self.btn_download.setObjectName("btn_download")
        self.btn_download.released.connect(self.download_mus_btn)
        self.btn_download.setStyleSheet(btn_style)
        self.textEdit = QtWidgets.QLineEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(100, 30, 181, 31))
        self.textEdit.setObjectName("textEdit")
        self.textline = QtWidgets.QLabel('test')
        self.textline.setGeometry(QtCore.QRect(140, 70, 91, 41))
        self.textline.setObjectName("textline")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        """
        In this function sets text and widget titles
        """
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Search music", "Search music"))
        self.btn_download.setText(_translate("Form", "Download"))

    def download_mus_btn(self):
        """
        This function call search_and_down_mus() function that download music
        """
        try:
            search_and_down_mus(self.textEdit.text())
        except:
            pass

def search_and_down_mus(song_name_inp : str):
    """
    The function downloads the first song from the site now.morsmusic.org by the name entered by the user
    """
    list_with_dicts = list()
    headers = {
        'authority' : 'now.morsmusic.org',
        'cache-control' : 'max-age=0',
        'upgrade-insecure-requests' : '1',
        'user-agent' : 'Chrome/111.0.5563.111',
        'sec-fetch-dest' : 'document',
        'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site' : 'same-origin',
        'sec-fetch-mode' : 'navigate',
        'sec-fetch-user' : '?1',
        'accept-language' : 'ua, ru; q=0.9'
    }

    session = requests.session()
    song_name_inp = song_name_inp.replace(' ', '+')
    resp = session.get(f'https://now.morsmusic.org/search/{song_name_inp}', headers = headers)

    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    for el in soup.find_all('div', class_ = 'track mustoggler __adv_list_track'):
        list_with_dicts.append(json.loads(el.get('data-musmeta')))
    song = requests.get('https://now.morsmusic.org' + list_with_dicts[0]['url'])
    name_song = list_with_dicts[0]['title']
    with open(f'downloaded/{name_song}.mp3', 'wb') as fl:
        fl.write(song.content)
    write_to_database('downloaded', list_with_dicts[0])
    shutil.rmtree('downloaded', ignore_errors=True)
    try:
        os.mkdir('downloaded')
    except:
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())