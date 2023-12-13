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
         "conf.default.output_path_name", "C:/Users/reore/Documents/RToutput",

         "conf.__widget__.output_path_name", "text",

         "conf.__type__.output_path_name", "string",

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
        """
        
         - Name:  output_path
         - DefaultValue: C:/Users/reore/Documents/RToutput
        """
        self._output_path = ['C:/Users/reore/Documents/RToutput']
		
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
        self.bindParameter("output_path_name", self._output_path, "C:/Users/reore/Documents/RToutput")
		
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

            print("ズームレベルを入力してください。（0～21の整数：数が大きくなるごとにズームされます。）")
            print("測れる被写体との距離の目安")
            print("20:～70m　19:～80m　18:～155m　17:～320m　16:～630m　15:～1240m")
            
            # パラメータの設定
            googleapikey = google_api
            #output_path = "C:/Users/reore/Documents/RToutput"
            pixel_size = "640x640"
            scale = "2"
            zoom_level = int(input())

            # defによる関数オブジェクトの作成
            # 画像をダウンロードする
            def download_image():

                # htmlの設定
                html1 = 'https://maps.googleapis.com/maps/api/staticmap?'

                #中心となる緯度経度の設定
                html2 = f'center={str(self.lat)},{str(self.lon)}'

                # maptypeで取得する地図の種類を設定
                html3 = '&maptype=roadmap'

                # sizeで画像の大きさを設定
                html4 = f'&size={pixel_size}'

                #scale=1のとき（640×640）での画像サイズの何倍の画像サイズにするか
                html5 = f'&scale={scale}'

                # zoomで地図の縮尺度を設定
                html6 = f'&zoom={zoom_level}'

                # key="googleから取得したキーコード"となるように設定
                html7 = f'&key={googleapikey}'

                #道路に色をつける
                html8 = '&style=feature:road%7Ccolor:0xb06eba'

                #全てのラベルに同じ色を付ける
                html9 = '&style=element:labels.text%7Ccolor:0xffffff'

                #フォーマットの設定
                html10 ='&format=jpg'

                # url
                url = html1 + html2 + html3 + html4 + html5 + html6 + html7 + html8 + html9 + html10

                # pngファイルのパスを作成
                dst_path = self._output_path[0] + '\\' + str(self.name) + ".jpg"

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

            self._d_airphoto_out.data = self.name
            self._airphoto_outOut.write()

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

