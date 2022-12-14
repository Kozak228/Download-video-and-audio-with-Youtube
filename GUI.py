from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QFileDialog
from PyQt6.QtCore import QTimer

from validators import url
from hurry.filesize import size 
from yt_dlp import YoutubeDL

from donload_y_GUI import Ui_MainWindow
from qyoutubedl import QYoutubeDL
from QHook import QHook
from Proverka import proverka_path
from Duration_in_file import duration_in_file

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_download.setEnabled(False)
        self.ui.pushButton_info_in_file.setEnabled(False)

        self.ui.pushButton_exit.clicked.connect(QApplication.instance().quit)
        self.ui.pushButton_FAQ_link.clicked.connect(self.vvod_FAQ_link)
        self.ui.pushButton_FAQ_put.clicked.connect(self.vvod_FAQ_put)
        self.ui.lineEdit_link.textChanged.connect(lambda text: self.ui.pushButton_info_in_file.setEnabled(bool(text)))
        self.ui.lineEdit_link.textChanged.connect(lambda text: self.ui.pushButton_download.setEnabled(bool(text)))
        self.ui.pushButton_download.clicked.connect(self.download)
        self.ui.pushButton_info_in_file.clicked.connect(self.info_file)
        self.ui.pushButton_path_folder.clicked.connect(self.path_folder)

        self.ui.radioButton.toggled.connect(lambda: self.btn_state(self.ui.radioButton))
        self.ui.radioButton_2.toggled.connect(lambda: self.btn_state(self.ui.radioButton_2))

        self.downloads = QYoutubeDL()

    def info_file(self):
        link = self.ui.lineEdit_link.text()
        yt_opts = {'format' : 'mp4/bestaudio/best'}

        if url(link):
            try:
                with YoutubeDL(yt_opts) as ydl:
                    info_file = ydl.extract_info(link, download=False)
            except:
                pass

            self.duration = info_file.get("duration", 0)

            self.ui.label_title.setText(info_file.get("title", "Інформації немає"))
            self.ui.label_time.setText(duration_in_file(self.duration) if self.duration > 0 else 0)

        else:
            self.msg("Error", "Перевір посилання!")
            self.ui.lineEdit_link.setText("")

    def download(self):
        link = self.ui.lineEdit_link.text()
        link_PC = self.ui.lineEdit_put.text()

        if url(link):
            link_bool = True
        else:
            link_bool = False
            self.msg("Error", "Перевір посилання!")
            self.ui.lineEdit_link.setText("")

        if self.ui.radioButton.isChecked():
            self.link_PC = proverka_path(link_PC, True)

        if self.ui.radioButton_2.isChecked():
            self.link_PC = proverka_path(link_PC, False)

        if link_bool:
            if self.ui.radioButton.isChecked():
                qhook = QHook()
                
                options = {
                'format':'mp4/best',
                "noplaylist": True,
                "noprogress": True,
                "progress_hooks": [qhook]}

            if self.ui.radioButton_2.isChecked():
                qhook = QHook()

                options = {
                'format' : 'mp4/bestaudio/best',
                'postprocessors' : [{
                'key' : 'FFmpegExtractAudio',
                'preferredcodec' : 'mp3',
                'preferredquality' : '192',
                }],
                "progress_hooks": [qhook]}

            self.downloads.download(link, options)
            qhook.infoChanged.connect(self.handle_info_changed)
            self.ui.progressBar.setValue(0)

    def handle_info_changed(self, d):
        if d['status'] == 'downloading':
            self.ui.label_progress_2.setText('Downloading...')
            self.ui.label_progress_2.setStyleSheet("color: #8B0000;")
            total = d["total_bytes"]
            downloaded = d["downloaded_bytes"]
            self.ui.label_progress.setText(f"{size(downloaded)} of {size(total)}")
            self.ui.progressBar.setMaximum(total)
            self.ui.progressBar.setValue(downloaded)
            
            if 0 <= (downloaded / total) * 100 <= 50:
                self.ui.progressBar.setStyleSheet("#progressBar:chunk {background-color: #8B0000; color: yellow;}")
            if 50 < (downloaded / total) * 100 <= 100:
                self.ui.progressBar.setStyleSheet("#progressBar:chunk {background-color: #006400; color: yellow;}")


        if d['status'] == 'finished':
            if self.ui.radioButton.isChecked():
                self.ui.label_progress_2.setText("Sucsess!")
                self.ui.label_progress_2.setStyleSheet("color: #00008B;")
        
                self.msg("Information", f"Відео завантажено!\nШукай тут: {self.link_PC[:-1]}")

            if self.ui.radioButton_2.isChecked():
                try:
                    if 0 < self.duration <= 450:
                        self.value = 18   
                    elif 450 < self.duration <= 850:
                        self.value = 25
                    else:
                        self.value = 30

                    self.ui.label_progress_2.setStyleSheet("color: #00008B;")
                    self.tick_timer()
                except:
                    self.msg("Error", "Помилка встановить 'FFmpeg'")

    def tick_timer(self):
        if self.value >= 0:
            self.ui.label_progress_2.setText(f"Now converting from mp4 to mp3, please wait {self.value} sec...")
            # Засекаем таймер - значение в милисекундах
            # метод singleShot создает поток в фоне, отменить его нельзя
            QTimer().singleShot(1000, self.tick_timer)
            self.value -= 1
        else:
            self.ui.label_progress_2.setText("Sucsess!")
            self.msg("Information", f"Аудіо завантажено!\nШукай тут: {self.link_PC[:-1]}")

    def btn_state(self, b):
        if b.isChecked() and b.objectName() == "radioButton":
            self.ui.label_progress.setText("")
            self.ui.label_progress_2.setText("")
            self.ui.progressBar.setValue(0)

        if b.isChecked() and b.objectName() == "radioButton_2":
            self.ui.label_progress.setText("")
            self.ui.label_progress_2.setText("")
            self.ui.progressBar.setValue(0)

    def path_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select a folder")
        path = path.replace("/", "\\")
        self.ui.lineEdit_put.setText(path)

    def vvod_FAQ_put(self):
        self.msg("Information", "Встав шлях до папки, куди завантажити відео, або залиште порожнім, відео завантажується до додатку.\nЩе можливо вибір папки, натиснувши на кнопку з назвою '...'.")

    def vvod_FAQ_link(self):
        self.msg("Information", "Встав посилання на відео з адресного рядка браузера.")

    def msg(self, reson, message):
        msg = QMessageBox()
        if reson == "Error": 
            msg.setWindowTitle(reson)
            msg.setText(message)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

        if reson == "Information":
            msg.setWindowTitle(reson)
            msg.setText(message)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()