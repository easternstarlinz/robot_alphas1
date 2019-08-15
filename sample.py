#-*- coding:utf-8
import serial
import time
import binascii

ser = serial.Serial("/dev/ttyUSB1",115200,timeout = 2)
print(ser.name)
print(ser.port)
print(ser.isOpen())

unl_s1 =  [0xA9,0x9A,0x03,0x22,0x01,0x26,0xED]
unl_s3 =  [0xA9,0x9A,0x03,0x22,0x03,0x28,0xED]
unl_all = [0xA9,0x9A,0x07,0x22,0x01,0x02,0x03,0x04,0X05,0x38,0xED]
l_all   = [0xA9,0x9A,0x07,0x21,0x01,0x02,0x03,0x04,0x05,0x37,0xED]
m_s3 =    [0xA9,0x9A,0x05,0x15,0x02,0x01,0x01,0x1F,0xED]


sleep_time = 1


def read_status():
    ser.write("a")
    time.sleep(sleep_time)
    return ser.readall()
    
def lock(command):
    ser.write(command)
    time.sleep(sleep_time)

def unlock(command):
    ser.write(command)
    time.sleep(sleep_time)

#A9 9A 05 15 {id} {high} {low} {sum} ED
def set_angle(sid,high,low):
    cmd = [0xA9,0x9A,0x05,0x15,sid,high,low,0x00,0xED]
    checksum =0x00
    for i in range(2,len(cmd)-2):
        checksum += cmd[i] 
    cmd[-2] = checksum
    str_cmd = ''
    for i in range(0,len(cmd)):
        str_cmd += format(cmd[i],'02x') + ' '
    print("Command is %s. CheckSum is %s" % (str_cmd,hex(checksum)))
    hex_cmd = bytearray.fromhex(str_cmd)
    ser.write(hex_cmd)
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
    

def get_angle():
    s1 = [0xA9,0x9A,0x03,0x12,0x01,0x16,0xED]
    ser.write(s1)
    time.sleep(sleep_time)
    return ser.readall()

def refresh_angle():
    s = [0xA9,0x9A,0x02,0x11,0x13,0xED]
    ser.write(s)
    time.sleep(sleep_time)
    return ser.readall()

#print("refresh")
#print(refresh_angle())
#unlock(unl_all)
#print("set angle 1\n %s" % set_angle(1,20,20))
print("move 1\n %s" % move_servo(0x01,10,0))
print(read_status())
print("move 1\n %s" % move_servo(0x01,20,0))
print(read_status())
print("move 1\n %s" % move_servo(0x01,30,0))
print(read_status())
print("move 1\n %s" % move_servo(0x01,40,0))
print(read_status())
#print(read_status())

#print("lock 1-5")
#lock(l_all)
#read_status()

#print("unlock 1-5")
#unlock(unl_all)
#print(read_status())

#print("get angle 1 \n %s" % get_angle())



#print("lock 1-5")
#lock(l_all)
#print(read_status())

