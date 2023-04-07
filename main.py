import os
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, \
QFrame, QGraphicsDropShadowEffect, QGraphicsView, QGraphicsScene, QLabel, \
QPushButton, QHBoxLayout, QStyle, QListWidget, QFileDialog, QSlider, QScrollBar
from PyQt5.QtGui import QGradient, QFont, QColor, QCursor, QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist, \
QMediaMetaData
from peewee import *
import shutil
import time
from database_fl.connect_to_database import *

class Window(QMainWindow):
    """
    The class, where creating the main window
    """
    def __init__(self, *args, **kwargs):
        """
        The function, where is all parametrs,
        buttons, sliders, texts, containers and so one
        """
        super().__init__(*args, **kwargs)
        self.setWindowTitle('MP3-Player')
 
        # Create a containers
        btn_box = QHBoxLayout()
        btn_box2 = QHBoxLayout()
        container = QGridLayout()
        container2 = QGridLayout()
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setFrameShadow(QFrame.Sunken)
        frame.setLayout(container2)
 
        # Create some variables
        self.dir = f'{QDir.currentPath()}'
        self.url = QUrl()
        self.player = QMediaPlayer()
        self.content = QMediaContent()
        self.playlist = QMediaPlaylist(self.player)
        self.player.setPlaylist(self.playlist)
        self.playlist.currentIndexChanged.connect(self.update)
 
        # Create Qlabel variables
        self.status = QLabel('Status: ')
        self.status.setFrameShape(QFrame.Box)
        self.status.setFrameShadow(QFrame.Sunken)
 
        self.track = QLabel('Track: ')
        self.track.setFrameShape(QFrame.Box)
        self.track.setFrameShadow(QFrame.Sunken)

        self.account_inf_text = QLabel('Account: ')
        self.account_inf_text.setFrameShadow(QFrame.Sunken)
 
        # Define and create the listbox
        self.musiclist = QListWidget()
        self.musiclist.setFrameShape(QFrame.Box)
        self.musiclist.setFrameShadow(QFrame.Sunken)
        self.musiclist.setStyleSheet('background-color: snow;')
 
        # Used for track play when double clicked
        self.musiclist.itemDoubleClicked.connect(self._doubleclick)

        # Create style for buttons and sliders
        btn_style = '''QPushButton{background-color: skyblue;}
                       QPushButton:hover{background-color: lightskyblue; color: dodgerblue; \
                       font-weight: bold;}'''
        slider_style="""
            QSlider{
                background: #fff;
            }
            QSlider::groove:horizontal {  
                height: 10px;
                margin: 0px;
                border-radius: 5px;
                background: #B0AEB1;
            }
            QSlider::handle:horizontal {
                background: #fff;
                border: 1px solid #E3DEE2;
                width: 17px;
                margin: -5px 0; 
                border-radius: 8px;
            }
            QSlider::sub-page:qlineargradient {
                background: lightskyblue;
                border-radius: 5px;
            }
        """

        # Create sliders
        self.volumeslider = QSlider(Qt.Horizontal)
        self.volumeslider.setFocusPolicy(Qt.NoFocus)
        self.volumeslider.valueChanged[int].connect(self.change_volume)
        self.volumeslider.setValue(100)
        self.volumeslider.setStyleSheet(slider_style)

        self.musicslider = QSlider(QtCore.Qt.Horizontal, self)
        self.musicslider.sliderReleased.connect(self.slider_released) 
        self.musicslider.setStyleSheet(slider_style)

        # Create text for sliders
        self.text_volume = QLabel('Volume:')
        self.text_music = QLabel('Music:')

        # Create buttons
        download_mus_btn = QPushButton('Add music')
        download_mus_btn.released.connect(self._download_mus)
        download_mus_btn.setCursor(Qt.PointingHandCursor)
        download_mus_btn.setStyleSheet(btn_style)
        download_mus_btn.setMaximumWidth(100)

        registration_btn = QPushButton('Registration')
        registration_btn.released.connect(self._registration)
        registration_btn.setCursor(Qt.PointingHandCursor)
        registration_btn.setStyleSheet(btn_style)
        registration_btn.setMaximumWidth(100)
        
        login_btn = QPushButton('Login')
        login_btn.released.connect(self._login)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet(btn_style)
        login_btn.setMaximumWidth(100)

        account_inf_btn = QPushButton('Account')
        account_inf_btn.released.connect(self._account_inf)
        account_inf_btn.setCursor(Qt.PointingHandCursor)
        account_inf_btn.setStyleSheet(btn_style)
        account_inf_btn.setMaximumWidth(100)

        file_btn = QPushButton('Get Playlist')
        file_btn.released.connect(self._files)
        file_btn.setCursor(Qt.PointingHandCursor)
        file_btn.setStyleSheet(btn_style)
        file_btn.setMaximumWidth(100)
 
        clear_btn = QPushButton('Clear Playlist')
        clear_btn.released.connect(self._clear)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet(btn_style)
        clear_btn.setMaximumWidth(100)
 
        # Create & style the control buttons
        self.play_btn = QPushButton('Play')
        self.play_btn.released.connect(self._state)
        self.play_btn.setCursor(Qt.PointingHandCursor)
        self.play_btn.setStyleSheet(btn_style)
 
        self.next_btn = QPushButton('Next')
        self.next_btn.released.connect(self._next)
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(btn_style)
 
        self.stop_btn = QPushButton('Stop')
        self.stop_btn.released.connect(self._stop)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setStyleSheet(btn_style)
 
        self.exit_btn = QPushButton('Exit')
        self.exit_btn.released.connect(self._exit)
        self.exit_btn.setCursor(Qt.PointingHandCursor)
        self.exit_btn.setStyleSheet('QPushButton{background-color: firebrick;} \
                                    QPushButton:hover{background-color: red; color: white; \
                                    font-weight: bold;}')

        # Create parametrs for self.musicslider
        self.Play_Pause = True
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.PlayMode)
        self.timer.start(1000)
 
        # Add the buttons to layout
        btn_box.addWidget(file_btn)
        btn_box.addWidget(clear_btn)
        btn_box2.addWidget(self.play_btn)
        btn_box2.addWidget(self.next_btn)
        btn_box2.addWidget(self.stop_btn)
        btn_box2.addWidget(self.exit_btn)
 
 
        # Add layouts to container layout
        container.addWidget(self._header_footer(100, 100, 40, 'MP3-Player'), 0, 0, 1, 3)
        container.addWidget(self.status, 1, 0, 1, 1)
        container.addWidget(self.track, 1, 1, 1, 1)
        container.addLayout(btn_box, 1, 2, 1, 1)
        container.addWidget(frame, 2, 0, 2, 1)
        container.addWidget(self.musiclist, 2, 1, 1, 2)
        container.addLayout(btn_box2, 3, 1, 1, 2)
        container2.addWidget(account_inf_btn, 0, 0, 1, 1)
        container2.addWidget(download_mus_btn, 1, 0, 1, 1)
        container2.addWidget(registration_btn, 2, 0, 1, 1)
        container2.addWidget(login_btn, 3, 0, 1, 1)
        container2.addWidget(self.text_music, 0, 2, 1, 1)
        container2.addWidget(self.musicslider, 1, 2, 1, 1)
        container2.addWidget(self.text_volume, 2, 2, 1, 1)
        container2.addWidget(self.volumeslider, 3, 2, 1, 1)
 
        # Create the widget and add the button box layout
        widget = QWidget()
        widget.setLayout(container)
        self.setCentralWidget(widget)
 
    def _header_footer(self, minheight, maxheight, fontsize, text):
        """
        This function create the header
        """
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(3)
        shadow.setOffset(3, 3)
 
        scene = QGraphicsScene()
 
        view = QGraphicsView()
        view.setMinimumSize(800, minheight)
        view.setMaximumHeight(maxheight)
        view.setScene(scene)
 
        gradient = QGradient(QGradient.RichMetal)
 
        scene.setBackgroundBrush(gradient)
 
        font = QFont('comic sans ms', fontsize, QFont.Bold)
 
        text = scene.addText(text)
        text.setDefaultTextColor(QColor(250,250,250))
        text.setFont(font)
 
        text.setGraphicsEffect(shadow)
 
        return view

    def change_volume(self, value):
        """
        The function can change volume for music
        """
        self.player.setVolume(value)

    def PlayMode(self):
        """
        The function help for self.musicslider, change time that play music and so one
        """
        if self.Play_Pause==False:
            self.musicslider.setMinimum(0)
            self.musicslider.setMaximum(self.player.duration())
            self.musicslider.setValue(self.musicslider.value() + 1000)

    def slider_released(self):
        """
        This function released slide for self.musicslider
        """
        self.player.setPosition(self.musicslider.value())
    
    def _download_mus(self):
        """
        When button 'Add functin' will press,
        start this code and open file 'widget_down_files/widget_download.py'
        """
        self._process = QtCore.QProcess(self)
        self._process.start('python', ["widget_down_files/widget_download.py"])
    
    def _registration(self):
        """
        When button 'Registration' will press,
        start this code and open file 'registration/registr.py'
        """
        self._process = QtCore.QProcess(self)
        self._process.start('python', ["registration/registr.py"])

    def _login(self):
        """
        When button 'Login' will press,
        start this code and open file 'login/log.py'
        """
        self._process = QtCore.QProcess(self)
        self._process.start('python', ["login/log.py"])

    def _account_inf(self):
        """
        When button 'Account' will press,
        start this code and open file 'ac_inf/account_information.py'
        """
        self._process = QtCore.QProcess(self)
        self._process.start('python', ["ac_inf/account_information.py"])

    def _doubleclick(self):
        """
        This function released double click on music,
        when on music in playlist will double click, song start
        """
        self.musicslider.setValue(0)
        self.playlist.setCurrentIndex(self.musiclist.currentRow())
        self.player.play()
        self.play_btn.setText('Pause')
 
    def _clear(self):
        """
        The function for clearing the playlist and musiclist
        """
        self.player.stop()
        self.musiclist.clear()
        self.playlist.clear()
        self.play_btn.setText('Play')
        self.status.setText('Status: ')
        pixmap = QPixmap()

    def _files(self):
        """
        The function takes music from database.sqlite and,
        add them to playlist"""
        try:
            for el in Musics.select():
                with open(f'musics/{el.music_name}.mp3', 'wb') as fl:
                    fl.write(el.mp3_file)
                self.playlist.addMedia(QMediaContent(self.url.fromLocalFile(f'musics/{el.music_name}.mp3')))
                self.musiclist.addItem(el.music_name)
        except:
            pass
 
    def _next(self):
        """
        When button 'Next' will press,
        start this code and start to play next music in playlist
        """
        self.musicslider.setValue(0)
        self.playlist.next()
        if self.playlist.currentIndex() == -1:
            self.playlist.setCurrentIndex(0)
            self.player.play()
 
    def _stop(self):
        """
        When button 'Stop' will press,
        start this code and stop the music
        """
        self.Play_Pause=True
        self.player.stop()
        self.play_btn.setText('Play')
        self.playlist.setCurrentIndex(0)
        self.musiclist.setCurrentRow(0)
        self.status.setText('Status: Now Stopped')

    def _state(self):
        """
        This function released button 'Play' and 'Pause'
        when this button.text() == 'Play': song will start play,
        and when this button.text == 'Pause': song will stop

        """
        if self.playlist.mediaCount() > 0:
            if self.player.state() != QMediaPlayer.PlayingState:
                self.Play_Pause=False
                self.play_btn.setText('Pause')
                self.status.setText('Status: Now Playing')
                self.player.play()
            else:
                self.Play_Pause=True
                self.play_btn.setText('Play')
                self.player.pause()
                self.status.setText('Status: Now Paused')
        else:
            pass

    def _exit(self):
        """
        When button 'Stop' clicked, all program will stop"""
        shutil.rmtree('musics', ignore_errors=True)
        sys.exit()

    def update(self):
        """
        The function for updating the listbox when the playlist updates
        """
        self.musiclist.setCurrentRow(self.playlist.currentIndex())
        if self.playlist.currentIndex() < 0:
            self.musiclist.setCurrentRow(0)
            self.playlist.setCurrentIndex(0)
 
def main():
    """
    The function which start all this program
    """
    try:
        os.mkdir('musics')
    except:
        pass
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

main()