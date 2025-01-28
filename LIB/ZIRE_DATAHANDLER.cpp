#include "ZIRE_DATAHANDLER.h"

ZIRE_DATAHANDLER::~ZIRE_DATAHANDLER() {

}

NI_RESULT ZIRE_DATAHANDLER::StartAcq(t_board *_buff, string path, bool save) {
	for (int i = 0; i < _buff->numof_asic; i++) {
		for (int j = 0; j < _buff->numof_ch; j++) {
			for (int k = 0; k < _buff->nbin; k++) {
				_buff->asic[i].ch[j].LG[k].bin = k;
				_buff->asic[i].ch[j].LG[k].occupancy = 0;
				_buff->asic[i].ch[j].HG[k].bin = k;
				_buff->asic[i].ch[j].HG[k].occupancy = 0;
			}
		}
	}

	if (save) {
		int result = mkdir(path.c_str(), 0777);
		if (result == 0) {
			file = fopen((path + "\\data.bin").c_str(), "wb");
		}
	}
	// Crea una lambda function che chiama la funzione Data_download
	// e passa il parametro buff a quella funzione.
	auto download_func = [this](t_board *buff) {
		if (buff->asic == NULL) {
			return NI_ALLOC_FAILED;
		}
		Data_decode(buff);
	};

	auto download_prod = [this]() {		
		Data_download();
	};

	// Crea un thread e passa la lambda function come argomento.
	// Nota che non stai passando il parametro buff qui.
	// Stai passando solo la lambda function che user� il parametro buff.
	
	datastream = true;
	start = true;
	data_new = false;

	download_thread = std::thread(download_prod);
	download_thread.detach();

	producer_thread = std::thread(download_func, _buff);
	producer_thread.detach();

	return NI_OK;
}

void ZIRE_DATAHANDLER::Data_download() {
	NI_RESULT ret = 0;
	lost_packets = 0;
	pck_from_server = 0;

	while (!queue.empty()) {
		queue.pop();
	}

	_hal->WriteData("tdatareq", 7, COMM_TIMEOUT, &rw);

	if (data_buffer == NULL) { return; }

	while (true) {
		if (datastream) {
			ret = _hal->ReadStream(data_buffer, sizeof(uint64_t) * 68, 0x8, 1000);
			if (ret == 0) {
				pck_from_server += 1;
				/***************PACKS TO FILE***********/
            
				if (file) {
					fwrite(data_buffer, sizeof(uint64_t), 67, file);
				}

				/***************************************/
				/********** PROD THREAD ****************/
				/*L'oggetto da proteggere � la queue poich� ci sar� anche il consumer che vuole leggerla*/
				lost_packets = data_buffer[67];
				timestamp = (((data_buffer[0] & 0xFFFFFFFF) << 32) + (data_buffer[0] >> 32));
				trig_id = (data_buffer[1] & 0xFFFFFFFF);
				trig_cnt = (data_buffer[1] >> 32);
				valid = (data_buffer[2] & 0xFFFFFFFF);
				flags = (data_buffer[2] >> 32);

				producer_mutex.lock();
				/* Controllo se c'� spazio per un pacchetto intero 128ch+lost+ts+trgid+trgcnt+vld+flag+open_w+close_w=137*/
				if (queue.write_available() > 136) {
					queue.push(open_w);
					queue.push(timestamp & 0xFFFFFFFF);
					queue.push(timestamp >> 32);
					queue.push(trig_id);
					queue.push(trig_cnt);
					queue.push(valid);
					queue.push(flags);
					queue.push(lost_packets);
					for (int i = 3; i<67; i++) {
						queue.push(data_buffer[i] & 0xFFFFFFFF);
						queue.push(data_buffer[i] >> 32);
					}
					queue.push(close_w);
				}
				/********** PROD THREAD ****************/
				producer_mutex.unlock();
			}			
		}
		else {
			return;
		}
	}
}

void ZIRE_DATAHANDLER::Data_decode(t_board *buff) {
	t_data_elem tmp;

	if (buff == NULL) { return; }

	bin_size = 16;// ((MAX_VALUE / buff->nbin) == 0 ? 1 : MAX_VALUE / buff->nbin);
	bin_num = buff->nbin;
	buff->lost = 0;	
	triggers = 0;
	pck_from_queue = 0;

	for (int i = 0; i < 4096; i++) {
		dataqueue[i] = 0;
	}

	while (true) {
		if (datastream) {			
			IsRunning = true;
			
			/********** THREAD CONSUMER *************/
			/* Appena il mutex si sblocca il consumer legge piu eventi possibili dalla coda e li salva in un buffer*/
			producer_mutex.lock();
			int i = 0;
			if (!queue.empty()) { 
				data_new = true;
			}
			/* Leggo finch� la coda non si svuota*/
			while (!queue.empty()) {
				queue.pop(dataqueue[i]);
				i++;
			}
			producer_mutex.unlock();
			/********** THREAD CONSUMER *************/
			 
			/********** THREAD DEC0DER *************/
			
			if (data_new) {
				data_new = false;

				/* Il mutex protegge dataqueue che � un buffer che contiene i dati salvati dalla coda e il buffer della GUI*/
				data_mutex.lock();

				/* Bool per ultima parola del buffer*/
				last_word = false;

				/* Allineo il paccheto, cerco la parole che apre il pacchetto*/
				i = 0;
				while (dataqueue[i] != open_w) {
					i++;
					if (i == 4095) {
						last_word = true;
						break;
					}
				}
				dataqueue[i] = 0;

				i++; //Leggo timestamp (31-0)
				buff->timestamp = dataqueue[i] >> 32;

				i++; //Leggo timestamp (63-32)
				buff->timestamp = ((dataqueue[i] & 0xFFFFFFFF) << 32) + buff->timestamp;

				i++; //Leggo trig_id
				buff->trgid = dataqueue[i];

				i++; //Leggo trig_cnt
				buff->trgcnt = dataqueue[i];

				i++; //Leggo valid
				buff->validated = dataqueue[i];

				i++; //Leggo flag
				buff->flag = dataqueue[i];

				i++; //Leggo lost_packets
				buff->lost = dataqueue[i];

				i++;

				int ch = 0, asic = 0;
				while (!last_word) {
					/* Leggo l'intero pacchetto */
					while (dataqueue[i] != close_w) {
						/*Decodifica parola*/

						tmp.hit = (dataqueue[i] >> 28 & 0x1);
						tmp.hg = ((dataqueue[i] >> 14) & 0x3FFF);
						tmp.lg = (dataqueue[i] & 0x3FFF);

						bin_hg = ((tmp.hg / bin_size) > bin_num ? bin_num : tmp.hg / bin_size);
						bin_lg = ((tmp.lg / bin_size) > bin_num ? bin_num : tmp.lg / bin_size);

						/*Popolo gli istogrammi*/
						buff->asic[asic].ch[ch].HG[bin_hg].occupancy += 1;
						buff->asic[asic].ch[ch].LG[bin_lg].occupancy += 1;

						/* Parola successiva */
						ch++;
						if (ch == 32) {
							ch = 0;
							asic++;
							if (asic == 4) {
								asic = 0;
							}
						}

						i++;
					}

					/*Dati aggiuntivi e conteggi*/
					triggers++;
					buff->totalsize = triggers;
					pck_from_queue += 1;

					/*Controllo che ci siano altri pacchetti */
					if (dataqueue[i + 1] == open_w) {
						dataqueue[i+1] = 0;
						buff->timestamp = ((dataqueue[i+3] & 0xFFFFFFFF) << 32) + dataqueue[i + 2];
						buff->trgid = dataqueue[i+4];
						buff->trgcnt = dataqueue[i+5];
						buff->validated = dataqueue[i+6];
						buff->flag = dataqueue[i+7];
						buff->lost = dataqueue[i+8];
						i += 9;
					}
					else last_word = true;
				}
				data_mutex.unlock();
			}/********** THREAD DEC0DER *************/
		}

		else {
			IsRunning = false;
			return;
		}		
	}
}

NI_RESULT ZIRE_DATAHANDLER::Data_Request_Start() {
	data_mutex.lock();
	return NI_OK;
}

NI_RESULT ZIRE_DATAHANDLER::Data_Request_End() {
	data_mutex.unlock();
	return NI_OK;
}

NI_RESULT ZIRE_DATAHANDLER::StopAcq(t_board *buff) {
	uint32_t rw;
	datastream = false;
	while (IsRunning) {}
	start = true;
	_hal->WriteData("tdataend", 7, COMM_TIMEOUT, &rw);
	free(buff);
	if (file) {
		fclose(file);
	}
	return NI_OK;
}

void ZIRE_DATAHANDLER::Data_download(string path, bool _time, uint32_t target, string role) {
	NI_RESULT ret = 0;
	time_t startTime;
	time_t startInfo;
    time_t currentTime;
	time_t infoTime;
    uint32_t packets = 0;
	bool first = false;

	uint32_t *stats = (uint32_t*)malloc(sizeof(uint32_t)*(128+128+16+16));

    _hal->WriteData("tdatareq", 7, COMM_TIMEOUT, &rw);

	if (data_buffer == NULL) { return; }

	ret = _hal->ReadSingle(sync, sizeof(uint32_t), 0x8, 100000);
    if (ret==0) std::cout << "[ZIRE-LIB]: Starting..." << endl;

	startTime = time(NULL);
	startInfo = time(NULL);    
	while (true) {
        ret = _hal->ReadStream(data_buffer, sizeof(uint64_t) * 138, 0x8, 1000);
        
		if (ret==0) {
			if (!first) {
				uint32_t attempts = 0;
				while (attempts < 10000) {
					file = fopen((path + "_data.bin").c_str(), "ab");
				
					if (file) {
						fwrite(data_buffer, sizeof(uint64_t), 138, file);
						fclose(file);
						break;
					}
					else {
						std::cout << "TEXT FILE BUSY" << endl;
						usleep(100);
						attempts++;
					}
				}
				currentTime = time(NULL);
				packets++;
			}
			first = false;
			//If bool time is true, target is time target else is packet target
			if (target != 0) {
				if (_time) {
					if (currentTime - startTime >= target) {
						break;
					}    
				}
				else {
					if (packets >= target) {
						break;
					} 
				}
			}
			infoTime = time(NULL);
			if (infoTime - startInfo >= 2) {
				std::cout << "\t[ZIRE-LIB]: Triggers " << role << ": " << packets << endl;
				
				_hal->WriteData("getstats", 7, COMM_TIMEOUT, &rw);
				ret = _hal->ReadData(stats, sizeof(uint32_t)*(128+128+16+16), 0x8, 100000);

				if (ret==0) {
					ZIRE_DATAHANDLER::housek = fopen((path + "_housekeeping.bin").c_str(), "ab");				
					if (housek) {
						fwrite(stats, sizeof(uint32_t), 128+128+16+16, housek);
						fclose(housek);
					}
				}

				startInfo = time(NULL);
			}  
		}
		//else std::cout << "No data available!" << endl;
		
	}
	_hal->WriteData("tdataend", 7, COMM_TIMEOUT, &rw);

	free(stats);
    std::cout << "[ZIRE-LIB]: Acquisition completed!" << endl;
}

NI_RESULT ZIRE_DATAHANDLER::Stairs(string path, uint32_t target) {
	NI_RESULT ret = 0;
	uint32_t packets = 0;
	time_t startInfo;
	time_t infoTime;

	uint32_t *stairs_buff = (uint32_t*)malloc(sizeof(uint32_t)*(128+128+16+16));

	startInfo = time(NULL);    
	while (true) {
		infoTime = time(NULL);
		if (infoTime - startInfo >= 2) {
			_hal->ClearSocket();
			_hal->WriteData("getstats", 7, COMM_TIMEOUT, &rw);
			ret = _hal->ReadData(stairs_buff, sizeof(uint32_t)*(128+128+16+16), 0x8, 100000);

			if (ret==0) {
				ZIRE_DATAHANDLER::stairs = fopen((path + "_stairs.bin").c_str(), "ab");				
				if (stairs) {
					fwrite(stairs_buff, sizeof(uint32_t), 128+128+16+16, stairs);
					fclose(stairs);
				}
				packets++;
			}

			if (packets >= target) {
				break;
			} 

			startInfo = time(NULL);
		} 		
	}
    std::cout << "Stairs step completed!" << endl;
	free(stairs_buff);
	return NI_OK;
}