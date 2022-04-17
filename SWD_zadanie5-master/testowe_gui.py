""" ....... """


"""
#TODO
1. Podpiąć słownik do tego z klasy database (zainicjalizować go gdzieś najpierw). W tym pliku chyba 
   wystarczy tylko pozamieniać ze zmienną "self.main_dict" która dałem teraz tak dla sprawdzenia działania
2. Podpiąć listę ranking do wyników wyrzucanych przez metodę (mozna też zrobić taką listę w klasie Database i z niej wyciągać)
3. Dodać funkcjonalności:
    - do przycisku Import Data (wrzucanie danych z excela)
    - do przycisku Run alghoritm (odpalanie algorytmu i aktualizacja obrazu z plotem)
    - do radio buttonów (zmiana metody)
4. Poprawic niektóre metody ( jest przy nich napisane co nie działa)
"""
import os
import csv
import sys

from matplotlib import pyplot as plt
from UTA import UTA
from fuzzy_topsis import fuzzy_topsis
from RSM import RSM
from plot import plot
from PyQt5 import QtCore, QtGui, QtWidgets

# main_dict = {'M1': [58000, 36.5, 450, 7, 9, 4, 2, 9, 3, 5, 10, True, True, True, 7, 2004, False, 3, 200],
#              'M2': [108000, 60.0, 500, 3, 5, 4, 8, 2, 6, 7, 9, False, False, True, 5, 2012, False, 12, 300],
#              'M3': [72000, 15.4, 666, 9, 8, 2, 3, 4, 6, 7, 8, True, False, False, 6, 2021, False, 5, 600],
#              'M4': [99000, 70, 420, 6, 8, 7, 3, 5, 6, 7, 7, False, True, False, 4, 2010, True, 7, 1200],
#              'M5': [70000, 40, 500, 2, 10, 7, 5, 4, 3, 9, 1, True, True, True, 3, 2021, True, 15, 500],
#              'M6': [120000, 70, 350, 9, 1, 6, 8, 2, 6, 5, 5, False, False, True, 5, 2015, True, 4, 700],
#              'M7': [50000, 20, 750, 1, 5, 3, 4, 7, 4, 1, 6, False, True, False, 2, 1997, False, 3, 200],
#              'M8': [60000, 35, 440, 3, 5, 7, 10, 9, 7, 9, 5, True, True, True, 4, 2012, True, 6, 500],
#              'M9': [92000, 55, 580, 3, 6, 4, 8, 4, 6, 4, 4, True, True, False, 3, 2000, False, 2, 600],
#              'M10': [121000, 70, 700, 5, 8, 2, 3, 3, 5, 2, 9, False, True, True, 4, 2010, True, 7, 600],
#              'M11': [88000, 57, 550, 5, 10, 7, 6, 7, 6, 2, 5, True, True, False, 3, 2008, False, 3, 300],
#              'M12': [88000, 50, 500, 8, 5, 7, 7, 3, 6, 1, 5, True, True, True, 3, 2012, False, 12, 500],
#              'M13': [52000, 55, 580, 1, 7, 3, 4, 7, 9, 4, 9, False, True, False, 3, 1956, True, 3, 200],
#              'M14': [96000, 70, 700, 2, 1, 1, 9, 9, 5, 5, 7, False, False, True, 4, 1999, True, 1, 300],
#              'M15': [40000, 20, 300, 5, 2, 9, 4, 9, 1, 1, 6, False, True, True, 2, 2001, True, 4, 400],
#              'M16': [300000, 150, 1000, 7, 8, 4, 2, 9, 9, 9, 0, True, False, True, 8, 2021, False, 10, 1000],
#              'M17': [186000, 90, 800, 5, 9, 2, 3, 8, 8, 7, 9, False, True, True, 3, 2014, True, 15, 500],
#              'M18': [150000, 82, 700, 6, 7, 3, 1, 4, 5, 7, 8, False, False, True, 3, 2017, False, 10, 300],
#              'M19': [212000, 110, 900, 7, 5, 1, 5, 6, 7, 8, 7, True, True, True, 4, 1998, False, 8, 1500],
#              'M20': [250000, 150, 1000, 8, 4, 1, 8, 7, 9, 9, 6, True, True, False, 5, 1986, True, 2, 800]}
#
# ranking = [[1, 'M1', 0.1], [2, 'M2', 0.2], [
#     3, 'M3', 0.3], [4, 'M4', 0.4], [5, 'M5', 0.5]]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1093, 883)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 70, 160, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(140, 30))
        self.label.setMaximumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.topsis_radbtn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.topsis_radbtn.setObjectName("topsis_radbtn")
        self.verticalLayout.addWidget(self.topsis_radbtn)
        self.rsm_radbtn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rsm_radbtn.setObjectName("rsm_radbtn")
        self.verticalLayout.addWidget(self.rsm_radbtn)
        self.uta_radbtn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.uta_radbtn.setObjectName("uta_radbtn")
        self.verticalLayout.addWidget(self.uta_radbtn)
        self.run_button = QtWidgets.QPushButton(self.centralwidget)
        self.run_button.setGeometry(QtCore.QRect(50, 230, 141, 41))
        self.run_button.setObjectName("run_button")
        self.plot_img = QtWidgets.QLabel(self.centralwidget)
        self.plot_img.setGeometry(QtCore.QRect(500, 470, 511, 331))
        self.plot_img.setMinimumSize(QtCore.QSize(511, 331))
        self.plot_img.setMaximumSize(QtCore.QSize(511, 331))
        self.plot_img.setText("")
        self.plot_img.setPixmap(QtGui.QPixmap("plot_img.png"))
        self.plot_img.setAlignment(QtCore.Qt.AlignCenter)
        self.plot_img.setObjectName("plot_img")
        self.ranking_button = QtWidgets.QPushButton(self.centralwidget)
        self.ranking_button.setGeometry(QtCore.QRect(50, 280, 141, 41))
        self.ranking_button.setObjectName("ranking_button")
        self.data_table = QtWidgets.QTableWidget(self.centralwidget)
        self.data_table.setGeometry(QtCore.QRect(240, 30, 931, 371))
        self.data_table.setObjectName("data_table")
        self.data_table.setColumnCount(20)
        self.data_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        for i in range(self.data_table.columnCount()):
            item = QtWidgets.QTableWidgetItem()
            self.data_table.setHorizontalHeaderItem(i, item)
        self.delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_button.setGeometry(QtCore.QRect(590, 410, 141, 41))
        self.delete_button.setObjectName("delete_button")
        self.add_row_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_row_button.setGeometry(QtCore.QRect(440, 410, 141, 41))
        self.add_row_button.setObjectName("add_row_button")
        self.import_button = QtWidgets.QPushButton(self.centralwidget)
        self.import_button.setGeometry(QtCore.QRect(290, 410, 141, 41))
        self.import_button.setObjectName("import_button")
        self.clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(890, 410, 141, 41))
        self.clear_button.setObjectName("clear_button")
        self.update_button = QtWidgets.QPushButton(self.centralwidget)
        self.update_button.setGeometry(QtCore.QRect(740, 410, 141, 41))
        self.update_button.setObjectName("update_button")
        self.ranking_label = QtWidgets.QLabel(self.centralwidget)
        self.ranking_label.setGeometry(QtCore.QRect(180, 470, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ranking_label.setFont(font)
        self.ranking_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ranking_label.setObjectName("ranking_label")
        self.ranking_table = QtWidgets.QTableWidget(self.centralwidget)
        self.ranking_table.setGeometry(QtCore.QRect(120, 500, 311, 301))
        self.ranking_table.setObjectName("ranking_table")
        self.ranking_table.setColumnCount(2)
        self.ranking_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ranking_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ranking_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ranking_table.setHorizontalHeaderItem(2, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Podłączanie przycisków do ich funkcji
        self.import_button.clicked.connect(self.insert_data)
        self.add_row_button.clicked.connect(self.add_row)
        self.delete_button.clicked.connect(self.delete_selected)
        self.update_button.clicked.connect(self.update_database)
        self.clear_button.clicked.connect(self.clear_database)
        self.ranking_button.clicked.connect(self.show_ranking)
        self.run_button.clicked.connect(self.run_method)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Choose method"))
        self.topsis_radbtn.setText(_translate("MainWindow", "Topsis"))
        self.rsm_radbtn.setText(_translate("MainWindow", "RSM"))
        self.uta_radbtn.setText(_translate("MainWindow", "UTA"))
        self.run_button.setText(_translate("MainWindow", "Run Alghoritm"))
        self.ranking_button.setText(_translate("MainWindow", "Show Ranking"))
        item = self.data_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(11)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(12)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(13)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(14)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(15)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(16)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(17)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(18)
        item.setText(_translate("MainWindow", ""))
        item = self.data_table.horizontalHeaderItem(19)
        item.setText(_translate("MainWindow", ""))
        self.delete_button.setText(_translate(
            "MainWindow", "Delete Selected Rows"))
        self.add_row_button.setText(_translate("MainWindow", "Add Row"))
        self.import_button.setText(_translate("MainWindow", "Import Data"))
        self.clear_button.setText(_translate("MainWindow", "Clear database"))
        self.update_button.setText(_translate("MainWindow", "Update Database"))
        self.ranking_label.setText(_translate("MainWindow", "RANKING"))
        self.ranking_table.setSortingEnabled(False)
        # item = self.ranking_table.horizontalHeaderItem(0)
        # item.setText(_translate("MainWindow", "Pozycja"))
        item = self.ranking_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Nazwa"))
        item = self.ranking_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Scoring"))

    def insert_data(self):
        '''
        Funkcja ładuje dane z słownika (naszej bazy danych) do tabeli w GUI.
        '''
        self.download_data()
        # self.set_headers(isFirst=False)
        self.load_data2table()

        item = self.data_table.horizontalHeaderItem(0)
        item.setText("Nazwa")
        for i, name in enumerate(self.param_names):
            item = self.data_table.horizontalHeaderItem(i+1)
            item.setText(name)

    def load_data2table(self):
        self.data_table.setRowCount(len(self.main_dict))
        for row, (key, values) in enumerate(self.main_dict.items()):
            self.data_table.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
            for i, val in enumerate(values):
                if isinstance(val, (int, float, bool)):
                    self.data_table.setItem(
                        row, i + 1, QtWidgets.QTableWidgetItem(str(val)))
                else:
                    self.data_table.setItem(
                        row, i + 1, QtWidgets.QTableWidgetItem(val))

    def add_row(self):
        '''
        Funkcja dodaje nowy rząd danych na końcu tabeli. Możemy wpisać do niego wartości. Żeby dodało się do bazy danych trzeba nacisnąć "Update database"
        '''
        self.data_table.setRowCount(self.data_table.rowCount() + 1)
        self.data_table.insertRow(self.data_table.rowCount() + 1)

    def delete_selected(self):
        '''
        Funkcja usuwa zaznaczone rzędy
        '''
        rows = []
        for idx in self.data_table.selectedIndexes():
            row = idx.row()
            if not row in rows:
                rows.append(row)

        rows.reverse()

        # removed = {}
        # for row in rows:
        #     for col in range(self.data_table.columnCount()):
        #         if col == 0:
        #             if not self.data_table.item(row, col):
        #                 break
        #             key = self.data_table.item(row, col).text()
        #             if key in self.main_dict.keys():
        #                 print("This name already exists")
        #                 pass
        #         else:
        #             if key in removed.keys():
        #                 removed[key].append(
        #                     self.data_table.item(row, col).text())
        #             else:
        #                 removed[key] = [self.data_table.item(row, col).text()]

        # print(removed)

        for row in rows:
            self.data_table.removeRow(row)
            print(f"Deleted {row} row..")

    def update_database(self):
        '''
        Funkcja leci po naszej tabeli danych z GUI i tworzy od nowa słownik z bazą danych

        #TODO:
            Przy przepisywaniu do słownika trzeba zamieniać zmienne ze stringów na inty, boole (oprócz nazwy).
            Przydałoby się też uwzględnić czy wpisane wartości są w poprawnych zakresach (np. Oceny są od 1 do 10) jak nie - np.
            wywalała błąd i wywala kryterium z bazy lub pozwala go jakos poprawić.
        '''
        print(self.main_dict)
        self.main_dict.clear()
        if self.data_table.rowCount() != 0:
            for row in range(self.data_table.rowCount()):
                for col in range(self.data_table.columnCount()):
                    if col == 0:
                        if not self.data_table.item(row, col):
                            break
                        key = self.data_table.item(row, col).text()
                        if key in self.main_dict.keys():
                            print("This name already exists")
                            pass
                    else:
                        if not self.data_table.item(row, col):
                            break
                        if key in self.main_dict.keys():
                            self.main_dict[key].append(
                                self.data_table.item(row, col).text())
                        else:
                            self.main_dict[key] = [
                                self.data_table.item(row, col).text()]
        else:
            self.data_table.setRowCount(0)

        self.main_dict = self._change_data_type(self.types, self.main_dict)
        print(self.main_dict)
        self.data_table.clearContents()
        self.load_data2table()

    def clear_database(self):
        '''
        Funkcja czyści naszą tabele.
        '''

        self.data_table.clearContents()

        for i in range(20):
            item = self.data_table.horizontalHeaderItem(i)
            item.setText("")


    def show_ranking(self):
        '''
        Funkcja wrzuca ranking do tabeli
        '''
        ranking = self.ranking
        self.ranking_table.setRowCount(len(ranking))
        for row, el in enumerate(ranking):
            # self.ranking_table.setItem(
            #     row, 0, QtWidgets.QTableWidgetItem(str(el[0])))
            self.ranking_table.setItem(
                row, 0, QtWidgets.QTableWidgetItem(el[0]))
            self.ranking_table.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(el[1])))

    def run_method(self):

        if self.topsis_radbtn.isChecked():
            self.ranking = fuzzy_topsis(
                self.main_dict, self.weights, self.max_min, A0=self.A0, A1=self.A1)
            plot(self.main_dict, self.weights,
                 self.ranking, self.param_names, "Topsis")
            self.plot_img.setPixmap(QtGui.QPixmap("plot_img.png"))

        if self.rsm_radbtn.isChecked():
            cols = []
            for idx in self.data_table.selectedIndexes():
                col = idx.column()
                if not col in cols:
                    cols.append(col)
            rank, self.ranking = RSM(self.main_dict, cols)
            self.plot_img.setPixmap(QtGui.QPixmap("plot_img.png"))
            # plot(self.main_dict, self.weights,
            #      self.ranking, self.param_names, "RSM")
            # self.plot_img.setPixmap(QtGui.QPixmap("data/plot_img.png"))
            # plot(self.main_dict, self.weights, self.ranking, self.param_names, "RSM")

        if self.uta_radbtn.isChecked():
            consider = []
            for idx in self.data_table.selectedIndexes():
                col = idx.column()
                if not col in consider:
                    consider.append(col-1)
            reversed(consider)
            self. ranking = UTA(self.main_dict, self.weights,
                                self.uta_data['UTA_DATA'], self.max_min, consider)
            plot(self.main_dict, self.weights,
                 self.ranking, self.param_names, "UTA")
            self.plot_img.setPixmap(QtGui.QPixmap("plot_img.png"))

    def download_data(self):
        path = os.path.abspath("data")
        qfd = QtWidgets.QFileDialog()
        fname = QtWidgets.QFileDialog.getOpenFileName(
            qfd, 'Open File', path, "Excel files (*.csv)")
        rows = self._import_data_from_csv(fname[0])
        rows = self._extract_only_data_to_consider(rows)
        self._arrange_data(rows)

    def _import_data_from_csv(self, fname):
        rows = []
        with open(fname, "r", encoding='utf8') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        return rows

    def _get_mask(self, rows):
        for row in rows:
            if row[0] == "CONSIDER":
                mask = row[1:]
                break
        bool_mask = [True if cryt == "1" else False for cryt in mask]
        bool_mask = [True] + bool_mask
        return bool_mask

    def _extract_only_data_to_consider(self, rows):
        new_rows = []
        mask = self._get_mask(rows)
        for row in rows:
            new_row = []
            for nr, el in enumerate(row):
                if mask[nr] is True:
                    new_row.append(el)
            new_rows.append(new_row)
        return new_rows

    def _change_data_type(self, types, group):
        new_group = {}
        for key, vals in group.items():
            new_vals = []
            for nr in range(len(vals)):
                if types[nr] == "INT":
                    new_vals.append(float(vals[nr]))
                elif types[nr] == "BOOL":
                    if vals[nr] == "False":
                        new_vals.append(False)
                    if vals[nr] == "True":
                        new_vals.append(True)
            new_group.update({key: new_vals})
        return new_group

    def _arrange_data(self, rows):
        main_dict = {}
        A0 = {}
        A1 = {}
        weights = {}
        self.param_names = rows[0][1:]
        min_max = {}
        self.types = []
        uta_data = {}
        for row in rows[1:]:
            tag = row[0]
            vals = row[1:]
            if tag == "":
                continue
            if tag == "WEIGHTS":
                weights = list(map(float, vals))
            elif tag == "MAX MIN":
                min_max = list(map(int, vals))
            elif tag == "CONSIDER":
                self.consider = list(map(int, vals))
            elif tag == "TYPE":
                self.types = vals
            elif tag == "UTA_DATA":
                uta_data.update({tag: list(map(int, vals))})
            elif "M" in tag:
                main_dict.update({tag: vals})
            elif "A0" in tag and "#" not in tag:
                A0.update({tag: vals})
            elif "A1" in tag and "#" not in tag:
                A1.update({tag: vals})

        main_dict = self._change_data_type(self.types, main_dict)
        if A0:
            A0 = self._change_data_type(self.types, A0)
            self.A0 = A0
        else:
            self.A0 = None
        if A1:
            A1 = self._change_data_type(self.types, A1)
            self.A1 = A1
        else:
            self.A1 = None

        self.main_dict = main_dict
        self.weights = weights
        self.uta_data = uta_data
        self.max_min = min_max


if __name__ == "__main__":
    path = os.path.abspath("plot_img.png")
    plt.figure(figsize=(9, 6))
    plt.savefig(path, bbox_inches='tight')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
