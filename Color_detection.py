
import cv2
import serial
import time
serial_port = 'COM3' #replace with your COM port
baud_rate = 9600 #Set baudrate , Note: baudrate must be same as in the microcontroller used
ser = serial.Serial(serial_port, baud_rate, timeout=1)

video = cv2.VideoCapture(1)
video.set(cv2.CAP_PROP_FRAME_WIDTH,720) 
video.set(cv2.CAP_PROP_FRAME_HEIGHT,720) 
sum_hue = 0
hue =0
val1=1.75
val2=2.5
while(True):
    data = ser.readline().decode()    


    sum_hue = 0
    _,frame = video.read()
    height,width,_ = frame.shape
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cx1 = int(width/2)
    cy1 = int(height/2)
    
    cx2 = int(width/val1)
    cy2 = int(height/val1)

    cx3 = int(width/val2)
    cy3 = int(height/val2)

    cx4 = int(width/val2)
    cy4 = int(height/val1)

    cx5 = int(width/val1)
    cy5 = int(height/val2)

    
    center = hsv[cy1,cx1]
    side1 = hsv[cy2,cx2]
    side2 = hsv[cy3,cx3]
    side3 = hsv[cy4,cx4]
    side4 = hsv[cy5,cx5]
    for x in (center,side1,side2,side3,side4):
        hue = x[0]
        sum_hue = sum_hue + hue

    color_hue = int(sum_hue/5)    
    # print(color_hue)

    if(color_hue<=35 and color_hue>=3):
       color_detected = '1'
       print("orange")
     
    elif(color_hue>=75 and color_hue<=135):
        color_detected = '2'
        print("blue")
    else:
        color_detected = '3'
        print("other")
    if(data == '0'):
        print("Arduino")
        ser.write(color_detected.encode('utf-8'))


    
    cv2.circle(frame,(cx1,cy1),10,(0,0,255),thickness=2)
    cv2.circle(frame,(cx2,cy2),10,(0,0,255),thickness=2)
    cv2.circle(frame,(cx3,cy3),10,(0,0,255),thickness=2)
    cv2.circle(frame,(cx4,cy4),10,(0,0,255),thickness=2)
    cv2.circle(frame,(cx5,cy5),10,(0,0,255),thickness=2)
    cv2.imshow("COLOR DETECTION",frame)
    

    key = cv2.waitKey(1)
    if (key==27):
        break 

video.release()
cv2.destroyAllWindows()    
