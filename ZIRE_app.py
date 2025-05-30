import os
import sys
import time
import subprocess
import shutil
from datetime import datetime
from ZIRE_errorcode import *
from ZIRE_dataclass import *
from ZIRE_configure import *
from ZIRE_lib import ZIRE

ZireDAQ = ZIRE()
ZireCFG = CONFIGURATOR()
settings = {}
arguments = sys.argv[1:] 
concentrator_A_IP = "" 
target = 0
save_path = ""
comment = ""
role = ""

configure = False
data_acq = False
stairs = False
monitor = False
ts_reset = False

first = False
ip_check = False
json_check = False
target_check = False
time_check = False
pack_check = False
path_check = False
free_check = False
comment_check = False
maxt_check = False
startt_check = False
stept_check = False
times_check = False
daq_check = False
asic_check = False
ch_check = False
status_check = False
ctest_check = False
########################################
########################################
#concentrator_A_IP = "192.168.102.16" 
#path = "cfg_sample.json"
#first = True
#ip_check = True
#json_check = True
#configure = True
########################################
########################################

while arguments:
    arg = arguments.pop(0)
    if arg == '-ip':
        concentrator_A_IP = arguments.pop(0)
        ip_check = True

    elif arg == '-json':
        path = arguments.pop(0)
        if os.path.exists(path):
            json_check = True
        else:
            print("[ZIRE-APP]: The file does not exsist!")
            exit
    elif arg == "-config":
        configure = True

    elif arg == '-first':
        first = True

    elif arg == '-start':
        data_acq = True
    
    elif arg == '-packets':
        target = arguments.pop(0)
        pack_check = True

    elif arg == '-time':
        target = arguments.pop(0)
        time_check = True

    elif arg == '-free':
        free_check = True

    elif arg == '-name':
        if arguments:  # Controlla se ci sono ulteriori argomenti
            save_path = arguments.pop(0)
        path_check = True

    elif arg == '-comment':
        comment = arguments.pop(0)
        comment_check = True
    
    elif arg == '-role':
        role = arguments.pop(0)

    elif arg == '-stairs':
        stairs = True

    elif arg == '-min':
        start_t = arguments.pop(0)
        startt_check = True

    elif arg == '-max':
        max_t = arguments.pop(0)
        maxt_check = True

    elif arg == '-times':
        times = arguments.pop(0)
        times_check = True

    elif arg == '-step':
        step_t = arguments.pop(0)
        stept_check = True

    elif arg == '-test':
        test_type = arguments.pop(0)
        monitor = True

    elif arg == '-daq':
        daq_id = arguments.pop(0)
        daq_check = True

    elif arg == '-asic':
        asic_id = arguments.pop(0)
        asic_check = True

    elif arg == '-ch':
        ch_id = arguments.pop(0)
        ch_check = True
    
    elif arg == '-status':
        test_status = arguments.pop(0)
        status_check = True

    elif arg == '-ctest':
        ctest_check = True

    elif arg == '-reset':
        ts_reset = True

        
if __name__ == "__main__":
    if configure:
        print("[ZIRE-APP]: \n\tMODE --> CONFIGURATION\n")
        if ip_check and json_check:
            print(f"[ZIRE-APP]: Ip entered: {concentrator_A_IP}")
            print("[ZIRE-APP]: Configuration File Found!")

            settings, valid = ZireCFG.load_settings(path, True)

            if valid:
                print("[ZIRE-APP]: Starting connection..")
                ret = ZireDAQ.connect(concentrator_A_IP)

                if ret == NI_OK:
                    print(f"[ZIRE-APP]: ZIRE Concentrator at {concentrator_A_IP} succefully connected!")
                    ZireCFG.send_configuration(ZireDAQ, settings)

                else:
                    print(f"[ZIRE-APP]: Something wrong conneting ZIRE Concentrator at {concentrator_A_IP} !")
                    exit
            else:
                exit

        elif not ip_check:
            print("[ZIRE-APP]: Missing IP")
            
        elif not ip_check:
            print("[ZIRE-APP]: Missing cfg.json")

    elif data_acq:
        print("[ZIRE-APP]: \n\tMODE --> DATA ACQUISITION\n")
        if ip_check and comment_check and path_check:

            #if not os.path.exists(save_path):
            #    os.mkdir(save_path)

            if os.path.exists(save_path+"data.bin"):
                print("[ZIRE-APP]: Directory non empty")
                ow = input("Overwrite ? y/n: ")

                if ow == "y":
                    print("[ZIRE-APP]: Overwriting...")
                    os.remove(save_path+"data.bin")
                else:
                    print("[ZIRE-APP]: Closing connection, exiting application...")
                    sys.exit()

            if os.path.exists(save_path+"housekeeping.bin"):
                os.remove(save_path+"housekeeping.bin")

            if time_check and pack_check:
                print("[ZIRE-APP]: Too many targets")

            elif time_check:
                if target == 0:
                    print ("[ZIRE-APP]: Selected 0 as target. Invalid!")
                    sys.exit()

                print("[ZIRE-APP]: Starting connection..")
                ret = ZireDAQ.connect(concentrator_A_IP)
                if ret == NI_OK:
                    print(f"[ZIRE-APP]: ZIRE Concentrator at {concentrator_A_IP} succefully connected!")
                    if os.path.exists(f".{concentrator_A_IP}_prev_cfg.json"):
                        print("[ZIRE-APP]: Storing cfg settings")
                        with open(f".{concentrator_A_IP}_prev_cfg.json", 'r') as file:
                            data = json.load(file)

                        data['Date'] =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        data['Comment'] = comment
                        data['Measure'] = f"Acquisition for {target} packets"

                        # Salva il JSON aggiornato su un nuovo file

                        with open(save_path + "_cfg.json", 'w') as file:
                            json.dump(data, file, indent=4)

                    print(f"[ZIRE-APP]: Acquisition for {target} seconds")
                    ZireDAQ.start_acq_raw(save_path, True, int(target), role)
                    ret = ZireCFG.reset_timestamp(ZireDAQ)

            elif pack_check:
                if target == 0:
                    print ("[ZIRE-APP]: Selected 0 as target. Invalid!")
                    sys.exit()

                print("[ZIRE-APP]: Starting connection..")
                ret = ZireDAQ.connect(concentrator_A_IP)
                if ret == NI_OK:
                    print(f"[ZIRE-APP]: ZIRE Concentrator at {concentrator_A_IP} succefully connected!")
                    if os.path.exists(f".{concentrator_A_IP}_prev_cfg.json"):
                        print("[ZIRE-APP]: Storing cfg settings")
                        with open(f".{concentrator_A_IP}_prev_cfg.json", 'r') as file:
                            data = json.load(file)

                        data['Date'] =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        data['Comment'] = comment
                        data['Measure'] = f"Acquisition for {target} packets"

                        # Salva il JSON aggiornato su un nuovo file

                        with open(save_path + "_cfg.json", 'w') as file:
                            json.dump(data, file, indent=4)

                    print(f"[ZIRE-APP]: Acquisition for {target} packets...")
                    ZireDAQ.start_acq_raw(save_path, False, int(target), role)
                    subprocess.run(["/bin/python3", "decode_data.py", save_path])
                    ret = ZireCFG.reset_timestamp(ZireDAQ)

            elif free_check:
                print("[ZIRE-APP]: Starting connection..")
                ret = ZireDAQ.connect(concentrator_A_IP)
                if ret == NI_OK:
                    print(f"[ZIRE-APP]: ZIRE Concentrator at {concentrator_A_IP} succefully connected!")
                    if os.path.exists(f".{concentrator_A_IP}_prev_cfg.json"):
                        print("[ZIRE-APP]: Storing cfg settings")
                        with open(f".{concentrator_A_IP}_prev_cfg.json", 'r') as file:
                            data = json.load(file)

                        data['Date'] =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        data['Comment'] = comment
                        data['Measure'] = "Free Acquisition Mode"

                        # Salva il JSON aggiornato su un nuovo file

                        with open(save_path + "_cfg.json", 'w') as file:
                            json.dump(data, file, indent=4)

                    print("[ZIRE-APP]: Free Acquisition Mode...")
                    ZireDAQ.start_acq_raw(save_path, False, 0, role)
                    #subprocess.run(["python", "decode_data.py", save_path])
                    #ret = ZireCFG.reset_timestamp(ZireDAQ)

        elif not ip_check:
            print("[ZIRE-APP]: Missing IP")
        elif not comment_check:
            print("[ZIRE-APP]: Missing comment")
        elif not path_check:
            print("[ZIRE-APP]: Missing path where save data")

    elif stairs:
        print("[ZIRE-APP]: \n\tMODE --> STAIRS\n")

        if ip_check and path_check:
            if not os.path.exists(save_path):
                os.mkdir(save_path)
        
            if os.path.exists(save_path+"stairs.bin"):
                print("[ZIRE-APP]: Directory non empty")
                ow = input("Overwrite ? y/n: ")

                if ow == "y":
                    print("[ZIRE-APP]: Overwriting...")
                    os.remove(save_path+"stairs.bin")
                else:
                    print("[ZIRE-APP]: Closing connection, exiting application...")
                    sys.exit()
        elif not ip_check:
            print("[ZIRE-APP]: Missing IP")
        elif not path_check:
            print("[ZIRE-APP]: Missing path where save data")

        if maxt_check and startt_check and stept_check and times_check:
            print("[ZIRE-APP]: Starting connection..")
            ret = ZireDAQ.connect(concentrator_A_IP)
            if ret == NI_OK:
                print(f"[ZIRE-APP]: ZIRE Concentrator at {concentrator_A_IP} succefully connected!")

                threshold = int(start_t)
                ZireCFG.all_tlatch_off(ZireDAQ)
                while (threshold < int(max_t)):
                    print(f"[ZIRE-APP]: Setting threshold to {threshold}")
                    ZireCFG.stairs_setthres(ZireDAQ, threshold)

                    #RUN WITH DAC SET TO 0
                    #print("[ZIRE-APP]: Setting DAC THRS to 0")
                    #ZireCFG.stairs_setdac(ZireDAQ, 0)
                    #if (ZireDAQ.start_stairs(save_path, int(times)) != 0) :
                    #    print("[ZIRE-APP]: Something went wrong while acquiring stairs")

                    #RUN WITH DAC SET TO 7
                    print("[ZIRE-APP]: Setting DAC THRS to 7")
                    ZireCFG.stairs_setdac(ZireDAQ, 7)
                    if (ZireDAQ.start_stairs(save_path, int(times)) != 0) :
                        print("[ZIRE-APP]: Something went wrong while acquiring stairs")

                    #RUN WITH DAC SET TO 15
                    #print("[ZIRE-APP]: Setting DAC THRS to 15")
                    #ZireCFG.stairs_setdac(ZireDAQ, 255)
                    #if (ZireDAQ.start_stairs(save_path, int(times)) != 0) :
                    #    print("[ZIRE-APP]: Something went wrong while acquiring stairs")

                    threshold += int(step_t)

                ZireCFG.all_tlatch_on(ZireDAQ)
                print("[ZIRE-APP]: Stairs procedure completed!")
                #subprocess.run(["python", "decode_data.py", "stairs", save_path])
                ret = ZireCFG.reset_timestamp(ZireDAQ)

            else:
                print("[ZIRE-APP]: Something went wrong while acquiring stairs")
        else:
            print("[ZIRE-APP]: Missing parameter")
   
    elif monitor:
        print("[ZIRE-APP]: \n\tMODE --> SET MONITOR\n")
        if ip_check:
            print("[ZIRE-APP]: Starting connection..")
            ret = ZireDAQ.connect(concentrator_A_IP)

            if ret == NI_OK:
                print(f"[ZIRE-APP]: ZIRE Concentrator at {concentrator_A_IP} succefully connected!")            
                ret = ZireCFG.set_monitor(ZireDAQ, test_type, daq_id, int(asic_id), ch_id, "on")

                if ret == 0:
                    print(f"[ZIRE-APP]: Setting channel {ch_id} of ASIC {asic_id} of DAQ {daq_id } for test of {test_type}")
                else:
                    print("[ZIRE-APP]: Something went wrong setting monitor")
            else:
                print(f"[ZIRE-APP]: Something wrong conneting ZIRE Concentrator at {concentrator_A_IP} !")
                exit

        elif not ip_check:
            print("[ZIRE-APP]: Missing IP")

        elif not daq_check:
            print("[ZIRE-APP]: Missing DAQ ID")

        elif not asic_check:
            print("[ZIRE-APP]: Missing ASIC ID")

        elif not ch_check:
            print("[ZIRE-APP]: Missing CHANNEL ID") 

        elif not status_check:
            print("[ZIRE-APP]: Missing Test Status")   

    elif ts_reset:
        if ip_check:
            print("[ZIRE-APP]: Starting connection..")
            ret = ZireDAQ.connect(concentrator_A_IP)
            if ret == NI_OK:
                print(f"[ZIRE-APP]: ZIRE Concentrator at {concentrator_A_IP} succefully connected!")
                ret = ZireCFG.reset_timestamp(ZireDAQ)
                print("[ZIRE-APP]: Timestamp reset!")
                
        elif not ip_check:
            print("[ZIRE-APP]: Missing IP")

    elif ctest_check:
        print("[ZIRE-APP]: \n\tMODE --> CTEST\n")
        print("[ZIRE-APP]: Starting connection..")
        ret = ZireDAQ.connect("192.168.102.16")
        if not os.path.exists("RUNS/ctest"):
                os.mkdir("RUNS/ctest")
                
        if os.path.exists("RUNS/ctest/data.bin"):
            print("[ZIRE-APP]: Directory non empty, overwriting...")
            os.remove("RUNS/ctest/data.bin")

        gain = 62

        while (gain != 0):
            print("[ZIRE-APP]: CTEST HG GAIN", gain)
            ZireCFG.set_hg_gain(ZireDAQ, 0, "00", gain)
            time.sleep(2)
            ZireDAQ.start_acq_raw("RUNS/ctest", False, 1)
            gain -= 1


    else:
        print("[ZIRE-APP]: No valid command detected!")
    
    print("[ZIRE-APP]: Closing connection, exiting application...")