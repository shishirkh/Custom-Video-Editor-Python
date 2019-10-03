import vlc
import ctypes
from ctypes.util import find_library
import sys
import speech_recognition as sr
import cv2
import math
from tkinter import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
import os
import pathlib
from threading import Thread, Event
import time
import platform



#Global Variables.....
ButtonNames = []
tempbtn = []
start_time = 0.0
end_time = 0.0
filename_store= ''
dicname = ''
directory_store=''
saved_dir = ''
filename = ''
v1 = ''
v2 = ''


def maximum(a,b):
    if(a>=b):
        return a
    else:
        return b
    
def mspf(mp):
    return mp.get_fps()



class ttkTimer(Thread):
    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0
    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += self.tick
            self.callback()
    def stop(self):
        self.stopFlag.set()
    def get(self):
        return self.iters


    
global index
index=0
class Player(Tk.Frame):
    def __init__(self, parent, title=None):
        global index,v2,v1
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        if title == None:
            title = "Intelligent Video Editor"
        self.parent.title(title)
        menubar = Tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        fileMenu = Tk.Menu(menubar)
        fileMenu.add_command(label="Open", underline=0, command=self.OnOpen)
        fileMenu.add_command(label="Exit", underline=1, command=_quit)
        menubar.add_cascade(label="File", menu=fileMenu)
        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)
        ctrlpanel = ttk.Frame(self.parent)
        
        ctrlpanel1 = ttk.Frame(self.parent)
        ctrlpanel3 = ttk.Frame(self.parent)
        ctrlpanel2 = ttk.Frame(self.parent)
        ctrlpanel2.pack(side=BOTTOM,anchor=E)



       
        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = Tk.Scale(ctrlpanel, variable=self.scale_var, width=1.5,command=self.scale_sel,from_=0, to=1000, orient=Tk.HORIZONTAL, length=830)
        self.timeslider.pack(side=Tk.TOP, fill=Tk.X,expand=1)
        self.timeslider_last_update = time.time()


        style = ttk.Style()
        style.configure("TButton", foreground="white", background="blue")

        

        
        pause  = Tk.Button(ctrlpanel, text=" Pause ", command=self.OnPause,bg="blue",fg="white",relief=RAISED,bd=5)
        screenshot  = Tk.Button(ctrlpanel, text=" Screenshot ",bg="blue",fg="white",bd=5)
        plus5  = Tk.Button(ctrlpanel, text="   >>  ", command=self.plus5,bg="blue",fg="white",bd=5)
        minus5  = Tk.Button(ctrlpanel, text="  <<  ", command=self.minus5,bg="blue",fg="white",bd=5)
        play   = Tk.Button(ctrlpanel, text=" Play ", command=self.OnPlay,bg="blue",fg="white",bd=5)
        stop   = Tk.Button(ctrlpanel, text=" Stop ", command=self.OnStop,bg="blue",fg="white",bd=5)
        Clip_Start = Tk.Button(ctrlpanel, text="Start Clip", command=self.OnClipStart, bg="green",fg="white",bd=5)
        Clip_Clear = Tk.Button(ctrlpanel3, text=" Clear", command=self.OnClipClear,bg="blue",fg="white",bd=5)
        edit = Tk.Button(ctrlpanel, text="/",width=4,bd=5)
        extraButton = Tk.Button(ctrlpanel, text="|||",command=self.task,width=4,bd=5 )
        extraButton1 = Tk.Button(ctrlpanel, text="---",command=self.ScreenShot,width=3,bg="blue",fg="white",bd=5 )


        v1 = StringVar()
        v2 = StringVar()

        S_Time = Entry(ctrlpanel3, textvariable=v1, width=9)
        S_Time.pack(side=LEFT,anchor=W)
        
        Clip_Clear.pack(side=LEFT, padx=(24,0))
        
       
        max_lbl = Label(ctrlpanel3, text="Max").pack(side=LEFT,padx=(80,0))





        self.volume_var = Tk.IntVar()
        self.volslider = Tk.Scale(ctrlpanel3, variable=self.volume_var,width=1.5, command=self.volume_sel,from_=0, to=100, orient=Tk.HORIZONTAL, length=200)
        self.volslider.pack(side=LEFT)


        min_lbl = Label(ctrlpanel3, text="Min").pack(side=LEFT)
        
        












    
        global filename_store,directory_store,fullname
        
        textBox=Text(ctrlpanel3, height=1, width=10)
        textBox.pack(side=LEFT,padx=(110,10))
        
        text_buttonAdd = Button(ctrlpanel3, height=1, width=9, bg="blue",fg="white",bd=5, text="Add button", command=lambda:[Tk.Button(ctrlpanel2,   text=textBox.get("1.0","end-1c"),height=1, width=9, bg="blue",fg="white",bd=5, 
                command=lambda dummy=textBox.get("1.0","end-1c"): self.click_event(dummy)).pack(side="right",anchor=E),os.mkdir(directory_store+'/'+textBox.get("1.0","end-1c")),ButtonNames.append(textBox.get("1.0","end-1c"))])
        text_buttonAdd.pack(side="left",padx=(0,0))
        

        Clip_Start.pack(side=Tk.LEFT,padx=(0,5))
       
        minus5.pack(side=Tk.LEFT,padx=(0,5))
        play.pack(side=Tk.LEFT,padx=(0,0))
        plus5.pack(side=Tk.LEFT,padx=(5,0))
        pause.pack(side=Tk.LEFT,padx=(5,0))
        stop.pack(side=Tk.LEFT,padx=(5,0))
        screenshot.pack(side=Tk.LEFT,padx=(5,0))
        edit.pack(side=Tk.LEFT,padx=(5,0))
        extraButton1.pack(side=Tk.LEFT,padx=(5,0))
        extraButton.pack(side=Tk.LEFT,padx=(5,0))
        
        edit.pack(side=Tk.LEFT,padx=(5,0))
       
       
        
        ctrlpanel2.pack(side=Tk.BOTTOM)
        ctrlpanel3.pack(side=Tk.BOTTOM)
        ctrlpanel.pack(side=Tk.BOTTOM)
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()
        self.parent.update()
    
    def click_event(self,text):
        global start_time,end_time,v1,ButtonNames
        print('click event')
        print(ButtonNames)
        global filename_store,directory_store
        tyme = self.player.get_time()
        tyme=tyme*0.001
        
        if start_time > 0 and start_time < tyme:
                ffmpeg_extract_subclip(filename_store,start_time,tyme,targetname=directory_store+"/"+text+"/"+str(start_time)+"_"+str(tyme)+".mp4")
                print('video saved')
        else:
                ffmpeg_extract_subclip(filename_store,tyme-3,tyme+5, targetname=directory_store+"/"+text+"/"+str(tyme-3)+"_"+str(tyme+5)+".mp4")
                print('video saved')

        start_time = 0.0
        v1.set(start_time)


    def SaveClip(self,end):
        global start_time,end_time,v1
        print('Saving Video of 8 seconds....')
        global filename_store,directory_store
        
       
        if start_time > 0 and start_time < end:
                ffmpeg_extract_subclip(filename_store,start_time,end,targetname=directory_store+"/"+'output_'+str(start_time)+"_"+str(end)+".mp4")
                print('video saved')
        else:
                ffmpeg_extract_subclip(filename_store,end-3,end+5, targetname=directory_store+"/"+'output_'+str(end-3)+"_"+str(end+5)+".mp4")
                print('video saved')

        start_time = 0.0
        v1.set(start_time)



    def ClipButtonValue(self,end,text):
        global start_time,end_time,v1,dicname
        print('click event')
        global filename_store,directory_store
        
        
        if start_time > 0 and start_time < end:
                ffmpeg_extract_subclip(filename_store,start_time,end,targetname=dicname+"/"+str(start_time)+"_"+str(end)+".mp4")
                print('video saved')
        else:
                ffmpeg_extract_subclip(filename_store,end-3,end+5, targetname=dicname+"/"+str(end-3)+"_"+str(end+5)+".mp4")
                print('video saved')

        start_time = 0.0
        v1.set(start_time)





        
    def set_string(self,text,number):
        global string1,string2,string3,string4,string5
        if(number==1):
            string1=text
        elif(number==2):
            string2=text
        elif(number==3):
            string3=text
        elif(number==4):
            string4=text
        elif(number==5):
            string5=text

    def OnExit(self, evt):
        self.Close()


    def task(self):
        global ButtonNames,dicname,directory_store,tempbtn
        end = 0.0
        for i in ButtonNames:
           src = i.lower()
           if src not in tempbtn:
              tempbtn.append(src)

        r = sr.Recognizer()
        m = sr.Microphone()

        tyme = self.player.get_time()
        end=tyme*0.001
        print("Say something!")
        with m as source:
             
             audio = r.listen(source)
             print(end)
             print("Got it! Now to recognize it...")
             try:
                 value = r.recognize_google(audio)     
                 print("You said: {}".format(value))
                 
                 if value == 'play' or value == 'Play' :
                     self.OnPlay()
   
                 if value == 'clear' or value == 'Clear' :
                     self.OnClipClear()

                 if value == 'start' or value == 'Start' :
                     self.OnClipStart()

                 
                 if value == 'pause' or value == 'Pause' or value == 'Freeze' or value == 'freeze' or value == 'hold' or value == 'Hold' :
                     self.OnPause()

                 if value == 'stop' or value == 'Stop' or value == 'end' or value == 'terminate' :
                     self.OnStop()

                 if value == 'back' or value == 'Back' or value == 'backward' or value == 'Backward' :
                     self.minus5()


                 if value == 'forward' or value == 'Forward' or value == 'skip' or value == 'Skip' :
                     self.plus5()
 
                 if value == 'open' or value == 'Open' :
                     self.OnOpen()

   
                 if value == 'start' or value == 'Start' or value == 'Start clip' or value == 'start clip' :
                     self.OnClipStart()


                 if value == 'clear' or value == 'Clear' :
                     self.OnClipClear()

                 if value == 'clip' or value == 'clip' or value == 'cut' or value == 'Cut' or value == 'save' or value == 'Save' :
                     self.SaveClip(end)
        
                 if value in tempbtn : 
                    for i in range(0,len(tempbtn)) : 
         
                        if value.lower() == tempbtn[i]:
                           dicname = directory_store+'/'+ButtonNames[i]
                           print(dicname,'     button name is  :',ButtonNames[i])
                           self.ClipButtonValue(end,i)
                        else:
                           print('No Such Button Found....')


             except sr.UnknownValueError:
                 print("Oops Unable to Recognize the words......")

        


    def OnClipStart(self):
        global start_time,v1,v2
        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        start_time = dbl
        v1.set(dbl)
        v2.set(' ')
        
       

    def OnClipClear(self):
        global start_time,v1
        start_time = 0.0
        v1.set(start_time)


    def ScreenShot(self):
       global fullname,directory_store
       print(directory_store)
       cap = cv2.VideoCapture(fullname)
       fps = cap.get(cv2.CAP_PROP_FPS)
       print('fps:',fps)
       tyme = self.player.get_time()
       tyme = tyme*0.001
       frame_no = int(fps*tyme)
       print(frame_no)
       cap.set(1,frame_no);
       ret, frame = cap.read()
       cv2.imwrite(directory_store+'/'+str(tyme)+'.jpeg',frame)
 
        
        

    def OnOpen(self):
        global filename_store,directory_store,fullname,filename
        self.OnStop()
        p = pathlib.Path(os.path.expanduser("~"))
        fullname =  askopenfilename(initialdir = p, title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
        print(fullname)
        if os.path.isfile(fullname):
            dirname  = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            print(dirname)
            print(filename)
            filename_store=str(dirname)+'/'+str(filename)
            directory_store=str(dirname)
            print(filename)
            self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)
            if platform.system() == 'Windows':
                self.player.set_hwnd(self.GetHandle())
            else:
                self.player.set_xwindow(self.GetHandle())
            self.OnPlay()
            self.volslider.set(self.player.audio_get_volume())

    def OnPlay(self):
        if not self.player.get_media():
            self.OnOpen()
        else:
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")

    def GetHandle(self):
        return self.videopanel.winfo_id()

    def plus5(self):
        global index
        print('index : ' ,index)
        self.player.pause()
        new_time = 25*5 * mspf(self.player)
        self.player.set_time(math.ceil(self.player.get_time()+new_time))
        print('no of frames : ',mspf(self.player))
        self.player.play()
        
    def minus5(self):
        self.player.pause()
        new_time = 25*6 * mspf(self.player)
        self.player.set_time(maximum(0,math.floor(self.player.get_time()-new_time)))
        print('no of frames : ',mspf(self.player))
        self.player.play()
        

    def OnPause(self):
        global filename_store
        print(filename_store)
        self.player.pause()

    def OnStop(self):
        self.player.stop()
        self.timeslider.set(0+100)

    def OnTimer(self):
        #global filename_store
        global index
    
        if self.player == None:
            return
        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        print('player length : ',dbl)
        #print(filename_store)
        
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        if time.time() > (self.timeslider_last_update + 2.0):
            self.timeslider.set(dbl)

    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval))


    def volume_sel(self, evt):
        if self.player == None:
            return
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def OnToggleVolume(self, evt):
        is_mute = self.player.audio_get_mute()
        self.player.audio_set_mute(not is_mute)
        self.volume_var.set(self.player.audio_get_volume())

    def OnSetVolume(self):
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def errorDialog(self, errormessage):
        Tk.tkMessageBox.showerror(self, 'Error', errormessage)

def Tk_get_root():
    if not hasattr(Tk_get_root, "root"):
        Tk_get_root.root= Tk.Tk()
    return Tk_get_root.root

def _quit():
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()    
    root.destroy()
    os._exit(1)

if __name__ == "__main__":
    root = Tk_get_root()
    root.geometry("830x500")
    root.protocol("WM_DELETE_WINDOW", _quit)
    player = Player(root, title="tkinter vlc")
    root.mainloop()
