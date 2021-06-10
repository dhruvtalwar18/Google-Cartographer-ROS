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


min_lat=28.5306000
min_lon=77.1618000

#p0=geodesy.utm.fromLatLong(min_lat,min_lon).toPoint()
#x = p0.x
#y = p0.y

'''def GPS_receiver(data):
	lat1 = data.latitude
	long1 = data.longitude
	p=geodesy.utm.fromLatLong(lat1,lon1).toPoint()
	x = p.x
	y = p.y
'''	

def callback(data):
	global x 
	x = data.data - min_lat
	global y
	y = data.data - min_lon
	print (x,y)

class rosThread(QThread):
	def run(self):
		print "Spinned"
		rospy.spin()
			
class Thread(QThread):
	changePixmap = pyqtSignal(QImage)
	def run(self):
		i = 100
		while True:
			time.sleep(0.5)
			point_x = int(x)
			point_y = int(y)
			cv2.circle(cvImage, (point_x, point_y), 5, (0,0,255), 1)
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
		cvImage = cv2.imread("/home/suniljha/Downloads/road_map.jpg")
		self.height, self.width, self.byteValue = cvImage.shape
		self.byteValue = self.byteValue * self.width

		cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)

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
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('chatter', Int32, callback)
	print "Showed"
	app.exec_()
	

