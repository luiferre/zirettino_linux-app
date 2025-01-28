#pragma once
#pragma once
#ifndef HEADER_H_DATAHANDLER
#define HEADER_H_DATAHANDLER

#define _CRT_SECURE_NO_WARNINGS
#include "NIErrorCode.h"
#include "databuffers.h"
#include "ZIRE_HAL.h"
#include "globals.h"
#include <string>
#include <mutex>
#include <functional>
#include <chrono>
#include <thread>
#include <algorithm>
#include <thread>
#include <ctime>
#include <boost/lockfree/spsc_queue.hpp>
#include <sys/stat.h>
#include <dirent.h>
#include <time.h>

#ifdef __linux__ 
#include <unistd.h>
#elif _WIN32
#include <windows.h>
#else

#endif

#define MAX_VALUE 16384
using namespace std;

class ZIRE_DATAHANDLER {

public:
	ZIRE_DATAHANDLER(ZIRE_HAL *hal) {
		_hal = hal;
	}

	~ZIRE_DATAHANDLER();

	//Start Data Stream
	NI_RESULT StartAcq(t_board *_buff, string path, bool save);

	//Stop Data Stream
	NI_RESULT StopAcq(t_board *buff);

	//RAW data download
	void Data_download();
    void Data_download(string path, bool _time, uint32_t target, string role);
  	void Data_decode(t_board *buff);
	NI_RESULT Stairs(string path, uint32_t target);
	
	//Data Request
	NI_RESULT Data_Request_Start();
	NI_RESULT Data_Request_End();

private:

	ZIRE_HAL	*_hal;			//puntatore hal

	std::thread producer_thread;
	std::thread download_thread;
	bool		datastream = false;
	bool		IsRunning = false;
	bool		data_vd = false;
	bool		start = true;
	bool		last_word = false;
	bool		data_new = false;
	mutex		data_mutex;
	mutex		producer_mutex;
	uint32_t rw = 0, triggers = 0;
	uint64_t *data_buffer = (uint64_t*)malloc(sizeof(uint64_t) * (200));
	uint32_t *sync = (uint32_t*)malloc(sizeof(uint32_t));
	uint32_t open_w = 0xCAFECAFE, close_w = 0xBEEFBEEF;
	boost::lockfree::spsc_queue<uint32_t, boost::lockfree::capacity<4096>> queue;
	uint32_t dataqueue[4096];

	//Data from packet
	uint64_t timestamp = 0;
	uint32_t trig_id = 0;
	uint32_t trig_cnt = 0;
	uint32_t valid = 0;
	uint32_t flags = 0;
	uint32_t lost_packets = 0;

	uint32_t pck_from_server = 0;
	uint32_t pck_from_queue = 0;

	FILE* file;
	FILE* housek;
	FILE* stairs;

	//Decode data
	int bin_hg, bin_lg, bin_num, bin_size;
};

#endif
