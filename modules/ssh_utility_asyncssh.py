import asyncio
import re

import asyncssh
import sys
import time
import threading
from modules.MyReFiler import ReFilter

class CapLogcat():
    def __init__(self,ip):
        self.ip = ip

    async def start_logcat(self):
        async with asyncssh.connect(self.ip, known_hosts='known_hosts', username='root', password=None) as conn:
            res = await conn.run('logcat | grep airplay', check=False)
            # logs = open('SSHlogcat.log', 'a')
            # logs.write(res.stdout)
            # logs.close()
            with open('./Logs/SSHlogcat.log', 'w',encoding="UTF-8") as f:
                f.write(res.stdout)
            # print(res.stdout if res.stdout else res.stderr, end='')

    async def stop_logcat(self):
         async with asyncssh.connect(self.ip, known_hosts='known_hosts', username='root', password=None) as conn:
            await conn.run('killall -9 logcat', check=False)
            # logs = open('SSHlogcat.log', 'a')
            # logs.write(res.stdout)
            # logs.close()

    def run(self,name):

        if "start" == name:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(self.start_logcat())
            loop.run_until_complete(asyncio.wait([task]))
            # asyncio.get_event_loop().run_until_complete(start_logcat())
        else:
            # asyncio.get_event_loop().run_until_complete(stop_logcat())
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(self.stop_logcat())
            loop.run_until_complete(asyncio.wait([task]))
            # stop_logcat()

    def capLog(self,times):
        try:
            thread1 = threading.Thread(target=self.run, args=("start",))
            thread2 = threading.Thread(target=self.run, args=("stop",))

            thread1.start()
            print('logcat start')
            time.sleep(times)
            thread2.start()
            print('logcat stop')

            thread1.join()
            thread2.join()

        except Exception as e:
            print("Error: 无法启动线程")
            print(e.args)

if __name__ == '__main__':
    try:
        L = CapLogcat('10.86.79.139')
        L.capLog(5)
        mytxtfilter = ReFilter()
        code = mytxtfilter.getAirplayCode('./Logs/SSHlogcat.log')
        print(code)
    except Exception as e:
        print(e.args)
    # try:
    #     asyncio.get_event_loop().run_until_complete(start_logcat())
    #     # run_client()
    # except(OSError, asyncssh.Error) as exc:
    #     # asyncssh.Error.args
    #     sys.exit("SSH connection failed" + str(exc))