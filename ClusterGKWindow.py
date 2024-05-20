from PyQt5.QtWidgets import QMainWindow, QDialog, QComboBox, QWidget, QSplitter, QPushButton, QVBoxLayout, QShortcut, QAction, QTableWidget, QAbstractItemView, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence
from clusterization import clusterization
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from BestPlayersDialog import ResultsDialog, SelectCriterialDialog
import matplotlib.pyplot as plt

class ClusterGKWindow(QMainWindow):
    def __init__(self, gk_window, dictOfGKs, listOfChar):
        super().__init__()
        self.GKWindow = gk_window
        self.dct = dictOfGKs.copy()
        self.setWindowTitle("КтоЗабил. Вратари. Анализ")
        self.setMinimumSize(QSize(700, 700))
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        splitter = QSplitter(Qt.Horizontal, self)
        layout.addWidget(splitter)

        menuWidget = QWidget(splitter)
        dataWidget = QWidget(splitter)
        splitter.addWidget(menuWidget)
        splitter.addWidget(dataWidget)

        menuLayout = QVBoxLayout(menuWidget)
        self.dataLayout = QVBoxLayout(dataWidget)

        self.bestPlayersTable = QTableWidget(0, 2)
        self.bestPlayersTable.setHorizontalHeaderLabels(["Имя игрока", "Значение"])
        menuLayout.addWidget(self.bestPlayersTable)

        exit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        exit_shortcut.activated.connect(self.close)

        back_action = QAction('&Назад', self)
        back_action.setShortcut('Ctrl+Z')
        back_action.triggered.connect(self.backToGK)

        best_action = QAction('&Определить лучших', self)
        best_action.setShortcut('Ctrl+B')
        best_action.triggered.connect(self.getBestGK)

        help_action = QAction('&Помощь', self)
        help_action.setShortcut('Ctrl+H')
        help_action.triggered.connect(self.showHelp)

        file_menu = self.menuBar()
        file_menu.addAction(back_action)
        file_menu.addAction(best_action)
        file_menu.addAction(help_action)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.dataLayout.addWidget(self.canvas)
        if listOfChar is None:
            lengths = []
            for position, players in self.dct.items():
                for name, characteristics in players.items():
                    lengths.append(len(characteristics))

            if lengths:
                average_length = round(sum(lengths) / len(lengths))
            else:
                average_length = 0
            self.enum = ['Characteristic' + str(i + 1) for i in range(average_length)]
        else:
            self.enum = listOfChar
        self.comboBox1 = QComboBox()
        self.comboBox2 = QComboBox()
        self.comboBox1.addItems(self.enum)
        self.comboBox2.addItems(self.enum)
        menuLayout.addWidget(self.comboBox1)
        menuLayout.addWidget(self.comboBox2)

        analyze_button = QPushButton("Анализировать", menuWidget)
        analyze_button.clicked.connect(self.performAnalysis)
        menuLayout.addWidget(analyze_button)
    
    def performAnalysis(self):
        index1 = self.comboBox1.currentIndex()
        index2 = self.comboBox2.currentIndex()
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        labels, centroids, players, origX, origY = clusterization(index1, index2, self.dct, ax, self.enum[index1], self.enum[index2])
        self.canvas.draw()

        if index1 == index2 or not self.enum[index1] == 'Goals Against':
            best_cluster_index = np.argmax(np.mean(centroids, axis=1))
        else:
            best_cluster_index = np.argmax(centroids[:, 0] + centroids[:, 1])
        best_players_indices = np.where(labels == best_cluster_index)[0]
        best_players = [(players[i][1], (origX[i], origY[i])) for i in best_players_indices]

        self.bestPlayersTable.setRowCount(0)
        for player, point in best_players:
            row_position = self.bestPlayersTable.rowCount()
            self.bestPlayersTable.insertRow(row_position)
            self.bestPlayersTable.setItem(row_position, 0, QTableWidgetItem(player))
            self.bestPlayersTable.setItem(row_position, 1, QTableWidgetItem(f"{point[0]:.2f}, {point[1]:.2f}"))
        self.bestPlayersTable.resizeColumnsToContents()
        self.bestPlayersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getBestGK(self):
        if self.enum:
            dialog = SelectCriterialDialog(self.enum, self)
        if dialog.exec_() == QDialog.Accepted:
            selected_stats = dialog.selected_criteria()
            if not selected_stats:
                QMessageBox.warning(self, "Внимание", "Не выбраны критерии для анализа.")
                return

            player_stats = {}
            for position, players in self.dct.items():
                for player_name, stats in players.items():
                    player_stats[player_name] = stats

            player_scores = {}
            for player_name, stats in player_stats.items():
                player_scores[player_name] = [stats[self.enum.index(stat)] for stat, _ in selected_stats]

            best_players = []
            for player_name, stats in player_scores.items():
                score = sum([len(self.enum) - priority + 1 for _, priority in selected_stats]) * sum(stats)
                best_players.append((player_name, *stats, score))

            best_players = sorted(best_players, key=lambda x: x[-1], reverse=True)[:5]
            results_dialog = ResultsDialog(best_players, self)
            results_dialog.exec_()

    def backToGK(self):
        self.close()
        self.GKWindow.show()
    
    def showHelp(self):
        QMessageBox.information(self, "Помощь", """Для возврата на главный экран нажмите кнопку \"Назад\" в меню либо используйте сочетание клавиш \"Ctrl+Z\"

Для выхода из приложения нажмите знак выхода в верхней части приложения либо используйте сочетание клавиш \"Ctrl+Q\"""")