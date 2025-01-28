import ctypes
import time
from ZIRE_errorcode import *
from ZIRE_dataclass import *

# Definizione classe ZIRE
class ZIRE:
    def __init__(self):
        dll_path = ".//lib_zire.so"
        self.zire_dll = ctypes.CDLL(dll_path)

        ################################################################
        #	ZIRE_DLL_API NI_RESULT ZIRE_Connect(char *url, void *buffer, NI_HANDLE *handle);
        #   ZIRE_DLL_API NI_RESULT ZIRE_Disconnect(char *url, NI_HANDLE *handle);
        #   ZIRE_DLL_API NI_RESULT ZIRE_SetParameter(char *Path, uint32_t value, NI_HANDLE * handle);
        #   ZIRE_DLL_API NI_RESULT ZIRE_GetParameter(char *Path, uint32_t *value, NI_HANDLE * handle);
        #   ZIRE_DLL_API NI_RESULT ZIRE_ExecuteCommand(char *Path, uint32_t value, NI_HANDLE * handle);
        #   ZIRE_DLL_API NI_RESULT ZIRE_AllocateBoard(void **buffer, uint32_t nbin, NI_HANDLE * handle);
        #   ZIRE_DLL_API NI_RESULT ZIRE_StartAcq(void *buffer, char *path, bool save, NI_HANDLE * handle);
        #   ZIRE_DLL_API NI_RESULT ZIRE_StartAcqRaw(char *Path, bool _time, uint32_t target, char *role, NI_HANDLE * handle)
        #   ZIRE_DLL_API NI_RESULT ZIRE_StartStairs(char *Path, uint32_t target, NI_HANDLE * handle);
        #   ZIRE_DLL_API NI_RESULT ZIRE_Req_Start(NI_HANDLE *handle);
        #   ZIRE_DLL_API NI_RESULT ZIRE_Req_End(NI_HANDLE *handle);
        #   ZIRE_DLL_API NI_RESULT ZIRE_StopAcq(void *buffer, NI_HANDLE * handle);
        ################################################################

        # Definisci le firme delle funzioni
        self.ZIRE_Connect = self.zire_dll.ZIRE_Connect
        self.ZIRE_Connect.argtypes = [ctypes.c_char_p, ctypes.POINTER(DAQ_DEVICE), ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_Disconnect = self.zire_dll.ZIRE_Disconnect
        self.ZIRE_Disconnect.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_SetParameter = self.zire_dll.ZIRE_SetParameter
        self.ZIRE_SetParameter.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_GetParameter = self.zire_dll.ZIRE_GetParameter
        self.ZIRE_GetParameter.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_ExecuteCommand = self.zire_dll.ZIRE_ExecuteCommand
        self.ZIRE_ExecuteCommand.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_AllocateBoard = self.zire_dll.ZIRE_AllocateBoard
        self.ZIRE_AllocateBoard.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_StartAcq = self.zire_dll.ZIRE_StartAcq
        self.ZIRE_StartAcq.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool, ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_StartAcqRaw = self.zire_dll.ZIRE_StartAcqRaw
        self.ZIRE_StartAcqRaw.argtypes = [ctypes.c_char_p, ctypes.c_bool, ctypes.c_uint32, ctypes.c_char_p, ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_StartStairs = self.zire_dll.ZIRE_StartStairs
        self.ZIRE_StartStairs.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_Req_Start = self.zire_dll.ZIRE_Req_Start
        self.ZIRE_Req_Start.argtypes = [ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_Req_End = self.zire_dll.ZIRE_Req_End
        self.ZIRE_Req_End.argtypes = [ctypes.POINTER(ctypes.c_long)]

        self.ZIRE_StopAcq = self.zire_dll.ZIRE_StopAcq
        self.ZIRE_StopAcq.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_long)]

        # Definisci i tipi di dati ZIRE_BUFFER e ZIRE_HANDLE come puntatori
        self.ZIRE_HANDLE = ctypes.POINTER(ctypes.c_long)
        self.ZIRE_DEVICE = ctypes.POINTER(DAQ_DEVICE)
        self.ZIRE_BOARD = ctypes.POINTER(t_board)

        # Inizializza l'handle
        self.handle = self.ZIRE_HANDLE()
        self.handle = ctypes.create_string_buffer(4)
        self.handle_ptr = ctypes.cast(self.handle, self.ZIRE_HANDLE)

        # buffer DAQ_device
        self.device = self.ZIRE_DEVICE()
        self.device = ctypes.create_string_buffer(20)
        self.device_ptr = ctypes.cast(self.device, self.ZIRE_DEVICE)

        # buffer data board 
        self.board = ctypes.POINTER(t_board)



    def connect(self, url):
        return self.ZIRE_Connect(url.encode('utf-8'), self.device_ptr, self.handle_ptr)

    def disconnect(self, url):
        return self.ZIRE_Disconnect(url.encode('utf-8'), self.handle_ptr)

    def set_parameter(self, path, value):
        time.sleep(0.001)
        return self.ZIRE_SetParameter(path.encode('utf-8'), value, self.handle_ptr)

    def get_parameter(self, path):
        value = ctypes.c_uint32()
        result = self.ZIRE_GetParameter(path, ctypes.byref(value), self.handle_ptr)
        return result, value.value  
    
    def execute_command(self, path, value):
        return self.ZIRE_ExecuteCommand(path, value, self.handle_ptr)
    
    def allocate_board(self, path):
        return self.ZIRE_AllocateBoard(path, ctypes.byref(self.board_ptr), self.handle_ptr)
    
    def start_acq(self, path, save):
        return self.ZIRE_StartAcq(ctypes.byref(self.board_ptr), path, save, self.handle_ptr)
    
    def start_acq_raw(self, path, time, target, role):
        return self.ZIRE_StartAcqRaw(path.encode('utf-8'), time, target, role.encode('utf-8'), self.handle_ptr)
    
    def start_stairs(self, path, target):
        return self.ZIRE_StartStairs(path.encode('utf-8'), target, self.handle_ptr)
    
    def stop_acq(self):
        result = self.ZIRE_StopAcq(ctypes.byref(self.boar_ptr), self.handle_ptr)
        return result, self.board 
    
    def req_start(self):
        return self.ZIRE_Req_Start( self.handle_ptr)

    def req_end(self):
        return self.ZIRE_Req_End(self.handle_ptr)

