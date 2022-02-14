
import subprocess
import time
from modules.TestCfgParse import TestCfgParse


class FFMpegCapture(object):
    
    def cameraInit(self,CamDevName):
        
        deviceList="ffmpeg -list_devices true -f dshow -i dummy"
        p=subprocess.Popen(deviceList,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
        
        cmdOutput=''
        
        for line in iter(p.stdout.readline, b''):
            
            print(line.strip())
            print(CamDevName)
            
            if CamDevName.encode() in line.strip():
                cmdOutput= line
                
            if not subprocess.Popen.poll(p) is None:
                if line == "":
                    break
        print("*****************************")
         
        if CamDevName.encode() in cmdOutput:
            print("%s Camera is ready for use!"%CamDevName)
        else:
            print("Please check your camera installation!")   
            
        print("*****************************")
        
        p.stdout.close()
        
        
    def ffmpeg_video_record(self,CamVName,CamAName,videoFileName,recordTime,videoTag):    
            
        #save_path = ".\\Video"
        #cur_ts = str(int(time.time()))
        #filename = '{}.mkv'.format(cur_ts)
        #file_path = '{}\\{}'.format(save_path, filename)
        
        # the order in args is important
        # you can speicy your ffmpeg flags here
        args = [
            ['-f', 'dshow'],
            ['-s', '800x600'],
            ['-framerate', '30'],        
            ['-i', 'video="'+CamVName+'"'],
            ['-f', 'dshow'],
            ['-i', 'audio="'+CamAName+'"'],
            ['-vcodec', 'libx264'],
            ['-acodec', 'aac'],
            ['-strict', '-2'],
            ['-t',recordTime],
            ['-vf','drawtext=fontfile=FreeSerif.ttf:text='+videoTag+':fontcolor=white:fontsize=30'],
            ['', videoFileName]
    
        ]
    
        cmd = 'ffmpeg '
        for arg in args:
            cmd += '{} {} '.format(arg[0], arg[1])
        print(cmd)
        #return cmd
        child_proc=subprocess.Popen(cmd, shell=True)
        time.sleep(float(recordTime))
        child_proc.terminate()
        print("Video Recording is suscceed")
  

if __name__ == "__main__":
    
    CameraCfg=TestCfgParse()
    CameraVDN=CameraCfg.GetTestCfgInfo("Camera_Video_Device_Name")
    CameraADN=CameraCfg.GetTestCfgInfo("Camera_Audio_Device_Name")       
    
    videoPath=".\\Video\\test24.mkv"
    ffmpegCap=FFMpegCapture()
    ffmpegCap.cameraInit(CameraVDN)
    ffmpegCap.ffmpeg_video_record(CameraVDN,CameraADN,videoPath,6,'"test 001"')