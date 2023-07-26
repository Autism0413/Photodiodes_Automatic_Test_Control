import time # 需要调用延时函数
import serial  # 需要调用串口库
import binascii  # 需要将传送的字符进行转换

def Quer_power(ser):
    if (ser.is_open):
        ser.write(b'\x55\xAA\x25\x01\xDA')  # 将传输字符串写入串口
        time.sleep(1)  # 延时1s，时间可以设置，最好设置大点，以免传输字符过多，传输
        n = ser.inWaiting()  # 求取串口缓存中回传的字符个数
        print('n=', n)  # 打印字符个数
        if n:
            data = ''
            data = ser.read(1000)  # 读取缓存中1000个字符，值越大越好，如果该值小于传输字
            # 符总长度，多余的字符会被抛弃
            print('get data from serial port:', data)  # 打印回传的字符
            # 计算power
            data_str = data.hex()#将传回数值转为字符串
            d6 = data_str[12] + data_str[13]
            d7 = data_str[14] + data_str[15]#取出字符串6.7位
            d6_10 = int(d6, 16)  #
            d7_10 = int(d7, 16)  # 将6.7位转为十进制
            dbm = (d6_10 * 256 + d7_10) / 100  #计算power
            return dbm
            # print(str(dbm)+'dBm')

def Quer_lenth(ser):
    if (ser.is_open):
        x=b'\x55\xAA\x25\x01\xDA'
        print(x)
        ser.write(x)  # 将传输字符串写入串口
        time.sleep(1)  # 延时1s，时间可以设置，最好设置大点，以免传输字符过多，传输
        n = ser.inWaiting()  # 求取串口缓存中回传的字符个数
        print('n=', n)  # 打印字符个数
        if n:
            data = ''
            data = ser.read(1000)  # 读取缓存中1000个字符，值越大越好，如果该值小于传输字
            # 符总长度，多余的字符会被抛弃
            print('get data from serial port:', data)  # 打印回传的字符
            #计算lenth
            data_str=data.hex()  #将返回值改为字符串
            d4= data_str[8] + data_str[9]
            d5= data_str[10] + data_str[11]#获取第4.5位十六进制
            d4_10=int(d4, 16)
            d5_10=int(d5, 16)#将4.5位转为10进制
            GHZ=(191099+d4_10*256+d5_10)
            length=299792458.0 /(GHZ+0.5)
            return GHZ,length
            # print(str(GHZ)+"\tGHz")
            # print(str(length)+"\tnm")

def set_lenth(ser,l):
    if (ser.is_open):
        a=l-191099
        # a = (299792458.0 / l - 191099 - 0.5)
        print(a)
        b4 = a / 256
        b5=a%256   #计算需要发送的四五位数值（十进制）
        # b4_16 = hex(int(b4))
        b4_16 = hex(int(b4))
        b5_16 = hex(int(b5))
        # b5_16 = hex(int(b5))  #将计算数值换为16进制
        c4=b4_16[2:]
        c5=b5_16[2:]
        #计算校验位并转为16进制
        c = int("55", 16) + int("aa", 16) + int("30", 16) + int("03", 16) + int(b4_16, 16) + int(b5_16, 16)
        c1 = 256 - (c % 256)
        c2=hex(c1-1)
        c3=c2[2:]
        if b4<16:
            c4="0"+str(c4)
        if b5<16:
            c5="0"+str(c5)
        if (c1-1)<16:
            c3="0"+str(c3)
        # x=r"\x55\xAA\x30\x03"+r"\x"+c4+r"\x"+c5+r"\x"+c3    + c4 + b'\\x' + c5 + b"\\x" + c3
        x = "55 AA 30 03"+" "+c4+" "+c5+" "+c3
        x1 = bytes.fromhex(x)
        print(x1)
        ser.write(x1)  # 将传输字符串写入串口


def set_power(ser,p):
    if (ser.is_open):
        a=p
        b4 = a / 256
        b5 = a % 256   #计算出4.5位
        b41=hex(int(b4))
        b51 = hex(int(b5))  #将4.5位转为十六进制字符串
        c4 = b41[2:]
        c5 = b51[2:]  #取出十六进制中的ox标识符
        d = int("55", 16) + int("aa", 16) + int("31", 16) + int("03", 16) + int(b41, 16) + int(b51, 16)
        d1 = 256 - (d % 256)
        d2 = hex(d1 - 1)
        d3 = d2[2:] #获得校验位去除ox后的16进制码
        if b4<16:
            c4="0"+str(c4)
        if b5<16:
            c5="0"+str(c5)
        if (d1-1)<16:
            d3="0"+str(d3)
        x = "55 AA 31 03" + " " + c4 + " " + c5 + " " + d3
        x1 = bytes.fromhex(x)
        print(x1)
        ser.write(x1)  # 将传输字符串写入串口

def open(ser):
    if (ser.is_open):
        ser.write(b'\x55\xAA\x32\x02\x08\xc4')

def close(ser):
    if(ser.is_open):
        ser.write(b'\x55\xAA\x32\x02\x00\xcc')

if __name__ == '__main__':
    ser = serial.Serial()  # 生成串口
    ser.parity=serial.PARITY_NONE
    ser.stopbits=serial.STOPBITS_ONE
    ser.baudrate = 9600  # 设置串口波特率
    ser.port = 'COM9'  # 设置串口号
    ser.timeout = 0.1  # 设置串口通信超时时间
    ser.close()  # 先关闭串口，以免串口被占用
    ser.open()  # 打开串口
    print(ser.is_open)  # 打印串口状态
    strSerial = ''  # 初始化串口传输字符串
    # if (ser.is_open):
    #     # ser.write(b'\x55\xAA\x24\x01\xDB')  # 将传输字符串写入串口
    #     ser.write(b'\xEF\xEF\x05\xFF\x88\x01\x00\xFF')  # 将传输字符串写入串口
    #     time.sleep(1)  # 延时1s，时间可以设置，最好设置大点，以免传输字符过多，传输
    #     # 时间过长，回传失败
    #     n = ser.inWaiting()  # 求取串口缓存中回传的字符个数
    #     print('n=', n)  # 打印字符个数
    #     if n:
    #         data = ''
    #         data = ser.read(1000) # 读取缓存中1000个字符，值越大越好，如果该值小于传输字
    #         # 符总长度，多余的字符会被抛弃
    #         print('get data from serial port:', data)  # 打印回传的字符

            # # 计算power
            # data_str=data.hex()
            # d4= data_str[8] + data_str[9]
            # d5= data_str[10] + data_str[11]
            # d6 = data_str[12] + data_str[13]
            # d7 = data_str[14] + data_str[15]
            # d6_10 = int(d6, 16)  #
            # d7_10 = int(d7, 16)  # 7
            # d4_10=int(d4, 16)
            # d5_10=int(d5, 16)
            # dbm = (d6_10 * 256 + d7_10) / 100
            # print(str(dbm)+'dBm')
            # GHZ=(191099+d4_10*256+d5_10)
            # length=299792458.0 /(GHZ+0.5)
            # print(str(GHZ)+"\tGHz")
            # print(str(length)+"\tnm")
            # 计算minGHZ
            # data_str=data.hex()
            # print(data_str)
            # d6 = data_str[12] + data_str[13]
            # d7 = data_str[14] + data_str[15]
            # d8 = data_str[16] + data_str[17]
            # d6_10 = int(d6, 16)  #
            # d7_10 = int(d7, 16)  # 7
            # d8_10=int(d8, 16)
            # minghz = d6_10 * 65536 + d7_10*256+d8_10
            # print(str(minghz)+'ghz')

    # ser.close()  # 程序结束时关闭串口，以免串口被占用
    # dbm= Quer_power(ser)
    # print(str(dbm) + 'dBm')
    # open(ser)
    set_lenth(ser,193370)
    l = 299792458.0 / (193370+ 0.5)
    l1 = round(l, 3)
    print(l1)
    # time.sleep(10)
    # strSerial = ''  # 初始化串口传输字符串
    # GHZ,length=Quer_lenth(ser)
    # print(str(GHZ)+"\tGHz")
    # print(str(length)+"\tnm")

    # p=12.5*100
    # set_power(ser,p)
    # print(not ser.is_open)


