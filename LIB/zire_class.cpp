#include "zire_class.h"

ZireSDK::ZireSDK() {
	hal = new ZIRE_HAL();
	data_handler = new ZIRE_DATAHANDLER(hal);
}

ZireSDK::~ZireSDK() {
}

std::vector<std::string> ZireSDK::ZSplitPath(string path, char separator) {

	std::stringstream test(path);
	std::string segment;
	std::vector<std::string> seglist;

	while (std::getline(test, segment, separator))
	{
		seglist.push_back(segment);
	}
	return seglist;

}

NI_RESULT ZireSDK::ExtractParamSubPaths(string path, string *board, string *asic, string *cmd) {

	std::vector<std::string> qPP = ZSplitPath(path, '/');
	std::vector<std::string> qPS = ZSplitPath(qPP[0], '.');

	//Esempio comando "BOARD.1/CITIROC.A/CMD.
	if (qPS[0] == "BOARD") {
		*board = qPS[1];				//Board id (1, .., 4)

		qPS = ZSplitPath(qPP[1], '.');
		if (qPS[0] == "CITIROC") {
			*asic = qPS[1];				//Citiroc id (A, B, C, D)
			qPS = ZSplitPath(qPP[2], '.');
			*cmd = qPS[1];				//cmd
		}
		else if (qPS[0] == "CMD") {
			*asic = "";
			*cmd = qPS[1];
		}
	}
	else if (qPS[0] == "CMD") {
		*board = "";
		*asic = "";
		*cmd = qPS[1];
	}
	else {
		return NI_NOT_FOUND;
	}
	return NI_OK;
}

NI_RESULT ZireSDK::Connect(string url, DAQ_DEVICE *buffer) {
	uint32_t rw;
	NI_RESULT ret;

	if (hal->Connect(url, false) == NI_OK) {		
		char *daq_buffer = (char*)malloc(20);
		ret = hal->WriteData("boardinf", 7, COMM_TIMEOUT, &rw);
		ret = hal->ReadCharData(daq_buffer, 20, 0x8, COMM_TIMEOUT);

		memcpy(&buffer->PID, &daq_buffer[0], 4);
		memcpy(&buffer->MODEL, &daq_buffer[4], 4);
		memcpy(&buffer->FW_ver, &daq_buffer[8], 4);
		memcpy(&buffer->SW_ver, &daq_buffer[12], 4);
		memcpy(&buffer->Staus, &daq_buffer[16], 4);

		return NI_OK;
	}
	else {
		return NI_ERROR_NOTCONNECTED;
	}
}

NI_RESULT ZireSDK::Disconnect() {
	uint32_t rw;
	hal->WriteData("closesoc", 7, COMM_TIMEOUT, &rw);
	return hal->CloseConnection();
}

NI_RESULT ZireSDK::SetParameter(string Path, uint32_t value) {
	string board, asic, cmd;
	uint32_t rw;
	int idx = 0;

	ExtractParamSubPaths(Path, &board, &asic, &cmd);

	/* DEGUB COMANDI*/
	/*
	char* char_ptr = const_cast<char*>(Path.c_str());
    FILE *file = fopen("output.txt", "a");
    if (file == NULL) {
        printf("Errore nell'apertura del file.\n");
        return 1;
    }
    fprintf(file, "%s, %d\n", Path.c_str(), value);
    fclose(file);
	*/
	
	if (board == "1") {
		hal->WriteData("cfgb0001", 7, COMM_TIMEOUT, &rw);
	}
	else if (board == "2") {
		hal->WriteData("cfgb0002", 7, COMM_TIMEOUT, &rw);
	}
	else if (board == "3") {
		hal->WriteData("cfgb0003", 7, COMM_TIMEOUT, &rw);
	}
	else if (board == "4") {
		hal->WriteData("cfgb0004", 7, COMM_TIMEOUT, &rw);
	}

	if (asic == "A") {
		hal->WriteData("cfgasica", 7, COMM_TIMEOUT, &rw);
	}
	else if (asic == "B") {
		hal->WriteData("cfgasicb", 7, COMM_TIMEOUT, &rw);
	}
	else if (asic == "C") {
		hal->WriteData("cfgasicc", 7, COMM_TIMEOUT, &rw);
	}
	else if (asic == "D") {
		hal->WriteData("cfgasicd", 7, COMM_TIMEOUT, &rw);
	}
	if (cmd == "conctrig") {
		hal->WriteData("conctrig", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "trglogic") {
		hal->WriteData("trglogic", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "conctper") {
		hal->WriteData("conctper", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "triggper") {
		hal->WriteData("triggper", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
    else if (cmd == "teditper") {
		hal->WriteData("teditper", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
    else if (cmd == "holdwind") {
		hal->WriteData("holdwind", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
    else if (cmd == "lgscapdt") {
		hal->WriteData("lgscapdt", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
    else if (cmd == "hgscapdt") {
		hal->WriteData("hgscapdt", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "d1trigen") {
		hal->WriteData("d1trigen", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "d2trigen") {
		hal->WriteData("d2trigen", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "trigmode") {
		hal->WriteData("trigmode", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
    else if (cmd == "tcrgmask") {
		hal->WriteData("tcrgmask", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "vldtiout") {
		hal->WriteData("vldtiout", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "writespi") {
		hal->WriteData("writespi", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "HGshtime") {
		hal->WriteData("HGshtime", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "LGshtime") {
		hal->WriteData("LGshtime", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "timethrs") {
		hal->WriteData("timethrs", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "chargeth") {
		hal->WriteData("chargeth", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd == "indacref") {
		hal->WriteData("indacref", 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd.substr(0, 6) == "timeco") {
		hal->WriteData((char*)cmd.c_str(), 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd.substr(0, 6) == "charco") {
		hal->WriteData((char*)cmd.c_str(), 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd.substr(0, 6) == "hggain") {
		hal->WriteData((char*)cmd.c_str(), 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd.substr(0, 6) == "lggain") {
		hal->WriteData((char*)cmd.c_str(), 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd.substr(0, 6) == "inputd") {
		hal->WriteData((char*)cmd.c_str(), 7, COMM_TIMEOUT, &rw);
		return hal->WriteINTData(value, 7, COMM_TIMEOUT, &rw);
	}
	else if (cmd != "") {
		return hal->WriteData((char*)cmd.c_str(), 7, COMM_TIMEOUT, &rw);
	}
	else {
		return NI_NOT_FOUND;
	}


	return NI_OK;
}

NI_RESULT ZireSDK::GetParameter(string Path, uint32_t *value) {
	string board, asic, cmd;
	int idx = 0;
	ExtractParamSubPaths(Path, &board, &asic, &cmd);

	if (cmd == "readrspi") {
		hal->ReadData(value, 7, 0x8, COMM_TIMEOUT);
	}

	else {
		return NI_NOT_FOUND;
	}
	return NI_OK;
}

NI_RESULT ZireSDK::ExecuteCommand(string Path, uint32_t value) {
	string board, asic, cmd;
	uint32_t rw;
	int idx = 0;
	ExtractParamSubPaths(Path, &board, &asic, &cmd);

	if (cmd == "datadownload") {
		
	}
	else {
		return NI_NOT_FOUND;
	}
	return NI_OK;
}

NI_RESULT ZireSDK::AllocateHistogram(void *buffer, uint32_t bins) {
	
	t_board *board = (t_board*)buffer;
	board->allocated_size = bins;
	board->nbin = bins;
	board->validated = 0;
	board->numof_asic = 4;
	board->numof_ch = 32;
	board->lost = 0;
	board->totalsize = 0;
	board->asic = (t_asic*)malloc(sizeof(t_asic[4]));

	if (board->asic == NULL) {
		return NI_ALLOC_FAILED;
	}
	for (int i = 0; i < board->numof_asic; i++) {
		board->asic[i].ch = (t_asic_channel*)malloc(sizeof(t_asic_channel)*32);
		board->asic[i].id = i;
		
		if (board->asic[i].ch == NULL) {
			return NI_ALLOC_FAILED;
		}

		for (int j = 0; j < board->numof_ch; j++) {
			board->asic[i].ch[j].LG = (t_histo_elem*)malloc(sizeof(t_histo_elem)*bins);
			if (board->asic[i].ch[j].LG == NULL) {
				return NI_ALLOC_FAILED;
			}

			board->asic[i].ch[j].HG = (t_histo_elem*)malloc(sizeof(t_histo_elem)*bins);
			if (board->asic[i].ch[j].HG == NULL) {
				return NI_ALLOC_FAILED;
			}

			board->asic[i].ch[j].id = i;

			for (int k = 0; k < bins; k++) {
				board->asic[i].ch[j].LG[k].bin = k;
				board->asic[i].ch[j].LG[k].occupancy = 0;
				board->asic[i].ch[j].HG[k].bin = k;
				board->asic[i].ch[j].HG[k].occupancy = 0;
			}
		}
	}
	return NI_OK;
}

NI_RESULT ZireSDK::StartAcq(t_board *buffer, string path, bool save) {
	data_handler->StartAcq(buffer, path, save);
	return NI_OK;
}

NI_RESULT ZireSDK::StartAcqRaw(string path, bool _time, uint32_t target, string role) {
	data_handler->Data_download(path, _time, target, role);
	return NI_OK;
}

NI_RESULT ZireSDK::StartStairs(string path, uint32_t target) {
	return data_handler->Stairs(path, target);
}

NI_RESULT ZireSDK::Data_Request_Start() {
	data_handler->Data_Request_Start();
	return NI_OK;
}

NI_RESULT ZireSDK::Data_Request_End() {
	data_handler->Data_Request_End();
	return NI_OK;
}

NI_RESULT ZireSDK::StopAcq(t_board *buffer) {
	data_handler->StopAcq(buffer);
	return NI_OK;
}

