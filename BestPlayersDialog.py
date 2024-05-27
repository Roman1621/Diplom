from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QWidget, QScrollArea, QPushButton, QLabel, QCheckBox, QSpinBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

class SelectCriterialDialog(QDialog):
    def __init__(self, en, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор критериев")
        self.setGeometry(100, 100, 400, 300)
        scroll = QScrollArea(self)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(scroll)

        self.setStyleSheet("""
            QDialog {
                background-color: #C2E7D9;
                border: 4px solid #26408B;
                border-radius: 10px;
            }
        """)
        widget.setStyleSheet("""
            QWidget {
                background-color: #a6cfd5;
                color: #0D0221;
                font-size: 18px;
                padding: 4px;
            }
        """)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #a6cfd5;
                color: #0D0221;
                font-size: 18px;
                padding: 4px;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #C2E7D9;
                width: 20px;
                margin: 20px 0 20px 0;
            }
            QScrollBar::handle:vertical {
                background-color: #26408B;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                background-color: #C2E7D9;
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background-color: #C2E7D9;
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #a6cfd5;
            }
        """)

        self.numOfBestPlayersLabel = QLabel("Число лучших игроков:", self)
        layout.addWidget(self.numOfBestPlayersLabel)
        self.numOfBestPls = QSpinBox(self)
        self.numOfBestPls.setRange(3,10)
        layout.addWidget(self.numOfBestPls)

        self.checkboxes = []
        self.spinboxes = []
        self.dirCombos = []
        for stat in en:
            cb = QCheckBox(stat, self)
            sb = QSpinBox(self)
            sb.setRange(1, len(en))
            sb.setEnabled(False)
            cb.stateChanged.connect(lambda state, sb=sb: sb.setEnabled(state == Qt.Checked))
            layout.addWidget(cb)
            layout.addWidget(sb)
            self.checkboxes.append(cb)
            self.spinboxes.append(sb)
            dirCmb = QComboBox(self)
            dirCmb.addItems(['По возрастанию', 'По убыванию'])
            layout.addWidget(dirCmb)
            self.dirCombos.append(dirCmb)
        
        selectAllcb = QCheckBox("Выбрать все", self)
        selectAllcb.stateChanged.connect(lambda state: [cb.setChecked(state) for cb in self.checkboxes])
        layout.addWidget(selectAllcb)

        self.btnOk = QPushButton("OK", self)
        self.btnOk.clicked.connect(self.accept)
        layout.addWidget(self.btnOk)

        self.applyStyles()

    def applyStyles(self):
        self.numOfBestPlayersLabel.setStyleSheet("QLabel { color: #0D0221; font-size: 18px; }")
        for cb in self.checkboxes:
            cb.setStyleSheet("QCheckBox { background-color: #a6cfd5; color: #0D0221; font-size: 18px; padding: 4px; }")
        for sb in self.spinboxes:
            sb.setStyleSheet("QSpinBox { background-color: #a6cfd5; color: #0D0221; font-size: 18px; padding: 4px; }")
        for dc in self.dirCombos:
            dc.setStyleSheet("QComboBox { background-color: #a6cfd5; color: #0D0221; font-size: 18px; padding: 4px; }")
        self.btnOk.setStyleSheet("""
            QPushButton {
                background-color: #26408B;
                color: #0D0221;
                font-size: 18px;
                padding: 10px 50px;
                margin-left: auto;
                margin-right: auto;
            }
            QPushButton:hover {
                color: #C2E7D9;
                border: 2px solid #C2E7D9;
                border-radius: 5px;
            }
            QPushButton:pressed {
                color: #C2E7D9;
            }
        """)

    def selected_criteria(self):
        return [(cb.text(), sb.value(), dc.currentText()) for cb, sb, dc in zip(self.checkboxes, self.spinboxes, self.dirCombos) if cb.isChecked()], self.numOfBestPls

class ResultsDialog(QDialog):
    def __init__(self, diction, header_labels, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Результаты анализа")
        self.setGeometry(100, 100, 1000, 300)
        
        layout = QVBoxLayout(self)

        num_stats = len(diction[0]) - 2
        self.resultsTable = QTableWidget(0, num_stats + 1)
        self.resultsTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        
        header_labels = ["Имя игрока"] + header_labels
        self.resultsTable.setHorizontalHeaderLabels(header_labels)
        layout.addWidget(self.resultsTable, 1)

        for data in diction:
            name = data[0]
            stats = data[1:-1]
            row_position = self.resultsTable.rowCount()
            self.resultsTable.insertRow(row_position)
            self.resultsTable.setItem(row_position, 0, QTableWidgetItem(name))
            for i, stat in enumerate(stats):
                self.resultsTable.setItem(row_position, i + 1, QTableWidgetItem(f"{stat:.2f}"))
        self.adjustSize()

        self.setStyleSheet("""
            QDialog {
                background-color: #C2E7D9;
                border: 4px solid #26408B;
                border-radius: 10px;
            }
        """)
        self.resultsTable.setStyleSheet("""
            QTableWidget {
                background-color: #0F084B;
                gridline-color: #26408B;
                font-size: 18px;
            }
            QHeaderView::section {
                background-color: #26408B;
                color: #C2E7D9;
                padding: 4px;
                font-size: 18px;
                font-weight: bold;
            }
            QTableCornerButton::section {
                background-color: #26408B;
            } 
            QTableWidget::item {
                color: #0D0221;
                background-color: #a6cfd5;
            }
            QTableWidget::item:selected {
                background-color: #C2E7D9;
                color: #0D0221;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                border: 1px solid #26408B;
                background: #a6cfd5;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #0D0221;
                min-height: 20px;
                min-width: 20px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: #26408B;
            }
        """)
        self.resultsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        close_button = QPushButton("&Назад", self)
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #26408B;
                color: #0D0221;
                font-size: 18px;
                padding: 10px 50px;
                margin-left: auto;
                margin-right: auto;
            }
            QPushButton:hover {
                color: #C2E7D9;
                border: 2px solid #C2E7D9;
                border-radius: 5px;
            }
            QPushButton:pressed {
                color: #C2E7D9;
            }
        """)
        layout.addWidget(close_button)