# -*- coding:utf-8 -*-
from util.Face_read_so import opt,Sourece,Initializer,ASF_DETECT_MODE_IMAGE,ASF_OP_0_ONLY
from util import Face_read_so
from ctypes import *


Handle=c_void_p()
c_ubyte_p = POINTER(c_ubyte)


# 激活函数
def sourece_license():
    license = Sourece(opt.license_path.encode())
    return license, Face_read_so


# 初始化函数
def Initialize():# 1：视频或图片模式,2角度,3最大需要检测的人脸个数，取值范围[1,10],4功能,5返回激活句柄
    result = Initializer(ASF_DETECT_MODE_IMAGE,ASF_OP_0_ONLY,8,Face_read_so.MASK,byref(Handle))
    return result,Handle

