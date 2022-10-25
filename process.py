
from unittest import result
from datetime import datetime
import os
from PyQt5.QtWidgets import *

def into_parking(self, results):
    chkfp = open("parking_car.txt", "r")

    if not chkfp:
        print("\n데이터 불러오기에 실패하였습니다.")
    else:
        while True:
            line = chkfp.readline()
            if not line: break
            line = line.strip()
            tmp_results = line.split(",")
            if results[0] == tmp_results[0]:
                QMessageBox.information(self,'오류','이미 입차된 차량입니다.')
                self.view.clear()
                return
    fp = open("parking_car.txt", "a")

    if not fp:
        print("\n데이터 불러오기에 실패하였습니다.")
    else:
        fp.write(results[0]+','+results[1]+','+results[2]+','+results[3]+'\n')
        self.listWidget_Test.addItem(results[0]+'차량  입차시간 : '+results[2]+'시'+results[3]+'분')
        fp.close()

def rate_check(self, id):
    fp = open("parking_car.txt", "r")

    if not fp:
        print("\n데이터 불러오기에 실패하였습니다.")
    else:
        self.listWidget_Test.addItem("차량번호\t\t이용시간\t\t이용요금")
        while True:
            line = fp.readline()
            if not line: break
            line = line.strip()
            results = line.split(",")
            if id == results[1]:
                chk_timeA = int(datetime.now().strftime('%H'))*60 + int(datetime.now().strftime('%M'))
                chk_timeB = int(results[2])*60 + int(results[3])
                fare = int((chk_timeA - chk_timeB) / 10) * 800
                self.listWidget_Test.addItem(results[0]+'\t\t'+str(chk_timeA-chk_timeB)+ '분\t\t'+ str(fare)+'원' )

    fp.close()
def view_parking(self):
    fp = open("parking_car.txt", "r")

    if not fp:
        print("\n데이터 불러오기에 실패하였습니다.")
    else:
        self.listWidget_Test.addItem("차량번호\t\t입차시간")
        while True:
            line = fp.readline()
            if not line: break
            line = line.strip()
            results = line.split(",")
            self.listWidget_Test.addItem(results[0]+'\t\t'+results[2]+'시 '+results[3]+'분' )
    fp.close()

def leave_parking(self, license_plate):
    fp = open("parking_car.txt", "r")
    ft = open("temp.txt","w")

    if not fp:
        print("\n데이터 불러오기에 실패하였습니다.")
    else:
        
        while True:
            line = fp.readline()
            if not line: break
            line = line.strip()
            results = line.split(",")
            if results[0] == license_plate :
                self.listWidget_Test.addItem(results[0]+"차량 출차가 완료되었습니다.")
            else :
                ft.write(line+'\n')
    fp.close()
    ft.close()
    os.remove("Parking_car.txt")
    os.rename("temp.txt", "Parking_car.txt")
