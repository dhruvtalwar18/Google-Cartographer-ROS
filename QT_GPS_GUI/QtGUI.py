#!/usr/bin/python
import sys
import numpy 
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, QThread
import time
#import geodesy.props
#import geodesy.utm
#import geodesy.wu_point
import rospy
import traceback
from std_msgs.msg import Int32
from sensor_msgs.msg import NavSatFix
import utm

'''class gpsMap(QLabel):
	def __init__(self, parent = None):
		super(gpsMap, self).__init__(parent)

		self.cvImage = cv2.imread("/Users/admin/Desktop/BTP/road_map.jpg")
		height, width, byteValue = self.cvImage.shape
		byteValue = byteValue * width

		cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)

		#cv2.imshow("Display", self.cvImage)


		self.mQImage = QImage(self.cvImage.data, width, height, byteValue, QImage.Format_RGB888)
		self.pixmap = QPixmap.fromImage(self.mQImage)
		self.setPixmap(self.pixmap)

	def paintEvent(self, QPaintEvent):
		painter = QPainter()
		painter.begin(self)
		painter.drawImage(0,0,self.mQImage)
		painter.end()
'''		


min_lat=28.547388
min_lon=77.183628

p0=utm.from_latlon(min_lat,min_lon)



'''def GPS_receiver(data):
	lat1 = data.latitude
	long1 = data.longitude
	p=geodesy.utm.fromLatLong(lat1,lon1).toPoint()
	x = p.x
	y = p.y
'''	

def callback(data):
	global lat1 
	lat1 = data.latitude
	global long1
	long1 = data.longitude
	global p
	p = utm.from_latlon(lat1,long1)
	global x
	x = p[0]-p0[0]
	x = x/0.160722909
	global y
	y = p[1]-p0[1]
	y = y/0.148029157
	y = y*(-1)
	print(x,y)


class rosThread(QThread):
	def run(self):
		print "Spinned"
		rospy.spin()
			
class Thread(QThread):
	changePixmap = pyqtSignal(QImage)
	def run(self):
		global x
		global y
		while True:
			time.sleep(0.5)
			point_x = int(x)
			point_y = int(y)
			cv2.circle(cvImage, (point_x, point_y), 1, (0,0,255), 3)
			
			rgbImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
			h, w, ch = rgbImage.shape
			bytesPerLine = ch * w
			convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
			p = convertToQtFormat
			self.changePixmap.emit(p)


class Home(QWidget):
	def __init__(self, parent = None):
		super(Home, self).__init__(parent)
		global cvImage 
		cvImage = cv2.imread("/home/dhruv/Downloads/T-Sac.png")
		self.height, self.width, self.byteValue = cvImage.shape
		self.byteValue = self.byteValue * self.width
		
		cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)

		'''
		sac_lat = 28.546587
		sac_long = 77.185146

		nilt_lat = 28.547350
		nilt_long = 77.183538

		hosp_lat = 28.545435
		hosp_long = 77.188217

		gupta_lat = 28.545292
		gupta_long = 77.182498

		himadri_lat = 28.544814
		himadri_long = 77.194455

		tnp_lat = 28.544154
		tnp_long = 77.191280

		p1 = utm.from_latlon(sac_lat, sac_long)
		p1_x = int((p1[0] - p0[0])*0.17867)
		p1_y = int((p1[1] - p0[1])*0.17837)
		cv2.circle(cvImage, (p1_x, p1_y), 5, (0,255,0), 2)
		cv2.putText(cvImage, 'SAC', (p1_x, p1_y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

		p2 = utm.from_latlon(nilt_lat, nilt_long)
		p2_x = int((p2[0] - p0[0])*0.17867)
		p2_y = int((p2[1] - p0[1])*0.17837)
		cv2.circle(cvImage, (p2_x, p2_y), 5, (0,255,0), 2)
		cv2.putText(cvImage, 'T-Point', (p2_x, p2_y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

		p3 = utm.from_latlon(hosp_lat, hosp_long)
		p3_x = int((p3[0] - p0[0])*0.17867)
		p3_y = int((p3[1] - p0[1])*0.17837)
		cv2.circle(cvImage, (p3_x, p3_y), 5, (0,255,0), 2)
		cv2.putText(cvImage, 'Hospital', (p3_x, p3_y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

		p4 = utm.from_latlon(gupta_lat, gupta_long)
		p4_x = int((p4[0] - p0[0])*0.17867)
		p4_y = int((p4[1] - p0[1])*0.17837)
		cv2.circle(cvImage, (p4_x, p4_y), 5, (0,255,0), 2)
		cv2.putText(cvImage, 'Gupta', (p4_x, p4_y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

		p5 = utm.from_latlon(tnp_lat, tnp_long)
		p5_x = int((p5[0] - p0[0])*0.17867)
		p5_y = int((p5[1] - p0[1])*0.17837)
		cv2.circle(cvImage, (p5_x, p5_y), 5, (0,255,0), 2)
		cv2.putText(cvImage, 'TnP', (p5_x, p5_y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

		p6 = utm.from_latlon(himadri_lat, himadri_long)
		p6_x = int((p6[0] - p0[0])*0.17867)
		p6_y = int((p6[1] - p0[1])*0.17837)
		cv2.circle(cvImage, (p6_x, p6_y), 5, (0,255,0), 2)
		cv2.putText(cvImage, 'Himadri', (p6_x, p6_y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

		'''

		self.mQImage = QImage(cvImage.data, self.width, self.height, self.byteValue, QImage.Format_RGB888)
		self.pixmap = QPixmap.fromImage(self.mQImage)

		self.map = QLabel()
		self.map.setPixmap(self.pixmap)

		self.startPlot = QCheckBox('Plot')
		self.startPlot.stateChanged.connect(lambda:self.btnState(self.startPlot))

		hbox = QHBoxLayout()
		element1 = QWidget()
		element1.setLayout(hbox)
		hbox.addWidget(self.map)
		hbox.addWidget(self.startPlot)
		self.setLayout(hbox)

		self.setGeometry(0, 0, 1600, 800)
		self.setWindowTitle('DLive-Visualizer')

	def setImage(self, image):
		self.map.setPixmap(QPixmap.fromImage(image))	
		
	def btnState(self, btn):
		if btn.isChecked() == True:
			print "Button is checked"
			
			th = Thread(self)
			th.changePixmap.connect(self.setImage)
			th.start()

			r = rosThread(self)
			r.start()

			'''for i in range (50, 55):
				x = i
				y = i
				print "Plotted" + str(i)
				time.sleep(1)

			def plotPoint(x,y):
				cv2.circle(self.cvImage, (x, y), 5, (0,0,255), 1)
				cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)
				mQImage1 = QImage(self.cvImage.data, self.width, self.height, self.byteValue, QImage.Format_RGB888)
				pixmap1 = QPixmap.fromImage(mQImage1)
				self.map.setPixmap(pixmap1)
				#time.sleep(5)

			for i in range(100,200, 5):
				plotPoint(i,i)'''


'''class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.setGeometry(0, 0, 1600, 800)'''


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = Home()
	w.show()
	rospy.init_node('gps_plotter', anonymous=True)
	rospy.Subscriber('/gps/pixhawk', NavSatFix, callback)
	print "Showed"
	app.exec_()
	

