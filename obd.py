import bluetooth
import time

bd_addr1 = "00:1D:A5:68:98:8B"   #the address
port1 = 1    #Connect Port
sock1 = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  #config

RAW_dic={
    "0104" : "0A",
    "0105" : "35",
    "0106" : "22",
    "010B" : "75",
    "010C" : "3E80",
    "010D" : "10",
    "010E" : "05",
    "010F" : "50",
    "0110" : "6000",
    "011F" : "0200",
    "0121" : "0500",
    "012F" : "70",
    "0133" : "10",
    "013C" : "FF01",
    "0144" : "5656"
}

DATA={
    "ENG_LOAD" : 00,
    "COOLANT" : 00,
    "Short_Trim" : 00,
    "Intake_Press" : 00,
    "RPM" : 00,
    "Speed" : 00,
    "Valve_Time" : 00,
    "Intake_Temp" : 00,
    "Air_flow" : 00,
    "Run_Time" : 00,
    "Distance_MIL" : 00,
    "Fuel_Tank" : 00,
    "Baro_Press" : 00,
    "Catalyst_Temp" : 00,
    "FA_Raito" : 00
}


print("connect......")
time.sleep(2)

sock1.connect((bd_addr1 ,port1))

print("connected")

sock1.send(b'atl1\r')
time.sleep(0.2)
print(sock1.recv(1024).decode('utf-8').replace('\r\n',''))

sock1.send(b'ati\r')
time.sleep(0.2)
print(sock1.recv(1024).decode('utf-8').rstrip('\r\n'))

f=open("./obd.log",mode='w')


def acc(code):
        code += '\r'
        b_code=code.encode('utf-8')
        sock1.send(b_code)
        time.sleep(0.2)

        CH=sock1.recv(1024).decode('utf-8').strip().splitlines()

        print(CH)

        if len(CH)>2:
            TXT=CH[1].replace(" ","")
            RAW_dic[CH[0]]=TXT[4:]

        return 0


while True:

        # Coolant
        acc("0105")
        DAT=int(RAW_dic["0105"],16) - 40
        DATA["COOLANT"]=DAT

        #RPM
        acc("010C")
        DAT=int(RAW_dic["010C"]) / 4
        DATA["RPM"]

        #Speed
        acc("010D")
        DAT=int(RAW_dic["010D"])
        DATA["Speed"]=DAT

        #Timing Valve
        acc("010E")
        DAT=int(RAW_dic["010E"])/2 - 64
        DATA["Valve_Time"]=DAT

        #END load
        acc("0104")
        DAT=int(RAW_dic["0104"])/255
        DATA["ENG_LOAD"]=DAT

        # Intake Press
        acc("010B")
        DAT=int(RAW_dic["010B"])
        DATA["Intake_Press"]=DAT

        # Intake Temp
        acc("010F")
        DAT=int(RAW_dic["010F"])-40
        DATA["Intake_Temp"]=DAT

        # Catalyst Temp
        acc("013C")
        DAT=int(RAW_dic["013C"])/10-40
        DATA["Catalyst_Temp"]=DAT

        # MAF
        acc("0110")
        DAT=int(RAW_dic["0110"])/100
        DATA["Air_flow"]=DAT

        # ENG Time
        acc("011F")
        DAT=int(RAW_dic["011F"])
        DATA["Run_Time"]=DAT

        # Short
        acc("0106")
        DAT=int(RAW_dic["0106"])/128
        DATA["Short_Trim"]=DAT

        # distance
        acc("0121")
        DAT=int(RAW_dic["0121"])
        DATA["Distance_MIL"]=DAT

        # Fuel
        acc("012F")
        DAT=int(RAW_dic["012F"]) *100 /255
        DATA["Fuel_Tank"]=DAT

        # Baro
        acc("0133")
        DAT=int(RAW_dic["0133"])
        DATA["Baro_Press"]=DATA

        # Raito
        acc("0144")
        DAT=int(RAW_dic["0144"])/32768
        DATA["FA_Raito"]=DAT

        print(RAW_dic)
        print(DATA)


f.close()

