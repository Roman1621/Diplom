from PyQt5.QtWidgets import QMainWindow, QWidget, QSpinBox, QComboBox, QDialog, QVBoxLayout, QSplitter, QPushButton, QShortcut, QAction, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtWidgets

from clusterization import clusterization
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from BestPlayersDialog import SelectCriterialDialog, ResultsDialog

class ClusterFPWindow(QMainWindow):
    def __init__(self, fp_window, dictOfFPs, listOfChar):
        super().__init__()
        self.FPWindow = fp_window
        self.dct = dictOfFPs.copy()
        self.setWindowTitle("КтоЗабил. Полевые игроки. Анализ")
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
        self.bestPlayersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.bestPlayersTable.setStyleSheet("""
            QTableWidget {
                background-color: #0F084B;
                gridline-color: #26408B;
                font-size: 18px;
            }
            QHeaderView::section {
                background-color: #a6cfd5;
                color: #0D0221;
                padding: 4px;
                font-size: 18px;
                font-weight: bold;
            }
            QTableCornerButton::section {
                background-color: #a6cfd5;
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
        self.setStyleSheet("""
            ClusterFPWindow {
                background-color: #C2E7D9;
                border: 4px solid #26408B;
                border-radius: 10px;
            }
        """)

        exit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        exit_shortcut.activated.connect(self.close)

        back_action = QAction('&Назад', self)
        back_action.setShortcut('Ctrl+Z')
        back_action.triggered.connect(self.backToFP)

        best_action = QAction('&Определить лучших', self)
        best_action.setShortcut('Ctrl+B')
        best_action.triggered.connect(self.getBestFP)

        help_action = QAction('&Помощь', self)
        help_action.setShortcut('Ctrl+H')
        help_action.triggered.connect(self.showHelp)

        file_menu = self.menuBar()
        file_menu.addAction(back_action)
        file_menu.addAction(best_action)
        file_menu.addAction(help_action)
        
        file_menu.setStyleSheet("""
            QMenuBar {
                background-color: #26408B;
                color: #0D0221;
                font-size: 18px;
                font-family: Montserrat;
                font-style: Italic;
                padding: 4px 4px;
            }
            QMenuBar::item {
                background: transparent;
            }
            QMenuBar::item:selected { 
                color: #C2E7D9;
                background-color: transparent;
                border: 2px solid #C2E7D9;
                border-radius: 5px;
            }
        """)

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
        self.dirs = ['По возрастанию', 'По убыванию']

        self.numOfClusters = QSpinBox()
        self.numOfClusters.setRange(3,10)

        self.comboBox1 = QComboBox()
        self.comboBox2 = QComboBox()
        self.comboBox1.addItems(self.enum)
        self.comboBox2.addItems(self.enum)
        
        self.dirBox1 = QComboBox()
        self.dirBox2 = QComboBox()
        self.dirBox1.addItems(self.dirs)
        self.dirBox2.addItems(self.dirs)

        menuLayout.addWidget(self.numOfClusters)
        menuLayout.addWidget(self.comboBox1)
        menuLayout.addWidget(self.dirBox1)
        menuLayout.addWidget(self.comboBox2)
        menuLayout.addWidget(self.dirBox2)

        self.numOfClusters.setStyleSheet("""
            QSpinBox {
                background-color: #a6cfd5;
                color: #0D0221;
                font-size: 18px;
                padding: 4px;
            }
        """)

        self.comboBox1.setStyleSheet("""
            QComboBox {
                background-color: #a6cfd5;
                color: #0D0221;
                font-size: 18px;
                padding: 4px;
            }
        """)

        self.comboBox2.setStyleSheet("""
            QComboBox {
                background-color: #a6cfd5;
                color: #0D0221;
                font-size: 18px;
                padding: 4px;
            }
        """)

        self.dirBox1.setStyleSheet("""
            QComboBox {
                background-color: #a6cfd5;
                color: #0D0221;
                font-size: 18px;
                padding: 4px;
            }
        """)

        self.dirBox2.setStyleSheet("""
            QComboBox {
                background-color: #a6cfd5;
                color: #0D0221;
                font-size: 18px;
                padding: 4px;
            }
        """)

        analyze_button = QPushButton("Анализировать", menuWidget)
        analyze_button.clicked.connect(self.performAnalysis)
        menuLayout.addWidget(analyze_button)
        analyze_button.setStyleSheet("""
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
    
    def performAnalysis(self):
        index1 = self.comboBox1.currentIndex()
        direction1 = self.dirBox1.currentText()
        index2 = self.comboBox2.currentIndex()
        direction2 = self.dirBox2.currentText()
        number = self.numOfClusters.value()
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        labels, centroids, players, origX, origY = clusterization(index1, index2, self.dct, ax, self.enum[index1], self.enum[index2], direction1, direction2, number)
        self.canvas.draw()

        if index1 == index2:
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
        self.bestPlayersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def getBestFP(self):
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
                score = 0
                selStats = []
                for stat, priority, direction in selected_stats:
                    index = self.enum.index(stat)
                    value = stats[index]
                    if direction == "По убыванию":
                        value = -value
                    score += value * priority
                    selStats.append(stats[index])
                player_scores[player_name] = (selStats, score)

            best_players = sorted(player_scores.items(), key=lambda x: x[1][1], reverse=True)[:5]
            results_dialog = ResultsDialog([(name, *data[0], data[1]) for name, data in best_players], self.enum, self)
            results_dialog.exec_()
    
    def backToFP(self):
        self.close()
        self.FPWindow.show()
    
    def showHelp(self):
        QMessageBox.information(self, "Помощь", """Для возврата на главный экран нажмите кнопку \"Назад\" в меню либо используйте сочетание клавиш \"Ctrl+Z\"

Для выхода из приложения нажмите знак выхода в верхней части приложения либо используйте сочетание клавиш \"Ctrl+Q\"""")