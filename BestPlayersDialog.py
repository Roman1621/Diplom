from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QCheckBox, QSpinBox
from PyQt5.QtCore import Qt

class SelectCriterialDialog(QDialog):
    def __init__(self, en, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор критериев")
        layout = QVBoxLayout(self)
        
        self.checkboxes = []
        self.spinboxes = []
        for stat in en:
            cb = QCheckBox(stat, self)
            sb = QSpinBox(self)
            sb.setRange(1, len(en))  # Приоритеты от 1 до количества показателей
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

        for player, score in diction:
            layout.addWidget(QLabel(f"{player}: {score:.2f}"))

        close_button = QPushButton("&Назад", self)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

    def set_results(self, results):
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.deleteLater()
        for player, score in results:
            self.layout().insertWidget(self.layout().count() - 1, QLabel(f"{player}: {score:.2f}"))