# SNMP Manufacturing functions
from MFT512_W21 import *
from toolslib_W21 import *
import dbi,odbc
import socket
import htx,time,os,threading

snmplib="22" 


def lOpenBackDoor(ipaddr):
    for i in xrange(5):
        mac_dict = Snmp.SnmpGet(ipaddr,ifPhysAddress2_OID,community="private")
        if mac_dict: break
        time.sleep(1)
    else:
        print "Can't get MAC address"
        return 0
    mac_addr = mac_dict.values()[0]
    print "Cable Modem MAC address:%s"%MacTrans(mac_addr)
    word1 = ord(mac_addr[0])*256+ord(mac_addr[1])
    word2 = ord(mac_addr[2])*256+ord(mac_addr[3])
    word3 = ord(mac_addr[4])*256+ord(mac_addr[5])
    mib_backdoor = ".%d.%d"%(word1^word2^word3,word1+word2+word3)
    #print "Open backdoor!!!\n\n"
    Snmp.SnmpGet(ipaddr,docsDevServerBootState_OID+mib_backdoor)
    return 1

def Insert_mac_csn_ssidkey(mac,csn,key):
       db = odbc.odbc("TEST/TEST/test")
       cursor = db.cursor()
       tmp = time.localtime(time.time())
       testtime =  "%d/%d/%d %d:%d:%d"%tmp[:6]
       cursor.execute("insert into BVW3653Elisa_mac_sn_ssidkey (MAC,CSN,SSIDKey,DateTime) values('%s','%s','%s','%s')"%(mac,csn,key,testtime))
       #time.sleep(1)
       cursor.execute("select CSN from BVW3653Elisa_mac_sn_ssidkey where MAC = '%s'"%mac)
       data = cursor.fetchone()
       if data:
          SetPatternColor(1)
          print 'Insert key to DB finish.'
          SetPatternColor()
          return 1
       else:
          return 0


def lDumpMemory(ipaddr,address,length):
    result = ""
    while length:
        if length > 1024:
            size=1024
        else:
            size=length
        for i in xrange(3):
            modemProdMemoryRead_OID = "1.3.6.1.4.1.8595.1.400.4.1.10.%d.%d.%d"%(int("5ca",16),size,address)
            data = TransferBinaryToHex(Snmp.SnmpGet(ipaddr,modemProdMemoryRead_OID,community="private").values()[0])
            if data:
                break
            time.sleep(1)
        result += data
        length -= size
        address += size
    return TransferHexToBinary(result)
   


def lCommandSnmp(ipaddr,command):
    modemProdCommandLine_OID = ".1.3.6.1.4.1.8595.1.400.4.1.9.0"
    return Snmp.SnmpSet(ipaddr,modemProdCommandLine_OID,"s","SetTelnetd 1 1 1",community=rw_community)
    #tmp = Xurl("snmp://%s/private/HITRON-DOCSIS-PRODUCTION-EXT-MIB/modemProdCommandLine.0/s"%(ipaddr))
    #return tmp.set(command)



def lPrintSysDescr(ipaddr):
    sysDescr_OID = "1.3.6.1.2.1.1.1.0"
    value = result = Snmp.SnmpGet(ipaddr,sysDescr_OID).values()[0]
    #value = result = Xurl("snmp://%s/private/RFC1213-MIB/sysDescr.0/s"%
                       #(ipaddr)).get()
    print SetPatternColor()+               "DOCSIS Version:      ",
    print SetPatternColor(1)+           result[:result.find("<<")].strip()
    result = result[result.find("<<")+2:result.find(">>")].split(";")
    print SetPatternColor()+               "Hardware Version:    ",
    print SetPatternColor(1)+           result[0].split(":")[1].strip()
    print SetPatternColor()+               "Vendor:              ",
    print SetPatternColor(1)+           result[1].split(":")[1].strip()
    print SetPatternColor()+               "BootLoader Version:  ",
    print SetPatternColor(1)+           result[2].split(":")[1].strip()
    print SetPatternColor()+               "Software Version:    ",
    print SetPatternColor(1)+           result[3].split(":")[1].strip()
    print SetPatternColor()+               "Model Name:          ",
    print SetPatternColor(1)+           result[4].split(":")[1].strip()
    SetPatternColor()
    return value

def lCompareSysDescr(ipaddr):
    value = 0 
    sysDescr_OID = "1.3.6.1.2.1.1.1.0"
    result = Snmp.SnmpGet(target,sysDescr_OID).values()[0]
    #result = Xurl("snmp://%s/private/RFC1213-MIB/sysDescr.0/s"%
                       #(ipaddr)).get()
    print SetPatternColor()+               "DOCSIS Version:      ",
    print SetPatternColor(True)+           result[:result.find("<<")].strip()
    result = result[result.find("<<")+2:result.find(">>")].split(";")
    print SetPatternColor()+               "Hardware Version:    ",
    if result[0].split(":")[1].strip()<> HW_REV:
        SetPatternColor(0)
        value+=1
    else:
        SetPatternColor(1)
    print result[0].split(":")[1].strip()
    print SetPatternColor()+               "Vendor:              ",
    if result[1].split(":")[1].strip()<> VENDOR:
        SetPatternColor(0)
        value+=1
    else:
        SetPatternColor(1)
    print result[1].split(":")[1].strip()
    print SetPatternColor()+               "BootLoader Version:  ",
    print SetPatternColor(True)+           result[2].split(":")[1].strip()
    print SetPatternColor()+               "Software Version:    ",
    if result[3].split(":")[1].strip()<> SW_REV:
        SetPatternColor(0)
        value+=1
    else:
        SetPatternColor(1)
    print result[3].split(":")[1].strip()
    print SetPatternColor()+               "Model Name:          ",
    if result[4].split(":")[1].strip()<> MODEL:
        SetPatternColor(0)
        value+=1
    else:
        SetPatternColor(1)
    print result[4].split(":")[1].strip()
    SetPatternColor()
    return value

def lLinkReady(target,network_card,connect_timeout):
    SendMessage(msgcolor_std+"Waiting linkup")
    if not IsLinkup(network_card,7200):
        raise Except("PC NIC never linkup")
    SendMessage(msgcolor_std+"LAN Connecting\n")
    if not htx.IsConnect(target,connect_timeout):
        raise Except("Can't connect to %s in %d seconds"%(target,connect_timeout))
    


def lComLogin(term,username,password,time_out):
    print "CLI serial port Login...."
    a = 0
    while 1:
        term.get()
        term<< ""
        if 'ZON HUB>' in term.wait("",2)[-1]:return 1
        term.get()
        term<< ""
        data = term.wait("Password:",2)[-1]
        #data = lWaitCmdTerm(term,"","Username:",5)
        #print data
        if "Password" in data or "Username" in data:
            while 1:
                term<<username
                data = term.wait(">",1)
                if "ZON HUB>" in data[-1]: return 1
                
        else:
            a = a+1
            if a*2 > time_out:
                raise Except("Can't login in %d seconds"%(time_out))
            
        
    
    

def lWaitRebootReady(term):
    for i in range(3):
        data = term.wait("Scanning frequency",15)
    if not data:
        raise Except("Reboot fail")

def lIniCmd1(term,device_ip):
    lWaitCmdTerm(term,"prod cbccm","production>",5)
    lWaitCmdTerm(term,"setdef 2","production>",5)
    lWaitCmdTerm(term,"exit","MAIN>",5)
    term<<"reset"
    return IsDisconnect(device_ip,30)

def lIniCmd2(term):
    lWaitCmdTerm(term,"debug calibration_on","MAIN>",5)
    lWaitCmdTerm(term,"prod cbccm","production>",5)
    lWaitCmdTerm(term,"prodmib 1","production>",5)
    lWaitCmdTerm(term,"exit","MAIN>",5)

def WlanDload(term,tftp_IP,ver):
    print "Install Wireless lan"
    lWaitCmdTerm(term,"prod cbccm","production>",5)
    lWaitCmdTerm(term,"wlandld","Server IP",5)
    lWaitCmdTerm(term,tftp_IP,"production>",10)
    lWaitCmdTerm(term,"exit","MAIN>",5)
    lWaitCmdTerm(term,"wla","wlan_ap>",5)
    data = lWaitCmdTerm(term,"ver","wlan_ap>",5)
    data = data.split("EEPROM Version =")[1].split("wlan_ap>")[0].strip()
    if data<>ver:
        raise Except("EEPROM Version = %s"%(data))
    SetPatternColor(1)
    print "Wireless EEPROM Version: %s (%s)"%(data,ver)
    SetPatternColor()
    lWaitCmdTerm(term,"exit","MAIN>",5)


    
def lDebug(term):
    lWaitCmdTerm(term,"prod cbccm","production>",3)
    term << "cal"
    data = term.wait(">",5)
    if "Command not found" in data:
        lWaitCmdTerm(term,"exit",">",3) 
        lWaitCmdTerm(term,"debug 8004",">",3)
    else:
        lWaitCmdTerm(term,"exit",">",3)
        lWaitCmdTerm(term,"exit",">",3) 

def lDebugCmd(term,cmd1,cmd2):
    lWaitCmdTerm(term,"prod cbccm","production>",3)
    term << cmd1
    data = term.wait(">",5)[-1]
    if "Command not found" in data:
        lWaitCmdTerm(term,"exit",">",3) 
        lWaitCmdTerm(term,"debug %s"%cmd2,">",3)
    else:
        lWaitCmdTerm(term,"exit",">",3)

def MacTrans(mac):
    return "%02X%02X%02X%02X%02X%02X"%(ord(mac[0]),ord(mac[1]),ord(mac[2]),ord(mac[3]),ord(mac[4]),ord(mac[5]))

def GetMAC(term):
    
    lWaitCmdTerm(term,"doc","docsis>",3)
    lWaitCmdTerm(term,"P","Production>",3)
    data = lWaitCmdTerm(term,"prodsh","Production>",3)
    data = data.split("Cable Modem MAC")[-1].split("Lan MAC")[0]
    data = data.split("- <")[-1].split(">")[0].strip()
    print data
    data = "".join(data.split("-"))
    return data

def StartCmd(term,cmd,waitstr,wait_time):
    a = 0
    while 1:
        term.get()
        term << "%s"%cmd
        data = term.wait("%s"%waitstr,1)
        a = a+1
        if not waitstr in data[-1]:
            if a < wait_time:
                continue
            raise Except("failed: %s"%cmd)
        else:
            return data

def GetModelName(mac,ServerIP='127.0.0.1',ServerPort=1800,timeout=25):#BC14012EFAA0
    MesSocket=htx.UDPService(ServerIP,ServerPort,timeout)
    MesSocket.set('4,'+ mac)  
    Result=MesSocket.get()
    print '\n======================='
    print '|ModelName:%s'%Result
    print '=======================\n'
    if Result != '':
       return Result
    raise Except("failed: Connection MES Server Fail ")
            
def GetModelName_(target):
    sysDescr_OID = "1.3.6.1.2.1.1.1.0"
    value = Snmp.SnmpGet(target,sysDescr_OID).values()[0]
    model_name =  value.split("MODEL:")[1].split(">>")[0].strip()
    #if not os.path.isfile("c:/product/BRG-35503/%s.ini"%model_name):
    #    raise Except ("failed:No such file %s.ini"%model_name)
    return model_name

def GetConsoleModelName(term):
    #lWaitCmdTerm(term,"cli",">",3)
    value = lWaitCmdTerm(term,"ven",">",3)
    model = value.split("Model Name:")[1].split("Vendor Name")[0].strip()
    return model


        




