from PyQt6.QtCore import QObject, pyqtSignal

class QHook(QObject):
    infoChanged = pyqtSignal(dict)

    def __call__(self, d):
        self.infoChanged.emit(d.copy())