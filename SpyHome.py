
import os
import sys
import time
#import Adafruit_DHT
import cv2
from matplotlib.testing.jpl_units import m
import numpy as np
from PyQt4.QtGui import *
#import Adafruit_BBIO.GPIO as GPIO
from PyQt4.QtGui import QRadioButton
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import smtplib
from PyQt4 import QtCore, QtGui
from time import sleep

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Capture(object):
    def __init__(self):
	self.capturing = False	
        self.c =cv2.VideoCaptuure(0)
    

    def startCapture(self):
        print ("pressed start")
        self.capturing = True
        cap = self.c
        while(self.capturing):
            ret, frame = cap.read()
            cv2.imshow("Podglad", frame)
            cv2.waitKey(5)
        cv2.destroyAllWindows()

    def	nagrajCapture(self):
	self.capturing = True
        cap = self.c
        f = cv2.cv.CV_FOURCC(*'MJPG')
        z = cv2.VideoWriter('putput.avi' , f , 20, ( 640 , 480 ))
        while(self.capturing):
            ret, frame = cap.read()
            frame = cv2.flip(frame,0)
            cv2.imshow("ramka", frame)
            z.write(frame)
            cv2.waitKey(5)
        cap.release()
        z.release()
        cv2.destroyAllWindows()

    

    def koniecCapture(self):
        print ("pressed End")
        self.capturing = False

    def detektor(self):
	print 'Zinicjalizowano czujnik ruchu'
	print"temp wl"
	print 'Run sensor HR'
	#GPIO.setup('P8_12', GPIO.IN)
	#GPIO.add_event_detect('P8_12', GPIO.FALLING)
	war = self.spinBox.value()
	war1 = self.spinBox_2.value()
	pin = 'P8_11'
	humidity, temperature = Adafruit_DHT.read_retry(11, pin)
	
	GPIO.setup('P8_12', GPIO.IN)
	GPIO.add_event_detect('P8_12', GPIO.FALLING)
	while True:
		if GPIO.event_detected('P8_12'):
			
			self.nagrajCapture()
			#print 'Wysylam wiadomosc o naruszeniu strefy'
						
			self.wiadomoscruch()
			break

		elif temperature > war:
			self.wiadomosctemperatura()	
			#time.sleep(120)		
			break
    		elif humidity > war1:
		
			self.wiadomoscwilgotnosc()
			#time.sleep(120)
			break
			
		
		else:
			continue		

    
    def wiadomoscruch(self):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	my_email = "domprywatny4@gmail.com"
	my_password = "debian123"
	destination = "domprywatny4@gmail.com"
	text = "Naruszono strefe nadzoru!!"
	
	server.login(my_email, my_password)
	server.sendmail(my_email, destination, text)
	server.quit()
	print 'Wiadomoc wysmlana STREFA!!'

    def wiadomoscwilgotnosc(self):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	my_email = "domprywatny4@gmail.com"
	my_password = "debian123"
	destination = "domprywatny4@gmail.com"
	text = "Przekroczono minimalna wartosc wilgoci!! "

	server.login(my_email, my_password)
	server.sendmail(my_email, destination, text)
	server.quit()
	print 'Wiadomoc wysmlana HR ! !'

    def wiadomosctemperatura(self):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	my_email = "domprywatny4@gmail.com"
	my_password = "debian123"
	destination = "domprywatny4@gmail.com"
	text = "Przekroczono dozwolona temperature"

	server.login(my_email, my_password)
	server.sendmail(my_email, destination, text)
	server.quit()
	print 'Wiadomoc wysmlana temp!!'

    def	LCDnumber(self):
	
	
	humidity,temperature = Adafruit_DHT.read(11, 'P8_11')
	self.lcdNumber.display('{0:0.1f}'.format(temperature))
	self.lcdNumber_2.display('{0:0.1f}'.format(humidity))
			

class Ui_MainWindow(QtGui.QWidget, Capture):
    
	

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(350, 301)

	
        self.centralwidget = QtGui.QWidget(MainWindow)
	self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 350, 341))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))

        self.podgladButton = QtGui.QPushButton(self.tab)
        self.podgladButton.setGeometry(QtCore.QRect(30, 20, 161, 27))
        self.podgladButton.setObjectName(_fromUtf8("podgladButton"))
	self.podgladButton.clicked.connect(self.startCapture)

	
        self.nagrajButton = QtGui.QPushButton(self.tab)
        self.nagrajButton.setGeometry(QtCore.QRect(30, 50, 161, 27))
        self.nagrajButton.setObjectName(_fromUtf8("nagrajButton"))
	self.nagrajButton.clicked.connect(self.nagrajCapture)
	
        self.koniecButton = QtGui.QPushButton(self.tab)
        self.koniecButton.setGeometry(QtCore.QRect(30, 80, 161, 27))
        self.koniecButton.setObjectName(_fromUtf8("koniecButton"))
	self.koniecButton.clicked.connect(self.koniecCapture)

        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(30, 130, 171, 31))
        self.label.setObjectName(_fromUtf8("label"))

        self.lcdNumber = QtGui.QLCDNumber(self.tab)
        self.lcdNumber.setGeometry(QtCore.QRect(210, 130, 71, 31))
	self.lcdNumber.setSmallDecimalPoint(False)
	self.lcdNumber.setDigitCount(8)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))

        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(30, 180, 181, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.lcdNumber_2 = QtGui.QLCDNumber(self.tab)
        self.lcdNumber_2.setGeometry(QtCore.QRect(210, 180, 71, 31))
	self.lcdNumber_2.setSmallDecimalPoint(False)
	self.lcdNumber_2.setDigitCount(8)
        self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))

	self.Pomiar = QtGui.QPushButton(self.tab)
        self.Pomiar.setGeometry(QtCore.QRect(30, 240, 251, 27))
        self.Pomiar.setObjectName(_fromUtf8("koniecButton"))
	self.Pomiar.clicked.connect(self.LCDnumber)

        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))

        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(30, 50, 131, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(30, 10, 201, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.spinBox = QtGui.QSpinBox(self.tab_2)
        self.spinBox.setGeometry(QtCore.QRect(160, 50, 61, 31))
        self.spinBox.setMaximum(50)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))

        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(30, 90, 131, 31))
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.spinBox_2 = QtGui.QSpinBox(self.tab_2)
        self.spinBox_2.setGeometry(QtCore.QRect(160, 90, 61, 31))
        self.spinBox_2.setMinimum(20)
        self.spinBox_2.setMaximum(90)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))

        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(230, 50, 70, 31))
        self.label_6.setObjectName(_fromUtf8("label_6"))

        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(230, 90, 90, 31))
        self.label_7.setObjectName(_fromUtf8("label_7"))

        self.label_8 = QtGui.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(30, 130, 201, 31))
        self.label_8.setObjectName(_fromUtf8("label_8"))

        self.pushButton = QtGui.QPushButton(self.tab_2)
        self.pushButton.setGeometry(QtCore.QRect(30, 170, 241, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        #self.pushButton.clicked.connect(self.czujniktemperatura)
	#self.pushButton.clicked.connect(self.czujnikwilgoci)
	self.pushButton.clicked.connect(self.detektor)

        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        
        #self.timerTemp = QtCore.QTimer(self.tab) 
	#self.timerTemp.timeout.connect(self.timerTemp_TimeOut)
	#self.timerTemp.start(3000)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
	
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
	#self.capturing = True
	
        self.c = cv2.VideoCapture(0)

	#self.f = cv2.cv.CV_FOURCC(*'XVID')
        #self.z = cv2.VideoWriter('putput1.avi' , self.f , 20.0, ( 640 , 480 ))	
        MainWindow.setWindowTitle(_translate("MainWindow", "SpyHome", None))
        self.podgladButton.setText(_translate("MainWindow", "Podglad obrazu", None))
        self.nagrajButton.setText(_translate("MainWindow", "Nagrywaj obraz", None))
        self.koniecButton.setText(_translate("MainWindow", "Koniec ", None))
        self.label.setText(_translate("MainWindow", 'Temperatura [C]', None))
        self.label_2.setText(_translate("MainWindow", "Wilgotnosc [%]", None))

	self.Pomiar.setText(_translate("MainWindow","Pomiar",None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Podglad", None))
        self.label_3.setText(_translate("MainWindow", "Temperatura ", None))
        self.label_4.setText(_translate("MainWindow", "Ustawienie parametrow", None))
        self.label_5.setText(_translate("MainWindow", "Wilgotnosc ", None))
        self.label_6.setText(_translate("MainWindow", "0-50 [C]", None))
        self.label_7.setText(_translate("MainWindow", "20-90 [%]", None))
        self.label_8.setText(_translate("MainWindow", "Uruchomienie", None))
        self.pushButton.setText(_translate("MainWindow", "Start", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Uruchomienie", None))
   


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #ui.nagrajczujnik(MainWindow)
    MainWindow.show()
    #capture = Capture()
    sys.exit(app.exec_())



