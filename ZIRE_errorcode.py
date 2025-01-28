NI_OK = 0x00000000
NI_ERROR_GENERIC = 0x00000001
NI_ERROR_INTERFACE = 0x00000002
NI_ERROR_FPGA = 0x00000003
NI_ERROR_TRANSFER_MAX_LENGTH = 0x00000004
NI_ERROR_NOTCONNECTED = 0x00000005
NI_NO_DATA_AVAILABLE = 0x00000006
NI_TOO_MANY_DEVICES_CONNECTED = 0x00000007
NI_INVALID_HANDLE = 0x00000008
NI_INVALID_KEY = 0x00000009
NI_INVALID_PARAMETER = 0x0000000A
NI_PARAMETER_OUT_OF_RANGE = 0x0000000B
NI_INCOMPLETE_READ = 0x0000000C
NI_INVALID_COMMAND = 0x0000000D
NI_ERROR_SOCKET = 0x0000000E
NI_DATA_END_REQ = 0x0000000F
NI_ALREADY_CONNECTED = 0x00000100
NI_ALLOC_FAILED = 0x00000200
NI_MEMORY_NOT_ALLOCATED = 0x00000201
NI_INVALID_BUFFER_TYPE = 0x00000202
NI_INVALID_BUFFER_SIZE = 0x00000203
NI_INCOMPATIBLE_BUFFER = 0x00000204
NI_INVALID_BUFFER = 0x00000205
NI_TIMEOUT = 0x00000300
NI_SOCKET_NOT_CONNECTED = 0x00000301
NI_INVALID_CFG_JSON = 0x10000000
NI_CFG_JSON_NOT_FOUND = 0x10000001
NI_DEVICE_NAME_ALREADY_EXISTS = 0x10000002
NI_INVALID_PATH = 0x10001000
NI_NOT_FOUND = 0x10001FFE
NI_INVALID_TYPE = 0x10001FFF
NI_ALREADY_RUNNING = 0x10003000
NI_NOT_RUNNING = 0x10003001
NI_NOT_ARMED = 0x20000000
NI_SPECIFIC_ERROR = 0xFFFFFFFD

def help():
    print("\n\t ** Available commands **\t\n")
    print("\t- config:\n\tSend 'config' command, then write the .json path. If there is a default path set type 'd' (stands for default)\n")

    print("\t- exit:\n\tClose the application correctly.\n")

def home_screen():
    z_app = """                                                                                              
  _______        __                         
 |___  (_)      /_/     /\                
    / / _ _ __ ___     /  \   _ __  _ __  
   / / | | '__/ _ \   / /\ \ | '_ \| '_ \ 
  / /__| | | |  __/  / ____ \| |_) | |_) |
 /_____|_|_|  \___| /_/    \_\ .__/| .__/ 
                             | |   | |    
                             |_|   |_|    
    """

    print(z_app)
    print("\t--- BY NUCLEAR INSTRUMENTS ---\t\n\n")


