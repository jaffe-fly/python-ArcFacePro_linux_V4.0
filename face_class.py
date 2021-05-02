# -*- coding:utf-8 -*-
import cv2
from util import Face_data_class, Serverce, Face_read_so
from ctypes import *
from io import BytesIO
import os
import numpy as np
from logzero import logger


class Image_dect():
    def __init__(self):
        self.license, self.Face_read_so = Serverce.sourece_license()
        self.ret, self.Handle = Serverce.Initialize()
        if self.ret == 90114 or self.ret == 0:
            logger.info(f"Initialization successful:{self.ret},Handle:{self.Handle},License:{self.license}")
        else:
            logger.info(f"Initialization fail:{self.ret},Handle:{self.Handle},License:{self.license}")
        self.image_data = None  # 源数据
        self.handle_data = None  # 压缩后的数据
        self.width = 0
        self.height = 0
        self.MulFaces = Face_data_class.ASF_MultiFaceInfo()  # 多人脸识别
        self.DetectedFaces = Face_data_class.ASF_FaceFeature()  # 人脸特征
        self.SingleFaces = Face_data_class.ASF_SingleFaceInfo()  # 单个人脸识别
        self.Face3DAngle = Face_data_class.ASF_Face3DAngle()
        self.asvloffscreen = Face_data_class.ASVLOFFSCREEN()


    # cv2记载图片并处理
    def LoadImg(self, image_data):
        self.image_data = image_data
        sp = image_data.shape
        image = cv2.resize(image_data, (sp[1] // 4 * 4, sp[0] // 4 * 4))
        sp = image.shape
        self.handle_data = image
        self.width = sp[1]
        self.height = sp[0]

    # 激活文件信息
    def ASFGetActiveFileInfo(self):
        """
        获取激活文件信息
        :return: 状态码， 激活文件信息
        """
        activeFileInfo = Face_data_class.ASF_ActiveFileInfo()
        return self.Face_read_so.ASFGetActiveFileInfo(byref(activeFileInfo)), activeFileInfo

    # 激活设备信息
    def ASFGetActiveDeviceInfo(self):
        deviceInfo = c_char_p()
        res = self.Face_read_so.ASFGetActiveDeviceInfo(byref(deviceInfo))
        return res, deviceInfo.value

    # 人脸检测
    def MultiFaceInfo(self):
        self.image_bytes = bytes(self.handle_data)
        self.image_cast_bytes = cast(self.image_bytes, Serverce.c_ubyte_p)
        Face_result = self.Face_read_so.Discern(self.Handle, self.width, self.height, 0x201, self.image_cast_bytes,
                                                byref(self.MulFaces))
        return Face_result

    # 提取人脸特征
    def GetFeature(self, registerOrNot=0x1, mask=0):
        """
        registerOrNot :
            注册照：ASF_REGISTER 0x1
            识别照：ASF_RECOGNITION 0x0
        mask: 带口罩 1，否则0
        """
        result = self.Face_read_so.Feature(self.Handle,
                                           self.width,
                                           self.height,
                                           0x201,
                                           self.image_cast_bytes,
                                           byref(self.SingleFaces),
                                           registerOrNot,
                                           mask,
                                           byref(self.DetectedFaces))
        if result == 0:
            # print(self.DetectedFaces.featureSize)# featureSize 2056
            # print(self.DetectedFaces.feature)
            f = BytesIO(string_at(self.DetectedFaces.feature, self.DetectedFaces.featureSize))
            value = f.getvalue()
            # NewDetectedFaces = Face_data_class.ASF_FaceFeature()
            # NewDetectedFaces.featureSize = self.DetectedFaces.featureSize
            # 必须操作内存来保留特征值,因为c++会在过程结束后自动释放内存
            # NewDetectedFaces.feature = self.Face_read_so.malloc(self.DetectedFaces.featureSize)
            # self.Face_read_so.memcpy(NewDetectedFaces.feature, self.DetectedFaces.feature,
            #                          self.DetectedFaces.featureSize)
            return value
        else:
            return result

    # 从多人中提取单人数据
    def GetSingleFace(self, index):
        ra = self.MulFaces.faceRect[index]
        rb = self.MulFaces.faceDataInfoList[index]
        self.SingleFaces.faceRect.left = ra.left
        self.SingleFaces.faceRect.right = ra.right
        self.SingleFaces.faceRect.top = ra.top
        self.SingleFaces.faceRect.bottom = ra.bottom
        self.SingleFaces.faceOrient = self.MulFaces.faceOrient[index]
        self.SingleFaces.faceDataInfo.data = rb.data
        self.SingleFaces.faceDataInfo.dataSize = rb.dataSize

    # 单个人脸比较
    def SingelFaceCompare(self, Feature1, Feature2):
        Score = c_float()
        result = self.Face_read_so.Compare(self.Handle, Feature1, Feature2, byref(Score),
                                           self.Face_read_so.ASF_ID_PHOTO)
        return result, Score.value

    # 人脸属性检测
    def Process(self):
        res = self.Face_read_so.Process(self.Handle,
                                        self.width,
                                        self.height,
                                        self.Face_read_so.PAF_RGB24_B8G8R8,
                                        self.image_cast_bytes,
                                        byref(self.MulFaces),
                                        self.Face_read_so.PROCESS_MASK)
        return res

    # 获取年龄
    def getAge(self):
        get_ageInfo = Face_data_class.ASF_AgeInfo()
        res = self.Face_read_so.ASFGetAge(self.Handle, byref(get_ageInfo))
        return res, get_ageInfo.ageArray, get_ageInfo.num

    # 性别信息
    def getGender(self):
        get_Gneder = Face_data_class.ASF_GenderInfo()
        res = self.Face_read_so.ASFGetGender(self.Handle, byref(get_Gneder))
        return res, get_Gneder.genderArray, get_Gneder.num

    # 获取3D角度信息
    def get3Dangle(self):
        get3dangle = Face_data_class.ASF_Face3DAngle()
        res = self.Face_read_so.ASFGetFace3DAngle(self.Handle, byref(get3dangle))
        return res, get3dangle

    # 销毁引擎
    def uninitialize(self):
        self.Face_read_so.ASFUninitEngine(self.Handle)

    # 图像质量检测
    def ImageQualityDetect(self, isMask=0, detectModel=0x01):
        """
        isMask:仅支持传入1、0、-1，戴口罩 1，否则认为未戴口罩
        detectModel:预留字段，当前版本使用默认参数即可 ASF_DETECT_MODEL_RGB  0x01
        """
        confidenceLevel = c_float()
        res = self.Face_read_so.ASFImageQualityDetect(self.Handle, self.width, self.height,
                                                      self.Face_read_so.PAF_RGB24_B8G8R8,
                                                      self.image_cast_bytes, self.SingleFaces, isMask,
                                                      byref(confidenceLevel), detectModel)
        return res, confidenceLevel.value

    # 图像质量检测(图像数据)
    def imageQuality(self):
        self.asvloffscreen.u32PixelArrayFormat = self.Face_read_so.PAF_RGB24_B8G8R8
        self.asvloffscreen.i32Width = self.width
        self.asvloffscreen.i32Height = self.height
        self.asvloffscreen.pi32Pitch[0] = self.width * 3
        self.asvloffscreen.ppu8Plane[0] = self.image_cast_bytes
        # self.imageQualityInfo.faceQualityValue =
        # self.imageQualityInfo.faceNum =
        res = self.Face_read_so.ASFImageQualityDetectEx(self.Handle,
                                                        byref(self.asvloffscreen),
                                                        byref(self.MulFaces),
                                                        byref(self.imageQualityInfo))
        return res

    #人脸额头点数组，每张人脸额头区域通过四个点表示
    def facelandmark(self):
        landmarkinfo = Face_data_class.ASF_LandMarkInfo()
        res = self.Face_read_so.ASFGetFaceLandMark(self.Handle,byref(landmarkinfo))
        if res ==0:
            return landmarkinfo
        else:
            return res


if __name__ == '__main__':
    imde = Image_dect()

    # 获取激活文件信息
    # res = imde.ASFGetActiveFileInfo()
    # print("激活文件信息",res[1])

    # 获取设备信息
    # res = imde.ASFGetActiveDeviceInfo()
    # print("设备信息", res)

    # 属性检测
    imgpath = r'test_pic/124.jpg'
    img = cv2.imread(imgpath)
    imde.LoadImg(img)
    imde.MultiFaceInfo()
    faceNum = imde.MulFaces.faceNum
    print("检测到的人脸数量：", faceNum)
    imde.GetSingleFace(0)
    Feature = imde.GetFeature()
    feature_value = [i for i in Feature]
    print("人脸特征int型：", feature_value)
    print("特征长度：", len(feature_value))
    res = imde.Process()
    print("人脸属性检测开启：",res)
    ageinfo = imde.getAge()
    print("检测到的 人脸年龄：", ageinfo[1][0])
    genderinfo = imde.getGender()  # 0:男性; 1:女性; -1:未知
    print("检测到的 人脸性别：", genderinfo[1][0])
    get3Dangle = imde.get3Dangle()
    # 不支持f-string格式化
    # TODO status数值显示不正确，待调试
    print("检测到的 3DAngle roll: {:.2f}".format(get3Dangle[1].roll[0]))
    print("检测到的 3DAngle yaw: {:.2f}".format(get3Dangle[1].yaw[0]))
    print("检测到的 3DAngle pitch: {:.2f}".format(get3Dangle[1].pitch[0]))
    print("检测到的 3DAngle num: {}".format(get3Dangle[1].num))

    quality = imde.ImageQualityDetect()
    print("检测到的 人脸质量：", quality[1])
    imde.Process()
    resm = imde.facelandmark()
    print("检测到的 额头位置",(resm.point[0].x,resm.point[0].y))
    print("检测到的 额头位置", (resm.point[1].x, resm.point[1].y))
    print("检测到的 额头位置", (resm.point[2].x, resm.point[2].y))
    print("检测到的 额头位置", (resm.point[3].x, resm.point[3].y))

