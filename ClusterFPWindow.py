from PyQt5.QtWidgets import QMainWindow, QWidget, QComboBox, QVBoxLayout, QSplitter, QPushButton, QShortcut, QAction, QTableWidget, QSizePolicy, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence
from clusterization import clusterization
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class ClusterFPWindow(QMainWindow):
    def __init__(self, fp_window, dictOfFPs):
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

        exit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        exit_shortcut.activated.connect(self.close)

        back_action = QAction('&Назад', self)
        back_action.setShortcut('Ctrl+Z')
        back_action.triggered.connect(self.backToFP)

        help_action = QAction('&Помощь', self)
        help_action.setShortcut('Ctrl+H')
        help_action.triggered.connect(self.showHelp)

        file_menu = self.menuBar()
        file_menu.addAction(back_action)
        file_menu.addAction(help_action)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.dataLayout.addWidget(self.canvas)
        self.enum = ['Non-Penalty Goals', 'Non-Penalty xG', 'Shots Total', 'Assists', 'xAG', 'npxG+xAG', 'Shot-Creating Actions', 'Passes Attempted', 'Pass Completion %', 'Progressive Passes', 'Progressive Carries', 'Successful Take-Ons', 'Touches', 'Progressive Passes Rec', 'Tackles', 'Interceptions', 'Blocks', 'Clearances', 'Aerials won']
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
        self.bestPlayersTable.resizeColumnsToContents()

    def backToFP(self):
        self.close()
        self.FPWindow.show()
    
    def showHelp(self):
        QMessageBox.information(self, "Помощь", """Для возврата на главный экран нажмите кнопку \"Назад\" в меню либо используйте сочетание клавиш \"Ctrl+Z\"

Для выхода из приложения нажмите знак выхода в верхней части приложения либо используйте сочетание клавиш \"Ctrl+Q\"""")