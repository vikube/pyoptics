from ctypes import (
    Structure,
    cdll,
    c_bool,
    c_short,
    c_int,
    c_uint,
    c_int16,
    c_int32,
    c_char,
    c_byte,
    c_long,
    c_float,
    c_double,
    POINTER,
    CFUNCTYPE,
    c_ushort,
    c_ulong,
    c_char_p,
    c_wchar_p,
    ARRAY,
    c_void_p,
    c_ubyte
)

c_word = c_ushort
c_dword = c_ulong

from ...ctools.tools import bind, null_function
from . import _enum as enum

# lib_api_path = r"C:\Windows\System32\uEye_api_64.dll"
# lib_api = cdll.LoadLibrary(lib_api_path)

from ...locateDll import locateDll
libname = "uEye_api_64.dll"
foldername = "System32"
dllpath  = locateDll(libname,  foldername, "C:\\Windows")
lib_api = cdll.LoadLibrary(dllpath.replace("\\","\\\\"))


class StructureEx(Structure):

    def getdict(self):
        return dict((f, getattr(self, f)) for f, _ in self._fields_)

    def loaddict(self, d):
        """
        d -- a dictionary of parameters. The keys of the dictionary much match the attributes of the class.
        """
        for f in d.keys():
            if not hasattr(self, f):
                raise AttributeError('Given dictionary has unmatched attributes.')
            for field, ctype in self._fields_:
                if field == f:
                    break
            if ctype in [c_short, c_long, c_int, c_int16, c_int32, c_uint, c_ushort, c_ulong]:
                setattr(self, f, ctype(int(d[f])))
            if ctype in [c_float, c_double]:
                setattr(self, f, ctype(float(d[f])))

    def __str__(self):
        return str(self.getdict())


class UEYE_CAMERA_INFO(StructureEx):
	_fields_ = [("CameraID", c_dword),
				("DeviceID", c_dword),
				("SensorID", c_dword),
				("InUse", c_dword),
				("SerNo", 16*c_char),
				("Model", 16*c_char),
				("Status", c_dword),
				("Reserved", 2*c_dword),
				("FullModelName", 32*c_char),
				("Reserved2", 5*c_dword)]

class UEYE_CAMERA_LIST(StructureEx):
    # Making it 'incomplete' ctypes type. It didn't work well because once the detailed is declared, it is fixed. Kernel reboot is needed to alter it. This is inconvenient.
    # pass

    # for now, assume that the number of cameras would be only 10 max.
	_fields_ = [("count", c_ulong),
				("cameras", ARRAY(UEYE_CAMERA_INFO,10)) ]

class UEYE_CAMERA_LIST_Ex(StructureEx):
    # Making it 'incomplete' ctypes type. It didn't work well because once the detailed is declared, it is fixed. Kernel reboot is needed to alter it. This is inconvenient.
    pass

    # for now, assume that the number of cameras would be only 100 max.
    # _fields_ = [("count", c_ulong),
    #             ("cameras", ARRAY(UEYE_CAMERA_INFO,100)) ]

class CAMINFO(StructureEx):
    _fields_ = [("SerialNo", 12*c_char),
                ("ID", 20*c_char),
                ("Version", 10*c_char),
                ("Date", 12*c_char),
                ("Select", c_ubyte),
                ("Type", c_ubyte),
                ("Reserved", 8*c_char)]

    def __str__(self):
        super().__str__()


class SENSORINFO(StructureEx):
    _fields_ = [("SensorID", c_word),
                ("Sensorname", 32*c_char),
                ("ColorMode", c_char),
                ("MaxWidth", c_dword),
                ("MaxHeight", c_dword),
                ("MasterGain", c_bool),
                ("RGain", c_bool),
                ("GGain", c_bool),
                ("BGain", c_bool),
                ("GlobShutter", c_bool),
                ("PixelSize", c_word),
                ("UpperLeftBayerPixel", c_char),
                ("Reserved", 13*c_char)]

######################################################################################
######################################################################################
######################################################################################

GetNumberOfCameras = bind(lib_api, "is_GetNumberOfCameras", [POINTER(c_int)], c_int)
GetCameraList = bind(lib_api, "is_GetCameraList", [POINTER(UEYE_CAMERA_LIST)], c_int)
# GetCameraListEx = bind(lib_api, "is_GetCameraList", [POINTER(UEYE_CAMERA_LIST_Ex)], c_int)

GetCameraInfo = bind(lib_api, "is_GetCameraInfo", [enum.HIDS, POINTER(CAMINFO)], c_int)
GetSensorInfo = bind(lib_api, "is_GetSensorInfo", [enum.HIDS, POINTER(SENSORINFO)], c_int)

InitCamera = bind(lib_api, "is_InitCamera", [POINTER(enum.HIDS), POINTER(enum.HWND)], c_int)
ExitCamera = bind(lib_api, "is_ExitCamera", [enum.HIDS], c_int)

SetDisplayMode = bind(lib_api, "is_SetDisplayMode", [enum.HIDS, c_int], c_int)
SetColorMode = bind(lib_api, "is_SetColorMode", [enum.HIDS, c_int], c_int)

GetError = bind(lib_api, "is_GetError", [enum.HIDS, POINTER(c_int), c_char_p], c_int)

AllocImageMem = bind(lib_api,"is_AllocImageMem", [enum.HIDS, c_int, c_int, c_int, POINTER(c_char_p), POINTER(c_int)], c_int)
SetImageMem = bind(lib_api, "is_SetImageMem", [enum.HIDS, c_char_p, c_int], c_int)
CopyImageMem = bind(lib_api, "is_CopyImageMem", [enum.HIDS, c_char_p, c_int, c_char_p], c_int)
FreeImageMem = bind(lib_api, "is_FreeImageMem", [enum.HIDS, c_char_p, c_int], c_int)

FreezeVideo = bind(lib_api, "is_FreezeVideo", [enum.HIDS, c_int], c_int)
StopLiveVideo = bind(lib_api, "is_StopLiveVideo", [enum.HIDS, c_int], c_int)

SetExternalTrigger = bind(lib_api, "is_SetExternalTrigger", [enum.HIDS, c_int], c_int)

PixelClock = bind(lib_api, "is_PixelClock", [enum.HIDS, c_uint, c_void_p, c_uint], c_int)
Exposure = bind(lib_api, "is_Exposure", [enum.HIDS, c_uint, c_void_p, c_uint], c_int)
# GetFramesPerSecond = bind(lib_api, "is_GetFramesPerSecond", [enum.HIDS, POINTER(c_double)])
# SetFrameRate = bind(lib_api, "is_SetFrameRate", [enum.HIDS, c_double, POINTER(c_double)], c_int)

BlackLevel = bind(lib_api, "is_Blacklevel", [enum.HIDS, c_uint, c_void_p, c_uint], c_int)