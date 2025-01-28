#pragma once
#ifndef HEADER_H_ZIRE_HAL
#define HEADER_H_ZIRE_HAL

#include <iostream>
#include <fstream>
#include <vector>
#include "NIErrorCode.h"


using namespace std;

class ZIRE_HAL {

public:

	ZIRE_HAL();
	~ZIRE_HAL();

	NI_RESULT sockInit();

	NI_RESULT sockQuit();

	NI_RESULT Connect(string Path, bool istesting);

	NI_RESULT CloseConnection();

	NI_RESULT Enumerate(string board_model, vector<string> devices);

	NI_RESULT WriteData(char *value,
		uint32_t length,
		uint32_t timeout_ms,
		uint32_t *written_data);

	NI_RESULT WriteINTData(int value,
		uint32_t length,
		uint32_t timeout_ms,
		uint32_t *written_data);

	NI_RESULT WriteLONGData(unsigned long long value,
		uint32_t length,
		uint32_t timeout_ms,
		uint32_t *written_data);

	NI_RESULT ReadData(uint32_t *value, uint32_t length, uint32_t flag, uint32_t timeout_ms);
	NI_RESULT ReadSingle(uint32_t *value, uint32_t length, uint32_t flag, uint32_t timeout_ms);
	NI_RESULT ReadCharData(char *value, uint32_t length, uint32_t flag, uint32_t timeout_ms);
	NI_RESULT ReadStream(uint64_t *value, uint32_t length, uint32_t flag, uint32_t timeout_ms);
	NI_RESULT ReadFlowStream(uint64_t *value, uint32_t length, uint32_t flag, uint32_t timeout_ms, int *valid_data);
	NI_RESULT ClearSocket();
	
private:
	void *_handle;
	bool connected_ctrl;
	bool connected_stream;

	NI_RESULT ConnectSTREAM(string Path);
	NI_RESULT CloseSTREAM();
};

#endif
