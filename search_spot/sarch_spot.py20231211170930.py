#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file sarch_spot.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

# 必要なモジュールのインポート
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
sarch_spot_spec = ["implementation_id", "sarch_spot", 
         "type_name",         "sarch_spot", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "Reo", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class sarch_spot
# @brief ModuleDescription
# 
# 
# </rtc-template>
class sarch_spot(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_airphoto_in = OpenRTM_aist.instantiateDataType(RTC.TimedString)
        """
        """
        self._airphoto_inIn = OpenRTM_aist.InPort("airphoto_in", self._d_airphoto_in)
        self._d_photospot_out = OpenRTM_aist.instantiateDataType(RTC.TimedString)
        """
        """
        self._photospot_outOut = OpenRTM_aist.OutPort("photospot_out", self._d_photospot_out)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
		
        # Set InPort buffers
        self.addInPort("airphoto_in",self._airphoto_inIn)
		
        # Set OutPort buffers
        self.addOutPort("photospot_out",self._photospot_outOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK
	
    ###
    ## 
    ## The finalize action (on ALIVE->END transition)
    ## 
    ## @return RTC::ReturnCode_t
    #
    ## 
    #def onFinalize(self):
    #

    #    return RTC.RTC_OK
	
    ###
    ##
    ## The startup action when ExecutionContext startup
    ## 
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onStartup(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The shutdown action when ExecutionContext stop
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onShutdown(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ##
    #
    # The activated action (Active state entry action)
    #
    # @param ec_id target ExecutionContext Id
    # 
    # @return RTC::ReturnCode_t
    #
    #
    def onActivated(self, ec_id):
    
        return RTC.RTC_OK
	
    ###
    ##
    ## The deactivated action (Active state exit action)
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onDeactivated(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ##
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onExecute(self, ec_id):

        if self._airphoto_inIn.isNew(): #テキストデータが来たか確認
            self.name = self._airphoto_inIn.read().data #値を読み込む
        
            print("写真を撮りたい観光スポットと被写体との距離の範囲を設定してください。")
            print("何m以上から写真を取りたいか[m]")
            distance_1 = int(input())
            print("写真取る最大の距離を指定[m]")
            distance_2 = int(input())

            #googlemapの縮尺レベル
            googlemap_scale_level_list = [123456.79012,61728.39506,30303.03030,15151.51515,7,75.75758,3773.58491,1941.74757,970.87379,485.43689,238.09524,119.04762,59.52381,29.85075,14.92537,7.46269,3.70370,1.88679,0.94340,0.47170,0.23529]

            # ファイルシステムから画像を読み込む
            image_path = f'{self.name}.jpg'  # 正しい画像パスに置き換えてください
            image = Image.open(image_path)

            # 画像をnumpy配列に変換する
            image_array = np.array(image)

            # 指定された色かどうかをチェックする関数
            def is_desired_color(point, color, tolerance=10):
                return all(abs(point[i] - color[i]) <= tolerance for i in range(3))

            # ブレゼンハムの線アルゴリズムを使用して、線上のピクセルを取得する
            def get_line_pixels(start, end):
                # 初期条件を設定
                x1, y1 = start
                x2, y2 = end
                dx = x2 - x1
                dy = y2 - y1

                # 線の傾きが急かどうか判定
                is_steep = abs(dy) > abs(dx)

                # 線を回転させる
                if is_steep:
                    x1, y1 = y1, x1
                    x2, y2 = y2, x2

                # 必要に応じて開始点と終了点を交換し、交換状態を記録
                swapped = False
                if x1 > x2:
                    x1, x2 = x2, x1
                    y1, y2 = y2, y1
                    swapped = True

                # 差分を再計算
                dx = x2 - x1
                dy = y2 - y1

                # エラーを計算
                error = int(dx / 2.0)
                ystep = 1 if y1 < y2 else -1

                # 端点間のバウンディングボックスを反復処理してポイントを生成
                y = y1
                points = []
                for x in range(x1, x2 + 1):
                    coord = (y, x) if is_steep else (x, y)
                    points.append(coord)
                    error -= abs(dy)
                    if error < 0:
                        y += ystep
                        error += dx

                # 座標が交換された場合はリストを逆転
                if swapped:
                    points.reverse()
                return points

            # 条件を更新して線を描画する関数
            def draw_lines_updated(image_array, center, angle_increment, desired_color, road_colors, ignore_radius_ratio):
                rows, cols, _ = image_array.shape
                fig, ax = plt.subplots()
                ax.imshow(image_array)
    
                # どれくらい線を引くか
                radius = googlemap_scale_level_list[googlemap_scale_level] * (max_photo_distance  - ignore_radius_ratio) #線をどこまで引くか
                ignore_radius = googlemap_scale_level_list[googlemap_scale_level] * ignore_radius_ratio/2  # 無視する半径を定義(googlemapのzoomレベル17を基準に(0.94340 m/pix))
    
                # `angle_increment`度ごとに線を描画する
                for angle in range(0, 360, angle_increment):
                    rad_angle = np.deg2rad(angle)
                    end_x = int(center[0] + radius * np.cos(rad_angle))
                    end_y = int(center[1] + radius * np.sin(rad_angle))
        
                    # 線上の各ピクセルに対して処理を行う
                    line_pixels = get_line_pixels(center, (end_x, end_y))
                    line_started = False
                    for point in line_pixels:
                        x, y = point
                        if 0 <= x < cols and 0 <= y < rows:
                            if np.hypot(x - center[0], y - center[1]) >= ignore_radius:
                                if not line_started:
                                    # 無視する半径の外で線の描画を開始
                                    line_start = point
                                    line_started = True
                                if is_desired_color(image_array[y, x], desired_color):
                                    # 特定の色に接触したら赤い線で描画を終了
                                    ax.add_patch(patches.FancyArrowPatch(posA=line_start, posB=point,
                                                                arrowstyle='-', color='red', linewidth=1))
                                    break
                    # 特定の色に接触していない場合は黒い線で描画
                    if line_started and not is_desired_color(image_array[y, x], desired_color):
                        ax.add_patch(patches.FancyArrowPatch(posA=line_start, posB=(end_x, end_y),
                                                    arrowstyle='-', color='black', linewidth=1))

                plt.axis('off')
                plt.tight_layout()
                plt.show()

            #googlemapの縮尺レベルを定義する
            googlemap_scale_level = 17

            # 画像の中心と特定の色、道路の色、写真を撮る距離を定義する
            center_of_image = (image_array.shape[1] // 2, image_array.shape[0] // 2)
            specific_color = (223, 224, 229)  # 特定の色()
            road_colors = [(169, 185, 201), (219, 223, 232),(221,244,224)]  # 道路の色のリスト
            ignore_radius_ratio = distance_1  # 何m以上から写真を取りたいか(メートルで)
            max_photo_distance = distance_2 #写真取る最大の距離を指定(メートルで)

            # 条件を更新して15度ごとに線を描画する
            draw_lines_updated(image_array, center_of_image, 15, specific_color, road_colors, ignore_radius_ratio)

        return RTC.RTC_OK
	
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onAborting(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The error action in ERROR state
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onError(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The reset action that is invoked resetting
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onReset(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The state update action that is invoked after onExecute() action
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##

    ##
    #def onStateUpdate(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The action that is invoked when execution context's rate is changed
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK
	



def sarch_spotInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=sarch_spot_spec)
    manager.registerFactory(profile,
                            sarch_spot,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    sarch_spotInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("sarch_spot" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

