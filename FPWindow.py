from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QShortcut, QAction, QTableWidget, QSizePolicy, QTableWidgetItem, QMessageBox, QInputDialog, QAbstractItemView
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtWidgets
from ClusterFPWindow import *

class FieldPlayersWindow(QMainWindow):
    def __init__(self, main_window, dictOfPls, nonGKChar):
        super().__init__()
        self.mainWindow = main_window
        self.setWindowTitle("КтоЗабил. Полевые")
        self.setMinimumSize(QSize(1500, 960))
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        self.setStyleSheet("""
            FieldPlayersWindow {
                background-color: #C2E7D9;
                border: 4px solid #26408B;
                border-radius: 10px;
            }
        """)

        exit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        exit_shortcut.activated.connect(self.close)

        back_action = QAction('&Назад', self)
        back_action.setShortcut('Ctrl+Z')
        back_action.triggered.connect(self.backToMain)

        sorting_action = QAction('&Включить/Отключить сортировку', self)
        sorting_action.setShortcut('Ctrl+S')
        sorting_action.triggered.connect(self.toggleSorting)

        filter_action = QAction('&Фильтровать по позициям', self)
        filter_action.setShortcut('Ctrl+F')
        filter_action.triggered.connect(self.filterByPos)

        reset_filter = QAction('&Сбросить фильтр', self)
        reset_filter.setShortcut('Ctrl+R')
        reset_filter.triggered.connect(self.resetFilter)

        clusterization_action = QAction('&Анализ данных', self)
        clusterization_action.setShortcut('Ctrl+A')
        clusterization_action.triggered.connect(self.openClusterFPWindow)

        help_action = QAction('&Помощь', self)
        help_action.setShortcut('Ctrl+H')
        help_action.triggered.connect(self.showHelp)
        
        file_menu = self.menuBar()
        file_menu.addAction(back_action)
        file_menu.addAction(sorting_action)
        file_menu.addAction(filter_action)
        file_menu.addAction(reset_filter)
        file_menu.addAction(clusterization_action)
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

        self.enum = nonGKChar
        self.original_data = dictOfPls.copy()
        self.display_data = dictOfPls.copy()
        self.numOfPos = len(dictOfPls)
        self.FPtable = QTableWidget(self)
        self.FPtable.setColumnCount(21)
        self.populateTable()
        self.FPtable.setSortingEnabled(True)
        self.centralWidget().layout().addWidget(self.FPtable)
    
    def populateTable(self):
        numberOfCharacterisitic = 0
        if self.enum is None:
            lengths = []
            for position, players in self.original_data.items():
                for name, characteristics in players.items():
                    lengths.append(len(characteristics))

            if lengths:
                average_length = round(sum(lengths) / len(lengths))
            else:
                average_length = 0
            numberOfCharacterisitic = average_length
        else:
            numberOfCharacterisitic = len(self.enum)

        self.FPtable.setSortingEnabled(False)
        self.FPtable.setColumnCount(numberOfCharacterisitic+2)
        row = 0

        if self.enum is None:
            headers = ['Name', 'Position'] + ['']*numberOfCharacterisitic
        else:
            headers = ['Name', 'Position'] + self.enum
        self.FPtable.setHorizontalHeaderLabels(headers)
        header = self.FPtable.horizontalHeader()
        for i in range(numberOfCharacterisitic+2):
            header.setDefaultAlignment(Qt.AlignHCenter)
    
        for position, players in self.display_data.items():
            for player, charac in players.items():
                self.FPtable.insertRow(row)
                for col in range(numberOfCharacterisitic+2):
                    item = QTableWidgetItem()
                    if col == 0:
                        item.setData(Qt.DisplayRole, player)
                    elif col == 1:
                        item.setData(Qt.DisplayRole, position)
                    else:
                        item.setData(Qt.DisplayRole, float(charac[col-2]))
                    self.FPtable.setItem(row, col, item)
                row += 1
        
        header = self.FPtable.horizontalHeader()
        for i in range(numberOfCharacterisitic):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(numberOfCharacterisitic, QtWidgets.QHeaderView.Stretch)

        self.FPtable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.centralWidget().layout().addWidget(self.FPtable)
        
        self.FPtable.setStyleSheet("""
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

    def toggleSorting(self):
        cur = self.FPtable.isSortingEnabled()
        self.FPtable.setSortingEnabled(not cur)
        if not cur:
            pass
        else:
            self.FPtable.clearContents()
            self.populateTable()

    def filterByPos(self):
        positions = list(self.original_data.keys())
        if len(positions) == 1:
            QMessageBox.information(self, "Предупреждение: только одна позиция", "Нечего фильтровать")
        
        else:
            position, ok = QInputDialog.getItem(self, "Выберите позицию", "Фильтр по позициям:", positions, 0, False)

            if ok and position:
                self.display_data = {position: self.original_data[position]}
                self.populateTable()

    def resetFilter(self):
        self.display_data = self.original_data.copy()
        self.populateTable()

    def backToMain(self):
        self.close()
        self.mainWindow.show()

    def openClusterFPWindow(self):
        self.cluster_window = ClusterFPWindow(self, self.display_data, self.enum)
        self.cluster_window.show()
    
    def showHelp(self):
        QMessageBox.information(self, "Помощь", """Для возврата на главный экран нажмите кнопку \"Назад\" в меню либо используйте сочетание клавиш \"Ctrl+Z\"

Для применения сортировки по значениям таблицы нажмите кнопку \"Включить/Отключить сортировку\" в меню либо используйте сочетание клавиш \"Ctrl+S\"

Для применения фильтра по позициям нажмите кнопку \"Фильтр по позициям\" в меню либо используйте сочетание клавиш \"Ctrl+F\"
                                
Для отмены применения фильтра нажмите кнопку \"Сбросить фильтр\" в меню либо используйте сочетание клавиш \"Ctrl+R\"

Для выполнения кластерного анализа имеющихся статистических данных нажмите знак \"Анализ\" в верхней части приложения либо используйте сочетание клавиш \"Ctrl+A\" 

Для выявления лучших игроков по выбранным критериям нажмите знак \"Определить лучших\" в верхней части приложения либо используйте сочетание клавиш \"Ctrl+B\" 

Для выхода из приложения нажмите знак выхода в верхней части приложения либо используйте сочетание клавиш \"Ctrl+Q\"""")