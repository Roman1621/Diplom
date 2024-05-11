from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QCheckBox

class SelectCriterialDialog(QDialog):
     def __init__(self, en, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор критериев")
        layout = QVBoxLayout(self)
        
        self.checkboxes = []
        for stat in en:
            cb = QCheckBox(stat, self)
            layout.addWidget(cb)
            self.checkboxes.append(cb)
        
        self.btnOk = QPushButton("OK", self)
        self.btnOk.clicked.connect(self.accept)
        layout.addWidget(self.btnOk)

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

sort_direction = {
    'Goals Against': False,
    'Avg. Length of Goal Kicks': False
}

def get_sort_direction(criteria):
    return sort_direction.get(criteria, True)

def sort_and_rank(data, criteria, ascending=True):
    sorted_data = sorted(data.items(), key=lambda x: x[1][criteria], reverse=not ascending)
    ranks = {name: rank for rank, (name, _) in enumerate(sorted_data, start=1)}
    return ranks

def calculate_scores(data, selected_criteria):
    scores = {name: 0 for name in data}
    for priority, criteria in enumerate(selected_criteria, start=1):
        ascending = get_sort_direction(criteria)
        ranks = sort_and_rank(data, criteria, ascending)
        for name in scores:
            scores[name] += ranks[name] * priority
    return scores