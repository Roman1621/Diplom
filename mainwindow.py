from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QShortcut, QSizePolicy, QFileDialog, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView
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
 
        self.setMinimumSize(QSize(480, 320))
        self.setWindowTitle("КтоЗабил")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)
 
        self.title = QLabel("Добро пожаловать в приложение\nИмпортируйте датасет со статистическими данными\nИнструкции о формате данных и возможных действиях представлена во вкладке \"Помощь\"", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        grid_layout.addWidget(self.title, 0, 0)

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
                QMessageBox.information(self, "Неизввестные атрибуты", "Неизвестное имя атрибутов\nПриведите файл к виду:\n#NON-GK\n[list of attributes]\n#GK\n[list of attributes]\nИли выберите другой файл")
        

    def importDS(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Импорт датасета", QtCore.QDir.homePath(), "CSV Files (*.csv)", options=options)
        if files:
            for f in files:
                curFile = parsDStoDict(f)
                curDict = dict()
                name = os.path.splitext(os.path.basename(f))[0]
                curDict[name] = curFile
                self.result.update(curDict)

            if 'GoalKeepers' in self.result.keys():
                self.create_GKButton()
            if 'AtMid_Wingers' in self.result.keys() or 'CenterBacks' in self.result.keys() or 'Forwards' in self.result.keys() or 'FullBacks' in self.result.keys() or 'Midfielders' in self.result.keys():
                self.create_FPButton()
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
        self.centralWidget().layout().addWidget(self.goalkeepers_button)

    def open_GK_window(self):
        self.gk_window = GoalkeepersWindow(self, self.editListOfPls(1), self.GKCharac)
        self.gk_window.show()
        self.close()

    def create_FPButton(self):
        if self.fieldPlayers_button:
            self.fieldPlayers_button.deleteLater()
        self.fieldPlayers_button = QPushButton("Полевые игроки", self)
        self.fieldPlayers_button.clicked.connect(self.open_FP_window)
        self.centralWidget().layout().addWidget(self.fieldPlayers_button)
    
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

        row = 0
        for key, players in self.result.items():
            for player in players:
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(player))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(key))
                row += 1
        self.table.resizeColumnsToContents()
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
                    QMessageBox.information(self, "Удаление", "Датасеты удалены.")
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