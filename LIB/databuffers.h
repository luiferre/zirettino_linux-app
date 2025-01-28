#pragma once
#ifndef __DATABUFFERS_H
#define __DATABUFFERS_H
#include <stdint.h>

#pragma pack(push, 1)
typedef struct {
	int PID;
	int MODEL;
	int FW_ver;
	int SW_ver;
	int Staus;
} DAQ_DEVICE;

#pragma pack(push, 1)
typedef struct {
	uint32_t hit;
	uint32_t lg;
	uint32_t hg;
} t_data_elem;

#pragma pack(push, 1)
typedef struct {
	uint32_t bin;
	uint32_t occupancy;
} t_histo_elem;

#pragma pack(push, 1)
typedef struct {
	t_histo_elem *LG;
	t_histo_elem *HG;
	uint32_t id;
} t_asic_channel;

#pragma pack(push, 1)
typedef struct {
	t_asic_channel *ch;
	uint32_t id;
} t_asic;

#pragma pack(push, 1)
typedef struct {
	t_asic *asic;
	uint32_t numof_asic=4;
	uint32_t numof_ch=32;
	uint32_t allocated_size;
	uint32_t nbin;
	uint32_t lost;
	uint32_t validated;
	uint32_t totalsize;
	uint64_t timestamp;
	uint32_t trgid;
	uint32_t trgcnt;
	uint32_t flag;
} t_board;

#endif
#pragma once
