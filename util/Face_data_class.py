# coding:utf-8
"""
按照ARCSOFT_ARC_FACE_DEVELOPER'S_GUIDE.pdf 文件中3.3 数据结构依次封装

"""
from ctypes import *

c_ubyte_p = POINTER(c_ubyte)


# 人脸框
class MRECT(Structure):
    _fields_ = [(u'left', c_int32), (u'top', c_int32), (u'right', c_int32), (u'bottom', c_int32)]


# 3.3.1版本信息
# 版本号,构建日期,版权说明
class ASF_VERSION(Structure):
    _fields_ = [('Version', c_char_p), ('BuildDate', c_char_p), ('CopyRight', c_char_p)]


# 3.3.2激活文件信息
class ASF_ActiveFileInfo(Structure):
    # startTime:bytes
    # endTime:bytes
    # platform:bytes
    # sdkType:bytes
    # appId:bytes
    # sdkKey:bytes
    # sdkVersion:bytes
    # fileVersion:bytes
    _fields_ = [('startTime', c_char_p),  # SDK开始时间
                ('endTime', c_char_p),  # SDK截止时间
                ('activeKey', c_char_p),  # 激活码
                ('platform', c_char_p),  # 平台版本
                ('sdkType', c_char_p),  # SDK 类型
                ('appId', c_char_p),  # APPID
                ('sdkKey', c_char_p),  # SDKKEY
                ('sdkVersion', c_char_p),  # SDK 版本号
                ('fileVersion', c_char_p)] # 激活文件版本号


    def __str__(self):
        return "ASF_ActiveFileInfo(startTime={},endTime={},platform={},sdkType={},appId={},sdkKey={},sdkVersion={},fileVersion={})" \
            .format(self.startTime, self.endTime, self.platform, self.sdkType, self.appId, self.sdkKey,
                    self.sdkVersion, self.fileVersion)


# 3.3.3人脸信息
class ASF_FaceDataInfo(Structure):
    _fields_ = [('data', c_void_p), ('dataSize', c_int32)]


# 3.3.4单人人脸信息  人脸框,人脸角度
class ASF_SingleFaceInfo(Structure):
    _fields_ = [('faceRect', MRECT), ('faceOrient', c_int32), ('faceDataInfo', ASF_FaceDataInfo)]


# 3.3.5多人人脸信息
class ASF_MultiFaceInfo(Structure):
    _fields_ = [
        (u'faceRect', POINTER(MRECT)),  # 人脸框数组
        (u'faceOrient', POINTER(c_int32)),  # 人脸角度数组
        (u'faceNum', c_int32),  # 人脸数
        ('faceID', POINTER(c_int32)),  # 一张人脸从进入画面直到离开画面，faceID不变。在VIDEO模式下有效，IMAGE模式下为空。
        ('wearGlasses', POINTER(c_float)),  # 戴眼镜置信度[0-1],推荐阈值0.5
        ('leftEyeClosed', POINTER(c_int32)),  # 左眼状态 0 未闭眼；1 闭眼
        ('rightEyeClosed', POINTER(c_int32)),  # 右眼状态 0 未闭眼；1 闭眼
        ('faceShelter', POINTER(c_int32)),  # "1" 表示 遮挡, "0" 表示 未遮挡, "-1" 表示不确定
        ('faceDataInfoList', POINTER(ASF_FaceDataInfo))  # 多张人脸信息 TODO 确认是否指针
    ]


# 3.3.6人脸特征 人脸特征,人脸特征长度
class ASF_FaceFeature(Structure):
    _fields_ = [('feature', c_ubyte_p), ('featureSize', c_int32)]


# 3.3.7 年龄信息
# ageArray 0:未知; >0:年龄
# num 检测的人脸数
class ASF_AgeInfo(Structure):
    _fields_ = [('ageArray', POINTER(c_int32)), ('num', c_int32)]


# 3.3.8 性别信息
# genderArray 0:男性; 1:女性; -1:未知
# num 检测的人脸数
class ASF_GenderInfo(Structure):
    _fields_ = [('genderArray', POINTER(c_int32)), ('num', c_int32)]


# 3.3.9
# 人脸角度信息
class ASF_Face3DAngle(Structure):  # 人脸角度信息
    _fields_ = [
        ('roll', POINTER(c_float)),
        ('yaw', POINTER(c_float)),
        ('pitch', POINTER(c_float)),
        ('status', POINTER(c_int32)),
        ('num', c_int32)]


# 3.3.10
# 活体置信度。
class ASF_LivenessThreshold(Structure):
    _fields_ = [('thresholdmodel_BGR', c_float),  # BGR活体检测阈值设置，默认值0.5
                ('thresholdmodel_IR', c_float)]  # IR活体检测阈值设置，默认值0.7


# 3.3.11
# 活体信息
class ASF_LivenessInfo(Structure):
    _fields_ = [('islive', POINTER(c_int32)), ('num', c_int32)]


# 3.3.12
# 口罩信息
class ASF_MaskInfo(Structure):
    _fields_ = [('maskArray', POINTER(c_int32)), ('num', c_int32)]


# 3.3.13
# 特征点信息
class ASF_FaceLandmark(Structure):
    _fields_ = [('x', c_float), ('y', c_float)]


# 3.3.14
class ASF_LandMarkInfo(Structure):
    _fields_ = [('point', POINTER(ASF_FaceLandmark)), ('num', c_int32)]


# 3.3.15
# 图像数据信息
class ASVLOFFSCREEN(Structure):
    _fields_ = [(u'u32PixelArrayFormat', c_uint32), (u'i32Width', c_int32), (u'i32Height', c_int32),
                (u'ppu8Plane', c_ubyte_p * 4), (u'pi32Pitch', c_int32 * 4)]

    def __init__(self):
        Structure.__init__(self)
        self.gc_ppu8Plane0 = None
        self.gc_ppu8Plane1 = None
        self.gc_ppu8Plane2 = None
        self.gc_ppu8Plane3 = None
