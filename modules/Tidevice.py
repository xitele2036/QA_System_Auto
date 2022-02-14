
import subprocess
from time import sleep


class TideviceSetUp():

    def __init__(self):
        pass


    def run(self):
        try:
            subprocess.Popen('tidevice wdaproxy -B com.facebook.jasonliu.xctrunner --port 8100', creationflags=subprocess.CREATE_NEW_CONSOLE)
            print("tidevice server boot up")

        except Exception as e:
            print("Error: 无法启动进程")
            print(e.args)


    def kill(self):
        try:
            subprocess.Popen('taskkill /im tidevice.exe', creationflags=subprocess.CREATE_NEW_CONSOLE)
            print("kill tidevice server")

        except Exception as e:
            print("Error: 无法启动进程")
            print(e.args)


if __name__ == '__main__':
    subprocess.Popen('tidevice wdaproxy -B com.facebook.jasonliu.xctrunner --port 8100', creationflags=subprocess.CREATE_NEW_CONSOLE)
    sleep(60)
    subprocess.Popen('taskkill /im tidevice.exe',creationflags=subprocess.CREATE_NEW_CONSOLE)

    # process.stdin.write(("tidevice wdaproxy -B com.facebook.jasonliu.xctrunner --port 8100").encode('utf-8'))
    # 往控制台里写入ffmpeg命令
    # 这样执行完ffmpeg命令不会退出，想要调用完自动退出要使用('%s&exit\n' % ffmpeg_cmd)
    # process.stdin.flush()
    # T = tidevicesetup()
    # T.run()
    # os.popen(r"tidevice wdaproxy -B com.facebook.jasonliu.xctrunner --port 8100","r")
    # subprocess.Popen("tidevice wdaproxy -B com.facebook.jasonliu.xctrunner --port 8100", creationflags=subprocess.CREATE_NEW_CONSOLE)