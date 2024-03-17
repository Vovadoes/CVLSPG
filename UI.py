from typing import Callable
from typing import List, Any

from PyQt5 import QtWidgets

from files.MainWindow import Ui_MainWindow
from files.ResultWindow import Ui_Form
from files.TableWindow import Ui_Form as Ui_Form_Table

from main import Calculation
from functions import change_size, get_sub, get_super
from MyThread import MyThread
from TableLoader import TableLoader
# from ChartPLTWindow import ChartPLTWindow

from settings import DEDUG

import sys


# from functions import get_super, get_sub


class Variables:
    def __init__(self, main_window):
        self.main_window: mywindow = main_window
        self.n = None
        self.m = None
        self.U = None
        self.nl = None
        self.cos_fi = None
        self.P_kpd = None
        self.q = None
        self.k = None
        self.U2 = None
        self.load()

    def load(self):
        self.n = mywindow.is_int(self.main_window.ui.doubleSpinBox)
        self.m = mywindow.is_int(self.main_window.ui.doubleSpinBox_2)
        self.U = mywindow.is_float(self.main_window.ui.doubleSpinBox_4)
        self.nl = mywindow.is_float(self.main_window.ui.doubleSpinBox_7)
        self.cos_fi = mywindow.is_float(self.main_window.ui.doubleSpinBox_6)
        self.P_kpd = mywindow.is_float(self.main_window.ui.doubleSpinBox_5)
        self.q = mywindow.is_float(self.main_window.ui.doubleSpinBox_10)
        self.k = mywindow.is_int(self.main_window.ui.doubleSpinBox_3)
        self.U2 = mywindow.is_float(self.main_window.ui.doubleSpinBox_8)

    def update(self):
        self.load()
        self.main_window.table_loader1.m = self.m
        # self.main_window.table_loader2.n = self.n


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()

        self.calculation = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if DEDUG:
            self.ui.doubleSpinBox.setValue(96)  # n
            self.ui.doubleSpinBox_2.setValue(7)  # m
            self.ui.doubleSpinBox_4.setValue(0.4)  # U
            self.ui.doubleSpinBox_7.setValue(5)  # nl
            self.ui.doubleSpinBox_6.setValue(0.95)  # cos_fi
            self.ui.doubleSpinBox_5.setValue(80)  # P_kpd
            self.ui.doubleSpinBox_10.setValue(0.028)  # q
            self.ui.doubleSpinBox_3.setValue(3)  # k
            self.ui.doubleSpinBox_8.setValue(240)  # U2

        change_size(self)

        self.lst_Thread = []

        self.variables = Variables(self)

        loader1_n = 4
        loader1_m = self.variables.m
        loader1_label = self.ui.label_13
        loader1_data = [
            ["AB", 62, 350, 4],
            ["AC", 34, 390, 4],
            ["DB", 12, 120, 4],
            ["EF", 18, 172, 4],
            ["KL", 20, 200, 4],
            ["NM", 8, 80, 4],
            ["OC", 14, 120, 4],
        ]
        loader1_block = False
        loader1_heading_x = lambda iterator: \
            [
                "Наименование участков",
                "Количество домов на участке",
                "Длина участка, м",
                "Число жил провода по СИП-2"
            ][iterator]
        loader1_types_matrix = [[str, float, int, int] for _ in range(loader1_m)]

        # loader2_n = self.variables.n
        # loader2_m = 1
        # loader2_label = self.ui.label_4
        # loader2_data = [[1, 1.6]]
        # loader2_block = False
        # loader2_heading_x = lambda iterator: f"E{get_sub(str(iterator + 1))}"

        self.table_loader1 = TableLoader(
            self, loader1_n, loader1_m, loader1_label,
            block=loader1_block,
            heading_x=loader1_heading_x,
            types_matrix=loader1_types_matrix
        )
        # self.table_loader2 = TableLoader(
        #     self, loader2_n, loader2_m, loader2_label,
        #     block=loader2_block,
        #     heading_x=loader2_heading_x
        # )

        if DEDUG:
            pass
            self.table_loader1.data = loader1_data
            # self.table_loader2.data = loader2_data

        self.ui.pushButton_8.clicked.connect(self.table_loader1.open_table)
        # self.ui.pushButton_3.clicked.connect(self.table_loader2.open_table)

        # add_def_pushButton = lambda : self.calculation.simple_bid()
        # add_def_pushButton_2 = lambda : self.calculation.difficult_bet()
        # self.ui.pushButton.clicked.connect(lambda : self.calculate(add_def_pushButton))
        # self.ui.pushButton_2.clicked.connect(lambda : self.calculate(add_def_pushButton_2))

        add_def_pushButton = lambda: None
        self.ui.pushButton.clicked.connect(lambda: self.calculate(add_def_pushButton))

    def calculate(self, fun, *args, **kwargs):
        self.variables.update()
        # condition = self.table_loader1.valid(1, self.variables.m) and self.table_loader2.valid(
        # 1, self.variables.n)
        condition = True
        if condition:
            self.calculation = Calculation(
                n=self.variables.n,
                m=self.variables.m,
                lst=self.table_loader1.data,
                U1=self.variables.U,
                nl=self.variables.nl,
                cos_fi=self.variables.cos_fi,
                P_kpd=self.variables.P_kpd,
                q=self.variables.q,
                k=self.variables.k,
                U2=self.variables.U2,
            )
            fun(*args, **kwargs)
            window = Finish(
                self
            )
            window.show()

            # def main():
            #     window.exec_()
            #
            # t = MyThread(main)
            # t.start()
            windowThread = MyThread(lambda: window.exec_())
            windowThread.start()
            self.lst_Thread.append(windowThread)

    def exec_(self) -> int:
        a = super().exec_()
        for i in self.lst_Thread:
            i.wait()
        return a

    @staticmethod
    def is_float(value: QtWidgets.QDoubleSpinBox) -> float:
        try:
            a = float(value.value())
            value.setStyleSheet("QDoubleSpinBox {}")
            return a
        except ValueError:
            value.setStyleSheet("QDoubleSpinBox { background-color: red; }")
            raise ValueError()

    @staticmethod
    def is_int(value: QtWidgets.QDoubleSpinBox) -> int:
        try:
            a = int(round(float(value.value())))
            value.setStyleSheet("QDoubleSpinBox {}")
            return a
        except ValueError:
            value.setStyleSheet("QDoubleSpinBox { background-color: red; }")
            raise ValueError()


class Finish(QtWidgets.QDialog):
    def __init__(self, parent: mywindow):
        super(Finish, self).__init__()
        self.ui = Ui_Form()
        self.parent = parent
        self.ui.setupUi(self)
        change_size(self)

        # self.ui.doubleSpinBox_32.setValue(round(self.parent.calculation.i0 * 100, 1))

        lst = []
        for i in range(self.parent.variables.m):
            data = self.parent.table_loader1.data
            lst.append([
                data[i][0], round(self.parent.table_loader1.data[i][2], 4),
                self.parent.table_loader1.data[i][3], round(self.parent.calculation.lst_S_gost[i], 4),
                round(self.parent.calculation.lst_R_new[i], 4),
                round(self.parent.calculation.lst_I_new[i], 4),
                round(self.parent.calculation.lst_Un[i], 4),
                round(self.parent.calculation.lst_Uv[i], 4),
            ])
        print(f"{lst=}")

        filter_table_results_1 = lambda dct: dct['value']

        loader_results_1_n = 8
        loader_results_1_m = self.parent.variables.m
        loader_results_1_data = lst
        types_matrix_results_1 = [[str, float, int, int, float, float, float, float] for _ in range(loader_results_1_m)]
        loader_results_1_block = True
        loader_results_1_heading_x = lambda iterator: [
            "Наименование\n участка",
            "Длина участка L(м)",
            "Параметры СИП\nЧисло жил",
            f"Параметры СИП\nСечение жил, S/мм{get_super('2')}",
            "Сопротивление на\nучастке R(Ом)",
            "Сила тока на\nучастке I(А)",
            "Падение напряжения\nна участке Un(В)",
            "Напряжение на\nконечной точке\nпотребления Ui, (В)",
        ][iterator]

        loader_results_1_heading_y = lambda iterator: str(iterator)
        self.table_loader_results_1 = TableLoader(
            self.parent, loader_results_1_n, loader_results_1_m, data=loader_results_1_data,
            block=loader_results_1_block,
            heading_x=loader_results_1_heading_x, heading_y=loader_results_1_heading_y,
            filter_table=filter_table_results_1, types_matrix=types_matrix_results_1
        )

        # loader_v_y_data = self.parent.calculation.lst_v_y
        # self.table_loader_v_y = TableLoader(
        #     self.parent, loader_v_d_n, loader_v_d_m, data=loader_v_y_data,
        #     block=loader_v_d_block,
        #     heading_x=loader_v_d_heading_x, heading_y=loader_v_d_heading_y,
        #     filter_table=filter_table
        # )
        #
        # loader_v_s_data = self.parent.calculation.lst_v_s
        # self.table_loader_v_s = TableLoader(
        #     self.parent, loader_v_d_n, loader_v_d_m, data=loader_v_s_data,
        #     block=loader_v_d_block,
        #     heading_x=loader_v_d_heading_x, heading_y=loader_v_d_heading_y,
        #     filter_table=filter_table
        # )

        # self.ui.doubleSpinBox_19.setValue(round(self.parent.calculation.y))
        # self.ui.doubleSpinBox_20.setValue(round(self.parent.calculation.dy))
        # self.ui.doubleSpinBox_10.setValue(round(self.parent, 2))
        self.table_loader_results_1.kwargs['block'] = True
        # self.parent.table_loader2.kwargs['block'] = True

        self.lst_Thread = []

        self.lst_Thread.append(MyThread(lambda: self.table_loader_results_1.open_table()))
        self.ui.pushButton_2.clicked.connect(
            lambda: self.lst_Thread[0].start()
        )
        #
        # self.lst_Thread.append(MyThread(lambda: self.table_loader_v_s.open_table()))
        # self.ui.pushButton_4.clicked.connect(
        #     lambda: self.lst_Thread[1].start()
        # )
        #
        # self.lst_Thread.append(MyThread(lambda: self.table_loader_v_y.open_table()))
        # self.ui.pushButton_7.clicked.connect(
        #     lambda: self.lst_Thread[2].start()
        # )
        #
        # chart_plt_w = ChartPLTWindow(1)
        # chart_plt_w.line(self.parent.calculation.chart_v_y_data)
        # chart_plt_w.quad_regress(self.parent.calculation.chart_quad_regress_data)
        #
        # self.lst_Thread.append(MyThread(
        #     lambda: chart_plt_w.start())
        # )
        # self.ui.pushButton_8.clicked.connect(
        #     lambda: self.lst_Thread[3].start()
        # )

        self.ui.pushButton.clicked.connect(self.exit_w)
        # self.ui.pushButton_2.clicked.connect(self.view_table)

    def exit_w(self):
        self.table_loader_results_1.kwargs['block'] = False
        self.close()

    # def exec_(self) -> int:
    #     a = super().exec_()
    #     for i in self.lst_Thread:
    #         i.wait()
    #     return a

    def view_table(self):
        # self.parent.table_loader1.open_table()
        # self.parent.table_loader2.open_table()
        pass


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
