#-*- coding:utf-8
import serial
import time
import binascii
import cv2
ser = serial.Serial("/dev/ttyUSB1",115200,timeout = 2)
print(ser.name,ser.port,ser.isOpen())

sleep_time = 0.5

def read_status():
    ser.write("a")
    time.sleep(sleep_time)
    return ser.readall()

#A9 9A {len} 23 ({id} {angle} {time}) {sum} ED
def move_servo(sid,angle,t):
    cmd = [0xA9,0x9A,0x06,0x23,sid,angle,t/512,t,0x00,0xED]
    checksum = 0x00
    for i in range(2,len(cmd)-2):
        checksum += cmd[i]
    cmd[-2] = checksum
    str_cmd = ''
    for i in range(0,len(cmd)):
        str_cmd += format(cmd[i],'02x') + ' '
    print("Command is %s. CheckSum is %s" % (str_cmd,hex(checksum)))
    hex_cmd = bytearray.fromhex(str_cmd)
    ser.write(hex_cmd)

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output.mp4',fourcc, 20.0 , (640,480))

cnt =0
angle = 0
move_servo(0x01,0,0)
time.sleep(2)

while(cap.isOpened()):
    ret, frame = cap.read()
    cnt += 1
    if cnt %50 == 0:
        angle = cnt/50 *10
        print(angle)
        move_servo(0x01,angle,0)
    cv2.putText(frame,'angle=%s'% angle,(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),5)
    cv2.imshow("",frame)
    out.write(frame)
    if cnt >300:
        break

#print("move 1\n %s" % move_servo(0x01,10,0))
#print(read_status())
#print("move 1\n %s" % move_servo(0x01,20,0))
#print(read_status())
#print("move 1\n %s" % move_servo(0x01,30,0))
#print(read_status())
#print("move 1\n %s" % move_servo(0x01,40,0))
#print(read_status())

