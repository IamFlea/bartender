# -*- coding: utf-8 -*-
import win32api
import win32con
import win32gui
import win32ui

import numpy as np


class ScreenShooter(object):
    """ ScreenShooter class """
    def __init__(self):
        """ Creates handlers used for a screenshoting. """
        super(ScreenShooter, self).__init__()
        # Grab the Desktop handler.
        hdesktop = win32gui.GetDesktopWindow()
        # Determine the size of all monitors in pixels
        self.width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        self.height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        self.left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        self.top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        # Create a device context
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        self.img_dc = win32ui.CreateDCFromHandle(desktop_dc)
        # Create a memory based device context
        self.mem_dc = self.img_dc.CreateCompatibleDC()
        # Create a bitmap object
        self.screenshot = win32ui.CreateBitmap()
        self.screenshot.CreateCompatibleBitmap(self.img_dc, self.width, self.height)
        self.mem_dc.SelectObject(self.screenshot)
        # Garbage collector might delete this function.
        self.freeScreenshot = win32gui.DeleteObject

    def shot(self):
        """ Takes a screenshot.

        Returns:
            The RGBX screenshot in numpy array.
        """
        # Copy the screen into our memory device context
        self.mem_dc.BitBlt((0, 0), (self.width, self.height), self.img_dc, (self.left, self.top),win32con.SRCCOPY)
        # Save it into numpy array
        info = self.screenshot.GetInfo()
        img = np.fromstring(self.screenshot.GetBitmapBits(True), dtype=np.uint8) #
        img.shape = (info['bmHeight'], info['bmWidth'], 4) # four colours. RGBX
        return img

    def __del__(self):
        """ Free our objects """
        self.mem_dc.DeleteDC()		
        self.freeScreenshot(self.screenshot.GetHandle())


if __name__ == '__main__':
    screen = ScreenShooter()
    a = screen.shot()
    print(a)
    b = screen.shot()
    print(b)

