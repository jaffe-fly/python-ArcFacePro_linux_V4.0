# -*- coding:utf-8 -*-
from ctypes import *
from util.Face_data_class import *
import os
import yaml
from easydict import EasyDict

with open('MainConfing.yaml') as f:
    opt = yaml.load(f, Loader=yaml.SafeLoader)
opt = EasyDict(opt)
up_path = os.path.dirname(os.path.abspath(__file__))
path = os.path.abspath(os.path.join(up_path, "../"))
opt.dll_path = os.path.join(path, opt.dll_path)
opt.engine_path = os.path.join(path, opt.engine_path)
opt.license_path = os.path.join(path, opt.license_path)

_ = cdll.LoadLibrary(opt.dll_path)
dll = cdll.LoadLibrary(opt.engine_path)

dllc = CDLL("libc.so.6")
# dllc = cdll.msvcrt

# 枚举
ASF_DETECT_MODE_VIDEO = 0x00000000
ASF_DETECT_MODE_IMAGE = 0xFFFFFFFF
# 人脸检测方向
# 角度按逆时针方向。
ASF_OP_0_ONLY = 0x1  # 常规预览下正方向
ASF_OP_90_ONLY = 0x2  # 基于0°逆时针旋转90°的方向
ASF_OP_270_ONLY = 0x3  # 基于0°逆时针旋转270°的方向
ASF_OP_180_ONLY = 0x4  # 基于0°旋转180°的方向（逆时针、顺时针效果一样）
ASF_OP_ALL_OUT = 0x5  # 全角度
# 检测到的人脸角度
# 角度按逆时针方向
ASF_OC_0 = 0x1  # 0度
ASF_OC_90 = 0x2  # 90度
ASF_OC_270 = 0x3  # 270度
ASF_OC_180 = 0x4  # 180度
ASF_OC_30 = 0x5  # 30度
ASF_OC_60 = 0x6  # 60度
ASF_OC_120 = 0x7  # 120度
ASF_OC_150 = 0x8  # 150度
ASF_OC_210 = 0x9  # 210度
ASF_OC_240 = 0xa  # 240度
ASF_OC_300 = 0xb  # 300度
ASF_OC_330 = 0xc  # 330度
# 检测模型
# 根据图像颜色空间选择对应的算法模型进行检测。
ASF_DETECT_MODEL_RGB = 0x1  # RGB图像检测模型
# 人脸比对可选的模型
# 根据应用场景选择对应的模型进行人脸特征比对。
ASF_LIFE_PHOTO = 0x1  # 用于生活照之间的特征比对，推荐阈值0.80
ASF_ID_PHOTO = 0x2  # 用于证件照或生活照与证件照之间的特征比对，推荐阈值0.82
# 人脸特征提取可选的模型
# 根据应用场景选择对应的模型进行人脸特征提取
ASF_RECOGNITION = 0x0  # 用于识别照人脸特征提取
ASF_REGISTER = 0x1  # 用于注册照人脸特征提取
# 图像数据格式
PAF_RGB24_B8G8R8 = 0x201

ASF_NONE = 0x00000000  # 无属性
ASF_FACE_DETECT = 0x00000001  # 此处detect可以是tracking或者detection两个引擎之一，具体的选择由detect mode 确定
ASF_FACERECOGNITION = 0x00000004  # 人脸特征
ASF_AGE = 0x00000008  # 年龄
ASF_GENDER = 0x00000010  # 性别
ASF_FACE3DANGLE = 0x00000020  # 3D角度
ASF_FACELANDMARK = 0x00000040  # 额头区域检测
ASF_LIVENESS = 0x00000080  # RGB活体
ASF_IMAGEQUALITY = 0x00000200  # 图像质量检测
ASF_IR_LIVENESS = 0x00000400  # IR活体
ASF_FACESHELTER = 0x00000800  # 脸遮挡
ASF_MASKDETECT = 0x00001000  # 口罩检测
ASF_UPDATE_FACEDATA = 0x00002000  # 人脸信息

# 初始化功能组合
MASK = ASF_FACE_DETECT | ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_FACELANDMARK | ASF_LIVENESS | ASF_IMAGEQUALITY | ASF_IR_LIVENESS | ASF_FACESHELTER | ASF_MASKDETECT | ASF_UPDATE_FACEDATA

# 属性检测时的 combinedMask
PROCESS_MASK = ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS | ASF_FACELANDMARK | ASF_MASKDETECT

malloc = dllc.malloc
malloc.restype = c_void_p
malloc.argtypes = (c_size_t,)

free = dllc.free
free.restype = None
free.argtypes = (c_void_p,)

memcpy = dllc.memcpy
memcpy.restype = c_void_p
memcpy.argtypes = (c_void_p, c_void_p, c_size_t)

"""
3.5 功能接口
"""
# 3.5.1获取激活文件信息
ASFGetActiveFileInfo = dll.ASFGetActiveFileInfo
ASFGetActiveFileInfo.restype = c_int32
ASFGetActiveFileInfo.argtypes = ()

# 3.5.2 在线激活 (项目采用离线激活，未测试此接口)
# Sourece = dll.ASFOnlineActivation
# Sourece.restype = c_int32
# Sourece.argtypes = (c_char_p, c_char_p,c_char_p)

# 3.5.3 采集当前设备信息（可离线）
ASFGetActiveDeviceInfo = dll.ASFGetActiveDeviceInfo
ASFGetActiveDeviceInfo.restype = c_int32
ASFGetActiveDeviceInfo.argtypes = ()

# 3.5.4 离线激活
Sourece = dll.ASFOfflineActivation
Sourece.restype = c_int32
Sourece.argtypes = (c_char_p,)

# 3.5.5初始化
Initializer = dll.ASFInitEngine
Initializer.restype = c_int32
Initializer.argtypes = (c_long, c_int32, c_int32, c_int32, POINTER(c_void_p))

# 3.5.6人脸检测
Discern = dll.ASFDetectFaces
Discern.restype = c_int32
Discern.argtypes = (c_void_p, c_int32, c_int32, c_int32, POINTER(c_ubyte), POINTER(ASF_MultiFaceInfo))

# 3.5.7人脸检测(图像结构体)
Discern_str = dll.ASFDetectFacesEx
Discern_str.restype = c_int32
Discern_str.argtypes = (c_void_p, POINTER(ASVLOFFSCREEN), POINTER(ASF_MultiFaceInfo))

# 3.5.10 质量检测
# 该接口针对单张人脸区域的图像进行质量检测，不是针对整张图像
ASFImageQualityDetect = dll.ASFImageQualityDetect
ASFImageQualityDetect.restype = c_int32
ASFImageQualityDetect.argtypes = (
    c_void_p, c_int32, c_int32, c_int32, POINTER(c_ubyte), POINTER(ASF_SingleFaceInfo), c_int32, POINTER(c_float),
    c_int32)

# 3.5.11 质量检测(图像结构体)
ASFImageQualityDetect_str = dll.ASFImageQualityDetectEx
ASFImageQualityDetect_str.restype = c_int32
ASFImageQualityDetect_str.argtypes = (
    c_void_p, POINTER(ASVLOFFSCREEN), POINTER(ASF_SingleFaceInfo), c_int32, POINTER(c_float), c_int32)

# 3.5.12 特征提取
Feature = dll.ASFFaceFeatureExtract
Feature.restype = c_int32
Feature.argtypes = (
    c_void_p, c_int32, c_int32, c_int32, POINTER(c_ubyte), POINTER(ASF_SingleFaceInfo), c_int32, c_int32,
    POINTER(ASF_FaceFeature))

# 3.5.13 特征提取
Feature_str = dll.ASFFaceFeatureExtractEx
Feature_str.restype = c_int32
Feature_str.argtypes = (
    c_void_p, POINTER(ASVLOFFSCREEN), POINTER(ASF_SingleFaceInfo), c_int32, c_int32, POINTER(ASF_FaceFeature))

# 3.5.14 特征比对
Compare = dll.ASFFaceFeatureCompare
Compare.restype = c_int32
Compare.argtypes = (c_void_p, POINTER(ASF_FaceFeature), POINTER(ASF_FaceFeature), POINTER(c_float), c_int32)

# 3.5.15 活体检测阈值
Set_Liveness_param = dll.ASFSetLivenessParam
Set_Liveness_param.restype = c_int32
Set_Liveness_param.argtypes = (c_void_p, POINTER(ASF_LivenessThreshold))

# 3.5.16 人脸属性检测
Process = dll.ASFProcess
Process.restype = c_int32
Process.argtypes = (c_void_p, c_int32, c_int32, c_int32, POINTER(c_ubyte), POINTER(ASF_MultiFaceInfo), c_int32)

# 3.5.17 人脸属性检测(图像结构体)
Process_str = dll.ASFProcessEx
Process_str.restype = c_int32
Process_str.argtypes = (c_void_p, POINTER(c_ubyte), POINTER(ASF_MultiFaceInfo), c_int32)

# 3.5.18 获取年龄信息
ASFGetAge = dll.ASFGetAge
ASFGetAge.restype = c_int32
ASFGetAge.argtypes = (c_void_p,POINTER(ASF_AgeInfo))

# 3.5.19 性别信息
ASFGetGender = dll.ASFGetGender
ASFGetGender.restype = c_int32
ASFGetGender.argtypes = (c_void_p,POINTER(ASF_GenderInfo))

# 3.5.20 获取3D角度信息
ASFGetFace3DAngle = dll.ASFGetFace3DAngle
ASFGetFace3DAngle.restype = c_int32
ASFGetFace3DAngle.argtypes = (c_void_p,POINTER(ASF_Face3DAngle))

# 3.5.21 获取RGB活体信息
ASFGetLivenessScore = dll.ASFGetLivenessScore
ASFGetLivenessScore.restype = c_int32
ASFGetLivenessScore.argtypes = (c_void_p,POINTER(ASF_LivenessInfo))

# 3.5.22 设置遮挡算法检测的阈值
ASFSetFaceShelterParam = dll.ASFSetFaceShelterParam
ASFSetFaceShelterParam.restype = c_int32
ASFSetFaceShelterParam.argtypes = (c_void_p,c_float)

# 3.5.23 获取人脸是否戴口罩。
ASFGetMask = dll.ASFGetMask
ASFGetMask.restype = c_int32
ASFGetMask.argtypes = (c_void_p,POINTER(ASF_MaskInfo))

# 3.5.24 获取额头区域位置。
ASFGetFaceLandMark = dll.ASFGetFaceLandMark
ASFGetFaceLandMark.restype = c_int32
ASFGetFaceLandMark.argtypes = (c_void_p,POINTER(ASF_LandMarkInfo))

# 3.5.25 单人脸 IR 活体检测
# combinedMask 目前仅支持 ASF_IR_LIVENESS
ASFProcess_IR = dll.ASFProcess_IR
ASFProcess_IR.retype = c_int32
ASFProcess_IR.argtypes = (c_void_p,c_int32,c_int32,c_int32,POINTER(c_ubyte), POINTER(ASF_MultiFaceInfo), c_int32)

# 3.5.26 单人脸 IR 活体检测(图像结构)
ASFProcess_IR_str = dll.ASFProcessEx_IR
ASFProcess_IR_str.retype = c_int32
ASFProcess_IR_str.argtypes = (c_void_p,POINTER(c_ubyte), POINTER(ASF_MultiFaceInfo), c_int32)

# 3.5.27 获取IR活体信息
Liveness_IR = dll.ASFGetLivenessScore_IR
Liveness_IR.restype = c_int32  # 成功返回 MOK，失败详见 3.2 错误码列表
Liveness_IR.argtypes = (c_void_p,POINTER(ASF_LivenessInfo))

# 3.5.28 获取SDK版本信息
version = dll.ASFGetVersion
version.restype = c_int32
version.argtypes = (ASF_VERSION,)

# 3.5.29 销毁引擎
ASFUninitEngine = dll.ASFUninitEngine
ASFUninitEngine.restype = c_int32
ASFUninitEngine.argtypes = (c_void_p,)