from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QScrollArea, QPushButton, QCheckBox, QSpinBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class SelectCriterialDialog(QDialog):
    def __init__(self, en, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор критериев")
        scroll = QScrollArea(self)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(scroll)
        
        self.checkboxes = []
        self.spinboxes = []
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
        
        self.btnOk = QPushButton("OK", self)
        self.btnOk.clicked.connect(self.accept)
        layout.addWidget(self.btnOk)

    def selected_criteria(self):
        return [(cb.text(), sb.value()) for cb, sb in zip(self.checkboxes, self.spinboxes) if cb.isChecked()]

class ResultsDialog(QDialog):
    def __init__(self, diction, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Результаты анализа")
        self.setGeometry(100, 100, 400, 600)
        
        layout = QVBoxLayout(self)

        num_stats = len(diction[0]) - 1  # Определяем количество статистических характеристик

        self.resultsTable = QTableWidget(0, num_stats + 1)
        header_labels = ["Имя игрока"] + [f"Характеристика {i+1}" for i in range(num_stats)]
        self.resultsTable.setHorizontalHeaderLabels(header_labels)
        layout.addWidget(self.resultsTable)

        for player, *stats in diction:
            row_position = self.resultsTable.rowCount()
            self.resultsTable.insertRow(row_position)
            self.resultsTable.setItem(row_position, 0, QTableWidgetItem(player))
            for i, stat in enumerate(stats):
                self.resultsTable.setItem(row_position, i + 1, QTableWidgetItem(f"{stat:.2f}"))

        self.resultsTable.resizeColumnsToContents()
        close_button = QPushButton("&Назад", self)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)