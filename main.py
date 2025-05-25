import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from db import initialize_database
from app import App

def main():
    app = QApplication(sys.argv)

    if not initialize_database("transaction.db"):
        QMessageBox.critical(None, "Error", "Could not load database")

    window = App()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()