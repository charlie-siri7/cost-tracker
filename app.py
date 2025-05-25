# import widgets
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView

from PyQt6.QtCore import QDate, Qt
from db import get_cost, add_cost, delete_cost
from PyQt6.QtGui import QFont

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initialize_UI()
        self.load_data()
        self.previous_cell = None
        self.previous_cell = None
        self.previous_row_header = None
        self.previous_col_header = None
    def settings(self):
        # x/y/width/height of window
        self.setGeometry(340, 120, 600, 480)
        # Title
        self.setWindowTitle("Cost Tracker")
    def initialize_UI(self):
        # date box with current date
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        # Dropdown for type of expense (category)
        self.dropdown = QComboBox()
        # Amount spent
        self.amount = QLineEdit()
        # Description of what money is spent on
        self.description = QLineEdit()
        # buttons to add/delete transactions
        self.add_button = QPushButton("Add Transaction")
        self.add_button.setObjectName("add_button")
        self.delete_button = QPushButton("Delete Transaction")
        self.delete_button.setObjectName("delete_button")

        self.table = QTableWidget(0, 5)
        # params for each transaction
        self.table.setHorizontalHeaderLabels(["id", "Date", "Category", "Amount", "Description"])
        # Make columns stretch with table
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Call method when cell is clicked
        self.table.cellClicked.connect(self.handle_cell_click)

        self.fill_dropdown()

        self.add_button.clicked.connect(self.add_cost)
        self.delete_button.clicked.connect(self.delete_cost)

        self.style()

        self.layout_setup()

        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

    def layout_setup(self):
        main = QVBoxLayout()
        row_1 = QHBoxLayout()
        row_2 = QHBoxLayout()
        row_3 = QHBoxLayout()

        row_1.addWidget(QLabel("Date"))
        row_1.addWidget(self.date)
        row_1.addWidget(QLabel("Category"))
        row_1.addWidget(self.dropdown)

        row_2.addWidget(QLabel("Amount"))
        row_2.addWidget(self.amount)
        row_2.addWidget(QLabel("Description"))
        row_2.addWidget(self.description)
        
        row_3.addWidget(self.add_button)
        row_3.addWidget(self.delete_button)

        main.addLayout(row_1)
        main.addLayout(row_2)
        main.addLayout(row_3)
        main.addWidget(self.table)

        self.setLayout(main)

    def style(self):
        
        self.setStyleSheet("""
                            QWidget {
                                background-color: #f0f0f0;
                                font-family: Arial, sans-serif;
                                font-size: 14px;
                                color: #333333;
                            }
                           
                            QLabel {
                                font-size: 16px;
                                color: #303050;
                                font-weight: bold;
                                padding: 5px;
                            }
                           
                            QLineEdit, QComboBox, QDateEdit {
                                background-color: #ffffff;
                                color: #333333;
                            }
                           
                            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
                                background-color: #f0f0f0;
                            }
                           
                            QTableWidget {
                                background-color: white;
                                gridline-color: #c0d0d0;
                                selection-background-color: green;
                                selection-color: white;
                                font-size: 14px;
                                border: 1px solid #d0e0e0;
                            }
                           
                            #add_button {
                                background-color: #50b050;
                                color: white;
                                padding: 10px 15px;
                                border-radius: 5px;
                                font-size: 14px;
                                font-weight: bold;
                            }
                           
                            #add_button:hover {
                                background-color: #48a048;
                            }
                           
                            #add_button:pressed {
                                background-color: #409040;
                            }
                           
                            #delete_button {
                                background-color: #b05050;
                                color: white;
                                padding: 10px 15px;
                                border-radius: 5px;
                                font-size: 14px;
                                font-weight: bold;
                            }
                           
                            #delete_button:hover {
                                background-color: #a04848;
                            }
                           
                            #delete_button:pressed {
                                background-color: #904040;
                            }
                           """)
        
    def handle_cell_click(self, row, column):
        # Reset previous cell style
        if self.previous_cell:
            prev_row, prev_col = self.previous_cell
            prev_item = self.table.item(prev_row, prev_col)
            if prev_item:
                prev_item.setBackground(Qt.GlobalColor.white)
                prev_item.setForeground(Qt.GlobalColor.black)

        # Reset previous header fonts
        if self.previous_row_header is not None:
            font = self.table.verticalHeaderItem(self.previous_row_header).font()
            font.setWeight(QFont.Weight.Normal)
            self.table.verticalHeaderItem(self.previous_row_header).setFont(font)

        if self.previous_col_header is not None:
            font = self.table.horizontalHeaderItem(self.previous_col_header).font()
            font.setWeight(QFont.Weight.Normal)
            self.table.horizontalHeaderItem(self.previous_col_header).setFont(font)

        # Set new cell style
        item = self.table.item(row, column)
        if item:
            item.setBackground(Qt.GlobalColor.darkGray)
            item.setForeground(Qt.GlobalColor.white)

        # Bold new row header
        if self.table.verticalHeaderItem(row):
            font = self.table.verticalHeaderItem(row).font()
            font.setWeight(QFont.Weight.Bold)
            self.table.verticalHeaderItem(row).setFont(font)
            self.previous_row_header = row

        # Bold new column header
        if self.table.horizontalHeaderItem(column):
            font = self.table.horizontalHeaderItem(column).font()
            font.setWeight(QFont.Weight.Bold)
            self.table.horizontalHeaderItem(column).setFont(font)
            self.previous_col_header = column

        # Save current cell
        self.previous_cell = (row, column)

    def fill_dropdown(self):
        categories = ["Rent", "Food", "Transportation", "Utilities", "Subscriptions", "Personal", "Savings/Investments", "Debt/Loans", "Healthcare", "Miscellaneous"]
        self.dropdown.addItems(categories)

    def load_data(self):
        costs = get_cost()
        self.table.setRowCount(0)
        for row_index, cost in enumerate(costs):
            self.table.insertRow(row_index)
            for column_index, data in enumerate(cost):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
        for i in range(self.table.rowCount()):
            self.table.setVerticalHeaderItem(i, QTableWidgetItem(str(i)))

    def clear_inputs(self):
        self.date.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_cost(self):
        # Get each parameter of the new cost from user
        date = self.date.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self, "Error", "Amount and Description can't be empty")
            return
        
        if add_cost(date, category, amount, description):
            self.load_data()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to add cost")
        
    def delete_cost(self):
        row = self.table.currentRow()
        if row == -1: # Row not selected
            QMessageBox.warning(self, "Warning", "You must choose a row to delete")
            return

        cost_id = int(self.table.item(row, 0).text())
        confirm_popup = QMessageBox.question(self, "Confirm", "Are you sure you want to delete?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Yes)
        if confirm_popup == QMessageBox.StandardButton.Yes and delete_cost(cost_id):
            self.load_data()

