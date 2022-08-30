from threading import Thread

from PyQt6.QtCore import QObject 
from PyQt6.QtWidgets import QMessageBox 

from QHook import QHook
from yt_dlp import YoutubeDL

class QYoutubeDL(QObject):
    def download(self, urls, options):
        Thread(target=self._execute, args=(urls, options), daemon=True).start()

    def _execute(self, urls, options):
        try:
            with YoutubeDL(options) as ydl:
                ydl.download([urls])

            for hook in options.get("progress_hooks", []):
                if isinstance(hook, QHook):
                    hook.deleteLater()

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Щось пішло не так ;)")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()