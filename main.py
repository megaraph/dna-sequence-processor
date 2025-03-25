import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from gui import DNAProcessorApp


if __name__ == "__main__":
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    app = QApplication(sys.argv)
    window = DNAProcessorApp()
    window.show()
    sys.exit(app.exec_())
