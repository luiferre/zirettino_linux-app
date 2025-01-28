import subprocess
import json
import time

for asic in range(2, 3):
    print(f"************************************************************************")
    print(f"*************************** ASIC {asic} ********************************")
    print(f"************************************************************************\n")

    command_cfg = [
        '/bin/python3',
        'ZIRE_app.py',
        '-config',
        '-ip',
        '192.168.102.173',
        '-json',
        f'./test_asic{asic}/ctest.json'
    ] 

    for i in range (32):
        # Carica il JSON da un file o da una stringa
        with open("//home//utente//projects//ZIRETTINO//LINUXAPP//ctest.json", "r") as file:
            data = json.load(file)

        # Modifica il valore desiderato
        data["config"]["daq_1"][f"asic_{asic+1}"][f"ch_{i}"]["test_lg"] = True
        data["config"]["daq_1"][f"asic_{asic+1}"][f"ch_{i}"]["test_hg"] = True

        with open(f"//home//utente//projects//ZIRETTINO//LINUXAPP//test_asic{asic}//ctest.json", "w") as file:
            json.dump(data, file, indent=4)

        print(f"***********************************************************\tTEST CH {i}")
        cfg_process = subprocess.Popen(command_cfg)
        cfg_process.wait()
        time.sleep(2)

        command_start = [
            '/bin/python3',
            'ZIRE_app.py',
            '-start',
            '-ip',
            '192.168.102.173',
            '-name',
            f'./test_asic{asic}/ch_{i}',
            '-comment',
            'test_app',
            '-packets',
            '5000',
            '-asic',
            f'{asic}'
        ]
        run_process = subprocess.Popen(command_start)
        run_process.wait()
        time.sleep(2)
