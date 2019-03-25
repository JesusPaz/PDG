# basado en https://recursospython.com/codigos-de-fuente/reproductor-de-video-pyqt-4/

from tkinter import *
from PyQt5.QtCore import QEvent, QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QWidget, QPushButton, QSlider,
                             QVBoxLayout)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget



SONG_PATH = "../Music/gilberto-santa-rosa-conteo-regresivo.mp3"

class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()

        # Controles principales para organizar la ventana.
        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()

        # Control de reproducción de video de Qt.
        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer()
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(SONG_PATH)))
        self.media_player.setVideoOutput(self.video_widget)

        # Botones de reproducción y pausa.
        self.play_button = QPushButton("Pausa", self)
        self.stop_button = QPushButton("Detener", self)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())