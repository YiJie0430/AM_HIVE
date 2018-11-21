WIFI Calibration test program version: SR3_beta1.1 , Station: T8R1
---------------------------------------
Start Time:Tue Nov 20 17:10:29 2018
Scan MAC address:688F2E470700
Try to connect NI tester at 192.168.0.100
                             Success!

set Port=3
wait dut boot...........
root@xe1-plume-rdk-broadband-hitron-nvram:~# pmf -e
Device is already in factory mode. Exit operation
root@xe1-plume-rdk-broadband-hitron-nvram:~#
Software Version: root@xe1-plume-rdk-broadband-hitron-nvram:~# cat /.version
2.0.0-0-stable-20181115011227 (ubuntu@jvm-ch2h-yocto-705
root@xe1-plume-rdk-broadband-hitron-nvram:~# pmf -f -r
echo end of stdOUT buffer $?
Success, file /var/certs/ca.pem read!
Success, file /var/certs/client.pem read!
Success, file /var/certs/client_dec.key read!
Finished, no more certificates found!
OK
root@xe1-plume-rdk-broadband-hitron-nvram:~#
NrmSetup Test time: 15.18 (sec)
---------------------------------------------------------------------------
Start up 2G by cd / && ./etc/init.d/art start
Check 2G initial ready Test time: 5.42 (sec)
---------------------------------------------------------------------------

Waitting NI Running TEST...... 
OK----------WLAN Initialize----------

	Test Time: 1509 (ms)
	Error message: No error.

< WLAN PowerCalibration >
	frequency	txchain	txgain	power	pcorr	voltage	temp
	
	Test Time: 50089 (ms)
	Error message: Error 10056, DUT_Control_QCA9381_9986.lvlibp:TCP Wait For Specific Response.vi<ERR>
Timed out waiting for desired response.

----------WLAN Close----------

	Test Time: 48 (ms)
	Error message: No error.


Finish,0

FAIL: 2G Tx Rx Verify Fail

End Time:Tue Nov 20 17:11:51 2018
total time: 82.10
Test Result:FAIL
