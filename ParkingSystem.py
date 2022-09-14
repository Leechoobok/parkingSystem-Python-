import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import cv2
from easyocr import Reader
from datetime import datetime
import process
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Parking_Ui.ui")[0]
#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    license_plate = ""
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        #버튼에 기능을 연결하는 코드
        self.into_parking_btn.clicked.connect(self.into_parking)
        self.rate_check_btn.clicked.connect(self.rate_check)
        self.view_parking_btn.clicked.connect(self.view_parking)
        self.leave_parking_btn.clicked.connect(self.leave_parking)        
        self.end_btn.clicked.connect(self.end)
        

        self.listWidget_Test.itemClicked.connect(self.chkItemClicked)
        #self.listWidget_Test.itemDoubleClicked.connect(self.chkItemDoubleClicked)
        #self.listWidget_Test.currentItemChanged.connect(self.chkCurrentItemChanged)

    def into_parking(self) :
        self.listWidget_Test.clear()
        self.listWidget_Test.setEnabled(0)
        self.leave_parking_btn.setEnabled(0)
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', 'PNG(*.PNG)')
        if fname[0]=="" : return
        org_image = cv2.imread(fname[0],cv2.IMREAD_COLOR)
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(fname[0])
        size = self.view.size()
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(size.width())
        #self.qPixmapFileVar = self.qPixmapFileVar.scaledToHeight(size.height())
        self.view.setPixmap(self.qPixmapFileVar)
        langs = ['ko', 'en']
        reader = Reader(lang_list=langs, gpu=True)
        results = reader.readtext(org_image, detail = 0)
        results.append(results[0][len(results[0])-4:])
        results.append(datetime.now().strftime('%H'))
        results.append(datetime.now().strftime('%M'))
        process.into_parking(self, results)

    def rate_check(self) :
        self.view.clear()
        self.listWidget_Test.clear()
        self.listWidget_Test.setEnabled(1)
        self.leave_parking_btn.setEnabled(1)
        #self.InputText.setText("가가가")
        tmp=self.InputText.text()
        if not(tmp):
            QMessageBox.information(self,'오류','차량번호 네자리를 입력해 주세요')
        else:
            process.rate_check(self, tmp)
    def view_parking(self) :
        self.view.clear()
        self.leave_parking_btn.setEnabled(0)
        self.listWidget_Test.setEnabled(1)
        self.listWidget_Test.clear()
        process.view_parking(self)
    def leave_parking(self):
        global license_plate
        self.listWidget_Test.clear()
        self.leave_parking_btn.setEnabled(0)
        self.listWidget_Test.setEnabled(0)
        process.leave_parking(self, license_plate)
    def end(self) :
        myWindow.close()
    
    def chkItemClicked(self) :
        global license_plate
        tmp=self.listWidget_Test.currentItem().text()
        tmp_slice = tmp.split("\t")
        self.InputText.setText(tmp_slice[0][len(tmp_slice[0])-4:])
        license_plate=tmp_slice[0]

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()