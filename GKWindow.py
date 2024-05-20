from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QShortcut, QAction, QTableWidget, QSizePolicy, QTableWidgetItem, QMessageBox, QAbstractItemView
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence

from ClusterGKWindow import ClusterGKWindow

class GoalkeepersWindow(QMainWindow):
    def __init__(self, main_window, dictOfGKs, GKchar=None):
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

        help_action = QAction('&Помощь', self)
        help_action.setShortcut('Ctrl+H')
        help_action.triggered.connect(self.showHelp)

        file_menu = self.menuBar()
        file_menu.addAction(back_action)
        file_menu.addAction(sorting_action)
        file_menu.addAction(clusterization_action)
        file_menu.addAction(help_action)

        self.dct = dictOfGKs
        self.enum = GKchar
        self.GKtable = QTableWidget(self)
        self.populateTable()

    def populateTable(self):
        self.GKtable.setColumnCount(14)
        rowsCount = 0
        for cur in self.dct.values():
            rowsCount += len(cur)
        self.GKtable.setRowCount(rowsCount)
        
        if self.enum:
            headers = ['Name'] + self.enum   
        else:
            headers = ['Name'] + ['']*13
        
        self.GKtable.setHorizontalHeaderLabels(headers)
        for i in range(14):
            self.GKtable.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)

        row = 0
        invalid_players = []
        for players in self.dct.values():
            for player, charac in players.items():
                if len(charac) != 13:  # проверка на недостаток значений в массиве
                    invalid_players.append(player)
                    continue
                for col in range(14):
                    item = QTableWidgetItem()
                    if col == 0:
                        item.setData(Qt.DisplayRole, player)
                    else:
                        item.setData(Qt.DisplayRole, float(charac[col-1]))
                    self.GKtable.setItem(row, col, item)
                row += 1
        if invalid_players:
            QMessageBox.warning(self, "Внимание", f"У следующих игроков недостаточно значений в массиве:\n{', '.join(invalid_players)}")
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
        
    def backToMain(self):
        self.close()
        self.mainWindow.show()
    
    def openClusterGKWindow(self):
        self.cluster_window = ClusterGKWindow(self, self.dct, self.enum)
        self.cluster_window.show()

    def showHelp(self):
        QMessageBox.information(self, "Помощь", """Для возврата на главный экран нажмите кнопку \"Назад\" в меню либо используйте сочетание клавиш \"Ctrl+Z\"
    
Для применения сортировки по значениям таблицы нажмите кнопку \"Включить/Отключить сортировку\" в меню либо используйте сочетание клавиш \"Ctrl+S\"

Для выполнения кластерного анализа имеющихся статистических данных нажмите знак \"Анализ\" в верхней части приложения либо используйте сочетание клавиш \"Ctrl+A\" 

Для выявления лучших игроков по выбранным критериям нажмите знак \"Определить лучших\" в верхней части приложения либо используйте сочетание клавиш \"Ctrl+B\" 

Для выхода из приложения нажмите знак выхода в верхней части приложения либо используйте сочетание клавиш \"Ctrl+Q\"""")