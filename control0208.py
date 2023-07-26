import os.path
import shutil
import tkinter as tk
from tkinter import filedialog#读取文件夹路径包
import os
import sys
import serial  # 需要调用串口库

from PyQt5 import QtCore, QtGui, QtWidgets, sip
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QWaitCondition, QMutex
import matplotlib
import pymeasure
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from pymeasure.instruments import Instrument, RangeException
from math import log,exp
from PyQt5.QtWidgets import QGridLayout, QMessageBox

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg # pyqt5的画布

#

import time
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import test_laser
import C2438
import N7761A
from PyQt5.QtWidgets import *
import sys
import numpy as np
import threading
import gui630
import aboutprogram
import matplotlib.ticker as mtick
from pm5b import PM5B
import  math
import K8163B

#创建画布类型
class MyMatplotlibFigure(FigureCanvasQTAgg):
    """
    创建一个画布类，并把画布放到FigureCanvasQTAgg
    """
    def __init__(self, width=4, heigh=3, dpi=100):
        plt.rcParams['figure.facecolor'] = 'white' # 设置窗体颜色
        plt.rcParams['axes.facecolor'] = 'white' # 设置绘图区颜色
        # 创建一个Figure,该Figure为matplotlib下的Figure，不是matplotlib.pyplot下面的Figure
        # 这里还要注意，width, heigh可以直接调用参数，不能用self.width、self.heigh作为变量获取，因为self.width、self.heigh 在模块中已经FigureCanvasQTAgg模块中使用，这里定义会造成覆盖
        self.figs = plt.figure(figsize=(width, heigh), dpi=dpi)

        super(MyMatplotlibFigure, self).__init__(self.figs) # 在父类种激活self.fig， 否则不能显示图像（就是在画板上放置画布）
        self.axes = self.figs.add_subplot(111) # 添加绘图区
        self.axes.grid(linestyle='-.')
        self.axes.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))


    #bandwith mat
    def mat_plot_drow_axes(self, t, s):
        """
        用清除画布刷新的方法绘图
        :return:
        """
        self.axes.cla() # 清除绘图区
        # self.axes.spines['top'].set_visible(False) # 顶边界不可见
        # self.axes.spines['right'].set_visible(False) # 右边界不可见
        # 设置左、下边界在（0，0）处相交
        # self.axes.spines['bottom'].set_position(('data', 0)) # 设置y轴线原点数据为 0
        # self.axes.spines['left'].set_position(('data', 0)) # 设置x轴线原点数据为 0

        self.axes.plot(t, s, 'o-r', linewidth=0.5,color ='tab:blue')
        self.axes.grid(linestyle='-.')
        self.axes.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
        # self.axes.yticks(np.arange())
        self.figs.canvas.draw() # 这里注意是画布重绘，self.figs.canvas
        self.figs.canvas.flush_events() # 画布刷新self.figs.canvas

    #iv mat
    def mat_plot_drow_axes2(self, t, s):
        """
        用清除画布刷新的方法绘图
        :return:
        """
        self.axes.cla() # 清除绘图区
        # self.axes.spines['top'].set_visible(False) # 顶边界不可见
        # self.axes.spines['right'].set_visible(False) # 右边界不可见
        # 设置左、下边界在（0，0）处相交
        # self.axes.spines['bottom'].set_position(('data', 0)) # 设置y轴线原点数据为 0
        # self.axes.spines['left'].set_position(('data', 0)) # 设置x轴线原点数据为 0

        self.axes.plot(t, s, 'o-r', linewidth=0.5,color ='tab:blue')
        self.axes.grid(linestyle='-.')
        self.axes.set_yscale("log", base=10)
        self.axes.set_ylim(1e-12,1e-2)
        self.figs.canvas.draw() # 这里注意是画布重绘，self.figs.canvas
        self.figs.canvas.flush_events() # 画布刷新self.figs.canvas
        self.axes.grid(linestyle='-.')

    #saturation mat
    def mat_plot_drow_axes_s(self, t, s1,s2):
        """
        用清除画布刷新的方法绘图
        :return:
        """
        self.axes.cla() # 清除绘图区
        # self.axes.spines['top'].set_visible(False) # 顶边界不可见
        # self.axes.spines['right'].set_visible(False) # 右边界不可见
        # 设置左、下边界在（0，0）处相交
        # self.axes.spines['bottom'].set_position(('data', 0)) # 设置y轴线原点数据为 0
        # self.axes.spines['left'].set_position(('data', 0)) # 设置x轴线原点数据为 0

        self.axes.plot(t, s1, 'o-r', linewidth=0.5, color='tab:blue')
        self.axes.plot(t, s1, '*-b', linewidth=0.5, color='tab:red')
        self.axes.grid(linestyle='-.')
        self.axes.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
        self.axes.set_xscale("log", base=10)
        # self.axes.set_ylim(1e-12,1e-2)
        self.figs.canvas.draw() # 这里注意是画布重绘，self.figs.canvas
        self.figs.canvas.flush_events() # 画布刷新self.figs.canvas


class MyWindow2(QtWidgets.QWidget,aboutprogram.Ui_Dialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet('background-color: white;')


class MyWindow(QtWidgets.QMainWindow, gui630.Ui_MainWindow):
    xb=[]
    yb=[]


    flag=0
    xs=[]
    ys=[]
    ys1=[]
    xiv=[]
    yiv=[]
    j=0

    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.actionClear.triggered.connect(self.clear)
        self.actionAbout_Program.triggered.connect(self.about_program)
        self.actionAbout.triggered.connect(self.about)



        #bandwith页面连接2
        # 添加画布
        self.canvas = MyMatplotlibFigure(width=5, heigh=3, dpi=100)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        self.hboxlayout = QVBoxLayout(self.groupBox_7)
        self.h = QVBoxLayout(self.frame_40)
        self.hboxlayout.addSpacing(5)
        self.hboxlayout.addWidget(self.canvas)
        self.h.addWidget(self.mpl_toolbar,)
        self.canvas.figs.supylabel('RF Power (dBm)', fontsize=12, fontfamily='Calibri')
        self.canvas.figs.supxlabel('Frequency (GHz)', fontsize=12, fontfamily='Calibri')
        self.canvas.figs.subplots_adjust(left=0.14, right=0.9, bottom=0.14)




        #按钮功能

        self.b_lasebox_p.editingFinished.connect(self.b_laserpow_set)
        self.b_laserbox_fr.editingFinished.connect(self.b_laserfr_set)
        self.b_laserbutton_on.clicked.connect(self.b_laseron)
        self.b_laserbutton_off.clicked.connect(self.b_laseroff)
        self.b_smbox_sv.editingFinished.connect(self.b_smsv_set)
        self.b_smbox_com.editingFinished.connect(self.b_smcom_set)
        self.b_smbutton_able.clicked.connect(self.b_smable)
        self.b_pmbox_fr.editingFinished.connect(self.b_pmfr_set)
        self.b_atbox_p.editingFinished.connect(self.b_atp_set)
        self.b_manubutton.clicked.connect(self.m)
        self.b_savebutton.clicked.connect(self.b_save)
        self.b_autobutton_begin.clicked.connect(self.a)
        self.b_autobutton_stop.clicked.connect(self.b_autostop)
        self.b_autobutton_conti.clicked.connect(self.c)
        self.b_clearbutton.clicked.connect(self.b_clear)


        # saturation页面连接
        # 添加画布
        self.canvas2 = MyMatplotlibFigure(width=5, heigh=4, dpi=100)
        self.mpl_toolbar2 = NavigationToolbar(self.canvas2, self)
        self.hboxlayout2 = QVBoxLayout(self.groupBox_13)
        self.h2 = QVBoxLayout(self.frame_42)
        self.hboxlayout2.addSpacing(5)
        self.hboxlayout2.addWidget(self.canvas2)
        self.h2.addWidget(self.mpl_toolbar2)
        self.canvas2.figs.supxlabel('Photocurrent (mA)', fontsize=12, fontfamily='Calibri')
        self.canvas2.figs.supylabel('RF Power (dBm)', fontsize=12, fontfamily='Calibri')
        self.canvas2.figs.subplots_adjust(left=0.14, right=0.9, bottom=0.14)

        # 按钮功能
        self.s_lasebox_p.editingFinished.connect(self.s_laserpow_set)
        self.s_laserbox_fr.editingFinished.connect(self.s_laserfr_set)
        self.s_laserbutton_on.clicked.connect(self.s_laseron)
        self.s_laserbutton_off.clicked.connect(self.s_laseroff)
        self.s_smbox_sv.editingFinished.connect(self.s_smsv_set)
        self.s_smbox_com.editingFinished.connect(self.s_smcom_set)
        self.s_smbutton_able.clicked.connect(self.s_smable)
        self.s_pmbox_fr.editingFinished.connect(self.s_pmfr_set)
        self.s_atbox_p.editingFinished.connect(self.s_atp_set)
        self.s_manubutton.clicked.connect(self.s_manu)
        # self.s_manubutton.clicked.connect(self.cal)
        self.s_savebutton.clicked.connect(self.s_save)
        self.spinBox.editingFinished.connect(self.s_beat)
        self.s_clearbutton.clicked.connect(self.s_clear)
        self.s_stopbutton.clicked.connect(self.s_stop)

        #I-V界面的链接
        # 添加画布
        self.canvas3 = MyMatplotlibFigure(width=5, heigh=4, dpi=100)
        self.mpl_toolbar3 = NavigationToolbar(self.canvas3, self)
        self.hboxlayout3 = QVBoxLayout(self.groupBox_15)
        self.h3 = QVBoxLayout(self.frame_43)
        self.hboxlayout3.addSpacing(5)
        self.hboxlayout3.addWidget(self.canvas3)
        self.h3.addWidget(self.mpl_toolbar3)
        self.canvas3.figs.supxlabel('Source Voltage (V)', fontsize=12, fontfamily='Calibri')
        self.canvas3.figs.supylabel('Current (A)', fontsize=12, fontfamily='Calibri')
        self.canvas3.figs.subplots_adjust(left=0.14, right=0.9, bottom=0.14)
        # 按钮功能
        self.iv_smBox_sv.editingFinished.connect(self.iv_smsv_set)
        self.iv_smBox_com.editingFinished.connect(self.iv_smcom_set)
        self.iv_ablebutton.clicked.connect(self.iv_able)
        self.iv_swbutton.clicked.connect(self.iv_sweep)
        self.iv_savebutton.clicked.connect(self.iv_save)
        self.iv_clearbutton.clicked.connect(self.iv_clear)
        self.iv_stopbutton.clicked.connect(self.iv_stop)

        # self.statusBar().show()
        self.showMaximized()
        # # desktop=QApplication.desktop()
        # # rect=desktop.availableGeometry()
        # # print(rect)
        # self.setGeometry(0,0,960,200)




    #bandwidth里的方法
    #b_laser模块
    def b_laserpow_set(self):
        try:
            address = self.b_laserbox_gpib.currentText()
            power=self.b_lasebox_p.value()
            laser = K8163B.Keysight8163B("GPIB0::"+address+"::INSTR")  # 连接仪
            laser.set_laserpow=power
        except:
            QMessageBox.critical(self, "error", "laser error")

    def b_laserfr_set(self):
        try:
            address = self.b_laserbox_gpib.currentText()
            laser = K8163B.Keysight8163B("GPIB0::" + address + "::INSTR")  # 连接仪
            fr = self.b_laserbox_fr.value() * 1000
            l = 299792458.0 / (fr + 0.5)
            l1 = round(l, 3)
            self.lineEdit_b_laser.setText(str(l1))
            laser.set_laserwav=l1

        except:
            QMessageBox.critical(self, "error", "laser error")

    def b_laseron(self):
        address = self.b_laserbox_gpib.currentText()
        laser = K8163B.Keysight8163B("GPIB0::" + address + "::INSTR")
        try:
           laser.active_laser=1
        except:
            QMessageBox.critical(self, "error", "laser error")

    def b_laseroff(self):
        address = self.b_laserbox_gpib.currentText()
        laser = K8163B.Keysight8163B("GPIB0::" + address + "::INSTR")
        try:
            laser.active_laser=0
        except:
            QMessageBox.critical(self, "error", "laser error")



    #b_sm模块
    def b_smsv_set(self):
        try:
            address = self.b_smbox_gpib.currentText()
            keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address) + "::INSTR")
            sv = self.b_smbox_sv.value()

            keithley.source_voltage = sv
        except:
            QMessageBox.critical(self, "error", "source meter error")

    def b_smcom_set(self):
        try:
            address = self.b_smbox_gpib.currentText()
            keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address) + "::INSTR")
            comp=self.b_smbox_com.value()
            comp=comp*0.001
            keithley.compliance_current = comp
        except:
            QMessageBox.critical(self, "error", "source meter error")

    def b_smable(self):
        self.flag = 0
        try:
            address = self.b_smbox_gpib.currentText()
            keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address) + "::INSTR")
            keithley.measure_current()
            keithley.enable_source()
            # while True:
            #     if self.flag==0:
            output = keithley.current
            output1 = output * 1e3
            output2 = round(output1, 3)
            self.lineEdit_b_sm.setText(str(output2))

            QApplication.processEvents()
            time.sleep(1)
        except:
            QMessageBox.critical(self, "error", "source meter error")

    def b_pmfr_set(self):

        fr = self.b_pmbox_fr.value()
        try:
            address1 = self.b_pmbox_gpib.currentText()
            ceyear = C2438.Ceyear2438("GPIB0::" + str(address1) + "::INSTR")
            # ceyear.clear
            ceyear.freq = str(fr) + "GHz"
            output =ceyear.measure_show
            output1 = round(output, 3)
            self.lineEdit_b_pm.setText(str(output1))

        except:
            QMessageBox.critical(self, "error", "power meter error")

    def b_atp_set(self):
        a = self.b_atbox_p.value()  # 获取a框设置的值
        address = self.b_atbox_gpib.currentText()  # 获取gpib地址

        try:
            laser = N7761A.KeysightN7761A("GPIB0::" + str(address) + "::INSTR")
            laser.at_factor = a
            time.sleep(1)
            laser.output_on = "ON"

            output = laser.current_power
            output1 = round(output, 3)
            self.lineEdit_b_at.setText(str(output1))
        except:
            QMessageBox.critical(self, "error", "attenuator error")


        # 仅测试时使用函数
    def cal(self):
        address3 = self.s_pmbox_fr.value()
        address1 = self.s_laserbox_fr.value()
        self.ys.append(address3)
        self.xs.append(address1)
        x1 = [1,2,3,4,5]
        y1 = [1,2,3,4,5]
        y2=[]
        print(x1)
        print(y1)
        self.statusbar.showMessage('Running, frequency(GHz)=%s,RF power(dB)=%s' % (address1, address3))

        for i in range(0, len(x1)):

            # x1.append(self.xs[i])
            # y1.append(self.ys[i])
            y2.append(10 * np.log10(((x1[i]) * (x1[i]) * 25) / 0.001))

        self.canvas2.figs.supylabel('RF power(dB)', fontsize=5)
        self.canvas2.figs.suptitle('RF power(dB)')
        self.canvas2.figs.supxlabel('frequency(GHz)')

        self.canvas2.mat_plot_drow_axes_s(x1, y1,y2)

    def cal2(self):

        address1 = self.b_autobox_begin.value()
        address1_stop=self.b_autobox_stop.value()
        address3 = self.b_pmbox_fr.value()
        num=address1_stop-address1+1
        address1=address1-1
        begin_fr = self.b_autobox_begin.value()
        stop_fr = self.b_autobox_stop.value()
        address1=begin_fr
        while self.flag==0:
            for i in range(int(begin_fr),int(stop_fr)):
                if self.flag==1:
                    break
                address1+=1
                self.yb.append(address1)
                self.xb.append(address3)
                x1 = []
                y1 = []

                for i in range(0, len(self.xb)):
                    x1.append(self.xb[i])
                    y1.append(self.yb[i])

                self.canvas.figs.supxlabel('frequency(GHz)',fontsize=9,fontfamily='Calibri')
                self.canvas.figs.supylabel('RF Power(dBm)',fontsize=9,fontfamily='Calibri')
                self.canvas.figs.subplots_adjust(left=0.14, right=0.9,bottom=0.14)

                self.canvas.mat_plot_drow_axes(x1, y1)
                j=i
                time.sleep(5)
        while self.flag==1:
            time.sleep(5)
        while self.flag==2:
            begin_fr = self.b_autobox_begin.value()
            stop_fr = self.b_autobox_stop.value()
            if begin_fr <= j:
                begin_fr = begin_fr
            else:
                begin_fr = j
            for i in range(int(begin_fr), int(stop_fr)):
                if self.flag == 1:
                    break
                begin_fr += 1
                self.yb.append(begin_fr)
                self.xb.append(address3)
                x1 = []
                y1 = []

                for i in range(0, len(self.xb)):
                    x1.append(self.xb[i])
                    y1.append(self.yb[i])

                self.canvas.figs.supxlabel('frequency(GHz)', fontsize=9, fontfamily='Calibri')
                self.canvas.figs.supylabel('RF Power(dBm)', fontsize=9, fontfamily='Calibri')
                self.canvas.figs.subplots_adjust(left=0.14, right=0.9, bottom=0.14)

                self.canvas.mat_plot_drow_axes(x1, y1)

                time.sleep(5)
            self.flag=0



    #b_manualmode方法
    def b_manu(self):
        address3 = self.b_pmbox_gpib.currentText()
        address1 = self.b_laserbox_gpib.currentText()
        laser = K8163B.Keysight8163B("GPIB0::" + address1 + "::INSTR")  # 连接仪
        try:
            self.statusbar.showMessage('Running')
            fr1 = self.b_laserbox_fr.value()+0.001
            self.b_laserbox_fr.setValue(fr1)
            fr = fr1 * 1000
            l = 299792458.0 / (fr + 0.5)
            l1 = round(l, 3)
            self.lineEdit_b_laser.setText(str(l1))
            laser.set_laserwav=l1

            ceyear = C2438.Ceyear2438("GPIB0::" + str(address3) + "::INSTR")  # 连接仪器
            fr1 = (l1 - 1550) * 125
            self.b_pmbox_fr.setValue(abs(fr1))  # 将频率值输入pm

            ceyear.freq = str(abs(fr1)) + "GHz"

            time.sleep(20)

            tmp = []
            for i in range(0, 4):
                output = ceyear.measure_show
                tmp.append(round(output, 3))

            x = np.array(tmp)
            if (x.std() < 1):
                output1 = ceyear.measure_show
                output = round(output1, 3)
                self.lineEdit_b_pm.setText(str(output))
                QApplication.processEvents()
                time.sleep(1)
                self.yb.append(output)
                self.xb.append(abs(fr1))
                # file.write(str(fr1))
                # file.write("\t")
                # file.write(str(output))  # 将数组数据第0号元素写入txt文件中
                # file.write("\n")
                x1 = []
                y1 = []
                self.statusbar.showMessage('Completed                                    Frequency (GHz)=%s,   RF Power (dBm)=%s' % (abs(round(fr1,1)), output))
                self.statusbar.setToolTipDuration(500)
                for i in range(0, len(self.xb)):
                    x1.append(self.xb[i])
                    y1.append(self.yb[i])

                self.canvas.figs.supylabel('RF Power (dBm)',fontsize=12,fontfamily='Calibri')
                self.canvas.figs.supxlabel('Frequency (GHz)',fontsize=12,fontfamily='Calibri')
                self.canvas.figs.subplots_adjust(left=0.14, right=0.9,bottom=0.14)
                self.canvas.mat_plot_drow_axes(x1, y1)

            else:
                time.sleep(5)
                QMessageBox.warning(self, title='Warning', text='Laser not stable')
        except:
            QMessageBox.critical(self, "error", "error")

    def m(self):
        t = threading.Thread(target=self.b_manu, name='t')
        t.start()



    def b_save(self):
        try:
            # 实例化
            root = tk.Tk()
            root.withdraw()
            # 设置存储位置、获取文件夹路径
            f_path = filedialog.asksaveasfilename(filetypes=[("txt", ".txt")], defaultextension='.tif')

            # print('\n获取的文件地址：', f_path)
            if f_path:
                file = open(f_path, mode='w')



                print(self.xb)
                # 将数据存储至文件夹
                for i in range(0, len(self.xb)):
                    file.write(str(self.xb[i]))
                    file.write("\t")
                    file.write(str(self.yb[i]))  # 将数组数据第0号元素写入txt文件中
                    file.write("\n")
                    i += 1

            # 将数组清空，并清空画布
            # self.xb.clear()
            # self.yb.clear()
            # self.canvas.figs.supylabel('RF power(dB)',fontsize=9)
            # self.canvas.figs.supxlabel('frequency(GHz)',fontsize=9)
            # self.canvas.figs.subplots_adjust(left=0.2, right=0.9)
            # self.canvas.mat_plot_drow_axes(self.xb, self.yb)
            #
        except:
            QMessageBox.critical(self, "error", "save error")


    def b_autobegin(self):
        try:
            self.statusbar.showMessage('Running')
            address1 = self.b_laserbox_gpib.currentText()
            laser = K8163B.Keysight8163B("GPIB0::" + address1 + "::INSTR")  # 连接仪
            laser.active_laser=1
            address3 = self.b_pmbox_gpib.currentText()
            begin_fr=self.b_autobox_begin.value()
            stop_fr=self.b_autobox_stop.value()
            # num=(stop_fr-begin_fr)+1
            self.b_laserbox_fr.setValue(193.413+begin_fr*0.001)
            while self.flag == 0:
                for i in range(int(begin_fr),int(stop_fr)+1):
                    # while self.flag == 1:
                    #     time.sleep(5)
                    #     if self.flag == 2:
                    #         self.flag = 0
                    #         break
                    #flag=1 stop


                    if self.flag ==1:
                        break
                    self.j=i+1
                    fr1 = self.b_laserbox_fr.value() + 0.001
                    self.b_laserbox_fr.setValue(fr1)
                    fr = fr1 * 1000
                    l = 299792458.0 / (fr + 0.5)
                    l1 = l
                    self.lineEdit_b_laser.setText(str(round(l, 3)) )
                    laser.set_laserwav=l
                    ceyear = C2438.Ceyear2438("GPIB0::" + str(address3) + "::INSTR")  # 连接仪器
                    fr1 = (l1 - 1550) * 125
                    self.b_pmbox_fr.setValue(abs(fr1))  # 将频率值输入pm
                    # ceyear.clear
                    ceyear.freq = str(abs(fr1)) + "GHz"
                    time.sleep(20)

                    tmp = []
                    #判断激光器是否稳定
                    for i in range(0, 4):
                        output = ceyear.measure_show
                        tmp.append(round(output, 3))

                    x = np.array(tmp)
                    if (x.std() < 1):
                        output1 = ceyear.measure_show
                        output = round(output1, 3)
                        self.lineEdit_b_pm.setText(str(output))
                        QApplication.processEvents()
                        time.sleep(1)
                        self.yb.append(output)
                        self.xb.append(abs(fr1))
                        x1 = []
                        y1 = []
                        self.statusbar.showMessage('Runing                                    Frequency (GHz)=%s,   RF Power (dBm)=%s' % (abs(round(fr1,1)), output))
                        # self.statusbar.setToolTipDuration(30000)
                        for i in range(0, len(self.xb)):
                            x1.append(self.xb[i])


                            y1.append(self.yb[i])

                        self.canvas.figs.supxlabel('Frequency (GHz)',fontsize=12,fontfamily='Calibri')
                        self.canvas.figs.supylabel('RF Power (dBm)',fontsize=12,fontfamily='Calibri')
                        self.canvas.figs.subplots_adjust(left=0.14, right=0.9,bottom=0.14)
                        self.canvas.mat_plot_drow_axes(x1, y1)

                    else:
                        time.sleep(5)
                        QMessageBox.warning(self, title='Warning', text='Laser not stable')

                break
            # while self.flag ==1:
            #     time.sleep(5)

            self.flag = 0
            self.statusbar.showMessage('Completed')
            self.statusbar.setToolTipDuration(5000)
        except:
            QMessageBox.critical(self, "error", "error")

    def b_autostop(self):
        self.flag=1

    def b_autoconti(self):
        try:
            self.statusbar.showMessage('Running')
            address1 = self.b_laserbox_gpib.currentText()
            address3 = self.b_pmbox_gpib.currentText()
            ser1 = serial.Serial()  # 生成串口
            ser1.parity = serial.PARITY_NONE
            ser1.stopbits = serial.STOPBITS_ONE
            ser1.baudrate = 9600  # 设置串口波特率
            ser1.port = str(address1)  # 设置串口号
            ser1.timeout = 0.1  # 设置串口通信超时时间
            ser1.close()  # 先关闭串口，以免串口被占用
            ser1.open()  # 打开串口
            begin_fr=self.b_autobox_begin.value()
            stop_fr=self.b_autobox_stop.value()
            # num=(stop_fr-begin_fr)+1
            if begin_fr > self.j:
                start = begin_fr
            else:
                start = self.j
            self.b_laserbox_fr.setValue(193.413+start*0.001)
            self.flag=2
            while self.flag == 2:
                begin_fr = self.b_autobox_begin.value()
                stop_fr = self.b_autobox_stop.value()
                if self.flag==1:
                    break

                for i in range(int(start), int(stop_fr)+1):

                    # while self.flag == 1:
                    #     time.sleep(5)
                    #     if self.flag == 2:
                    #         self.flag = 0
                    #         break
                    # flag=1 stop

                    if self.flag == 1:
                        break
                    self.j = i + 1
                    fr1 = self.b_laserbox_fr.value() + 0.001
                    self.b_laserbox_fr.setValue(fr1)
                    fr = fr1 * 1000
                    l = 299792458.0 / (fr + 0.5)
                    l1 = l
                    self.lineEdit_b_laser.setText(str(round(l, 3)))
                    test_laser.set_lenth(ser1, fr)
                    # ceyear = C2438.Ceyear2438("GPIB0::" + str(address3) + "::INSTR")  # 连接仪器
                    # fr1 = (l1 - 1550) * 125
                    # self.b_pmbox_fr.setValue(abs(fr1))  # 将频率值输入pm
                    #
                    # ceyear.freq = str(abs(fr1)) + "GHz"
                    # time.sleep(20)

                    tmp = []
                    # 判断激光器是否稳定
                    # for i in range(0, 4):
                    #     output = ceyear.measure_show
                    #     tmp.append(round(output, 3))
                    #
                    # x = np.array(tmp)
                    # if (x.std() < 1):
                    #     output1 = ceyear.measure_show
                    #     output = round(output1, 3)
                    #     self.lineEdit_b_pm.setText(str(output))
                    #     QApplication.processEvents()
                    #     time.sleep(1)
                    #     self.yb.append(output)
                    #     self.xb.append(abs(fr1))
                    #     x1 = []
                    #     y1 = []
                    #     self.statusbar.showMessage(
                    #         'Runing                                    Frequency (GHz)=%s,   RF Power (dBm)=%s' % (abs(round(fr1, 1)), output))
                    #     # self.statusbar.setToolTipDuration(30000)
                    #     for i in range(0, len(self.xb)):
                    #         x1.append(self.xb[i])
                    #
                    #         y1.append(self.yb[i])
                    #
                    #     self.canvas.figs.supxlabel('Frequency (GHz)', fontsize=12, fontfamily='Calibri')
                    #     self.canvas.figs.supylabel('RF Power (dBm)', fontsize=12, fontfamily='Calibri')
                    #     self.canvas.figs.subplots_adjust(left=0.14, right=0.9, bottom=0.14)
                    #     self.canvas.mat_plot_drow_axes(x1, y1)
                    #
                    # else:
                    #     time.sleep(5)
                    #     QMessageBox.warning(self, title='Warning', text='Laser not stable')

                break
            self.flag = 0
            self.statusbar.showMessage('Completed')
            self.statusbar.setToolTipDuration(5000)
        except:
            QMessageBox.critical(self, "error", "error")


    def a(self):
        t = threading.Thread(target=self.b_autobegin, name='t')
        t.start()

    def c(self):
        t = threading.Thread(target=self.b_autoconti, name='t')
        t.start()

    def clear(self):
        # 将数组清空，并清空画布
        self.xb.clear()
        self.yb.clear()
        self.xs.clear()
        self.ys.clear()
        self.xiv.clear()
        self.yiv.clear()
        # self.canvas.figs.supylabel('RF power(dB)')
        # self.canvas.figs.supxlabel('frequency(GHz)')
        self.canvas.mat_plot_drow_axes(self.xb, self.yb)
        self.canvas2.mat_plot_drow_axes(self.xs, self.ys)
        self.canvas3.mat_plot_drow_axes(self.xiv, self.yiv)

    def b_clear(self):
        self.xb.clear()
        self.yb.clear()
        self.canvas.mat_plot_drow_axes(self.xb, self.yb)



    #saturation里的方法
    # s_laser模块
    def s_laserpow_set(self):
        try:
            address = self.s_laserbox_gpib.currentText()
            pow = self.s_lasebox_p.value()
            pow1 = int(pow * 100)
            ser = serial.Serial()  # 生成串口
            ser.parity = serial.PARITY_NONE
            ser.stopbits = serial.STOPBITS_ONE
            ser.baudrate = 9600  # 设置串口波特率
            ser.port = str(address)  # 设置串口号
            ser.timeout = 0.1  # 设置串口通信超时时间
            ser.close()  # 先关闭串口，以免串口被占用
            ser.open()  # 打开串口
            strSerial = ''
            test_laser.set_power(ser, pow1)
        except:
            QMessageBox.critical(self, "error", "error")

    def s_laserfr_set(self):
        try:
            address = self.s_laserbox_gpib.currentText()
            fr = self.s_laserbox_fr.value() * 1000

            print(int(fr))
            l = 299792458.0 / (fr + 0.5)
            l1 = round(l, 3)
            self.lineEdit_s_laser.setText(str(l1) )

            ser = serial.Serial()  # 生成串口
            ser.parity = serial.PARITY_NONE
            ser.stopbits = serial.STOPBITS_ONE
            ser.baudrate = 9600  # 设置串口波特率
            ser.port = str(address)  # 设置串口号
            ser.timeout = 0.1  # 设置串口通信超时时间
            ser.close()  # 先关闭串口，以免串口被占用
            ser.open()  # 打开串口
            strSerial = ''
            test_laser.set_lenth(ser, int(fr))
        except:
            QMessageBox.critical(self, "error", "error")

    def s_laseron(self):
        address = self.s_laserbox_gpib.currentText()
        try:
            ser = serial.Serial()  # 生成串口
            ser.parity = serial.PARITY_NONE
            ser.stopbits = serial.STOPBITS_ONE
            ser.baudrate = 9600  # 设置串口波特率
            ser.port = str(address)  # 设置串口号
            ser.timeout = 0.1  # 设置串口通信超时时间
            ser.close()  # 先关闭串口，以免串口被占用
            ser.open()  # 打开串口
            # print(ser.is_open)
            if (ser.is_open):
                test_laser.open(ser)
        except:
            QMessageBox.critical(self, "错误", "s_laser error")

    def s_laseroff(self):
        address = self.s_laserbox_gpib.currentText()
        try:
            ser = serial.Serial()  # 生成串口
            ser.parity = serial.PARITY_NONE
            ser.stopbits = serial.STOPBITS_ONE
            ser.baudrate = 9600  # 设置串口波特率
            ser.port = str(address)  # 设置串口号
            ser.timeout = 0.1  # 设置串口通信超时时间
            ser.close()  # 先关闭串口，以免串口被占用
            ser.open()  # 打开串口
            strSerial = ''
            test_laser.close(ser)
        except:
            QMessageBox.critical(self, "error", "s_laser error")

    # s_sm模块
    def s_smsv_set(self):
        try:
            address = self.s_smbox_gpib.currentText()
            sv = self.s_smbox_sv.value()
            keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address) + "::INSTR")
            keithley.source_voltage = sv
        except:
            QMessageBox.critical(self, "error", "s_source meter error")

    def s_smcom_set(self):
        try:
            address = self.s_smbox_gpib.currentText()
            comp = self.s_smbox_com.value()
            comp=comp*0.001
            keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address) + "::INSTR")
            keithley.compliance_current = comp
        except:
            QMessageBox.critical(self, "error", "s_source meter error")

    def s_smable(self):
        address = self.s_smbox_gpib.currentText()
        self.flag = 0
        try:
            keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address) + "::INSTR")
            keithley.measure_current()
            keithley.enable_source()
            # while True:
            #     if self.flag==0:
            output = keithley.current
            output1 = output * 1e3
            output2 = round(output1, 3)
            self.lineEdit_s_sm.setText(str(output2))

            QApplication.processEvents()
            time.sleep(1)
        except:
            QMessageBox.critical(self, "error", "s_source meter error")

    def s_pmfr_set(self):
        address = self.s_pmbox_gpib.currentText()
        fr = self.s_pmbox_fr.value()
        try:
            ceyear = C2438.Ceyear2438("GPIB0::" + str(address) + "::INSTR")
            # ceyear.clear
            ceyear.freq = str(fr) + "GHz"
            output = ceyear.measure_show
            output1 = round(output, 3)
            self.lineEdit_s_pm.setText(str(output1))

        except:
            QMessageBox.critical(self, "error", "s_power meter error")

    def s_atp_set(self):
        a = self.s_atbox_p.value()  # 获取a框设置的值
        address = self.s_atbox_gpib.currentText()  # 获取gpib地址


        try:
            laser = N7761A.KeysightN7761A("GPIB0::" + str(address) + "::INSTR")
            laser.at_factor=a
            time.sleep(1)
            laser.output_on = "ON"
            output = laser.current_power
            output1 = round(output, 3)
            self.lineEdit_s_at.setText(str(output1))
        except:
            QMessageBox.critical(self, "error", "s_at error")


    #s_manualmode方法
    def s_beat(self):
        try:
            address2 = self.s_pmbox_gpib.currentText()  # pm的地址
            address4 = self.s_laserbox_gpib.currentText()
            beat = self.spinBox.value()
            fr = 193.414 * 1000 + beat
            l = 299792458.0 / (fr + 0.5)
            l1 = round(l, 3)
            self.lineEdit_s_laser.setText(str(l1))
            self.s_laserbox_fr.setValue(fr*0.001)


            ser = serial.Serial()  # 生成串口
            ser.parity = serial.PARITY_NONE
            ser.stopbits = serial.STOPBITS_ONE
            ser.baudrate = 9600  # 设置串口波特率
            ser.port = str(address4)  # 设置串口号
            ser.timeout = 0.1  # 设置串口通信超时时间
            ser.close()  # 先关闭串口，以免串口被占用
            ser.open()  # 打开串口
            strSerial = ''
            test_laser.set_lenth(ser, int(fr))

            ceyear = C2438.Ceyear2438("GPIB0::" + str(address2) + "::INSTR")
            ceyear.freq = str(beat) + "GHz"
            output = ceyear.measure_show
            output1 = round(output, 3)
            self.lineEdit_s_pm.setText(str(output1))
            self.s_pmbox_fr.setValue(beat)


        except:
            QMessageBox.critical(self, "error", "error")

    def s_manu(self):
        address1 = self.s_atbox_gpib.currentText()  # 衰减器地址
        address2 = self.s_pmbox_gpib.currentText()  # pm的地址
        address3 = self.s_smbox_gpib.currentText()  # sm的地址

        try:
            self.statusbar.showMessage('Running')
            if self.checkBox.isChecked():
                a = self.s_atbox_p.value()

                AT = N7761A.KeysightN7761A("GPIB0::" + str(address1) + "::INSTR")


                time.sleep(1)

                step = self.comboBox.currentText()
                step1 = float(step)
                a = a - step1
                self.s_atbox_p.setValue(a)
                AT.at_factor = a
                AT.output_on = "ON"
                # time.sleep(0.5)
                AT_output = AT.current_power
                self.lineEdit_s_at.setText(str(round(AT_output, 3)))

                ceyear = C2438.Ceyear2438("GPIB0::" + str(address2) + "::INSTR")
                # ceyear.clear
                pm_output1 = ceyear.measure_show
                pm_output = round(pm_output1, 3)
                self.lineEdit_s_pm.setText(str(pm_output))

                keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address3) + "::INSTR")
                keithley.measure_current()
                keithley.enable_source()
                sm_output = keithley.current  # 获得电流A
                sm_output1 = sm_output * 1e3  # 转为mA
                sm_output2 = round(sm_output1, 3)
                self.lineEdit_s_sm.setText(str(sm_output2))

                # 作图
                self.xs.append(sm_output2)
                self.ys.append(pm_output)
                x1 = []
                y1 = []
                y2 = []
                self.statusbar.showMessage('Photocurrent (mA)=%s,   RF Power (dBm)=%s' % (abs(round(sm_output2,3)), pm_output))
                self.statusbar.setToolTipDuration(5000)
                for i in range(0, len(self.xs)):
                    x1.append(abs(self.xs[i]))
                    y1.append(self.ys[i])
                    y2.append( 10*np.log10( ((self.xs[i])*(self.xs[i])*25 )/0.001 ))
                    i += 1

                self.canvas2.figs.supxlabel('Photocurrent (mA)',fontsize=12,fontfamily='Calibri')
                self.canvas2.figs.supylabel('RF Power (dBm)',fontsize=12,fontfamily='Calibri')
                self.canvas2.figs.subplots_adjust(left=0.14, right=0.9,bottom=0.14)
                self.canvas2.mat_plot_drow_axes_s(x1, y1, y2)

            else:
                self.statusbar.showMessage('Running')
                ceyear = C2438.Ceyear2438("GPIB0::" + str(address2) + "::INSTR")  # 连接仪器
                # ceyear.clear
                pm_output1 = ceyear.measure_show
                pm_output = round(pm_output1, 3)
                self.lineEdit_s_pm.setText(str(pm_output))

                keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address3) + "::INSTR")
                keithley.measure_current()
                keithley.enable_source()
                sm_output = keithley.current  # 获得电流A
                sm_output1 = sm_output * 1e3  # 转为mA
                sm_output2 = round(sm_output1, 3)
                self.lineEdit_s_sm.setText(str(sm_output2))

                # 作图
                self.xs.append(sm_output2)
                self.ys.append(pm_output)

                x1 = []
                y1 = []
                y2 = []
                self.statusbar.showMessage('Photocurrent (mA)=%s,   RF Power (dBm)=%s' % (abs(round(sm_output2,3)), pm_output))
                # self.statusbar.setToolTipDuration(30000)
                self.statusbar.setToolTipDuration(5000)
                for i in range(0, len(self.xs)):
                    x1.append(abs(self.xs[i]))
                    y1.append(self.ys[i])
                    y2.append( 10*np.log10( ((self.xs[i])*(self.xs[i])*25 )/0.001 ))
                    i += 1
                self.canvas2.figs.supxlabel('Photocurrent (mA)',fontsize=12,fontfamily='Calibri')
                self.canvas2.figs.supylabel('RF Power (dBm)',fontsize=12,fontfamily='Calibri')
                self.canvas2.figs.subplots_adjust(left=0.14, right=0.9,bottom=0.14)

                self.canvas2.mat_plot_drow_axes_s(x1, y1, y2)

        except:
            QMessageBox.critical(self, "error", "error")
            AT = N7761A.KeysightN7761A("GPIB0::" + str(address1) + "::INSTR")


    def s_save(self):
        try:
            # 实例化
            root = tk.Tk()
            root.withdraw()
            # 设置存储位置、获取文件夹路径
            f_path = filedialog.asksaveasfilename(filetypes=[("txt", ".txt")], defaultextension='.tif')

            if f_path:
                file = open(f_path, mode='w')
                # 将数据存储至文件夹
                for i in range(0, len(self.xs)):
                    file.write(str(self.xs[i]))
                    file.write("\t")
                    file.write(str(self.ys[i]))  # 将数组数据第0号元素写入txt文件中

                    # file.write("\t")
                    # file.write(str(self.ys1[i]))
                    file.write("\n")
                    i += 1

            # 将数组清空，并清空画布
            # self.xs.clear()
            # self.ys.clear()
            # self.ys1.clear()
            # self.canvas2.mat_plot_drow_axes(self.xb, self.yb)
        except:
            QMessageBox.critical(self, "error", "save error")

    def s_clear(self):
        self.xs.clear()
        self.ys.clear()
        self.ys1.clear()
        self.canvas2.mat_plot_drow_axes_s(self.xs, self.ys,self.ys1)

    def s_stop(self):
        address = self.s_atbox_gpib.currentText()  # 衰减器地址
        a = self.s_atbox_p.value()
        a = a + 10
        AT = N7761A.KeysightN7761A("GPIB0::" + str(address) + "::INSTR")
        AT.at_factor = a
        self.s_atbox_p.setValue(a)
        AT.output_on = "ON"
        time.sleep(2)
        AT_output = AT.current_power
        self.lineEdit_s_at.setText(str(round(AT_output, 3)))

    #iv页面函数
    def iv_smsv_set(self):
        try:
            address = self.iv_smBox_gpib.currentText()
            sv = self.iv_smBox_sv.value()
            keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address) + "::INSTR")
            keithley.source_voltage = sv
        except:
            QMessageBox.critical(self, "error", "iv error")

    def iv_smcom_set(self):
        try:
            address = self.iv_smBox_gpib.currentText()
            comp=self.iv_smBox_com.value()
            comp = comp * 0.001
            keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address) + "::INSTR")
            keithley.compliance_current = comp
        except:
            QMessageBox.critical(self, "error", "iv error")

    def iv_able(self):
        address = self.iv_smBox_gpib.currentText()
        self.flag = 0
        try:
            keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address) + "::INSTR")
            keithley.measure_current()
            keithley.enable_source()
            # while True:
            #     if self.flag==0:
            output = keithley.current
            output1 = output * 1e3
            output2 = round(output1, 3)
            self.lineEdit_iv_c.setText(str(output2))

            QApplication.processEvents()
            time.sleep(1)
            # elif self.flag==1:
            #     break
        except:
            QMessageBox.critical(self, "error", "iv error")

    def iv_sweep(self):
        self.flag=0
        start_v = self.iv_smBox_start.value()
        stop_v=self.doubleSpinBox.value()
        wait_time=self.iv_timeBox.value()
        wait_time=wait_time*0.001
        # comp = self.iv_smBox_com.value()
        address = self.iv_smBox_gpib.currentText()
        try:
            keithley = pymeasure.instruments.keithley.Keithley2400("GPIB0::" + str(address) + "::INSTR")

            keithley.enable_source()

            # keithley.compliance_current = comp
            point=abs(stop_v*10-start_v*10)+1
            while self.flag==0:
                for i in range(int(point)):
                    if self.flag ==1:
                        break
                    keithley.source_voltage = start_v
                    time.sleep(wait_time)
                    keithley.measure_current()
                    output = keithley.current
                    # output1 = output * 1e3
                    # output2 = round(output1, 3)
                    # output2=np.power(10,output2)
                    self.iv_smBox_sv.setValue(start_v)
                    self.yiv.append(abs(output))
                    self.xiv.append(start_v)
                    x1 = []
                    y1 = []
                    self.statusbar.showMessage('Runing                                    Source Voltage (V)=%s,   Current (A)=%s' % (round(start_v,1), output))

                    for i in range(0, len(self.xiv)):
                        x1.append(self.xiv[i])
                        y1.append(self.yiv[i])

                    self.canvas3.figs.supxlabel('Source Voltage (V)', fontsize=12, fontfamily='Calibri')

                    self.canvas3.figs.supylabel('Current (A)', fontsize=12, fontfamily='Calibri')
                    self.canvas3.figs.subplots_adjust(left=0.14, right=0.9,bottom=0.14)
                    self.canvas3.mat_plot_drow_axes2(x1, y1)
                    if start_v<=stop_v:
                        start_v += 0.1
                    else:
                        start_v -= 0.1
                self.statusbar.showMessage('Completed')
                self.statusbar.setToolTipDuration(5000)
                break
        except:
            QMessageBox.critical(self, "error", "iv error")

    def s(self):
        t = threading.Thread(target=self.iv_sweep, name='t')
        t.start()

    def iv_stop(self):
        self.flag=1

    def iv_save(self):
        try:
            # 实例化
            root = tk.Tk()
            root.withdraw()
            # 设置存储位置、获取文件夹路径
            f_path = filedialog.asksaveasfilename(filetypes=[("txt", ".txt")], defaultextension='.tif')

            if f_path:
                file = open(f_path, mode='w')
                # 将数据存储至文件夹
                for i in range(0, len(self.xiv)):
                    file.write(str(self.xiv[i]))
                    file.write("\t")
                    file.write(str(self.yiv[i]))  # 将数组数据第0号元素写入txt文件中
                    file.write("\n")
                    i += 1

            # 将数组清空，并清空画布
            # self.xiv.clear()
            # self.yiv.clear()
            # self.canvas3.mat_plot_drow_axes(self.xb, self.yb)

        except:
            QMessageBox.critical(self, "error", "save error")

    def iv_clear(self):
        self.xiv.clear()
        self.yiv.clear()
        self.canvas3.mat_plot_drow_axes2(self.xiv, self.yiv)

    def about_program(self):
        pdf=r'D:\PDTest\help.pdf'
        os.startfile(pdf)

    def about(self):
        QMessageBox.information(self, "About",
                                """Design by Ziyun Wang, Yongtao Du, Chao Wei.\nGuided by Xiaojun Xie.\nCopyright: SWJTU-CIPC\nContect: 287935401@qq.com""",

                                QMessageBox.Yes)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


