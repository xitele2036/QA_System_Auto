#coding=utf-8
#!python
import wx
import os
from modules.TestCfgParse import CfgParse

log_file_path = os.path.realpath(os.path.dirname(os.path.dirname(__file__))+'/Config')
AutoTestAppINI = log_file_path + '/AutoTestApp.INI'

class SetFileIni(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Config Info")
        icon = wx.Icon(name=".\\icons\\Config.ico", type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        panel = wx.Panel(self)
        # First create the controls
        topLbl = wx.StaticText(panel, -1, "AutoTestApp Setting Information")#1 创建窗口部件
        topLbl.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.cfg = CfgParse(AutoTestAppINI)

        # RestConnection
        # self.RestConnection = wx.StaticText(panel, -1, "RestConnection")
        # self.SetFont(wx.Font(18,wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        type_value = self.cfg.GetCfgInfo("RestConnection", "Type")
        self.type_key = wx.StaticText(panel, -1, "Type:")
        self.type_value = wx.TextCtrl(panel, -1, type_value)

        ip_value = self.cfg.GetCfgInfo("RestConnection", "Ethernet.IP")
        self.ip_key = wx.StaticText(panel, -1, "Ethernet.IP:")
        self.ip_value = wx.TextCtrl(panel, -1, ip_value)

        port_value = self.cfg.GetCfgInfo("RestConnection", "Port")
        self.port_key = wx.StaticText(panel, -1, "Port:")
        self.port_value = wx.TextCtrl(panel, -1, port_value)

        dictfile_vale = self.cfg.GetCfgInfo("RestConnection", "DICT_FILE")
        self.dictfile_key = wx.StaticText(panel, -1, "DICT_FILE:")
        self.dictfile_vale = wx.TextCtrl(panel, -1, dictfile_vale)

        auth_token_value = self.cfg.GetCfgInfo("RestConnection", "Auth_Token")
        self.auth_token_key = wx.StaticText(panel, -1, "Auth_Token:")
        self.auth_token_value = wx.TextCtrl(panel, -1, auth_token_value)

        udp_port_value = self.cfg.GetCfgInfo("RestConnection", "UDP_PORT")
        self.udp_port_key = wx.StaticText(panel, -1, "UDP_PORT:")
        self.udp_port_value = wx.TextCtrl(panel, -1, udp_port_value)

        # AUTOTEST
        autotestcfg_value = self.cfg.GetCfgInfo("AUTOTEST", "AutoTestCfg")
        self.autotestcfg_key = wx.StaticText(panel, -1, "AutoTestCfg:")
        self.autotestcfg_value = wx.TextCtrl(panel, -1, autotestcfg_value)

        # SERIAL
        board_port_value = self.cfg.GetCfgInfo("SERIAL", "Board_PORT")
        self.board_port_key = wx.StaticText(panel, -1, "Board_PORT:")
        self.board_port_value = wx.TextCtrl(panel, -1, board_port_value)

        dev_qd_port_value = self.cfg.GetCfgInfo("SERIAL", "DEV_QD_PORT")
        self.dev_qd_port_key = wx.StaticText(panel, -1, "DEV_QD_PORT:")
        self.dev_qd_port_value = wx.TextCtrl(panel, -1, dev_qd_port_value)

        # TestPC
        testpc_ip_value = self.cfg.GetCfgInfo("TestPC", "TestPC_IP")
        self.testpc_ip_key = wx.StaticText(panel, -1, "TestPC_IP:")
        self.testpc_ip_value = wx.TextCtrl(panel, -1, testpc_ip_value)

        # Tablet
        tablet_ip_value = self.cfg.GetCfgInfo("Tablet", "Tablet_IP")
        self.tablet_ip_key = wx.StaticText(panel, -1, "Tablet_IP:")
        self.tablet_ip_value = wx.TextCtrl(panel, -1, tablet_ip_value)

        cast_device_model_value = self.cfg.GetCfgInfo("Tablet", "CAST_DEVICE_MODEL")
        self.cast_device_model_key = wx.StaticText(panel, -1, "CAST_DEVICE_MODEL:")
        self.cast_device_model_value = wx.TextCtrl(panel, -1, cast_device_model_value)

        # RedRat
        redrat_name_value = self.cfg.GetCfgInfo("RedRat", "RedRat_Name")
        self.redrat_name_key = wx.StaticText(panel, -1, "RedRat_Name:")
        self.redrat_name_value = wx.TextCtrl(panel, -1, redrat_name_value)

        redrat_dataset_value = self.cfg.GetCfgInfo("RedRat", "RedRat_dataset")
        self.redrat_dataset_key = wx.StaticText(panel, -1, "RedRat_dataset:")
        self.redrat_dataset_value = wx.TextCtrl(panel, -1, redrat_dataset_value)

        # VG859
        vg859_ip_value = self.cfg.GetCfgInfo("VG859", "VG859_IP")
        self.vg859_ip_key = wx.StaticText(panel, -1, "VG859_IP:")
        self.vg859_ip_value = wx.TextCtrl(panel, -1, vg859_ip_value)

        # QD980
        qd980_ip_value = self.cfg.GetCfgInfo("QD980", "QD980_IP")
        self.qd980_ip_key = wx.StaticText(panel, -1, "QD980_IP:")
        self.qd980_ip_value = wx.TextCtrl(panel, -1, qd980_ip_value)

        qd980_username_value = self.cfg.GetCfgInfo("QD980", "QD980_UserName")
        self.qd980_username_key = wx.StaticText(panel, -1, "QD980_UserName:")
        self.qd980_username_value = wx.TextCtrl(panel, -1, qd980_username_value)

        qd980_pw_value = self.cfg.GetCfgInfo("QD980", "QD980_PW")
        self.qd980_pw_key = wx.StaticText(panel, -1, "QD980_PW:")
        self.qd980_pw_value = wx.TextCtrl(panel, -1, qd980_pw_value)

        # Camera
        camera_video_name_value = self.cfg.GetCfgInfo("Camera", "Camera_Video_Device_Name")
        self.camera_video_name_key = wx.StaticText(panel, -1, "Camera_Video_Device_Name:")
        self.camera_video_name_value = wx.TextCtrl(panel, -1, camera_video_name_value)

        camera_audio_name_value = self.cfg.GetCfgInfo("Camera", "Camera_Audio_Device_Name")
        self.camera_audio_name_key = wx.StaticText(panel, -1, "Camera_Audio_Device_Name:")
        self.camera_audio_name_value = wx.TextCtrl(panel, -1, camera_audio_name_value)

        # EPCR3
        epcr3_ip_value = self.cfg.GetCfgInfo("EPCR3", "EPCR3_IP")
        self.epcr3_ip_key = wx.StaticText(panel, -1, "EPCR3_IP:")
        self.epcr3_ip_value = wx.TextCtrl(panel, -1, epcr3_ip_value)

        epcr3_username_value = self.cfg.GetCfgInfo("EPCR3", "EPCR3_UserName")
        self.epcr3_username_key = wx.StaticText(panel, -1, "EPCR3_UserName:")
        self.epcr3_username_value = wx.TextCtrl(panel, -1, epcr3_username_value)

        epcr3_pw_value = self.cfg.GetCfgInfo("EPCR3", "EPCR3_PW")
        self.epcr3_pw_key = wx.StaticText(panel, -1, "EPCR3_PW:")
        self.epcr3_pw_value = wx.TextCtrl(panel, -1, epcr3_pw_value)

        # 保存与取消按钮
        self.SaveBtn = wx.Button(panel, -1, "Save")
        self.Bind(wx.EVT_BUTTON, self.OnSaveBtn, self.SaveBtn)
        self.CancelBtn = wx.Button(panel, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancelBtn, self.CancelBtn)
        # Now do the layout.
        # mainSizer is the top-level one that manages everything
        #2 垂直的sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel), 0,
                wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        # addrSizer is a grid that holds all of the address info

        addrSizer = wx.FlexGridSizer(cols=2, hgap=23, vgap=5)
        addrSizer.AddGrowableCol(1)

        # type
        addrSizer.Add(self.type_key, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.type_value, 0, wx.EXPAND)
        # ip
        addrSizer.Add(self.ip_key, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.ip_value, 0, wx.EXPAND)
        # addrSizer.Add((10,10)) # some empty space
        # addrSizer.Add(addr2, 0, wx.EXPAND)

        # port
        addrSizer.Add(self.port_key, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.port_value, 0, wx.EXPAND)
        # the city, state, zip fields are in a sub-sizer
        # 水平嵌套
        # cstSizer = wx.BoxSizer(wx.HORIZONTAL)
        # cstSizer.Add(city, 1)
        # cstSizer.Add(state, 0, wx.LEFT|wx.RIGHT, 5)
        # cstSizer.Add(zip)
        # addrSizer.Add(cstSizer, 0, wx.EXPAND)

        addrSizer.Add(self.dictfile_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.dictfile_vale, 0, wx.EXPAND)

        # auth_token
        addrSizer.Add(self.auth_token_key, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.auth_token_value, 0, wx.EXPAND)

        # udp_port
        addrSizer.Add(self.udp_port_key, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.udp_port_value, 0, wx.EXPAND)

        # AutoTestCfg
        addrSizer.Add(self.autotestcfg_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.autotestcfg_value, 0, wx.EXPAND)
        # now add the addrSizer to the mainSizer

        # Board_PORT
        addrSizer.Add(self.board_port_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.board_port_value, 0, wx.EXPAND)

        # DEV_QD_PORT
        addrSizer.Add(self.dev_qd_port_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.dev_qd_port_value, 0, wx.EXPAND)

        # TestPC_IP
        addrSizer.Add(self.testpc_ip_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.testpc_ip_value, 0, wx.EXPAND)

        # Tablet_IP
        addrSizer.Add(self.tablet_ip_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.tablet_ip_value, 0, wx.EXPAND)

        # CAST_DEVICE_MODEL
        addrSizer.Add(self.cast_device_model_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.cast_device_model_value, 0, wx.EXPAND)

        # RedRat_Name
        addrSizer.Add(self.redrat_name_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.redrat_name_value, 0, wx.EXPAND)

        # RedRat_dataset
        addrSizer.Add(self.redrat_dataset_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.redrat_dataset_value, 0, wx.EXPAND)

        # VG859_IP
        addrSizer.Add(self.vg859_ip_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.vg859_ip_value, 0, wx.EXPAND)

        # QD980_IP
        addrSizer.Add(self.qd980_ip_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.qd980_ip_value, 0, wx.EXPAND)

        # QD980_UserName
        addrSizer.Add(self.qd980_username_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.qd980_username_value, 0, wx.EXPAND)

        # QD980_PW
        addrSizer.Add(self.qd980_pw_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.qd980_pw_value, 0, wx.EXPAND)

        # Camera_Video_Device_Name
        addrSizer.Add(self.camera_video_name_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.camera_video_name_value, 0, wx.EXPAND)

        # Camera_Audio_Device_Name
        addrSizer.Add(self.camera_audio_name_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.camera_audio_name_value, 0, wx.EXPAND)

        # EPCR3_IP
        addrSizer.Add(self.epcr3_ip_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.epcr3_ip_value, 0, wx.EXPAND)

        # EPCR3_UserName
        addrSizer.Add(self.epcr3_username_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.epcr3_username_value, 0, wx.EXPAND)

        # EPCR3_PW
        addrSizer.Add(self.epcr3_pw_key, 0,
                      wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.epcr3_pw_value, 0, wx.EXPAND)

        # 添加Flex sizer
        mainSizer.Add(addrSizer, 0, wx.EXPAND|wx.ALL, 10)
        # The buttons sizer will put them in a row with resizeable
        # gaps between and on either side of the buttons
        #8 按钮行
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(self.SaveBtn)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(self.CancelBtn)
        btnSizer.Add((20,20), 1)
        mainSizer.Add(btnSizer, 0, wx.EXPAND|wx.BOTTOM, 10)
        panel.SetSizer(mainSizer)
        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)


    def OnSaveBtn(self,event):
        #print("Before Close main")
        # logger.info("Before Close main")
        self.cfg.SetCfgInfo("RestConnection", "Type", self.type_value.GetValue())
        self.cfg.SetCfgInfo("RestConnection", "Ethernet.IP", self.ip_value.GetValue())
        self.cfg.SetCfgInfo("RestConnection", "Port", self.port_value.GetValue())
        self.cfg.SetCfgInfo("RestConnection", "DICT_FILE", self.dictfile_vale.GetValue())
        self.cfg.SetCfgInfo("RestConnection", "Auth_Token", self.auth_token_value.GetValue())
        self.cfg.SetCfgInfo("RestConnection", "UDP_PORT", self.udp_port_value.GetValue())

        self.cfg.SetCfgInfo("AUTOTEST", "AutoTestCfg", self.autotestcfg_value.GetValue())

        self.cfg.SetCfgInfo("SERIAL", "Board_PORT", self.board_port_value.GetValue())
        self.cfg.SetCfgInfo("SERIAL", "DEV_QD_PORT", self.dev_qd_port_value.GetValue())

        self.cfg.SetCfgInfo("TestPC", "TestPC_IP", self.testpc_ip_value.GetValue())

        self.cfg.SetCfgInfo("Tablet", "Tablet_IP", self.tablet_ip_value.GetValue())
        self.cfg.SetCfgInfo("Tablet", "CAST_DEVICE_MODEL", self.cast_device_model_value.GetValue())

        self.cfg.SetCfgInfo("RedRat", "RedRat_Name", self.redrat_name_value.GetValue())
        self.cfg.SetCfgInfo("RedRat", "RedRat_dataset", self.redrat_dataset_value.GetValue())

        self.cfg.SetCfgInfo("VG859", "VG859_IP", self.vg859_ip_value.GetValue())

        self.cfg.SetCfgInfo("QD980", "QD980_IP", self.qd980_ip_value.GetValue())
        self.cfg.SetCfgInfo("QD980", "QD980_UserName", self.qd980_username_value.GetValue())
        self.cfg.SetCfgInfo("QD980", "QD980_PW", self.qd980_pw_value.GetValue())

        self.cfg.SetCfgInfo("Camera", "Camera_Video_Device_Name", self.camera_video_name_value.GetValue())
        self.cfg.SetCfgInfo("Camera", "Camera_Audio_Device_Name", self.camera_audio_name_value.GetValue())

        self.cfg.SetCfgInfo("EPCR3", "EPCR3_IP", self.epcr3_ip_value.GetValue())
        self.cfg.SetCfgInfo("EPCR3", "EPCR3_UserName", self.epcr3_username_value.GetValue())
        self.cfg.SetCfgInfo("EPCR3", "EPCR3_PW", self.epcr3_pw_value.GetValue())

        self.cfg.Reloadini()
        self.Close()

    def OnCancelBtn(self,event):
        self.Close()

if __name__ == '__main__':
    # app = wx.PySimpleApp()
    app = wx.App()
    # frm = VsiliconAbout(None)
    # frm.Show()
    # app.MainLoop()
    SetFileIni().Show()
    app.MainLoop()