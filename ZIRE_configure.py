import json
import shutil
import os
import time
from ZIRE_lib import ZIRE

# Definizione classe daq_params
class daq_params:
    class asic:
        class ch:

            def __init__(self, name):
                self.id = name
                self.mask = False
                self.test_hg = False
                self.test_lg = False
                self.gain_hg = 0
                self.gain_lg = 0

        def __init__(self, name):
            self.id = name
            self.chs = [self.ch(str(i)) for i in range(32)]

    def __init__(self, name):
        self.id = name
        self.asics = [self.asic("a"), self.asic("b"), self.asic("c"), self.asic("d")]

# Definizione classe CONFIGURATOR
class CONFIGURATOR:
    def __init__(self):
        self.settings = {}
        self.first = True
        self.ftk_params = daq_params('ftk')
        self.pst_params = daq_params('pst')
        self.o_ftk_params = daq_params('ftk')
        self.o_pst_params = daq_params('pst')
        self.cfg = {}
        self.o_cfg = {}
        self.json = False
        self.changed_1 = False
        self.changed_2 = False
        self.corr = {
            0: 'A',
            1: 'B',
            2: 'C',
            3: 'D'
        }

    def load_json(self, json_path, cfg_d: dict):
        
        if os.path.exists(json_path):
            self.json = True
            with open(json_path) as file:
                data = json.load(file)
                cfg_d['identifier'] = data['identifier']
                cfg_d['ipaddress'] = data['ipaddress']
                self.config = data['config']

                self.trigger =  self.config['trigger']
                self.hv_settings =  self.config['hv_settings']
                
                cfg_d["conc_trg_mode"] = self.trigger['concentrator_mode']
                cfg_d["conc_trg_logic"] = self.trigger['concentrator_logic']
                cfg_d["concentrator_periodic"] = self.trigger['concentrator_periodic']
                cfg_d["ctrig_edit_counts"] = self.trigger['ctrig_edit_counts']
                cfg_d["daq1"] = self.trigger['daq1']
                cfg_d["daq1_trg_en"] = self.trigger['daq1_trg_en']
                cfg_d["daq1_trg_mode"] = self.trigger['daq1_trg_mode']
                cfg_d["daq1_trg_period"] = self.trigger['daq1_trg_period']
                cfg_d["daq1_trg_src"] = self.trigger['daq1_trg_src']
                cfg_d["daq2"] = self.trigger['daq2']
                cfg_d["daq2_trg_en"] = self.trigger['daq2_trg_en']
                cfg_d["daq2_trg_mode"] = self.trigger['daq2_trg_mode']
                cfg_d["daq2_trg_period"] = self.trigger['daq2_trg_period']
                cfg_d["daq2_trg_src"] = self.trigger['daq2_trg_src']
                cfg_d["validation"] = self.trigger['validation']
                cfg_d["validation_src"] = self.trigger['validation_src']                
                cfg_d["timeout_valid"] = self.trigger['timeout_valid']
                cfg_d["discard"] = self.trigger['discard']
                cfg_d["fake_gen"] = self.trigger['fake_gen']
                cfg_d["mode"] = self.trigger['mode']
                cfg_d["trigpsc"] = self.trigger['trigpsc']
                cfg_d["holdwin"] = self.trigger['holdwin']
                cfg_d["HGpdorth"] = self.trigger['HGpdorth']
                cfg_d["LGpdorth"] = self.trigger['LGpdorth']
                cfg_d["PSCbypass"] = self.trigger['PSCbypass']
                cfg_d["rstb_en"] = self.trigger['rstb_en']

                for i in range(4):
                    cfg_d[f"daq1_asics{i}_fastshsource"]    = self.config['daq_1']['asic_' + str(i+1)]['general']['fastsh_source']
                    cfg_d[f"daq1_asics{i}_HGshtime"]         = self.config['daq_1']['asic_' + str(i+1)]['general']['HGshtime']
                    cfg_d[f"daq1_asics{i}_LGshtime"]         = self.config['daq_1']['asic_' + str(i+1)]['general']['LGshtime']
                    cfg_d[f"daq1_asics{i}_timethrs"]         = self.config['daq_1']['asic_' + str(i+1)]['general']['timethrs']
                    cfg_d[f"daq1_asics{i}_chargeth"]         = self.config['daq_1']['asic_' + str(i+1)]['general']['chargeth']
                    cfg_d[f"daq1_asics{i}_inputDACref"]     = self.config['daq_1']['asic_' + str(i+1)]['general']['input_DACref']
                                      
                for j in range(4):
                    for i in range (32): 
                        cfg_d[f"daq1_asics{j}_chs{i}_mask"]       = self.config['daq_1']['asic_' + str(j+1)]['ch_' + str(i)]['mask']
                        cfg_d[f"daq1_asics{j}_chs{i}_testhg"]    = self.config['daq_1']['asic_' + str(j+1)]['ch_' + str(i)]['test_hg']
                        cfg_d[f"daq1_asics{j}_chs{i}_testlg"]    = self.config['daq_1']['asic_' + str(j+1)]['ch_' + str(i)]['test_lg']
                        cfg_d[f"daq1_asics{j}_chs{i}_gainhg"]    = self.config['daq_1']['asic_' + str(j+1)]['ch_' + str(i)]['gain_hg']
                        cfg_d[f"daq1_asics{j}_chs{i}_gainlg"]    = self.config['daq_1']['asic_' + str(j+1)]['ch_' + str(i)]['gain_lg'] 
                        cfg_d[f"daq1_asics{j}_chs{i}_inputDAC"]   = self.config['daq_1']['asic_' + str(j+1)]['ch_' + str(i)]['inputDAC']
                        cfg_d[f"daq1_asics{j}_chs{i}_DACtime"]    = self.config['daq_1']['asic_' + str(j+1)]['ch_' + str(i)]['DACtime']    
       
                for i in range(4):
                    cfg_d[f"daq2_asics{i}_fastshsource"] = self.config['daq_2']['asic_' + str(i+1)]['general']['fastsh_source']
                    cfg_d[f"daq2_asics{i}_HGshtime"] = self.config['daq_2']['asic_' + str(i+1)]['general']['HGshtime']
                    cfg_d[f"daq2_asics{i}_LGshtime"] = self.config['daq_2']['asic_' + str(i+1)]['general']['LGshtime']
                    cfg_d[f"daq2_asics{i}_timethrs"] = self.config['daq_2']['asic_' + str(i+1)]['general']['timethrs']
                    cfg_d[f"daq2_asics{i}_chargeth"] = self.config['daq_2']['asic_' + str(i+1)]['general']['chargeth']
                    cfg_d[f"daq2_asics{i}_inputDACref"] = self.config['daq_2']['asic_' + str(i+1)]['general']['input_DACref']

                for j in range(4):
                    for i in range (32):    
                        cfg_d[f"daq2_asics{j}_chs{i}_mask"]       = self.config['daq_2']['asic_' + str(j+1)]['ch_' + str(i)]['mask']
                        cfg_d[f"daq2_asics{j}_chs{i}_testhg"]    = self.config['daq_2']['asic_' + str(j+1)]['ch_' + str(i)]['test_hg']
                        cfg_d[f"daq2_asics{j}_chs{i}_testlg"]    = self.config['daq_2']['asic_' + str(j+1)]['ch_' + str(i)]['test_lg']
                        cfg_d[f"daq2_asics{j}_chs{i}_gainhg"]    = self.config['daq_2']['asic_' + str(j+1)]['ch_' + str(i)]['gain_hg']
                        cfg_d[f"daq2_asics{j}_chs{i}_gainlg"]    = self.config['daq_2']['asic_' + str(j+1)]['ch_' + str(i)]['gain_lg']
                        cfg_d[f"daq2_asics{j}_chs{i}_inputDAC"]   = self.config['daq_2']['asic_' + str(j+1)]['ch_' + str(i)]['inputDAC']
                        cfg_d[f"daq2_asics{j}_chs{i}_DACtime"]    = self.config['daq_2']['asic_' + str(j+1)]['ch_' + str(i)]['DACtime']  

        else:
            self.json = False
            print('[ZIRE-APP]: Something went wrong with cfg, please add -first when launch application')

    def load_settings(self, json_path, first: bool):

        #Loading JSON#
        #Se è la prima volta che viene configurata allora verranno settati tutti i parametri
        #Altrimenti solo quelli che sono cambiati rispetto alla cfg precedente
        if first:
            self.load_json(json_path, self.cfg)
            shutil.copy2(json_path, "./.{}_prev_cfg.json".format(self.cfg["ipaddress"]))

        self.first = first

        if self.json:
            print ('[ZIRE-APP]: Loading configuration')
            #Printing general info
            print(self.cfg["identifier"])

            #Checking configuration changes
            for name, value in self.cfg.items():
                if not first:
                    if self.cfg[name] != self.o_cfg[name]:
                        self.settings[name] = value
                else:
                    self.settings[name] = value
            

            print ('[ZIRE-APP]: Configuration loaded')
            return self.settings, True
        else:
            return self.settings, False
        
    def send_configuration(self, DAQ: ZIRE, params: dict):
        self.changed_1 = False
        self.changed_2 = False
        ret=0
        print ('[ZIRE-APP]: Sending configuration..')
        if self.first :
            ret += DAQ.set_parameter("CMD.glbreset", 0)

        for name, value in params.items():
            if name == "conc_trg_mode":
                ret += DAQ.set_parameter("CMD.conctrig", value)
            elif name == "conc_trg_logic":
                ret += DAQ.set_parameter("CMD.trglogic", value)
            elif name == "concentrator_periodic":
                ret += DAQ.set_parameter("CMD.conctper", value)
            elif name == "ctrig_edit_counts":
                ret += DAQ.set_parameter("CMD.teditper", value)
            elif name == "daq1_trg_en":
                ret += DAQ.set_parameter("CMD.d1trigen", value)
            elif name == "daq2_trg_en":
                ret += DAQ.set_parameter("CMD.d2trigen", value)
            elif name == "mode":
                if value == "slave":
                    ret += DAQ.set_parameter("CMD.slavecon", 0)
                elif value == "master":
                    ret += DAQ.set_parameter("CMD.mastconc", 0)

            elif name == "daq1":
                if value == "pst":
                    ret += DAQ.set_parameter("BOARD.1/CMD.daqispst", 0)
                elif value == "ftk":
                    ret += DAQ.set_parameter("BOARD.1/CMD.daqisftk", 0)

            elif name == "daq1_trg_mode":
                ret += DAQ.set_parameter("BOARD.1/CMD.trigmode", int(value, 2))
            
            elif name == "daq1_tcharge_mask":
                ret += DAQ.set_parameter("BOARD.1/CMD.tcrgmask", int(value, 2))

            elif name == "daq1_trg_src":
                if value == 0:
                    ret += DAQ.set_parameter("BOARD.1/CMD.triggint", 0)
                elif value == 1:
                    ret += DAQ.set_parameter("BOARD.1/CMD.triggext", 0)
                elif value == 2:
                    ret += DAQ.set_parameter("BOARD.1/CMD.triggper",  params["daq1_trg_period"])

            elif name == "daq2":
                if value == "pst":
                    ret += DAQ.set_parameter("BOARD.2/CMD.daqispst", 0)
                elif value == "ftk":
                    ret += DAQ.set_parameter("BOARD.2/CMD.daqisftk", 0)

            elif name == "daq2_trg_mode":
                ret += DAQ.set_parameter("BOARD.2/CMD.trigmode", int(value, 2))

            elif name == "daq2_tcharge_mask":
                ret += DAQ.set_parameter("BOARD.2/CMD.tcrgmask", int(value, 2))
                
            elif name == "daq2_trg_src":
                if value == 0:
                    ret += DAQ.set_parameter("BOARD.2/CMD.triggint", 0)
                elif value == 1:
                    ret += DAQ.set_parameter("BOARD.2/CMD.triggext", 0)
                elif value == 2:
                    ret += DAQ.set_parameter("BOARD.2/CMD.triggper",  params["daq2_trg_period"])

            elif name == "validation":
                if value == 0:
                    ret += DAQ.set_parameter("BOARD.1/CMD.valisoff", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.valisoff", 0)
                elif value == 1:
                    ret += DAQ.set_parameter("BOARD.1/CMD.valdison", 0)
                    ret += DAQ.set_parameter("BOARD.1/CMD.vldtiout", params["timeout_valid"])
                    ret += DAQ.set_parameter("BOARD.2/CMD.valdison", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.vldtiout", params["timeout_valid"])

            elif name == "validation_src":
                    if value == 0:
                        ret += DAQ.set_parameter("BOARD.1/CMD.validint", 0)
                        ret += DAQ.set_parameter("BOARD.2/CMD.validint", 0)
                    elif value == 1:
                        ret += DAQ.set_parameter("BOARD.1/CMD.validext", 0)
                        ret += DAQ.set_parameter("BOARD.2/CMD.validext", 0) 

            elif name == "discard":
                if value == 0:
                    ret += DAQ.set_parameter("BOARD.1/CMD.dscrdoff", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.dscrdoff", 0)
                elif value == 1:
                    ret += DAQ.set_parameter("BOARD.1/CMD.dscardon", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.dscardon", 0)
            
            elif name == "fake_gen":
                if value == 0:
                    ret += DAQ.set_parameter("BOARD.1/CMD.fkeisoff", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.fkeisoff", 0)
                elif value == 1:
                    ret += DAQ.set_parameter("BOARD.1/CMD.fakeison", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.fakeison", 0)

            elif name == "trigpsc":
                if value == True:
                    ret += DAQ.set_parameter("BOARD.1/CMD.ipsctrig", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.ipsctrig", 0)
                elif value == False:
                    ret += DAQ.set_parameter("BOARD.1/CMD.opsctrig", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.opsctrig", 0)
                    
            elif name == "PSCbypass":
                if value == True:
                    ret += DAQ.set_parameter("BOARD.1/CMD.onbypass", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.onbypass", 0)
                elif value == False:
                    ret += DAQ.set_parameter("BOARD.1/CMD.ofbypass", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.ofbypass", 0)

            elif name == "rstb_en":
                if value == True:
                    ret += DAQ.set_parameter("BOARD.1/CMD.rstbenab", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.rstbenab", 0)
                elif value == False:
                    ret += DAQ.set_parameter("BOARD.1/CMD.rstbdisb", 0)
                    ret += DAQ.set_parameter("BOARD.2/CMD.rstbdisb", 0)
                    
            elif name == "HGpdorth":
                if value == 0:
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.A/CMD.hgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.B/CMD.hgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.C/CMD.hgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.D/CMD.hgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.A/CMD.hgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.B/CMD.hgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.C/CMD.hgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.D/CMD.hgscapdt", 0)
                elif value == 1:
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.A/CMD.hgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.B/CMD.hgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.C/CMD.hgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.D/CMD.hgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.A/CMD.hgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.B/CMD.hgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.C/CMD.hgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.D/CMD.hgscapdt", 1)
            
            elif name == "LGpdorth":
                if value == 0:
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.A/CMD.lgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.B/CMD.lgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.C/CMD.lgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.D/CMD.lgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.A/CMD.lgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.B/CMD.lgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.C/CMD.lgscapdt", 0)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.D/CMD.lgscapdt", 0)
                elif value == 1:
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.A/CMD.lgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.B/CMD.lgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.C/CMD.lgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.1/CITIROC.D/CMD.lgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.A/CMD.lgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.B/CMD.lgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.C/CMD.lgscapdt", 1)
                    ret += DAQ.set_parameter("BOARD.2/CITIROC.D/CMD.lgscapdt", 1)
                    
            elif name == "holdwin":
                ret += DAQ.set_parameter("CMD.holdwind", value)
            
            if "daq1_asics" in name:
                id_asic = int(name.split("_")[1][5:])
                
                if "chs" in name:
                    id_ch = str(int(name.split("_")[2][3:])).zfill(2)
                    param = name.split("_")[3]
                else:
                    param = name.split("_")[2]

                if param == "fastshsource":
                    if value == "hg":
                        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.HGfshsrc", 0)
                    elif value == "lg":
                        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.LGfshsrc", 0)

                elif param == "HGshtime":
                    ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.HGshtime", value)

                elif param == "LGshtime":
                    ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.LGshtime", value)

                elif param == "timethrs":
                    ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.timethrs", value)

                elif param == "chargeth":
                    ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.chargeth", value)

                elif param == "inputDACref":
                    ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.indacref", value)

                elif param == "mask":
                    if value == True:
                        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.maskch" + id_ch, 0)
                        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.trmkch" + id_ch, 0)
                    elif value == False:
                        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.umskch" + id_ch, 0)
                        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.trumch" + id_ch, 0)

                elif param == "testhg":
                    if value == True:
                        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.hgtest" + id_ch, 0)
                    elif value == False:
                        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.hgutst" + id_ch, 0)

                elif param == "testlg": 
                    if value == True:
                        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.lgtest" + id_ch, 0)
                    elif value == False:
                        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.lgutst" + id_ch, 0)

                elif param == "gainhg": 
                    ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.hggain" + id_ch, value)

                elif param == "gainlg": 
                    ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.lggain" + id_ch, value)

                elif param == "inputDAC": 
                    ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.inputd" + id_ch, value)

                elif param == "DACtime": 
                    ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(id_asic) + "/CMD.timeco" + id_ch, value)

            elif "daq2_asics" in name:
                id_asic = int(name.split("_")[1][5:])

                if "chs" in name:
                    id_ch = str(int(name.split("_")[2][3:])).zfill(2)
                    param = name.split("_")[3]
                else:
                    param = name.split("_")[2]

                if param == "fastshsource":
                    if value == "hg":
                        ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.HGfshsrc", 0)
                    elif value == "lg":
                        ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.LGfshsrc", 0)

                elif param == "HGshtime":
                    ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.HGshtime", value)

                elif param == "LGshtime":
                    ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.LGshtime", value)

                elif param == "timethrs":
                    ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.timethrs", value)

                elif param == "chargeth":
                    ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.chargeth", value)

                elif param == "inputDACref":
                    ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.indacref", value)

                elif param == "mask":
                    if value == True:
                        ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.maskch" + id_ch, 0)
                        ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.trmkch" + id_ch, 0)
                    elif value == False:
                        ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.umskch" + id_ch, 0)
                        ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.trumch" + id_ch, 0)

                elif param == "testhg":
                    if value == True:
                        ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.hgtest" + id_ch, 0)
                    elif value == False:
                        ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.hgutst" + id_ch, 0)

                elif param == "testlg": 
                    if value == True:
                        ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.lgtest" + id_ch, 0)
                    elif value == False:
                        ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.lgutst" + id_ch, 0)

                elif param == "gainhg": 
                    ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.hggain" + id_ch, value)

                elif param == "gainlg": 
                    ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.lggain" + id_ch, value)

                elif param == "inputDAC": 
                    ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.inputd" + id_ch, value)

                elif param == "DACtime": 
                    ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(id_asic) + "/CMD.timeco" + id_ch, value)

        ret += DAQ.set_parameter("BOARD.1/CITIROC.A/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.1/CITIROC.B/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.1/CITIROC.C/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.1/CITIROC.D/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.1/CMD.progdfbs", 0)

        ret += DAQ.set_parameter("BOARD.2/CITIROC.A/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.2/CITIROC.B/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.2/CITIROC.C/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.2/CITIROC.D/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.2/CMD.progdfbs", 0)

        ret += DAQ.set_parameter("CMD.setdeflt", 0)

        if ret == 0:
            print("Configuration correctly set!")
        else:
            print("Something went wrong during sending configuration!", ret)


    def all_tlatch_off(self, DAQ: ZIRE):
        ret = 0
        for j in range(4):
            ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(j) + "/CMD.latchoff", 0)
            ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(j) + "/CMD.latchoff", 0)

        if ret == 0:
            print("Trigger latch off correctly set!")
        else:
            print("Something went wrong during sending configuration!")


    def all_tlatch_on(self, DAQ: ZIRE):
        ret = 0
        for j in range(4):
            ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(j) + "/CMD.latchton", 0)
            ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(j) + "/CMD.latchton", 0)
            ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(j) + "/CMD.writebts", 0)
            ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(j) + "/CMD.writebts", 0)
        if ret == 0:
            ret += DAQ.set_parameter("BOARD.1/CMD.progdfbs", 0)
            ret += DAQ.set_parameter("BOARD.2/CMD.progdfbs", 0)
            time.sleep(1)
            print("Trigger latch on correctly set!")
        else:
            print("Something went wrong during sending configuration!")


    def stairs_setdac(self, DAQ: ZIRE, value):
        ret = 0
        for j in range(4):
            for i in range (32): 
                ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(j) + "/CMD.timeco" + str(i).zfill(2), value)               
                ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(j) + "/CMD.timeco" + str(i).zfill(2), value)

            ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(j) + "/CMD.writebts", 0)
            ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(j) + "/CMD.writebts", 0)

        if ret == 0:
            ret += DAQ.set_parameter("BOARD.1/CMD.progdfbs", 0)
            ret += DAQ.set_parameter("BOARD.2/CMD.progdfbs", 0)
            time.sleep(1)
            print("DAC THRESHOLD correctly set!")
        else:
            print("Something went wrong during sending configuration!")


    def stairs_setthres(self, DAQ: ZIRE, value):
        ret = 0
        for j in range(4):
            ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(j) + "/CMD.timethrs", value)
            ret += DAQ.set_parameter("BOARD.2/CITIROC." + self.corr.get(j) + "/CMD.timethrs", value)


        if ret == 0:
            print("Threshold correctly set!")
        else:
            print("Something went wrong during sending configuration!", ret)

    def set_monitor(self, DAQ: ZIRE, type, board: str, asic: int, chn: str, test: str):
        ret=0
        ch = str(chn).zfill(2)
        
        if type == "reset":
            self.reset_monitor(DAQ)

        elif type == "out_fs":
            if test == "on":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.on_fs_" + ch, 0)
            elif test == "off":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.off_fs" + ch, 0)
        
        elif type == "ssh_lg":
            if test == "on":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.isshlg" + ch, 0)
            elif test == "off":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.osshlg" + ch, 0)
                
        
        elif type == "ssh_hg":
            if test == "on":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.isshhg" + ch, 0)
            elif test == "off":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.osshhg" + ch, 0)
                
        
        elif type == "ps_lg":
            if test == "on":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.onpslg" + ch, 0)
            elif test == "off":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.ofpslg" + ch, 0)
                
        
        elif type == "ps_hg":
            if test == "on":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.onpshg" + ch, 0)
            elif test == "off":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.ofpshg" + ch, 0)
                
        
        elif type == "pa_lg":
            if test == "on":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.onpalg" + ch, 0)
            elif test == "off":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.ofpalg" + ch, 0)
                
        
        elif type == "pa_hg":
            if test == "on":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.onpahg" + ch, 0)
            elif test == "off":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.ofpahg" + ch, 0)
                
        
        elif type == "dac_in":
            if test == "on":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.idacin" + ch, 0)
            elif test == "off":
                ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.odacin" + ch, 0)

        ret += DAQ.set_parameter("BOARD." + str(board) + "/CITIROC." + self.corr.get(asic) + "/CMD.setmoncf", 0)

        return ret

    def reset_monitor(self, DAQ: ZIRE):
        ret = 0
        ret += DAQ.set_parameter("BOARD.1/CMD.resetmon", 0)
        ret += DAQ.set_parameter("BOARD.2/CMD.resetmon", 0)
        if ret == 0:
            print("Monitor settings reset")
        else:
            print("Something went wrong during monitor reset procedure")

    def reset_timestamp(self, DAQ: ZIRE):
        ret = 0
        ret += DAQ.set_parameter("CMD.tmsreset", 0)
        if ret == 0:
            print("Timestamp reset armed")
        else:
            print("Something went wrong during reset timestamp")

    def set_hg_gain(self, DAQ: ZIRE, asic, ch, value):
        ret = 0
        
        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(asic) + "/CMD.hggain" + ch, value)
        ret += DAQ.set_parameter("BOARD.1/CITIROC." + self.corr.get(asic) + "/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.1/CMD.progdfbs", 0)
        if ret == 0:
            print("Ctest Set")

    def down_calo_6(self, DAQ: ZIRE):
        ret = 0
        
        for ch in (2, 5, 8, 11, 14, 17, 20, 23):
            ret += DAQ.set_parameter("BOARD.1/CITIROC.C/CMD.chpaof" + ch, 0)

        ret += DAQ.set_parameter("BOARD.1/CITIROC.C/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.1/CMD.progdfbs", 0)
        if ret == 0:
            print("Calo 6x6 PA powered down!")

    def up_calo_6(self, DAQ: ZIRE):
        ret = 0
        
        for ch in (2, 5, 8, 11, 14, 17, 20, 23):
            ret += DAQ.set_parameter("BOARD.1/CITIROC.C/CMD.chpaon" + ch, 0)

        ret += DAQ.set_parameter("BOARD.1/CITIROC.C/CMD.writebts", 0)
        ret += DAQ.set_parameter("BOARD.1/CMD.progdfbs", 0)
        if ret == 0:
            print("Calo 6x6 PA powered down!")

#if __name__ == "__main__":
#    ZireDAQ = ZIRE()
#    ZireCFG = CONFIGURATOR()
#    ZireDAQ.connect("192.168.102.16")
#    settings, valid = ZireCFG.load_settings("C:/Users/lferr/Desktop/ZIRE/GSSI/LINUXAPP/cfg_sample.json", True)
#    ZireCFG.send_configuration(ZireDAQ, settings)
