import cv2

class Camera:
	def __init__(self,index=2):
		self.cam = cv2.VideoCapture(index)

	
	
	def get_frame(self):
		return self.cam.read()
	
	

	def close(self):
		self.cam.release()
		cv2.destroyAllWindows()
	
	
if __name__ == '__main__':


	cam = Camera(-1)
	while True:
		ret, image = cam.get_frame()
		if not ret:
			print("No return")
			break
		image=cv2.resize(image,(1024,640))
		# im = cv.imread(cv.samples.findFile("lena.jpg"))
		cv2.imshow("Frames", image)
		if cv2.waitKey(30) & 0x7F == ord('q'):
			print("Exit requested.")
			break

		# cv2.imshow('test',image)
		k = cv2.waitKey(1)
		if k == 27:
			break
	# cv2.imwrite('/home/pi/testimage.jpg', image)
	# cv2.destroyWindow("foo")
	cam.close()
