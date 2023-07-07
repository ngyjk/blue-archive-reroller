import logging
logger = logging.getLogger('ProjectBA')
import time
import random
import ocrfuncs
import subprocess
import os
from win32gui import GetForegroundWindow, SetForegroundWindow
from contextlib import contextmanager

@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)

class dvc():

    def __init__(self, server, port, host = "127.0.0.1"):

        self.server = server
        self.port = port
        self.host = host
        
        logger.debug(f'dvc {port} initalized.')
    
    def connect(self):

        self.server.remote_connect(self.host, self.port)
        devices = self.server.devices()
        for d in devices:
            if d.serial == f'{str(self.host)}:{str(self.port)}':
                self.device = d
        self.ocr = ocrfuncs._ocr(temp_path = f'Images')

        logger.debug(f'dvc {self.device.serial} connected.')

    def disconnect(self):
        self.server.remote_disconnect(self.host, self.port)
        logger.debug(f'dvc {self.port} disconnected.')
    
    def tap(self, x = 1150, y = 500, times = 1, d = 0.5, 
            x_rnd = 25, y_rnd = 25, d_rnd = 0.5):
        # Defaults to 1 tap in center of screen if no values passed
        for t in range(times):
            nx = round(x + random.random() * (x_rnd * 2 - 1), 2)
            ny = round(y + random.random() * (y_rnd * 2 - 1), 2)
            nd = round(d + random.random() * d_rnd, 2)
            self.device.shell(f'input tap {nx} {ny}')
            logger.debug(f'Tap done at {nx} | {ny} - going to sleep for {nd}s.')
            time.sleep(nd)

    def swipe(self, x1, y1, x2, y2, duration, repeat = 1):
        for i in range(repeat):
            self.device.shell(f'input swipe {x1} {y1} {x2} {y2} {duration}')
            logger.debug(f'Swipe done from {x1} | {y1} to {x2},{y2}.')
            time.sleep(1)

    def type(self, text):
        text = text.replace(' ', '%')
        self.device.shell(f'input text {text}')
        logger.debug(f'Text {text} keyed in.')

    def get_screenshot(self, path = ''):
        if path == '':
            path = f'Users\Keane\Files\Scripts\Project BA\Images\screen{self.port}.png'
        image = self.device.screencap()
        with open(path, 'wb') as f:
            f.write(image)
        logger.debug(f'Screenshot Taken to {path}.')
        return path
    
    def ocr_texts(self, boxes = False):
        if boxes:
            return ocrfuncs.get_all_text_with_positions(self.get_screenshot())
        return ocrfuncs.get_all_text(self.get_screenshot())

    def open_and_hide(self):
        instance_name = self.get_instance_name()
        w = GetForegroundWindow()
        logger.debug(f'Current ForegroundWindow saved.')
        with cwd('Program Files\BlueStacks_nxt'):
            self.p = subprocess.Popen(f"HD-Player.exe --instance {instance_name}")
            logger.debug(f'Opened Instance {instance_name}.')
        try:
            while GetForegroundWindow() == w:
                time.sleep(0.1)
                if GetForegroundWindow() != w:
                    logger.info('Switching Back to Foreground Window')
                    SetForegroundWindow(w)
        except:
            logger.warning('Foregroundcheck error', exc_info = True)
    
    def kill_process(self):
        logger.debug(f'{self.port} killed.')
        self.p.kill()
                
    def open_ba_app(self):
        if self.device.shell('pidof com.nexon.bluearchive') == '':
            self.device.shell('monkey -p com.nexon.bluearchive -c android.intent.category.LAUNCHER 1')
            logger.info('Opening BA App.')
        else:
            logger.info('BA already open.')

    def get_instance_name(self):

        dct = {
            5645: 'Nougat64_9',
            5695: 'Nougat64_14',
            5795: 'Nougat64_24',
            5805: 'Nougat64_25',
            5815: 'Nougat64_26',
            5825: 'Nougat64_27',
        }
        
        return dct[self.port]
