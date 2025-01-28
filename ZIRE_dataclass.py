import ctypes

class DAQ_DEVICE(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("PID", ctypes.c_uint32),
        ("MODEL", ctypes.c_uint32),
        ("FW_ver", ctypes.c_uint32),
        ("SW_ver", ctypes.c_uint32),
        ("Status", ctypes.c_uint32),
    ]

class t_data_elem(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("hit", ctypes.c_uint32),
        ("lg", ctypes.c_uint32),
        ("hg", ctypes.c_uint32),
    ]

class t_histo_elem(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("bin", ctypes.c_uint32),
        ("occupancy", ctypes.c_uint32),
    ]

class t_asic_channel(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("LG", ctypes.POINTER(t_histo_elem)),
        ("HG", ctypes.POINTER(t_histo_elem)),
        ("id", ctypes.c_uint32),
    ]

class t_asic(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ch", ctypes.POINTER(t_asic_channel)),
        ("id", ctypes.c_uint32),
    ]

class t_board(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("asic", ctypes.POINTER(t_asic)),
        ("numof_asic", ctypes.c_uint32),
        ("numof_ch", ctypes.c_uint32),
        ("allocated_size", ctypes.c_uint32),
        ("nbin", ctypes.c_uint32),
        ("lost", ctypes.c_uint32),
        ("validated", ctypes.c_uint32),
        ("totalsize", ctypes.c_uint32),
        ("timestamp", ctypes.c_uint64),
        ("trgid", ctypes.c_uint32),
        ("trgcnt", ctypes.c_uint32),
        ("flag", ctypes.c_uint32),
    ]

class config_params(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("asic", ctypes.POINTER(t_asic)),
        ("numof_asic", ctypes.c_uint32),
        ("numof_ch", ctypes.c_uint32),
        ("allocated_size", ctypes.c_uint32),
        ("nbin", ctypes.c_uint32),
        ("lost", ctypes.c_uint32),
        ("validated", ctypes.c_uint32),
        ("totalsize", ctypes.c_uint32),
        ("timestamp", ctypes.c_uint64),
        ("trgid", ctypes.c_uint32),
        ("trgcnt", ctypes.c_uint32),
        ("flag", ctypes.c_uint32),
    ]

    