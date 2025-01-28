// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the ZIRE_DLL_EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// ZIRE_DLL_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.

#ifndef __ZIRE_API_C_H
#define __ZIRE_API_C_H

#include "zire_class.h"
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _WIN32
  #ifdef ZIRE_DLL_EXPORTS
    #define ZIRE_DLL_API extern "C" __declspec(dllexport)
  #else
    #define ZIRE_DLL_API extern "C" __declspec(dllimport)
  #endif
#else
  #ifdef ZIRE_DLL_EXPORTS
    #define ZIRE_DLL_API extern "C" __attribute__((visibility("default")))
  #else
    #define ZIRE_DLL_API extern "C"
  #endif
#endif

	typedef int NI_HANDLE;

#define MAX_NUMBER_OF_DEVICE (100)

	ZIRE_DLL_API NI_RESULT ZIRE_Connect(char *url, void *buffer, NI_HANDLE *handle);
	ZIRE_DLL_API NI_RESULT ZIRE_Disconnect(char *url, NI_HANDLE *handle);
	ZIRE_DLL_API NI_RESULT ZIRE_SetParameter(char *Path, uint32_t value, NI_HANDLE * handle);
	ZIRE_DLL_API NI_RESULT ZIRE_GetParameter(char *Path, uint32_t *value, NI_HANDLE * handle);
	ZIRE_DLL_API NI_RESULT ZIRE_ExecuteCommand(char *Path, uint32_t value, NI_HANDLE * handle);
	ZIRE_DLL_API NI_RESULT ZIRE_AllocateBoard(void **buffer, uint32_t nbin, NI_HANDLE * handle);
	ZIRE_DLL_API NI_RESULT ZIRE_StartAcq(void *buffer, char *Path, bool save, NI_HANDLE * handle);
  ZIRE_DLL_API NI_RESULT ZIRE_StartAcqRaw(char *Path, bool _time, uint32_t target, char *role, NI_HANDLE * handle);
  ZIRE_DLL_API NI_RESULT ZIRE_StartStairs(char *Path, uint32_t target, NI_HANDLE * handle);
	ZIRE_DLL_API NI_RESULT ZIRE_Req_Start(NI_HANDLE *handle);
	ZIRE_DLL_API NI_RESULT ZIRE_Req_End(NI_HANDLE *handle);
	ZIRE_DLL_API NI_RESULT ZIRE_StopAcq(void *buffer, NI_HANDLE * handle);

#ifdef __cplusplus
}
#endif

#endif 
