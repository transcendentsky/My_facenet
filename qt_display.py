import cv2
import numpy as np
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *  
from PyQt4.QtCore import *
from PyQt4 import phonon
from PyQt4.QtSql import *
import sys
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(760, 439)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(130, 390, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("打开"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(570, 390, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("关闭"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 31, 391, 311))
        self.label.setText(_fromUtf8(""))
        #self.label.setPixmap(QtGui.QPixmap(_fromUtf8("D:/用户目录/我的图片/15.bmp")))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(570, 170, 54, 12))
        self.label_2.setObjectName(_fromUtf8("label_2"))


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton.setText(_translate("Dialog", "打开", None))
        self.pushButton_2.setText(_translate("Dialog", "关闭", None))
        self.label.setText(_translate("Dialog", "视频", None))
        self.label_2.setText(_translate("Dialog", "截图", None))
        
        self.pushButton.clicked.connect(self.open_camer)
        self.pushButton_2.clicked.connect(self.take_picture)
    def open_camer(self):
        global cap,timer
        cap = cv2.VideoCapture(0)
        timer.start(100)
        #fourcc = cv2.cv.CV_FOURCC(*'XVID')
        #opencv3的话用:fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))#保存视频
        '''
        while True:
            ret,frame = cap.read()
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            out.write(frame)#写入视频
            cv2.imshow('frame',frame)#一个窗口用以显示原视频
            cv2.imshow('gray',gray)#另一窗口显示处理视频
            if cv2.waitKey(1) &0xFF == ord('q'):
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        '''
    def take_picture(self):
        global timer
        timer.stop()
        
class Dialog(QtGui.QDialog):
    def __init__(self,parent=None):
        global timer
        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_Dialog()                                         # Ui_Dialog为.ui产生.py文件中窗体类名，经测试类名以Ui_为前缀，加上UI窗体对象名（此处为Dialog，见上图）
        self.ui.setupUi(self)
        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), self.updtTime)


    def updtTime(self):
        global cap
        #cap = cv2.VideoCapture(0)
        ret,frame = cap.read()
        cv2.imwrite('1.jpg', frame)
        #out.write(frame)
        self.ui.label.setPixmap(QtGui.QPixmap(_fromUtf8('1.jpg')))
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    myapp=Dialog()
    myapp.show()
    app.exec_()
    pass