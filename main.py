from PyQt6.QtWidgets import QApplication
from GUI import MainWindow
from sys import exit, argv

def main():
    app = QApplication(argv)
    appl = MainWindow()
    appl.show()

    try:
        exit(app.exec())
    except:
        pass

if __name__ == '__main__':
    main()