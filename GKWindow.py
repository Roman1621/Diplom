from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QShortcut, QAction, QTableWidget, QSizePolicy, QTableWidgetItem, QMessageBox, QAbstractItemView
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence

from ClusterGKWindow import ClusterGKWindow
from BestPlayersDialog import ResultsDialog, SelectCriterialDialog, calculate_scores

class GoalkeepersWindow(QMainWindow):
    def __init__(self, main_window, dictOfGKs):
        super().__init__()
        self.mainWindow = main_window
        self.setWindowTitle("КтоЗабил. Вратари")
        self.setMinimumSize(QSize(1300, 960))
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        exit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        exit_shortcut.activated.connect(self.close)

        back_action = QAction('&Назад', self)
        back_action.setShortcut('Ctrl+Z')
        back_action.triggered.connect(self.backToMain)

        sorting_action = QAction('&Включить/Отключить сортировку', self)
        sorting_action.setShortcut('Ctrl+S')
        sorting_action.triggered.connect(self.toggleSorting)

        clusterization_action = QAction('&Анализ данных', self)
        clusterization_action.setShortcut('Ctrl+A')
        clusterization_action.triggered.connect(self.openClusterGKWindow)

        best_action = QAction('&Определить лучших', self)
        best_action.setShortcut('Ctrl+B')
        best_action.triggered.connect(self.showResults)

        help_action = QAction('&Помощь', self)
        help_action.setShortcut('Ctrl+H')
        help_action.triggered.connect(self.showHelp)

        file_menu = self.menuBar()
        file_menu.addAction(back_action)
        file_menu.addAction(sorting_action)
        file_menu.addAction(clusterization_action)
        file_menu.addAction(best_action)
        file_menu.addAction(help_action)

        self.dct = dictOfGKs
        self.GKtable = QTableWidget(self)
        self.populateTable()
        self.enum = ['PSxG-GA', 'Goals Against', 'Save Percentage', 'PSxG/SoT', 'Save%', 'Clean Sheet Percentage', 'Touches', 'Launch %', 'Goal Kicks', 'Avg. Length of Goal Kicks', 'Crosses Stopped %', 'Def. Actions Outside Pen. Area', 'Avg. Distance of Def. Actions']
    
    def populateTable(self):
        self.GKtable.setColumnCount(14)
        rowsCount = 0
        for cur in self.dct.values():
            rowsCount += len(cur)
        self.GKtable.setRowCount(rowsCount)

        self.GKtable.setHorizontalHeaderLabels(['Name', 'PSxG-GA', 'Goals\nAgainst', 'Save\nPercentage', 'PSxG/SoT', 'Save%', 'Clean\nSheet\nPercentage', 'Touches', 'Launch %', 'Goal\nKicks', 'Avg. Length\nof\nGoal Kicks', 'Crosses\nStopped %', 'Def. Actions\nOutside\nPen. Area', 'Avg. Distance\nof\nDef. Actions'])
        self.GKtable.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(5).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(6).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(7).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(8).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(9).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(10).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(11).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(12).setTextAlignment(Qt.AlignHCenter)
        self.GKtable.horizontalHeaderItem(13).setTextAlignment(Qt.AlignHCenter)

        row = 0
        for players in self.dct.values():
            for player, charac in players.items():
                for col in range(14):
                    item = QTableWidgetItem()
                    if col == 0:
                        item.setData(Qt.DisplayRole, player)
                    else:
                        item.setData(Qt.DisplayRole, float(charac[col-1]))
                    self.GKtable.setItem(row, col, item)
                row += 1
        self.GKtable.resizeColumnsToContents()
        self.GKtable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.GKtable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.centralWidget().layout().addWidget(self.GKtable)

    def toggleSorting(self):
        cur = self.GKtable.isSortingEnabled()
        self.GKtable.setSortingEnabled(not cur)
        if not cur:
            pass
        else:
            self.GKtable.clearContents()
            self.populateTable()
        
    def showResults(self):
        criterial = SelectCriterialDialog(self.enum, self)
        '''if criterial.exec_():
            print(criterial)
            selected = [cb.text() for cb in criterial.checkboxes if cb.isChecked()]
            scores = calculate_scores(self.dct, selected)
            results = sorted(scores.items, key=lambda x: x[1], reverse=True)
            res = ResultsDialog(results, self)
            res.exec_()
        else:
            QMessageBox.information(self, "Предупреждение: не выбраны ключевые показатели", "Невозможно определить лучших")
    '''
    def backToMain(self):
        self.close()
        self.mainWindow.show()
    
    def openClusterGKWindow(self):
        self.cluster_window = ClusterGKWindow(self, self.dct)
        self.cluster_window.show()

    def showHelp(self):
        QMessageBox.information(self, "Помощь", """Для возврата на главный экран нажмите кнопку \"Назад\" в меню либо используйте сочетание клавиш \"Ctrl+Z\"
    
Для применения сортировки по значениям таблицы нажмите кнопку \"Включить/Отключить сортировку\" в меню либо используйте сочетание клавиш \"Ctrl+S\"

Для выполнения кластерного анализа имеющихся статистических данных нажмите знак \"Анализ\" в верхней части приложения либо используйте сочетание клавиш \"Ctrl+A\" 

Для выявления лучших игроков по выбранным критериям нажмите знак \"Определить лучших\" в верхней части приложения либо используйте сочетание клавиш \"Ctrl+B\" 

Для выхода из приложения нажмите знак выхода в верхней части приложения либо используйте сочетание клавиш \"Ctrl+Q\"""")