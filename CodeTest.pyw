from tkinter import *
import os,sys,time
import tkinter.filedialog,importlib,glob
import threading
class MyGUI:
    def __init__(self):#初始化窗体对象
        self.root = Tk()
        self.title = self.root.title('POC检测')#设置title
        self.size = self.root.geometry('850x550+400+50')#设置窗体大小，850x550是窗体大小，400+50是初始位置
        self.exchange = self.root.resizable(width=False, height=False)#不允许扩大
        self.root.columnconfigure(0, weight=1)

    #创造幕布
    def CreateFrm(self):
        #定义frame
        self.frmA = Frame(self.root, width=600, height=50)#目标，输入框
        self.frmB = Frame(self.root, width=600, height=440, bg='white')#输出信息
        self.frmC = Frame(self.root, width=600, height=60, bg='white')#功能按钮
        #self.frmD = Frame(self.root, width=250, height=520)#POC
        self.frmE = Frame(self.root, width=250, height=30)#
        #创建帆布
        self.canvas = Canvas(self.root,width=250,height=500,scrollregion=(0,0,550,550)) #创建canvas
        #在帆布上创建frmD
        self.frmD = Frame(self.canvas,width=250,height=500)
        self.canvas.create_window((0,0), window=self.frmD)#create_window
        #表格布局
        self.frmA.grid(row=0, column=0, padx=2, pady=2)
        self.frmB.grid(row=1, column=0, padx=2, pady=2)
        self.frmC.grid(row=2, column=0, padx=2, pady=2)
        self.canvas.grid(row=1, column=1, rowspan=3, padx=2, pady=2)
        self.frmD.grid(row=1, column=1, padx=2, pady=2)
        self.frmE.grid(row=0, column=1, padx=2, pady=2)
        #固定大小
        self.frmA.grid_propagate(0)
        self.frmB.grid_propagate(0)
        self.frmC.grid_propagate(0)
        self.frmD.grid_propagate(0)
        self.frmE.grid_propagate(0)
        self.canvas.grid_propagate(0)

    #创造第一象限
    def CreateFirst(self):
        self.LabA = Label(self.frmA, text='目标')#显示
        self.EntA = Entry(self.frmA, width='60') #接受输入控件

        self.LabA2 = Label(self.frmA, text='端口')#显示
        self.EntA2 = Entry(self.frmA, width='7') #接受输入控件

        self.LabA3 = Label(self.frmA, text='额外')#显示
        self.EntA3 = Entry(self.frmA, width='60') #接受输入控件

        self.ButtonA1 = Button(self.frmA, text='TXT', width =7, command=LoadTXT)
        #表格布局
        self.LabA.grid(row=0,column=0)
        self.EntA.grid(row=0,column=1)

        self.LabA2.grid(row=0,column=2)
        self.EntA2.grid(row=0,column=3)

        self.LabA3.grid(row=1,column=0)
        self.EntA3.grid(row=1,column=1)

        self.ButtonA1.grid(row=1,column=2,padx=4, pady=4)
    #创造第二象限
    def CreateSecond(self):
        self.TexB = Text(self.frmB, font=("Times",10), width=95)
        self.ScrB = Scrollbar(self.frmB)  #滚动条控件
        #表格布局
        self.TexB.grid(row=1,column=0)
        self.ScrB.grid(row=1,column=1, sticky=S + W + E + N)#允许拖动
        self.ScrB.config(command=self.TexB.yview)
        self.TexB.config(yscrollcommand=self.ScrB.set)
    #创造第三象限
    def CreateThird(self):
        self.ButtonC1 = Button(self.frmC, text='验 证', width = 10, command=BugTest)
        self.ButtonC2 = Button(self.frmC, text='加载python', width = 15, command=LoadPython)
        self.ButtonC3 = Button(self.frmC, text='加载第三方环境', width = 15, command=Load)
        self.ButtonC4 = Button(self.frmC, text='当前环境变量', width = 15, command=ShowPython)
        #表格布局
        self.ButtonC1.grid(row=0, column=0)
        self.ButtonC2.grid(row=0, column=1)
        self.ButtonC3.grid(row=0, column=2)
        self.ButtonC4.grid(row=0, column=3)
    #创造第四象限
    def CreateFourth(self):
        self.ButtonE1 = Button(self.frmE, text='加载POC', width =8, command=LoadPoc)
        self.ButtonE2 = Button(self.frmE, text='打开脚本目录', width = 15, command=LoadCMD)
        self.ButtonE1.grid(row=0, column=0)
        self.ButtonE2.grid(row=0, column=1)

        self.vbar = Scrollbar(self.canvas, orient=VERTICAL) #竖直滚动条
        self.vbar.grid(row=1, sticky=S + W + E + N)#允许拖动
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand = self.vbar.set)
        
    #开始循环
    def start(self):
        self.CreateFrm()
        self.CreateFirst()
        self.CreateSecond()
        self.CreateThird()
        self.CreateFourth()


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert(END, str, (self.tag,))
        self.widget.configure(state="disabled")
        self.widget.see(END)

#####环境变量#####
threadLock = threading.Lock()#线程锁
scripts = []#lib下的脚本文件列表
threadList = []#线程列表
var = []#变量列表

row = 1#动态创建button控件
path = ''#python第三方库路径

#脚本路径
curPath = os.path.dirname(os.path.realpath(sys.executable))#当前执行路径
scriptPath = os.getcwd()
libPath = curPath+'/lib'
scriptLib = scriptPath+'/lib'
#追加搜索路径
sys.path.append(libPath)
sys.path.append(curPath)
sys.path.append(scriptPath)
sys.path.append(scriptLib)
#####环境变量#####

#####函数#####
#调用checkbutton按钮
def callCheckbutton(x,i):
    global scripts
    global vuln
    if var[i].get() == 1:
        try:
            vuln = importlib.import_module('.%s'%x,package='script')
            print('[*]%s模块已准备就绪!'%x)
        except Exception as e:
            print('[*]异常对象的内容是:%s'%e)
    else:
        print('[*]%s模块已取消!'%x)

#创建button
def Create(x,i):
    global row
    global var

    threadLock.acquire()
    button = Checkbutton(gui.frmD,text=x,command=lambda:callCheckbutton(x,i),variable=var[i])
    button.grid(row=row,sticky=W)
    print(x+'加载成功!')
    row += 1
    threadLock.release()

#填充线程列表
def CreateThread():
    for i in range(len(scripts)):

        thread = threading.Thread(target=Create,args=(scripts[i],i))

        thread.setDaemon(True)
        threadList.append(thread)

#加载script文件夹下的POC
def LoadPoc():
    global scripts
    global var

    for _ in glob.glob('D:/PythonScript/BugTest/CodeTest/script/*.py'):
        script_name = os.path.basename(_).replace('.py', '')
        scripts.append(script_name)
        m = IntVar()
        var.append(m)
    CreateThread()
    
    for t in threadList:
        t.start()

def LoadCMD():
    global scriptPath
    start_directory = scriptPath +'/script'
    os.startfile(start_directory)

def LoadTXT():
    print('加载外部TXT文件成功!')

#测试按钮功能
def BugTest():
    url = gui.EntA.get().strip('/')
    port = int(gui.EntA2.get()) if gui.EntA2.get() else None
    target = gui.EntA3.get() if gui.EntA3.get() else None

    if url == '':
        print('[*]请输入目标URL!')
        return

    try:
        if port:
            mess = vuln.check(url, port=port)
        elif target:
            mess = vuln.check(url, target=target)
        else:
            mess = vuln.check(url)
    except Exception as e:
        print('[*]异常对象的内容是:%s'%e)

def ShowPython():
    print(str(sys.path))

def Load():
    path = tkinter.filedialog.askdirectory()
    if path:
        sys.path.append(path)
        print('[*]加载成功!')
    else:
        print('[*]请选择路径!')

#加载python第三方库
def LoadPython():
    #userpath = 'C:'+os.path.expandvars('$HOMEPATH')+'/AppData/Roaming/Python/Python37/site-packages'
    path = tkinter.filedialog.askdirectory()
    if path:
        file_path = path+'/lib/site-packages'
        Lib_path = path+'/lib'
        DLll_path = path+'/DLLs'
        #win32Path = path+'/win32'
        #win32lib = path+'/win32/lib'
        #Pythonwin = path+'/Pythonwin'
        sys.path.append(path)
        #sys.path.append(userpath)
        sys.path.append(file_path)#python新安装的模块路径
        sys.path.append(Lib_path)#python自带的模块路径
        sys.path.append(DLll_path)

        #sys.path.append(win32Path)#python新安装的模块路径
        #sys.path.append(win32lib)#python自带的模块路径
        #sys.path.append(Pythonwin)

        print('[*]python依赖加载完毕!')
    else:
        print('[*]请选择路径!')


#退出时执行的函数
#def callbackClose():
    #sys.exit()

#输出字符到txt文本
#def Insert(str):
#    gui.TexB.insert(END, str)
#####函数#####

###主函数###
gui = MyGUI()
gui.start()
str1 = '''[*]请输入正确的网址,比如 [http://www.baidu.com]
[*]若找不到包，需要导入python的第三方库，选择python安装路径即可[如：D:/python]!
[*]请注意有些需要使用域名，有些需要使用IP!
'''

#输出重定向
sys.stdout = TextRedirector(gui.TexB, "stdout")
sys.stderr = TextRedirector(gui.TexB, "stderr")
gui.TexB.insert(INSERT, str1)  #INSERT表示输入光标所在的位置，初始化后的输入光标默认在左上角
#自定义退出函数
#gui.root.protocol("WM_DELETE_WINDOW", callbackClose)
gui.root.mainloop()