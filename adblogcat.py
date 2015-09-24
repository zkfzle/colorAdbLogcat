#!/usr/bin/env python
import subprocess
import re
import ctypes,sys,os

#set text feature and colors
SIMPLESTR_TYPE = 0
DATETIME_TYPE = 1
APPNAME_TYPE = 2
MSGLEVEL_TYPE = 3

regStr = r"([\d]{2}-[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2}\.[\d]{3})\s(([V|D|I|E])\/[^(]*)([\s\S]+)$"
pattern = re.compile(regStr)
#red green
color = [0x08,0x0a,0x70 ,0x0c]
msgColor = [0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f]
levelColor = [0xa0|0x00, 0x90|0x00, 0xc0|0x00]
STD_OUTPUT_HANDLE = -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

#process adb logcat ouput
def output_color_text(typeId, msg,handle=std_out_handle):
    if(typeId == SIMPLESTR_TYPE):
        resetColor()
        print msg,
    elif(typeId == DATETIME_TYPE):
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, 0x08)
        print "%s" % msg,
    elif(typeId == APPNAME_TYPE):
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, msgColor[len(msg) % len(msgColor)])
        print "%28.32s" % msg,
    elif(typeId == MSGLEVEL_TYPE):
        if(msg == 'I' or msg == 'V'):
            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, levelColor[0])
        elif(msg == 'D'):
            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, levelColor[1])
        else:
            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, levelColor[2])
        print msg,
    else:
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color[3])
        print msg,

#reset color output to normal cmd theme
def resetColor():    
    ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, 0x0e | 0x0a | 0x09)

def outputInColor(msg):    
    match = pattern.match(msg)
    if(match):
        output_color_text(DATETIME_TYPE,match.group(1))
        output_color_text(APPNAME_TYPE,match.group(2))
        output_color_text(MSGLEVEL_TYPE,match.group(3))
        output_color_text(SIMPLESTR_TYPE,match.group(4))
    else:
        output_color_text(SIMPLESTR_TYPE,msg)
def setCmdWH(width,height):
    os.system('mode con cols=%s lines=%s' % (width,height))
if __name__ == '__main__':
    try:
        #set input commond, default is 'adb logcat -v time'
        command = 'adb logcat -v time'
        if len(sys.argv) == 2 and sys.argv[1] == '--help':
            print "Usage: python adblogcat.py + [LOGCAT PARAMETERS]"
            sys.exit(0)
        elif len(sys.argv) >= 2:
            command = "adb logcat -v time " + ' '.join(sys.argv[1:])
            print command
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE)
        setCmdWH(200,300)
        for line in iter(pipe.stdout.readline, ''):
            outputInColor(line.strip())
            print ''
    except KeyboardInterrupt:
        resetColor()
        os.system('cls')
        setCmdWH(80,25)