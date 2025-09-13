import sys
import os
import random

import pygame

from PyQt6.QtWidgets import QVBoxLayout, QMainWindow, QLabel, QTableWidgetItem, QDialog, QWidget, QPushButton, QCheckBox
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QPixmap, QMovie, QPainterPath
from playerMP3vtoroiVar_ui import Ui_MainWindow
from viktorina_ui import Ui_Form
from PyQt6.QtCore import QTimer, QSize, QEasingCurve, QPropertyAnimation, QRect

class MusicPlayer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.movie = QMovie("gifVideo/doc_2024-11-02_18-05-16.gif")
        self.label.setMovie(self.movie)
        self.movie.setScaledSize(QtCore.QSize(290, 290))
        self.progresBarTrack.setDisabled(True)
        self.setWindowTitle("Плеер")
        self.one_show = False
        self.ok = False

        self.anmimation = QPropertyAnimation(self.next_button, b"geometry")
        self.anmimation.setDuration(300)
        self.anmimation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        path = QPainterPath()
        radius = 150  
        path.addRoundedRect(0, 0, 290, 290, radius, radius)
        rounded_rect = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.label.setMask(rounded_rect)
        pygame.mixer.init()
        pygame.mixer_music.set_volume(0.5)
        self.verticalSlider.setValue(50)
        self.track_len = 0
        self.slider_pressed = False
        self.current_time = None
        self.music_files = []



        self.second_window = None
        

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)



        self.movie.start()
        self.movie.stop()


        
        
        self.pushButton_loadDir.clicked.connect(self.loadImages)
        self.tableWidget.cellDoubleClicked.connect(self.play_track_double_click)
        self.pause_stop_button.clicked.connect(self.play_stop)
        self.verticalSlider.valueChanged.connect(self.volume_edit)
        self.next_button.clicked.connect(self.next_track)
        self.check_box.stateChanged.connect(self.check_vox_proverka)
        self.prev_button.clicked.connect(self.prev_track)
        self.pushButton_2.clicked.connect(self.vikt)


    def loadImages(self):
        self.musicFolder = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку с песними")
        
        if self.musicFolder:
            files = os.listdir(self.musicFolder)
            self.music_files = [f for f in files if f.endswith(('.mp3', '.wav', '.MP3', '.WAV'))]
            self.cur_index = 0
            if len(self.music_files) > 0:
                self.second_window = MusicViktorina(self.music_files, self.musicFolder)
            print(self.musicFolder)
            
            if self.music_files:
                self.tableWidget.setRowCount(len(self.music_files))
                self.tableWidget.setColumnCount(1)
                self.tableWidget.edit

                self.tableWidget.setHorizontalHeaderLabels(["Track"])
                for row_idx, row_data in enumerate(self.music_files):

                    item = QTableWidgetItem(row_data)
                    item.setBackground(QtGui.QColor("black"))
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                    item.setForeground(QtGui.QColor("White"))
                
                    
                    self.tableWidget.setItem(row_idx, 0, item)

                header = self.tableWidget.horizontalHeader()       
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
            else:
                pass
    


    def play_track_double_click(self, row, column):
        print(self.tableWidget.item(row, column))
        self.name_song = self.tableWidget.item(row, column).text()
        self.cur_index = self.music_files.index(self.tableWidget.item(row, column).text())
        self.file = f"{self.musicFolder}/{self.tableWidget.item(row, column).text()}"
        pygame.mixer.music.load(self.file)
        pygame.mixer.music.play()
        self.track_len = pygame.mixer.Sound(self.file).get_length()
        self.progresBarTrack.setMaximum(int(self.track_len * 1000))
        print(int(self.track_len * 1000))
        self.movie.start()
        self.timer.start(1)


        

    def play_stop(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.movie.setPaused(True)

        else:
            pygame.mixer.music.unpause()
            self.movie.start()

    def next_track(self, state):
        try:

            self.star_animation()

            pygame.mixer_music.stop()
            self.cur_index = (self.cur_index + 1) % len(self.music_files)
            pygame.mixer.music.load(f"{self.musicFolder}/{self.music_files[self.cur_index]}")
            pygame.mixer.music.play()
            self.track_len = pygame.mixer.Sound(f"{self.musicFolder}/{self.music_files[self.cur_index]}").get_length()
            self.progresBarTrack.setMaximum(int(self.track_len * 1000))
            self.timer.start(1)
            self.movie.start()
            self.anmimation.finished.connect(self.restore_button_size())
            
        except AttributeError:
            self.window_show()

    
    def prev_track(self):
        try:
            pygame.mixer_music.stop()
            self.cur_index = (self.cur_index - 1) % len(self.music_files)
            pygame.mixer.music.load(f"{self.musicFolder}/{self.music_files[self.cur_index]}")
            pygame.mixer.music.play() 
            self.track_len = pygame.mixer.Sound(f"{self.musicFolder}/{self.music_files[self.cur_index]}").get_length()
            self.progresBarTrack.setMaximum(int(self.track_len * 1000))   
            self.timer.start(1)
        except AttributeError:
            self.window_show()
   
    def volume_edit(self, event):
        pygame.mixer_music.set_volume(event / 100)
    
    def window_show(self):
        
        self.w = QDialog()
        self.label_wind = QLabel()
        self.label_wind.setText("Выберите сначала папку с песнями!")
        self.layout = QVBoxLayout(self.w)
        self.layout.addWidget(self.label_wind)
        self.w.setFixedSize(QSize(220, 150))
        self.w.setWindowTitle("Ошибка")

        self.w.exec()
    
    def check_vox_proverka(self, state):
        print(state, QtCore.Qt.CheckState.Checked)
        
        if state == 2:
            self.ok = True
            if self.one_show == False:
                self.w = QDialog()
                self.label_wind = QLabel()
                self.label_wind.setText("Вы включили автовоспроизведение")
                self.layout = QVBoxLayout(self.w)
                self.layout.addWidget(self.label_wind)
                self.w.setFixedSize(QSize(220, 150))
                self.w.setWindowTitle("Ошибка")
                self.one_show = True

                self.w.exec()
        else:
            self.ok = False
     
    
    def update_progress(self):
        self.current_time = pygame.mixer_music.get_pos()
        
        
        if self.current_time == -1 and self.ok:
            self.cur_index = (self.cur_index + 1) % len(self.music_files)
            pygame.mixer.music.load(f"{self.musicFolder}/{self.music_files[self.cur_index]}")
            pygame.mixer_music.play()
            self.track_len = pygame.mixer.Sound(f"{self.musicFolder}/{self.music_files[self.cur_index]}").get_length()
            self.progresBarTrack.setMaximum(int(self.track_len * 1000))
        print(self.current_time)
 
        self.progresBarTrack.setValue(self.current_time)


        elapsed_time = self.format_time(self.current_time // 1000)
        total_time = self.format_time(int(self.track_len))
        self.time.setText(f"{elapsed_time} / {total_time}")
        self.time.setStyleSheet("color: white; border: none; background: none;")

    def vikt(self):
        
        if not self.second_window: 
            try:
                self.second_window = MusicViktorina()
            except TypeError:
                self.window_show()
                return
        self.ok = False
        self.check_box.setChecked(False)
        pygame.mixer_music.stop()
        self.second_window.show()
        
        







    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02}"
    
    def resume_timer(self):

        self.slider_pressed = False  
        self.timer.start()
    
    def star_animation(self):
        start_rect = self.next_button.geometry()
        end_rect = QRect(start_rect.x(), start_rect.y(), start_rect.width() + 10, start_rect.height() + 10)
        self.anmimation.setStartValue(start_rect)
        self.anmimation.setEndValue(end_rect)
        self.anmimation.start()
    
    def restore_button_size(self):
        start_rect = self.next_button.geometry()
        end_rect = QRect(start_rect.x(), start_rect.y(), start_rect.width() - 10, start_rect.height() - 10)
        self.anmimation.setStartValue(start_rect)
        self.anmimation.setEndValue(end_rect)
        self.anmimation.start()

class MusicViktorina(QWidget):
    def __init__(self, music, MusicFolder):
        super().__init__()
        self.ui = Ui_Form()  
        self.ui.setupUi(self)
        self.ui.pushButton.setMaximumWidth(300)

        self.music_files = music
        self.music_folder = MusicFolder
        print(self.music_files)
        self.setFixedWidth(450)
        self.count = 0
        self.count_best = 0
        



        
        self.tek_trek = None
        self.options = []

        self.timer_event = QTimer(self)
        self.timer_event.timeout.connect(self.end)

        self.buttons = []
        self.ui.pushButton.clicked.connect(self.start)
        
    
    def start(self):
        self.tek_trek = random.choice(self.music_files)
        print(self.music_files)
        print(self.tek_trek)

        self.options = random.sample(self.music_files, len(self.music_files))

        if self.tek_trek not in self.options:
            return
        
        pygame.mixer_music.load(f"{self.music_folder}/{self.tek_trek}")
        print(f"{self.music_folder}/{self.tek_trek}")
        pygame.mixer_music.play()
        len_trek = pygame.mixer.Sound(f"{self.music_folder}/{self.tek_trek}").get_length()
        if  len_trek >= 100:
            pygame.mixer_music.set_pos(100)
        else:
            pygame.mixer_music.set_pos(len_trek // 2)

        self.buttons_options()

        self.timer_event.start(10000)
    
    def buttons_options(self):
        for button in self.buttons:
            button.deleteLater()
        self.buttons = []
        self.ui.pushButton.setText("Следующий")
        self.ui.label.hide()


        for option in self.options:
            button = QPushButton(option.split('.')[0])  
            button.clicked.connect(lambda checked, opt=option: self.check_answer(opt))
            self.ui.gridLayout.addWidget(button)
            button.setStyleSheet("""
    QPushButton {
        color: black;
        border: 1px solid white; 
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 5px;
        height: 30px;
        font-size: 15px;
    }
    QPushButton:hover {
        background-color: rgba(100, 30, 0, 1); 
        color: orange; 
    }
    QPushButton:pressed {
        background-color: rgba(255, 255, 255, 0.8);
    }
""")
            button.setMaximumWidth(350)
            self.buttons.append(button)
    

    def check_answer(self, opt):
        
        if opt == self.tek_trek:
            self.count += 1
            if self.count > self.count_best:
                self.count_best = self.count
            
            self.start()
        else:
            for but in self.buttons:
                but.hide()
            self.ui.pushButton.setText("Заново")
            self.ui.label.show()
            self.ui.label.setText(f"Вы проиграли!\nПравильный ответ:\n{self.tek_trek}\nВаш наилучший счет: {self.count_best}\n Ваш текущий счет: {self.count}")
            self.ui.label.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); color: black; font-size: 18px; border: 1px solid white; border-radius: 5px;")
            self.ui.label.setContentsMargins(10, 20, 10, 20)
            self.ui.label.adjustSize()
            self.count = 0
            self.timer_event.stop()
            pygame.mixer_music.stop()
    
    def end(self):
        for but in self.buttons:
            but.hide()
        self.ui.pushButton.setText("Заново")
        self.ui.label.show()
        self.ui.label.setText(f"Истекло время!\nПравильный ответ:\n{self.tek_trek}\nВаш наилучший счет: {self.count_best}\n Ваш текущий счет: {self.count}")
        self.ui.label.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); color: black; font-size: 18px; border: 1px solid white; border-radius: 5px;")
        self.ui.label.setContentsMargins(10, 20, 10, 20)
        self.ui.label.adjustSize()
        self.count = 0
        self.timer_event.stop()
        pygame.mixer_music.stop()

        
    



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MusicPlayer()
    ex.show()
    sys.exit(app.exec())