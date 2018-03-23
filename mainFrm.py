import datetime
import tkinter as tk
from tkinter import scrolledtext
import tkinter.messagebox
import threading
import os
import pygame.mixer
playing_music = ''
root = tk.Tk()
start_time = 0
track = []
pause_time = 0
pause_flag = False
close_pause_time = 0
start_volume = 0.6


def refresh(event):
    global list2
    list4 = tk.StringVar(value=music)
    list2 = tk.Listbox(root, width=28, height=16, listvariable=list4)
    list2.grid(row=3, column=0, rowspan=2, columnspan=4)
    list2.bind('<Double-Button-1>', get_music)


def search_music(event):
    global list2
    name = entry.get()
    find_music = []
    for i in music:
        if i.find(name) >= 0:
            find_music.append(i)
    if len(find_music):
        list3 = tk.StringVar(value=find_music)
        list2 = tk.Listbox(root, width=28, height=16, listvariable=list3)
        list2.grid(row=3, column=0, rowspan=2, columnspan=4)
        list2.bind('<Double-Button-1>', get_music)


def prev_music(event):
    global playing_music
    global music
    global pause_flag
    global pause_time
    global close_pause_time
    global track
    if len(track):
        pause_time = 0
        pause_flag = False
        close_pause_time = 0
        i = 0
        for m in music:
            if playing_music == m:
                break
            else:
                i = i + 1
        if i > 0:
            track = []
            play_music(file+'\\'+music[i-1], music[i-1])


def next_music(event):
    global playing_music
    global music
    global pause_flag
    global pause_time
    global close_pause_time
    global track
    if len(track):
        pause_time = 0
        pause_flag = False
        close_pause_time = 0
        i = 0
        for m in music:
            if playing_music == m:
                break
            else:
                i = i + 1
        if i+1 < len(music):
            track = []
            play_music(file + '\\' + music[i+1], music[i+1])
        else:
            print('歌曲已播放完。')


def auto_next_music(next_m):
    global playing_music
    global music
    global pause_flag
    global pause_time
    global close_pause_time
    global track
    if len(track):
        pause_time = 0
        pause_flag = False
        close_pause_time = 0
        i = 0
        for m in music:
            if playing_music == m:
                break
            else:
                i = i + 1
        if i+1 < len(music):
            track = []
            play_music(file + '\\' + music[i+1], music[i+1])
        else:
            play_music(file + '\\' + music[0], music[0])


def pause(event):
    global start_time
    global track
    global pause_time
    global pause_flag
    if len(track):
        if pause_flag:
            pass
        else:
            pause_time = datetime.datetime.now() - start_time
            pause_flag = True
            label5.config(text='播放时间: '+str(pause_time)[0:7])
            track[0].pause()


def close_pause(event):
    global track
    global close_pause_time
    global pause_time
    global pause_flag
    global start_time
    if len(track):
        if pause_flag:
            temp = datetime.datetime.now() - start_time
            close_pause_time = temp - pause_time
            start_time = start_time + close_pause_time
            pause_flag = False
            label5.config(text='播放时间: ' + str(pause_time)[0:7])
            track[0].unpause()


def add_voice(event):
    global track
    global start_volume
    if start_volume <= 1.0:
        start_volume = start_volume + 0.2
        if len(track):
            track[0].set_volume(start_volume)
    else:
        a = tkinter.messagebox.showinfo('提示', '已最大音量')


def min_voice(event):
    global track
    global start_volume
    if start_volume >= 0.2:
        start_volume = start_volume - 0.2
        if len(track):
            track[0].set_volume(start_volume)
    else:
        a = tkinter.messagebox.showinfo('提示', '已最小音量')


def display_time():
    global start_time
    global track
    global pause_flag
    global pause_time
    global playing_music
    time2 = datetime.datetime.now()
    if time2 != start_time:
        t = time2 - start_time
        if len(track):
            if track[0].get_busy():
                pass
            else:
                t = '00:00:00'
                auto_next_music(playing_music)
        if pause_flag:
            label5.config(text='播放时间: '+str(pause_time)[0:7])
        else:
            label5.config(text='播放时间: ' + str(t)[0:7])
    label5.after(200, display_time)


def get_music(event):
    name = list2.get(list2.curselection())
    music_name = file+'\\'+name
    t1 = threading.Thread(target=play_music, args=(music_name, name, ))
    t1.start()


def play_music(music_file, name):
    global start_time
    global track
    global playing_music
    playing_music = name
    start_time = datetime.datetime.now()
    label3['text'] = name
    n = name.find('.')
    music_lyric = name[0:n]
    get_lyric(music_lyric)
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.6)
    track.append(pygame.mixer.music)
    if len(track):
        display_time()
    return pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)


# 歌词显示
def get_lyric(name):
    scr.delete(0.0, tk.END)
    flag = os.path.exists('lyric\\'+name+'.txt')
    if flag:
        f = open('lyric\\'+name+'.txt', 'r', encoding="utf-8")  # 返回一个文件对象
        line = f.read()  # 调用文件的 readline()方法
        while line:
            scr.insert(tk.INSERT, line + '\n')
            line = f.read()
        f.close()
    else:
        pass


# 获取文件夹下的文件列表
def get_music_list(level, path):
    file_list = []
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(path + '/' + f):
            file_list.append(f)
    return file_list


# 左边栏
img = tk.PhotoImage(file="picture\\background.gif")
imageView = tk.Label(root, image=img, width=200, height=110)
imageView.grid(row=0, column=0, rowspan=2,  columnspan=4)  # columnspan两列合成一列

label4 = tk.Label(root, text="播放列表：")
label4.grid(row=2, column=0,  columnspan=2, sticky=tk.W)

label7 = tk.Button(root, text="列表重置")
label7.grid(row=2, column=2,  columnspan=2, sticky=tk.E)

file = 'music'    # 获取播放列表
music = get_music_list(1, file)
list1 = tk.StringVar(value=music)
list2 = tk.Listbox(root, width=28, height=16, listvariable=list1)
list2.grid(row=3, column=0, rowspan=2, columnspan=4)
list2.bind('<Double-Button-1>', get_music)

btn1 = tk.Button(root, text='上一首')
btn1.grid(row=5, column=0, sticky=tk.E)
btn0 = tk.Button(root, text='暂停')
btn0.grid(row=5, column=1)
btn = tk.Button(root, text='开始')
btn.grid(row=5, column=2, sticky=tk.W)
btn2 = tk.Button(root, text='下一首')
btn2.grid(row=5, column=3, sticky=tk.W)
btn.bind('<Button-1>', close_pause)
btn0.bind('<Button-1>', pause)
btn1.bind('<Button-1>', prev_music)
btn2.bind('<Button-1>', next_music)
label7.bind('<Button-1>', refresh)

# 中间分隔
img1 = tk.PhotoImage(file="picture\\bg.gif")
imageView1 = tk.Label(root, image=img1, width=6, height=460)
imageView1.grid(row=0, column=4, rowspan=6,  columnspan=1)

# 右边栏
search = tk.StringVar()
entry = tk.Entry(root, width=27, textvariable=search)
entry.grid(row=0, column=5)

label6 = tk.Button(root, text=" 搜 索 ")
label6.grid(row=0, column=6, sticky=tk.W)
label6.bind('<Button-1>', search_music)

label1 = tk.Label(root, text="  正  在  播  放:", font='10')
label1.grid(row=1, column=5, sticky=tk.W)

# 显示播放歌曲名组件
label3 = tk.Label(root, text='wait play')
label3.grid(row=1, column=6, sticky=tk.W)

label2 = tk.Label(root, text="  --------------歌词--------------")
label2.grid(row=2, column=5, sticky=tk.W)

label5 = tk.Label(root, text="时间")
label5.grid(row=2, column=6, sticky=tk.W)

scr = scrolledtext.ScrolledText(root, width=50, height=22, wrap=tk.WORD)
scr.grid(row=3, column=5, rowspan=2, columnspan=2)

btn_min = tk.Button(root, text="音量—")
btn_min.grid(row=5, column=5, sticky=tk.E)

btn_add = tk.Button(root, text="音量+")
btn_add.grid(row=5, column=6, sticky=tk.W)

btn_min.bind('<Button-1>', min_voice)
btn_add.bind('<Button-1>', add_voice)

if __name__ == '__main__':
    root.title('MusicPlayer')
    root.geometry('750x568')
    print('播放器启动成功！')
    root.mainloop()