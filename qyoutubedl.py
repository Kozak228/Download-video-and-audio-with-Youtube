from threading import Thread
from PyQt6.QtCore import QObject, pyqtSignal 
from PyQt6.QtWidgets import QMessageBox 

from yt_dlp import YoutubeDL

class QHook(QObject):
    infoChanged = pyqtSignal(dict)

    def __call__(self, d):
        self.infoChanged.emit(d.copy())

class QYoutubeDL(QObject):
    def download(self, urls, options):
        Thread(target=self._execute, args=(urls, options), daemon=True).start()

    def _execute(self, urls, options):
        try:
            with YoutubeDL(options) as ydl:
                ydl.download([urls])
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Щось пішло не так ;)")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

        for hook in options.get("progress_hooks", []):
            if isinstance(hook, QHook):
                hook.deleteLater()