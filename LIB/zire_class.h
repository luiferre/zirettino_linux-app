#pragma once
#ifndef HEADER_H_ZIRECLASS
#define HEADER_H_ZIRECLASS

#include "NIErrorCode.h"
#include "databuffers.h"
#include "ZIRE_HAL.h"
#include "ZIRE_DATAHANDLER.h"
#include "globals.h"
#include <thread>
#include <vector>
#include <iostream>
#include <cstdlib>
#include <cstring>
#include <string.h>
#include <stdlib.h>
#include <sstream>
#include <fstream>
using namespace std;


class ZireSDK {

public:
	ZireSDK();
	~ZireSDK();

	std::vector<std::string> ZSplitPath(string path, char separator);

	NI_RESULT Connect(string url, DAQ_DEVICE *buffer);
	NI_RESULT Disconnect();

	NI_RESULT SetParameter(string Path, uint32_t value);
	NI_RESULT GetParameter(string Path, uint32_t *value);

	NI_RESULT ExecuteCommand(string Path, uint32_t value);
	NI_RESULT StartAcq(t_board *buffer, string path, bool save);
    NI_RESULT StartAcqRaw(string path, bool _time, uint32_t target, string role);
	NI_RESULT StartStairs(string path, uint32_t target);
	NI_RESULT StopAcq(t_board *buffer);

	NI_RESULT Data_Request_Start();
	NI_RESULT Data_Request_End();

	NI_RESULT AllocateHistogram(void *buffer, uint32_t bins);

	//NI_RESULT SetParameter(string Path, int32_t value);
	//NI_RESULT GetParameter(string Path, int32_t *value);

	//NI_RESULT SetParameter(string Path, uint64_t value);
	//NI_RESULT GetParameter(string Path, uint64_t *value);

	//NI_RESULT SetParameter(string Path, int64_t value);
	//NI_RESULT GetParameter(string Path, int64_t *value);

	//NI_RESULT SetParameter(string Path, double value);
	//NI_RESULT GetParameter(string Path, double *value);

	//NI_RESULT SetParameter(string Path, string value);
	//NI_RESULT GetParameter(string Path, string *value);

	//allocate a data buffer for readout
	//NI_RESULT AllocateBufferList(void *buffer, uint32_t size);
	//NI_RESULT AllocateHistogram(void *buffer, uint32_t bins);
	//NI_RESULT AllocateFreqInfo(void *buffer);
	//NI_RESULT AllocateCalib(void *buffer);

	//download a buffer
	//NI_RESULT GetListEvent(t_tdc_list *buffer);

	//download histrogram
	//NI_RESULT GetHistogram(uint32_t id, t_tdc_histo *buffer);

	//download ch freq info
	//NI_RESULT GetFreqInfo(t_freq_info *buffer, bool scan);

	//download calib histo
	//NI_RESULT GetCalibHisto(t_tdc_calib *buffer_1, t_tdc_calib *buffer_2);

	//Set LEMO Monitor
	//NI_RESULT TdcSDK::SetLemo(t_lemo_params cfg_data);

	//Set SIGNAL GENERATOR
	//NI_RESULT TdcSDK::SetGen(t_gen_params cfg_data);

	//Set DACs references
	//NI_RESULT TdcSDK::SetDACs(t_dac_ref cfg_data);

	//Set COUNTERS
	//NI_RESULT TdcSDK::SetCounter(t_count_params cfg_data, char* buffer);

	//NI_RESULT SetCLOCKParam();
	//NI_RESULT SetTDCParam();
	//NI_RESULT SetDATAParam();
	//NI_RESULT SetGENERALParam();
	//NI_RESULT SetDMALISTParam();
	//NI_RESULT TestIpConnection(string addr, t_board_info *buffer);


private:
	NI_RESULT ExtractParamSubPaths(string path, string *board, string *asic, string *cmd);
	ZIRE_HAL *hal;
	ZIRE_DATAHANDLER *data_handler;

	//vector <TdcSDK_list*> *tdclst;
	//
	//TdcSDK_settings *tdc_set;
	//TdcSDK_histo *tdchisto;
	//TdcSDK_counter *tdc_count;
	//t_general_params gen_params;
	//t_cfg_data cfg_buffer;
};

#endif