# #!usr/bin/env python
# #code=utf-8

# # from tkinter import *
# from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
# from PyQt5.QtCore import Qt
# import wave
# import numpy as np
# import scipy.signal as signal
# import matplotlib.pyplot as plt
# import sys
# import time

# sys.setrecursionlimit(1000000)

# #define the params of wave
# channels = 1
# sampwidth = 2
# framerate = 9600
# file_name = 'sweep.wav'
# frequency_begin = 1
# frequency_end = 100
# #define the time of wave
# time_len = 2

# def Generate_Wav():
# 	#generate the time bar
# 	t = np.arange(0,time_len,1.0/framerate)
# 	#generate the chirp signal from 300 to 3300Hz
# 	# wave_data = signal.chirp(t, frequency_begin, time_len, frequency_end, method = 'linear')*10000
# 	#cast to the type of short
# 	# wave_data = wave_data.astype(np.short)
#     #samples = np.linspace(0, time_len, int(framerate*time_len), endpoint=False)
# 	#open a wav document
#     # wave_data = np.sin(t*3.1415926)
# 	f = wave.open(file_name,"wb")
# 	#set wav params
# 	f.setnchannels(channels)
# 	f.setsampwidth(sampwidth)
# 	f.setframerate(framerate)
# 	#turn the data to string
# 	f.writeframes(t.tostring())
# 	f.close()

def read_wave_data(file_path):  
    #open a wave file, and return a Wave_read object  
    f = wave.open(file_path,"rb")  
    #read the wave's format infomation,and return a tuple  
    params = f.getparams()  
    #get the info  
    nchannels, sampwidth, framerate, nframes = params[:4]  
    #Reads and returns nframes of audio, as a string of bytes.   
    str_data = f.readframes(nframes)  
    #close the stream  
    f.close()  
    #turn the wave's data to array  
    wave_data = np.fromstring(str_data, dtype = np.short)   
    time = np.arange(0, nframes) * (1.0/framerate)  
    return wave_data, time

def Plot_Wav(name = "sweep.wav"):
	wave_data, time = read_wave_data(name)
	plt.plot(time, wave_data)
	plt.grid(True)
	plt.show()

# def main():
#     Generate_Wav()
#     Plot_Wav()
#     # time.sleep(2)
# 	# root = Tk()
# 	# my_button(root, 'Generate a sweep wav', 'Generate', Generate_Wav)
# 	# my_button(root, 'Plot the wav', 'Plot', Plot_Wav)
# 	# root.mainloop()

# if __name__ == "__main__":
# 	main()



import wave
import numpy as np
import struct
import matplotlib.pyplot as plt
import math
#from compiler.ast import flatten
 
#db = 0
print ("math.pow(10, -12/20) : ", math.pow(10, -12/20)) # 0.251188643150958
print ("math.pow(10, -6/20) : ", math.pow(10, -6/20)) #0.5011872336272722
print ("math.pow(10, -3/20) : ", math.pow(10, -3/20)) #0.7079457843841379
print ("math.pow(10, -1/20) : ", math.pow(10, -1/20)) #0.8912509381337456
print ("math.pow(10, 0/20) : ", math.pow(10, 0/20)) #1.0
print ("math.pow(10, 1/20) : ", math.pow(10, 1/20)) #1.1220184543019633
print ('math.pow(10, 3/20) : ', math.pow(10, 3/20)) #1.4125375446227544
print ('math.pow(10, 6/20) : ', math.pow(10, 6/20)) #1.9952623149688795
print ('math.pow(10, 9/20) : ', math.pow(10, 9/20)) #2.8183829312644537
print ('math.pow(10, 12/20) : ', math.pow(10, 12/20)) #3.9810717055349722
# volume x_db
db_v = 0
db = math.pow(10, 0/20)
# sample/every second
framerate = 44100
# channel_num
channel_num = 2
# bytes needed every sample
sample_width = 2
bits_width = sample_width*8
# seconds, long of data
duration = 1
# frequeny of sinewave
sinewav_frequency_l = 15000
sinewav_frequency_r = 15000 
# max value of samples, depends on bits_width
max_val = 2**(bits_width-1) - 1
print ('max_val : ', max_val)
#volume = 32767*db #0x7FFF=32767
volume = max_val*db #2**(bits_width-1) - 1
#多个声道生成波形数据
x = np.linspace(0, duration, num=duration*framerate)
y_l = np.sin(2 * np.pi * sinewav_frequency_l * x) * volume
y_r = np.sin(2 * np.pi * sinewav_frequency_r * x) * volume
# 将多个声道的波形数据转换成数组
y = zip(y_l,y_r)
print("zip y", y)
y = list(y)
print("list y",y)
y = np.array(y,dtype=np.int)
print("array y",y)
y = y.reshape(-1)
print("reshap array y",y)
 
# 最终生成的一维数组
sine_wave = y
# wav file_name
file_name = "sine_"+str(framerate)+"_"+str(channel_num)+"ch_"+str(db_v)+"db_l"+str(sinewav_frequency_l)+"_r"+str(sinewav_frequency_r)+"_"+str(duration)+"s.wav"
print ('file_name: ', file_name)
#open wav file
wf = wave.open(file_name, 'wb')#wf = wave.open("sine.wav", 'wb')
wf.setnchannels(channel_num)
wf.setframerate(framerate)
wf.setsampwidth(sample_width)
for i in sine_wave:
    data = struct.pack('<h', int(i))
    wf.writeframesraw(data)
wf.close()
