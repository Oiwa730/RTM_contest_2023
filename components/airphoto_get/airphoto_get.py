#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file airphoto_get.py
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

# モジュールのインポート
import pandas as pd
import urllib
import urllib.error
import urllib.request
# Google API モジュール
import googlemaps


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
airphoto_get_spec = ["implementation_id", "airphoto_get", 
         "type_name",         "airphoto_get", 
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
# @class airphoto_get
# @brief ModuleDescription
# 
# 
# </rtc-template>
class airphoto_get(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_coordinate_in = OpenRTM_aist.instantiateDataType(RTC.TimedStringSeq)
        """
        """
        self._coordinate_inIn = OpenRTM_aist.InPort("coordinate_in", self._d_coordinate_in)
        self._d_airphoto_out = OpenRTM_aist.instantiateDataType(RTC.TimedString)
        """
        """
        self._airphoto_outOut = OpenRTM_aist.OutPort("airphoto_out", self._d_airphoto_out)


		


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
        self.addInPort("coordinate_in",self._coordinate_inIn)
		
        # Set OutPort buffers
        self.addOutPort("airphoto_out",self._airphoto_outOut)
		
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

        if self._coordinate_inIn.isNew(): #テキストデータが来たか確認
            self.data = self._coordinate_inIn.read().data #値を読み込む

            self.lat = float(self.data[0])
            self.lon = float(self.data[1])
            self.name = self.data[2]

            print("APIキーを入力してください。")
            google_api = input()
            
            # パラメータの設定
            googleapikey = google_api
            output_path = "C:/Users/reore/Documents/RToutput"
            pixel = "1300x1300"
            scale = "17"

            # defによる関数オブジェクトの作成
            # 画像をダウンロードする
            def download_image():

                # htmlの設定
                html1 = 'https://maps.googleapis.com/maps/api/staticmap?center='

                # maptypeで取得する地図の種類を設定
                html2 = '&maptype=terrain'

                # sizeでピクセル数を設定
                html3 = '&size='

                # sensorはGPSの情報を使用する場合にtrueとするので今回はfalseで設定
                html4 = '&sensor=false'

                # zoomで地図の縮尺を設定
                html5 = '&zoom='

                # マーカーの位置の設定（マーカーを表示させてくなければ無でも大丈夫）
                html6 = '&markers='

                # key="googleから取得したキーコード"となるように設定
                html7 = '&key='


                # 緯度経度の情報をセット
                axis = str(self.lat) + "," + str(self.lon)

                # url
                url = html1 + axis + html2 + html3 + pixel + html4 + html5 + scale + html6 + axis + html7 + googleapikey

                # pngファイルのパスを作成
                dst_path = output_path + '\\' + str(self.name) + ".png"

                # 画像を取得しローカルに書き込み
                try:
                    data = urllib.request.urlopen(url).read()
                    with open(dst_path, mode="wb") as f:
                        f.write(data)

                except urllib.error.URLError as e:
                    print(e)
            
            # 緯度経度の情報より画像を取得する
            download_image()
            print("画像入手完了しました。")
            

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
	



def airphoto_getInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=airphoto_get_spec)
    manager.registerFactory(profile,
                            airphoto_get,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    airphoto_getInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("airphoto_get" + args)

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

