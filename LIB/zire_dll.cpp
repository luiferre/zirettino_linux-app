// zire_dll.cpp : Defines the exported functions for the DLL application.
//

//#include "stdafx.h"
#include "zire_dll.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <iostream>
#include <cstdlib>
#include <cstring>
#include <string>
#include <string.h>
#include <stdlib.h>
#include <sstream>
using namespace std;

struct
{
	ZireSDK *zire;
	int valid;
	string url;

} Devices[MAX_NUMBER_OF_DEVICE];

ZIRE_DLL_API NI_RESULT ZIRE_Connect(char *url, void *buffer, NI_HANDLE *handle) {
	int newdevid;
	int i;
	newdevid = -1;

	for (i = 0; i<MAX_NUMBER_OF_DEVICE; i++)
	{
		if (Devices[i].valid == 0)
		{
			newdevid = i;
			break;
		}
	}
	if (newdevid == -1)
	{
		return NI_TOO_MANY_DEVICES_CONNECTED;
	}
	else
	{
		*handle = newdevid;
		Devices[*handle].zire = new ZireSDK();

		string surl(url);

		if (Devices[*handle].zire->Connect(surl, (DAQ_DEVICE*)buffer) == NI_OK)
		{
			Devices[*handle].valid = 1;
			Devices[*handle].url = surl;
			return NI_OK;
		}

		//Connection failed
		delete Devices[*handle].zire;
		return NI_ERROR;
	}

}

ZIRE_DLL_API NI_RESULT ZIRE_Disconnect(char *url, NI_HANDLE *handle) {

	if (*handle >= MAX_NUMBER_OF_DEVICE) return -101;
	if (Devices[*handle].valid == 1)
	{
		if (Devices[*handle].zire->Disconnect() == NI_OK)
		{
			Devices[*handle].valid = 0;
			Devices[*handle].url = "";
			delete Devices[*handle].zire;
			return NI_OK;
		}
		else
		{
			return NI_ERROR_SOCKET;
		}
	}
	else
	{
		return NI_INVALID_HANDLE;
	}


}

ZIRE_DLL_API NI_RESULT ZIRE_SetParameter(char *Path, uint32_t value, NI_HANDLE * handle) {
	NI_RESULT Status;
	if (Devices[*handle].valid == 1)
	{
		Status = Devices[*handle].zire->SetParameter(string(Path), value);
		return Status;
	}
	else
	{	
		return NI_INVALID_HANDLE;
	}
}

ZIRE_DLL_API NI_RESULT ZIRE_GetParameter(char *Path, uint32_t *value, NI_HANDLE * handle) {
	NI_RESULT Status;
	if (*handle >= MAX_NUMBER_OF_DEVICE) return -101;
	if (Devices[*handle].valid == 1)
	{
		Status = Devices[*handle].zire->GetParameter(string(Path), value);
		return Status;
	}
	else
	{
		return NI_INVALID_HANDLE;
	}
}

ZIRE_DLL_API NI_RESULT ZIRE_ExecuteCommand(char *Path, uint32_t value, NI_HANDLE * handle) {
	NI_RESULT Status;
	if (*handle >= MAX_NUMBER_OF_DEVICE) return -101;
	if (Devices[*handle].valid == 1)
	{
		Status = Devices[*handle].zire->ExecuteCommand(string(Path), value);
		return Status;
	}
	else
	{
		return NI_INVALID_HANDLE;
	}
}

ZIRE_DLL_API NI_RESULT ZIRE_AllocateBoard(void **buffer, uint32_t nbin, NI_HANDLE * handle) {
	NI_RESULT Status;
	if (*handle >= MAX_NUMBER_OF_DEVICE) return -101;
	if (Devices[*handle].valid == 1)
	{
		*buffer = malloc(sizeof(t_board));
		Status = Devices[*handle].zire->AllocateHistogram(*buffer, nbin);
		return Status;
	}
	else
	{
		return NI_INVALID_HANDLE;
	}
}

ZIRE_DLL_API NI_RESULT ZIRE_StartAcq(void *buffer, char *Path, bool save, NI_HANDLE * handle) {
	NI_RESULT Status;
	if (*handle >= MAX_NUMBER_OF_DEVICE) return -101;
	if (Devices[*handle].valid == 1)
	{
		Status = Devices[*handle].zire->StartAcq((t_board*)buffer, string(Path), save);
		return Status;
	}
	else
	{
		return NI_INVALID_HANDLE;
	}
}

ZIRE_DLL_API NI_RESULT ZIRE_StartAcqRaw(char *Path, bool _time, uint32_t target, char *role, NI_HANDLE * handle) {
	NI_RESULT Status;
	if (*handle >= MAX_NUMBER_OF_DEVICE) return -101;
	if (Devices[*handle].valid == 1)
	{
		Status = Devices[*handle].zire->StartAcqRaw(string(Path), _time, target, string(role));
		return Status;
	}
	else
	{
		return NI_INVALID_HANDLE;
	}
}

ZIRE_DLL_API NI_RESULT ZIRE_StartStairs(char *Path, uint32_t target, NI_HANDLE * handle) {
	NI_RESULT Status;
	if (*handle >= MAX_NUMBER_OF_DEVICE) return -101;
	if (Devices[*handle].valid == 1)
	{
		Status = Devices[*handle].zire->StartStairs(string(Path), target);
		return Status;
	}
	else
	{
		return NI_INVALID_HANDLE;
	}
}

ZIRE_DLL_API NI_RESULT ZIRE_Req_Start(NI_HANDLE * handle) {
	NI_RESULT Status;
	if (*handle >= MAX_NUMBER_OF_DEVICE) return -101;
	if (Devices[*handle].valid == 1)
	{
		Status = Devices[*handle].zire->Data_Request_Start();
		return Status;
	}
	else
	{
		return NI_INVALID_HANDLE;
	}
}

ZIRE_DLL_API NI_RESULT ZIRE_Req_End(NI_HANDLE * handle) {
	NI_RESULT Status;
	if (*handle >= MAX_NUMBER_OF_DEVICE) return -101;
	if (Devices[*handle].valid == 1)
	{
		Status = Devices[*handle].zire->Data_Request_End();
		return Status;
	}
	else
	{
		return NI_INVALID_HANDLE;
	}
}

ZIRE_DLL_API NI_RESULT ZIRE_StopAcq(void *buffer, NI_HANDLE * handle) {
	NI_RESULT Status;
	if (*handle >= MAX_NUMBER_OF_DEVICE) return -101;
	if (Devices[*handle].valid == 1)
	{
		Status = Devices[*handle].zire->StopAcq((t_board*)buffer);
		return Status;
	}
	else
	{
		return NI_INVALID_HANDLE;
	}
}