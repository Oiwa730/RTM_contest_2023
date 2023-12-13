#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file mark_output.py
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
from PIL import Image, ImageDraw


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
mark_output_spec = ["implementation_id", "mark_output", 
         "type_name",         "mark_output", 
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
# @class mark_output
# @brief ModuleDescription
# 
# 
# </rtc-template>
class mark_output(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_photospot_in = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        """
        self._photospot_inIn = OpenRTM_aist.InPort("photospot_in", self._d_photospot_in)


		


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
        self.addInPort("photospot_in",self._photospot_inIn)
		
        # Set OutPort buffers
		
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
    
        if self._photospot_inIn.isNew(): #テキストデータが来たか確認
            self.data = self._photospot_inIn.read().data #値を読み込む

            print("画像の保存名を入力してください。（最初に入力したものと必ず同じに）")
            name = input()
            '''
            # 文字列リストを整数リストに変換する
            points = [int(item) for item in self.data]

            blue_points = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]

            # 画像を読み込む
            image = Image.open(f"C:/Users/reore/Documents/RToutput/{name}.jpg")  # 画像のパスを指定

            # 画像に点を描画する
            draw = ImageDraw.Draw(image)
            for point in blue_points:
                draw.point(point, fill="blue")  # 青色で点を描画

            # 画像を保存する
            image_path = f'C:/Users/reore/Documents/RToutput/coordinates_plot_{name}.jpg'  # 保存するパス
            plt.savefig(image_path)

            plt.show()
            print("画像が保存されました。")
            '''

            # 画像を読み込む
            image = Image.open(f"C:/Users/reore/Documents/RToutput/{name}.jpg")  # 画像のパスを指定

            # 新しい画像に点を描画するためのコピーを作成
            draw_image = image.copy()
            draw = ImageDraw.Draw(draw_image)

            # 文字列リストを整数リストに変換する
            points = [int(item) for item in self.data]

            # 座標のタプルリストに変換
            blue_points = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]

            # 円の半径
            radius = 10

            # 画像に円を描画する
            for point in blue_points:
                x, y = point
                draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="blue")  # 青色で円を描画

            # 画像を保存する
            image_path = f'C:/Users/reore/Documents/RToutput/coordinates_plot_{name}.jpg'  # 保存するパス
            draw_image.save(image_path)

            print("画像が保存されました。")

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
	



def mark_outputInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=mark_output_spec)
    manager.registerFactory(profile,
                            mark_output,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    mark_outputInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("mark_output" + args)

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

