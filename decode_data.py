import struct
import csv
import sys
import os
from tqdm import tqdm

def decode_data_buffer(data_buffer):
    temp_hg = []
    temp_lg = []

    timestamp = data_buffer[0]
    trigger_id = data_buffer[1]

    daq1_id = (data_buffer[2] & 0xFFFFFFFF)
    trigger1_counts = (data_buffer[2] >> 32)
    valid1 = (data_buffer[3] & 0xFFFFFFFF)
    flag1 = (data_buffer[3] >> 32)

    for i in range(4, 68):
        temp_hg.append(data_buffer[i] & 0x3FFF)
        temp_lg.append(data_buffer[i] >> 14 & 0x3FFF)
        temp_hg.append((data_buffer[i] >> 32) & 0x3FFF)
        temp_lg.append((data_buffer[i] >> 32) >> 14 & 0x3FFF)

    lost1 = data_buffer[68]
    validated1 = data_buffer[69]

    daq2_id = (data_buffer[70] & 0xFFFFFFFF)
    trigger2_counts = (data_buffer[70] >> 32)
    valid2 = (data_buffer[71] & 0xFFFFFFFF)
    flag2 = (data_buffer[71] >> 32)

    for i in range(72, 136):
        temp_hg.append(data_buffer[i] & 0x3FFF)
        temp_lg.append(data_buffer[i] >> 14 & 0x3FFF)
        temp_hg.append((data_buffer[i] >> 32) & 0x3FFF)
        temp_lg.append((data_buffer[i] >> 32) >> 14 & 0x3FFF)

    lost2 = data_buffer[136]
    validated2 = data_buffer[137]

    new_data = {'TIMESTAMP (100ns)': timestamp, 'TRIGGERID': trigger_id, 
                'DAQ ID 1': str(hex(daq1_id)), 'TRIGGER COUNTS 1': trigger1_counts, 'VALID 1': valid1, 'FLAG 1': flag1, 'ACK 1': validated1, 'LOST 1': lost1,
                'DAQ ID 2': str(hex(daq2_id)), 'TRIGGER COUNTS 2': trigger2_counts, 'VALID 2': valid2, 'FLAG 2': flag2, 'ACK 2': validated2, 'LOST 2': lost2}
                
    for x in range(4):
        for y in range(32):
            asic_ch_hg = f'DAQ1_Asic{x}_CH{y}_HG'
            asic_ch_lg = f'DAQ1_Asic{x}_CH{y}_LG'
            new_data[asic_ch_hg] = temp_hg[(x*32)+(y)]
            new_data[asic_ch_lg] = temp_lg [(x*32)+(y)]   
    
    for x in range(4):
        for y in range(32):
            asic_ch_hg = f'DAQ2_Asic{x}_CH{y}_HG'
            asic_ch_lg = f'DAQ2_Asic{x}_CH{y}_LG'
            new_data[asic_ch_hg] = temp_hg[(x*32)+(y)+128]
            new_data[asic_ch_lg] = temp_lg [(x*32)+(y)+128]  

    return new_data

def open_csv(file_path, fieldnames):
    if os.path.exists(file_path):
        os.remove(file_path)
        
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        
def write_data_csv(file_path, data):
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys(), delimiter=';')
        writer.writerow(data)

def open_data(path):
    fieldnames = ['TIMESTAMP (100ns)',  'TRIGGERID', 'DAQ ID 1', 'TRIGGER COUNTS 1', 'VALID 1', 'FLAG 1', 'ACK 1', 'LOST 1', 'DAQ ID 2', 'TRIGGER COUNTS 2', 'VALID 2', 'FLAG 2', 'ACK 2', 'LOST 2']
    for x in range(4):
        for y in range(32):
            fieldnames.append(f'DAQ1_Asic{x}_CH{y}_HG')
            fieldnames.append(f'DAQ1_Asic{x}_CH{y}_LG')
    for x in range(4):
        for y in range(32):
            fieldnames.append(f'DAQ2_Asic{x}_CH{y}_HG')
            fieldnames.append(f'DAQ2_Asic{x}_CH{y}_LG')

    open_csv(path + "_data.csv", fieldnames)

    with open(path + "_data.bin", "rb") as file:
        # Calcola il numero totale di pacchetti nel file binario
        total_packets = os.path.getsize(path + "_data.bin") // struct.calcsize("Q" * 138)
        
        # Utilizza tqdm per visualizzare la barra di avanzamento
        with tqdm(total=total_packets, unit="packets") as pbar:
            while True:
                packet_data = file.read(struct.calcsize("Q" * 138))
                if not packet_data:
                    break

                # Esegui la decodifica del pacchetto e scrivi sul CSV
                write_data_csv(path + "_data.csv", decode_data_buffer(struct.unpack("Q" * 138, packet_data)))
                
                # Aggiorna la barra di avanzamento
                pbar.update(1)
                
if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if path:
            print(f"Decoding: DATA...")
            open_data(path)
            print("End Decoding...")
        else:
            print("Missing decoding parameters!")
    else:
        print("No Valid measure detected")
