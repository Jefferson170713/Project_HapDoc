import sys
from itertools import permutations
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

class HapDoc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HapDoc")
        self.setGeometry(100, 100, 600, 300)
        self.setWindowIcon(QIcon("./ARQUIVOS/logo/logo.ico"))

def main():
    app = QApplication(sys.argv)
    window = HapDoc()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
        