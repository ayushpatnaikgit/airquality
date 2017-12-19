import serial
import time
ser=serial.Serial(port='COM12',timeout=3,baudrate=9600)

def hexShow(argv):  
    result = ''  
    hLen = len(argv)  
    for i in range(hLen):  
        hvol = argv[i]
        hhex = '%02x'%hvol  
        result += hhex+' '  
    #print ('hexShow:',result)
  

while True:
    time.sleep(0.5)
    retstr = ser.read(10)
    hexShow(retstr)
    if len(retstr)==10:
        if(retstr[0]==0xaa and retstr[1]==0xc0):
            checksum=0
            for i in range(6):
                checksum=checksum+int(retstr[2+i])
            if checksum%256 == retstr[8]:
                pm25=int(retstr[2])+int(retstr[3])*256
                pm10=int(retstr[4])+int(retstr[5])*256
                print ("pm2.5:%.1f pm10 %.1f"%(pm25/10.0,pm10/10.0))

 
