#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
from rosservicehandler import ROSServiceHandler

def stop_mongodb():
    cmd = ['mongo', '--eval', 'db.getSiblingDB("admin").shutdownServer()']
    subprocess.Popen(cmd)

if __name__ == "__main__":
    print("VERSION 00.03")
    try:
        ros_service_handler = ROSServiceHandler()
        ros_service_handler.spin()

    except Exception as e:
        print("An error occurred: {}".format(e))
    finally:
        print("Finalizing...")
        stop_mongodb()
    