from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QShortcut, QFileDialog, QPushButton, QTableWidget, QAbstractItemView
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtWidgets
import os

from smParsDS import parsDStoDict, parsAtNames
from GKWindow import *
from FPWindow import *
# Главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
 
        self.setMinimumSize(QSize(700, 420))
        self.setWindowTitle("КтоЗабил")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)
 
        self.title = QLabel("Добро пожаловать в приложение\nИмпортируйте датасет со статистическими данными\nИнструкции о формате данных и возможных действиях представлена во вкладке \"Помощь\"", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        grid_layout.addWidget(self.title, 0, 0)
        self.title.setStyleSheet("QLabel { color: #0D0221; font-size: 18px; }")

        exit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        exit_shortcut.activated.connect(self.close)

        import_action = QAction('&Импорт', self)
        import_action.setShortcut('Ctrl+I')
        import_action.triggered.connect(self.importDS)

        charac_action = QAction('&Импорт характеристик', self)
        charac_action.setShortcut('Ctrl+C')
        charac_action.triggered.connect(self.importCharac)

        delete_action = QAction('&Удалить данные', self)
        delete_action.setShortcut('Ctrl+D')
        delete_action.triggered.connect(self.deleteData)
        
        
        help_action = QAction('&Помощь', self)
        help_action.setShortcut('Ctrl+H')
        help_action.triggered.connect(self.showHelp)

        file_menu = self.menuBar()
        file_menu.addAction(import_action)
        file_menu.addAction(charac_action)
        file_menu.addAction(delete_action)
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

        self.setStyleSheet("""
            QMainWindow {
                background-color: #C2E7D9;
                border: 4px solid #26408B;
                border-radius: 10px;
            }
        """)

        self.goalkeepers_button = None
        self.fieldPlayers_button = None
        self.result = dict()
        self.table = None
        self.titleDeleted = False
        self.nameCharac = dict()
        self.nonGKCharac = None
        self.GKCharac = None

    def importCharac(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        f, _ = QFileDialog.getOpenFileName(self, "Импорт характеристик", QtCore.QDir.homePath(), "TXT Files (*.txt)", options=options)
        if f:
            cur = parsAtNames(f)
            if 'NON-GK' in cur.keys():
                self.nonGKCharac = cur['NON-GK']
            if 'GK' in cur.keys():
                self.GKCharac = cur['GK']
            if 'NON-GK' not in cur.keys() and 'GK' not in cur.keys():
                QMessageBox.information(self, "Неизвестные атрибуты", "Неизвестное имя атрибутов\nПриведите файл к виду:\n#NON-GK\n[list of attributes]\n#GK\n[list of attributes]\nИли выберите другой файл")
        

    def importDS(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Импорт датасета", QtCore.QDir.homePath(), "CSV Files (*.csv)", options=options)
        if files:
            for f in files:
                curFile = parsDStoDict(f)
                if curFile == -1:
                    QMessageBox.information(self, "Неизвестный тип файла", "Неизвестный тип файла.\nПриведите его к виду:\nName\n[Attribute Vector]\nИли выберите другой файл")
                else:
                    curDict = dict()
                    name = os.path.splitext(os.path.basename(f))[0]
                    curDict[name] = curFile
                    self.result.update(curDict)

            if 'GoalKeepers' in self.result.keys():
                self.create_GKButton()
            if 'AtMid_Wingers' in self.result.keys() or 'CenterBacks' in self.result.keys() or 'Forwards' in self.result.keys() or 'FullBacks' in self.result.keys() or 'Midfielders' in self.result.keys():
                self.create_FPButton()
            if self.result:
                self.addTableToMainWindow()

    def editListOfPls(self, key):
        cur = self.result
        if key == 1:
            cur = {key: cur[key] for key in cur.keys() if key == 'GoalKeepers'}
        elif key == 2:
            cur = {key: cur[key] for key in cur.keys() if not key == 'GoalKeepers'}
        return cur
    
    def create_GKButton(self):
        if self.goalkeepers_button:
            self.goalkeepers_button.deleteLater()
        self.goalkeepers_button = QPushButton("Вратари", self)
        self.goalkeepers_button.clicked.connect(self.open_GK_window)
        self.goalkeepers_button.setStyleSheet("""
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
        self.centralWidget().layout().addWidget(self.goalkeepers_button, 0, 0)

    def open_GK_window(self):
        self.gk_window = GoalkeepersWindow(self, self.editListOfPls(1), self.GKCharac)
        self.gk_window.show()
        self.close()

    def create_FPButton(self):
        if self.fieldPlayers_button:
            self.fieldPlayers_button.deleteLater()
        self.fieldPlayers_button = QPushButton("Полевые игроки", self)
        self.fieldPlayers_button.clicked.connect(self.open_FP_window)
        self.fieldPlayers_button.setStyleSheet("""
            QPushButton {
                background-color: #26408B;
                color: #0D0221;
                font-size: 18px;
                padding: 10px 30px;
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
        self.centralWidget().layout().addWidget(self.fieldPlayers_button, 1, 0)
    
    def open_FP_window(self):
        self.fp_window = FieldPlayersWindow(self, self.editListOfPls(2), self.nonGKCharac)
        self.fp_window.show()
        self.close()

    def addTableToMainWindow(self):
        if not self.titleDeleted:
            self.title.deleteLater()
            self.titleDeleted = True
        if self.table:
            self.table.deleteLater()

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        rowsCount = 0
        for cur in self.result.values():
            rowsCount += len(cur)
        self.table.setRowCount(rowsCount)

        self.table.setHorizontalHeaderLabels(['Name', 'Postion'])
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.setStyleSheet("""
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
        
        row = 0
        for key, players in self.result.items():
            for player in players:
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(player))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(key))
                row += 1
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.centralWidget().layout().addWidget(self.table)

    def deleteData(self):
        items = ("Характеристики", "Датасеты", "Часть датасетов")
        if self.nonGKCharac is None and self.GKCharac is None and len(self.result) == 0:
            QMessageBox.information(self, "Нечего удалять", "Отсутствует контент доступный для удаления")
        else:
            item, ok = QInputDialog.getItem(self, "Удалить данные", "Выберите, что вы хотите удалить:", items, 0, False)
            if ok and item:
                if item == "Характеристики":
                    self.nonGKCharac = None
                    self.GKCharac = None
                    QMessageBox.information(self, "Удаление", "Характеристики удалены.")
                elif item == "Датасеты":
                    self.result.clear()
                    if self.table:
                        self.table.clear()
                        self.table.setRowCount(0)
                        self.table.deleteLater()
                        self.table = None
                    QMessageBox.information(self, "Удаление", "Датасеты удалены.")
                    self.title = QLabel("Добро пожаловать в приложение\nИмпортируйте датасет со статистическими данными\nИнструкции о формате данных и возможных действиях представлена во вкладке \"Помощь\"", self)
                    self.title.setAlignment(QtCore.Qt.AlignCenter)
                    self.centralWidget().layout().addWidget(self.title, 0, 0)
                    self.title.setStyleSheet("QLabel { color: #0D0221; font-size: 18px; }")
                    self.titleDeleted = False
                elif item == "Часть датасетов":
                    self.deletePartOfDatasets()
                self.updateButtons()

    def deletePartOfDatasets(self):
        keys = list(self.result.keys())
        key, ok = QInputDialog.getItem(self, "Удалить часть датасетов", "Выберите датасет для удаления:", keys, 0, False)
        if ok and key:
            if key in self.result:
                del self.result[key]
                QMessageBox.information(self, "Удаление", f"Датасет {key} удален.")
                if self.result == {}:
                    self.result.clear()
                    if self.table:
                        self.table.clear()
                        self.table.setRowCount(0)
                        self.table.deleteLater()
                        self.table = None
                    self.title = QLabel("Добро пожаловать в приложение\nИмпортируйте датасет со статистическими данными\nИнструкции о формате данных и возможных действиях представлена во вкладке \"Помощь\"", self)
                    self.title.setAlignment(QtCore.Qt.AlignCenter)
                    self.centralWidget().layout().addWidget(self.title, 0, 0)
                    self.title.setStyleSheet("QLabel { color: #0D0221; font-size: 18px; }")
                    self.titleDeleted = False
                else:
                    self.addTableToMainWindow()
                    self.updateButtons()
    
    def updateButtons(self):
        if 'GoalKeepers' not in self.result:
            if self.goalkeepers_button:
                self.goalkeepers_button.deleteLater()
                self.goalkeepers_button = None
        if not any(key in self.result for key in ['AtMid_Wingers', 'CenterBacks', 'Forwards', 'FullBacks', 'Midfielders']):
            if self.fieldPlayers_button:
                self.fieldPlayers_button.deleteLater()
                self.fieldPlayers_button = None

    def showHelp(self):
        QMessageBox.information(self, "Помощь", """Для корректной работы приложения статистические данные должны быть представлены в формате .csv

Для импорта данных нажмите кнопку \"Импорт\" в меню либо используйте сочетание клавиш \"Ctrl+I\"
                                
Для импорта характеристик нажмите кнопку \"Импорт характеристик\" в меню либо используйте сочетание клавиш \"Ctrl+C\"

Для удаления данных и/или характеристик нажмите кнопку \"Удалить данные\" в меню либо используйте сочетание клавиш \"Ctrl+D\"

Для выхода из приложения нажмите знак выхода в верхней части приложения либо используйте сочетание клаввиш \"Ctrl+Q\"""")