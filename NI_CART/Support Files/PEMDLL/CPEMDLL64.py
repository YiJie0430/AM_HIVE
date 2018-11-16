import os,sys,time
from ctypes import *  
para = sys.argv
if len(para) != 2 or para[1].upper() not in ("PON","POFF","GET3V3I"):
    print("Parameter Error\n  --- PON\n  --- POFF\n  --- GET3V3I\n") 
else:
    para = para[1].upper() 
    pem = CDLL('SolPeTsDll.dll')
    status = pem.PETS_INIT()
    if status != 0:
       print("failed: PETS_INIT NG !")
    else:
       
       #currpemno = 0
       #for i in range(4):
       #    status = pem.PETS_VALIDPEM(i)
       #    if status==1:
       #       currpemno = i
       #       break
       #else:print("Not found pem no.")
       if para=="POFF":
          status = pem.PETS_POFF()
       if para=="PON":
          status = pem.PETS_PON()
       if para=="GET3V3I":
          curr = c_double(0.00)
          status = pem.PETS_GET3V3I(byref(curr))
          print("GET3V3I : %0.2f mA"%(curr.value*1000))
       if status != 0:
          print("failed: PETS_%s NG!"%para)
       else: 
          print("PETS_%s OK!"%para)
