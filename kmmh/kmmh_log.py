#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os, sys

def log_control(src_folder):
    upper_folder = src_folder.split('kmmh/')[0]+'kmmh'
    print(upper_folder)
    with open(upper_folder+'/log.txt','r+') as f:
        if src_folder not in f.read():
            data = src_folder +'\n'
            f.write(data)
        else:
            pass
    f.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Warning')
        sys.exit()
    src_folder = sys.argv[1]
    try:
        log_control(src_folder)
    except:
        print('Wrong with log control')
