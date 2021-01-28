# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys
import os
import time
import shutil
import nibabel as nib
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg") 
from PyQt5 import  QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QSplashScreen
from Ui_BrainAtlas_PyQt5 import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from nilearn import plotting
from nistats.thresholding import map_threshold
from matplotlib.figure import Figure
from nilearn.image import new_img_like
import matplotlib.pyplot as plt

class MyFigure(FigureCanvas):
    def __init__(self):
         self.fig = Figure()
         super(MyFigure,self).__init__(self.fig)


    def initialMap(self, val):
         _Threshold_map, _Threshold = map_threshold(val, alpha = 0.05, height_control = 'fpr', cluster_threshold = 0)
         plotting.plot_stat_map(_Threshold_map, threshold = _Threshold,  title = None)
         plt.savefig('.\\temp\plotAtlas.png', dpi = 200)
         #plt.show()
         return _Threshold_map


    def plotAtlas(self,val, Level,  Height_control,  Cluster_threshold,  Cut_coords):
         #plt.close()
         Threshold_map, Threshold = map_threshold(val, alpha =  Level, height_control = Height_control, cluster_threshold = Cluster_threshold)
         plotting.plot_stat_map(Threshold_map, threshold = Threshold, cut_coords = Cut_coords)
         #self.draw()
         plt.savefig('.\\temp\plotAtlas.png', dpi = 200)
         #plt.show()
         return Threshold_map



class MainWindow(QMainWindow, Ui_MainWindow):
    fname = ''
    img_arr = []
    initialMap = 0
    signalSave = pyqtSignal()
    signalClose = pyqtSignal()
    
    def __init__(self, parent=None):
         super(MainWindow, self).__init__(parent)
         self.setupUi(self)
         self.retranslateUi(self)
         time.sleep(1.5)
         self.F = MyFigure()
         pIntValidator = QIntValidator(self)
         pIntValidator.setRange(1, 100)
         pDoubleValidator1 = QDoubleValidator(self)
         pDoubleValidator1.setRange(0, 1)
         pDoubleValidator1.setNotation(QDoubleValidator.StandardNotation)
         pDoubleValidator1.setDecimals(8)
         pDoubleValidator2 = QDoubleValidator(self)
         pDoubleValidator2.setRange(0, 1)
         pDoubleValidator2.setNotation(QDoubleValidator.StandardNotation)
         pDoubleValidator2.setDecimals(8)
         pDoubleValidator3 = QDoubleValidator(self)
         pDoubleValidator3.setRange(-90, 90)
         pDoubleValidator3.setNotation(QDoubleValidator.StandardNotation)
         pDoubleValidator3.setDecimals(1)
         pDoubleValidator4 = QDoubleValidator(self)
         pDoubleValidator4.setRange(-126, 90)
         pDoubleValidator4.setNotation(QDoubleValidator.StandardNotation)
         pDoubleValidator4.setDecimals(1)
         pDoubleValidator5 = QDoubleValidator(self)
         pDoubleValidator5.setRange(-72, 108)
         pDoubleValidator5.setNotation(QDoubleValidator.StandardNotation)
         pDoubleValidator5.setDecimals(1)
         pDoubleValidator6 = QDoubleValidator(self)
         pDoubleValidator6.setRange(0, 1)
         pDoubleValidator6.setNotation(QDoubleValidator.StandardNotation)
         pDoubleValidator6.setDecimals(8)
         self.lineEdit_2.setValidator(pIntValidator)
         self.lineEdit.setValidator(pDoubleValidator1)
         self.lineEdit_3.setValidator(pDoubleValidator2)
         self.lineEdit_4.setValidator(pDoubleValidator6)
         self.lineEdit_6.setValidator(pDoubleValidator3)
         self.lineEdit_7.setValidator(pDoubleValidator4)
         self.lineEdit_8.setValidator(pDoubleValidator5)
         
    
    def check_fname(self):
         if self.fname != '':
             return True
         else:
             return False

    def input_check(self):
         try:
             if self.lineEdit.text() == "":
                 FDRValue = 0
             else:
                 FDRValue = float(self.lineEdit.text())
        
             if FDRValue<0 or FDRValue>1:
                 QMessageBox.warning(self, "Warning!", "FDR's value should be set in 0~1.")
                 return False

             if self.lineEdit_3.text() == "":
                 PValue = 0
             else:
                 PValue = float(self.lineEdit_3.text())
        
             if PValue<0 or PValue>1:
                 QMessageBox.warning(self, "Warning!", "FPR's value should be set in 0~1.")
                 return False

             if self.lineEdit_2.text() == "":
                 KValue = 0
             else:
                 KValue = int(self.lineEdit_2.text())

             if self.lineEdit_4.text() == "":
                 FWEValue = 0
             else:
                 FWEValue = float(self.lineEdit_4.text())
        
             if FWEValue<0 or FWEValue>1:
                 QMessageBox.warning(self, "Warning!", "FWE's value should be set in 0~1.")
                 return False

         #print(type(FDRValue) , type(PValue), type(KValue), type(TitleValue))
             if PValue!= 0 and FDRValue!=0 and FWEValue!= 0:
                 QMessageBox.warning(self, "Warning!", "You can only select one to input from FPR,FDR and FWE.")
                 return False

             if PValue!= 0 and FDRValue!=0:
                 QMessageBox.warning(self, "Warning!", "You can only select one to input from FPR,FDR and FWE.")
                 return False

             if PValue!= 0 and FWEValue!= 0:
                 QMessageBox.warning(self, "Warning!", "You can only select one to input from FPR,FDR and FWE.")
                 return False

             if FDRValue!=0 and FWEValue!= 0:
                 QMessageBox.warning(self, "Warning!", "You can only select one to input from FPR,FDR and FWE.")
                 return False

             if PValue == 0 and FDRValue == 0 and FWEValue ==0:
                 QMessageBox.warning(self, "Warning!", "You must select one to give value from FPR,FDR and FWE.")
                 return False
        
             if PValue == 0 and FWEValue ==0 and FDRValue!= 0:
                 height_control = "fdr"
                 _Level = FDRValue
                 _Height_control = height_control
                 _Cluster_threshold = KValue
                 return _Level,  _Height_control,  _Cluster_threshold

             if PValue != 0 and FDRValue ==0 and FWEValue ==0:
                 height_control = "fpr"
                 _Level = PValue
                 _Height_control = height_control
                 _Cluster_threshold = KValue
                 return _Level,  _Height_control,  _Cluster_threshold

             if PValue == 0 and FDRValue ==0 and FWEValue !=0:
                 height_control = "bonferroni"
                 _Level = FWEValue
                 _Height_control = height_control
                 _Cluster_threshold = KValue
                 return _Level,  _Height_control,  _Cluster_threshold
         except:
             QMessageBox.warning(self, "Warning!", "input value error, please check!")

    def check_radiobutton(self):
         if self.radioButton_4.isChecked() == True:
             Task = self.radioButton_4.text()
             Task = Task.lower()
             Condition = self.comboBox_6.currentText()
             if Condition == "Alerting":
                 Condition = "c1alert"
             if Condition == "Orienting":
                 Condition = "c2orient"
             if Condition == "Executive":
                 Condition = "c3executive"
        
         if self.radioButton_7.isChecked() == True:
             Task = self.radioButton_7.text()
             Task = Task.lower()
             Condition = self.comboBox_4.currentText()
             if Condition == "Pump":
                 Condition = "c1pump"
             if Condition == "Cashout":
                 Condition = "c2cashout"
             if Condition == "Explode":
                 Condition = "c3explode"
           
         if self.radioButton_5.isChecked() == True:
             Task = self.radioButton_5.text()
             Task = Task.lower()
             Condition = self.comboBox_5.currentText()
             if Condition == "Emotion":
                 Condition = "c1emotion"
             if Condition == "Control":
                 Condition = "c2control"
             if Condition == "Emo-Con":
                 Condition = "c3emocon"
        
         if self.radioButton_6.isChecked() == True:
             Task = self.radioButton_6.text()
             Task = Task.lower()
             Condition = self.comboBox_3.currentText()
             if Condition == "0_back":
                 Condition = "c1nb00"
             if Condition == "1_back":
                 Condition = "c2nb11"
             if Condition == "2_back":
                 Condition = "c3nb22"
        
        
         return Task,  Condition


    def Age_gender(self):
         if self.radioButton_2.isChecked() != True:
             Age = self.comboBox_7.currentText()
         else:
             Age = "All"

         Gender = self.comboBox.currentText()
         if Age == "11":
             Age = "12"

         return Gender,  Age


    def Get_cut_coords(self):
         Xvalue = self.lineEdit_6.text()
         Yvalue = self.lineEdit_7.text()
         Zvalue = self.lineEdit_8.text()
         _cut_coords = ['', '', '']
         if Xvalue == '':
             return None

         if Yvalue == '':
             return None

         if Zvalue == '':
             return None

         if float(Xvalue) < -90.0 or float(Xvalue) > 90.0:
             QMessageBox.warning(self, "Warning!", "X's value ranges from - 90 to 90, please check!")
             return False

         if float(Yvalue) < -126.0 or float(Yvalue) > 90.0:
             QMessageBox.warning(self, "Warning!", "Y's value ranges from - 126 to 90, please check!")
             return False

         if float(Zvalue) < -72.0 or  float(Zvalue)> 108.0:
             QMessageBox.warning(self, "Warning!", "Z's value ranges from - 72 to 108, please check!")
             return False 

         
         _cut_coords[0] = float(Xvalue)
         _cut_coords[1] = float(Yvalue)
         _cut_coords[2] = float(Zvalue)
         print(_cut_coords)
         return _cut_coords


    @pyqtSlot()
    def on_pushButton_clicked(self):
         try:
             if self.radioButton.isChecked() == True:
                 task, condition = self.check_radiobutton()
                 gender, age = self.Age_gender()
                 self.fname = "Task-" + task + "_Age-" + age + "_Condition-" + condition + "_Gender-" + gender + ".nii"
                 if not os.path.exists("./temp"):
                     os.makedirs("./temp")
                 if not os.path.exists("./map/cognitive"):
                     os.makedirs("./map/cognitive")
                 filepath = "./map/cognitive"
                 files = os.listdir(filepath)
                 #print(files[2])
                 fileFind = False
                 for file in files:
                     if file == self.fname :
                         self.fname_path = filepath + "\\" + self.fname
                         self.fname = self.fname_path
                         img = nib.load(self.fname)
                         self.img_arr = img.get_fdata()
                         self.img_arr = np.squeeze(self.img_arr)
                         self.threshold_map = self.F.initialMap(self.fname)
                         hbox = QHBoxLayout (self)
                         pixmap = QPixmap('.\\temp\plotAtlas.png') 
                         self.label.setPixmap (pixmap) 
                         self.label.setScaledContents (True)
                         hbox.addWidget(self.label)
                         self.setLayout (hbox)
                         self.initialMap = 1
                         #print(self.img_arr)
                         fileFind = True
                         self.textBrowser.append("[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "]  " + self.fname + " has been loaded successfully! Default picture has been shown successfully!")
                         self.pushButton.setEnabled(False)
                         self.pushButton_3.setEnabled(True)
                 if fileFind == False:
                     QMessageBox.warning(self, "Warning!", "The specified file was not found! Please check the file name and path.")
                     self.fname = ''
             elif self.radioButton_2.isChecked() == True:
                 task, condition = self.check_radiobutton()
                 gender, age = self.Age_gender()
                 self.fname = "Task-" + task + "_Age-" + age + "_Condition-" + condition + "_Gender-" + gender + ".nii"
                 if not os.path.exists("./temp"):
                     os.makedirs("./temp")
                 if not os.path.exists("./map/age"):
                     os.makedirs("./map/age")
                 filepath = "./map/age"
                 files = os.listdir(filepath)
                 #print(files[2])
                 fileFind = False
                 for file in files:
                     if file == self.fname :
                         self.fname_path = filepath + "\\" + self.fname
                         self.fname = self.fname_path
                         img = nib.load(self.fname)
                         self.img_arr = img.get_fdata()
                         self.img_arr = np.squeeze(self.img_arr)
                         self.threshold_map = self.F.initialMap(self.fname)
                         hbox = QHBoxLayout (self)
                         pixmap = QPixmap('.\\temp\plotAtlas.png') 
                         self.label.setPixmap (pixmap) 
                         self.label.setScaledContents (True)
                         hbox.addWidget(self.label)
                         self.setLayout (hbox)
                         self.initialMap = 1
                         #print(self.img_arr)
                         fileFind = True
                         self.textBrowser.append("[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "]  " + self.fname + " has been loaded successfully! Default picture has been shown successfully!")
                         self.pushButton.setEnabled(False)
                         self.pushButton_3.setEnabled(True)
                 if fileFind == False:
                     QMessageBox.warning(self, "Warning!", "The specified file was not found! Please check the file name and path.")
                     self.fname = ''
             else:
                 QMessageBox.critical(self, "Error!", "You must choose atlas type and conditon!")
         except:
             QMessageBox.critical(self, "Error!", "You must choose atlas type and conditon!")

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
         #try:
             savepath = "./save"
             if not os.path.exists(savepath):
                 os.makedirs(savepath)
             self.filename = self.lineEdit_5.text()
             aaaa = self.filename[-4:]
             print(aaaa)
             if self.filename == "" :
                 QMessageBox.warning(self, "Warning!", "Not entering a filename will cause the original file to be overwritten.", QMessageBox.Ok)
                 self.filename = None
             elif aaaa != '.nii':
                 self.filename = self.filename +'.nii'
                 print(self.filename)
                 self.img_arr[self.img_arr > 0]  = 1
                 self.img_arr[self.img_arr <= 0] = 0
                 self.New_img_like = new_img_like(self.threshold_map,  self.img_arr)
                 self.New_img_like.to_filename(self.filename)
                 newfilepath = os.getcwd() + './' + self.filename
                 shutil.move(newfilepath, savepath)
                 self.pushButton_2.setEnabled(False)
                 self.textBrowser.append("[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "]" + "  File has been saved in save folder successfully!")
             else :
                 self.img_arr[self.img_arr > 0]  = 1
                 self.img_arr[self.img_arr <= 0] = 0
                 self.New_img_like = new_img_like(self.threshold_map,  self.img_arr)
                 self.New_img_like.to_filename(self.filename)
                 newfilepath = os.getcwd() + './' + self.filename
                 shutil.move(newfilepath, savepath)
                 self.pushButton_2.setEnabled(False)
                 self.textBrowser.append("[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "]" + "  File has been saved in save folder successfully!")
             aaaa = ''
         #except:
             #QMessageBox.critical(self, "Error!", "Error occur in saving!")
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
         result = self.check_fname()
         self._cut_coords = self.Get_cut_coords()
         if not os.path.exists("./temp"):
             os.makedirs("./temp")
         if result == True:
             if self.input_check() == False or self._cut_coords == False:
                 QMessageBox.warning(self, "Warning!", "Please input again.")
             else:
                 self._level,  self._height_control,  self._cluster_threshold = self.input_check()
                 self.threshold_map = self.F.plotAtlas(self.fname, self._level,  self._height_control,  self._cluster_threshold, self._cut_coords)
                 hbox = QHBoxLayout (self)
                 pixmap = QPixmap('.\\temp\plotAtlas.png') 
                 self.label.setPixmap (pixmap) 
                 self.label.setScaledContents (True)
                 hbox.addWidget(self.label)
                 self.setLayout (hbox)
                 self.mapsignal = 1
                 self.textBrowser.append("[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "]" + "  Picture has been shown successfully!")
                 self.pushButton_2.setEnabled(True)
         else:
             QMessageBox.warning(self, "Warning!", "Please import the file(.nii)!")
        

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
         self.textBrowser.clear()
    
    @pyqtSlot()
    def on_pushButton_6_clicked(self):
         self.signalClose.connect(self.on_actionClose_triggered)
         self.signalClose.emit()


    @pyqtSlot()
    def on_radioButton_6_clicked(self):
         self.comboBox.clear()
         comboBox_list = ['All']
         self.comboBox.addItems(comboBox_list)
         comboBox_3_list = ['0_back' , '1_back', '2_back']
         self.comboBox_3.addItems(comboBox_3_list)
         self.comboBox_4.clear()
         self.comboBox_5.clear()
         self.comboBox_6.clear()


    @pyqtSlot()
    def on_radioButton_7_clicked(self):
         self.comboBox.clear()
         comboBox_list = ['All']
         self.comboBox.addItems(comboBox_list)
         comboBox_4_list = ['Pump' , 'Cashout', 'Explode']
         self.comboBox_4.addItems(comboBox_4_list)
         self.comboBox_3.clear()
         self.comboBox_5.clear()
         self.comboBox_6.clear()



    @pyqtSlot()
    def on_radioButton_5_clicked(self):
         self.comboBox.clear()
         comboBox_list = ['All', 'Male', 'Female']
         self.comboBox.addItems(comboBox_list)
         comboBox_5_list = ['Emotion', 'Control', 'Emo-Con']
         self.comboBox_5.addItems(comboBox_5_list)
         self.comboBox_3.clear()
         self.comboBox_4.clear()
         self.comboBox_6.clear()

    
    
    @pyqtSlot()
    def on_radioButton_4_clicked(self):
         self.comboBox.clear()
         comboBox_list = ['All']
         self.comboBox.addItems(comboBox_list)
         comboBox_6_list = ['Alerting', 'Orienting', 'Executive']
         self.comboBox_6.addItems(comboBox_6_list)
         self.comboBox_3.clear()
         self.comboBox_4.clear()
         self.comboBox_5.clear()

    
    
    @pyqtSlot()
    def on_actionOpen_triggered(self):
         try:
             if not os.path.exists("./temp"):
                 os.makedirs("./temp")
             if self.fname == '':
                 self.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files(*.nii)")
                 img=nib.load(self.fname)
                 self.img_arr=img.get_fdata()
                 self.img_arr=np.squeeze(self.img_arr)
                 self.F.initialMap(self.fname)
                 hbox = QHBoxLayout (self)
                 pixmap = QPixmap('.\\temp\plotAtlas.png') 
                 self.label.setPixmap (pixmap) 
                 self.label.setScaledContents (True)
                 hbox.addWidget(self.label)
                 #print(self.img_arr)
                 self.initialMap = 1
                 self.mapsignal = 0
                 self.pushButton.setEnabled(False)
                 self.pushButton_3.setEnabled(True)
                 self.textBrowser.append("[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "]" + "  File has been imported successfully! Default picture has been shown successfully!")
             else:
                 QMessageBox.critical(self, "Error!", "File has been imported. New file cannot be imported again. To import new file, please close the opening file.")
         except:
             QMessageBox.critical(self, "Error!", "Error occurred during the file imported!")
             self.img_arr = []
             self.fname = ''

    @pyqtSlot()
    def on_actionClose_triggered(self): 
        try:
             self.img_arr = []
             self.fname = ''
             self.New_img_like = None
             self.threshold_map = None
             self._level = None  
             self._height_control = None
             self._cluster_threshold = None
             self._title = None
             self.mapsignal = None
             self.filename = None
             self.initialMap = 0
             #print(type(self.img_arr), self.img_arr)
             self.label.setPixmap(QPixmap(""))
             self.textBrowser.append("[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "]" + "  File has been closed successfully!")
             self.pushButton_3.setEnabled(False)
             self.pushButton_2.setEnabled(True)
             self.pushButton.setEnabled(True)
             self.lineEdit.clear()
             self.lineEdit_2.clear()
             self.lineEdit_3.clear()
             self.lineEdit_4.clear()
             self.lineEdit_5.clear()
             self.lineEdit_6.clear()
             self.lineEdit_7.clear()
             self.lineEdit_8.clear()
        except:
             QMessageBox.warning(self, "Warning!", "No executable file!")
    
    @pyqtSlot()
    def on_actionSave_triggered(self):
         if self.fname == '':
             QMessageBox.warning(self, "Warning!", "Please import the file(.nii)!")
         elif self.mapsignal == 0:
             QMessageBox.warning(self, "Warning!", "Please correct the threshold of the image before saving it!")
         else:
             self.signalSave.connect(self.on_pushButton_2_clicked)
             self.signalSave.emit()

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
         try:
             if not os.path.exists("./ResultPicture"):
                 os.makedirs("./ResultPicture")
             if self.initialMap == 1 :
                 pp ="./ResultPicture"
                 shutil.move('./temp/plotAtlas.png', pp)
                 tt = "./" + time.strftime('%Y-%m-%d_%H.%M.%S',time.localtime(time.time())) + '_pciture.png'
                 #print(tt)
                 aa= os.path.abspath('.')
                 #print(aa)
                 oldpath = os.path.join(aa,'ResultPicture','plotAtlas.png' )
                 #print(oldpath)
                 newpath =os.path.join(aa, 'ResultPicture', tt )
                 #print(newpath)
                 os.rename(oldpath, newpath)
                 self.textBrowser.append("[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "]" + "  Picture has been saved in ResultPicture folder successfully!")
             else:
                 QMessageBox.warning(self, "Warning!", "Can't find a picture object to save!")
         except:
             QMessageBox.warning(self, "Warning!", "Can't find a picture object to save!")

    
    @pyqtSlot(bool)
    def on_radioButton_toggled(self, checked):
         self.comboBox_7.clear()
         self.comboBox_2_list = ['All', '7', '8', '9', '10', '11', '12']
         self.comboBox_7.addItems(self.comboBox_2_list)
         self.comboBox_7.setEnabled(True)
    
    @pyqtSlot(bool)
    def on_radioButton_2_toggled(self, checked):
         self.comboBox_7.clear()
         self.comboBox_2_list = ['All']
         self.comboBox_7.addItems(self.comboBox_2_list)
         self.comboBox_7.setEnabled(False)


if __name__ == "__main__":
     app = QtWidgets.QApplication(sys.argv)
     splash = QSplashScreen(QPixmap("./Begin.png"))
     splash.show()
     splash.showMessage('Allocating memory space...', Qt.AlignHCenter | Qt.AlignBottom, Qt.blue)
     time.sleep(1)
     splash.showMessage('Loading .nii resources...',Qt.AlignHCenter | Qt.AlignBottom, Qt.blue)
     time.sleep(2)
     splash.showMessage('Loading main interface...', Qt.AlignHCenter | Qt.AlignBottom, Qt.blue)
     time.sleep(0.5)
     app.processEvents()
     ui = MainWindow()
     ui.show()
     splash.finish(ui)
     sys.exit(app.exec_())

