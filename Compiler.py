from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkPDFViewer import tkPDFViewer as pdf
from 词法分析 import RecognizeCode
from 递归下降_语法分析 import generate_tree
from 中间代码生成 import get_table,get_midcode
from 目标代码生成 import get_target_code
from re2minDFA import get_nfa,get_dfa,get_min_dfa,get_code
import os
class ChildFrame(Frame):


   def __init__(self,root,title_color,title='正则表达式转DFA',color='#f0f0f0'):
      self.root=root
      super().__init__(root,bg=color)#底层
      self.title=title
      self.tc=title_color
      self.titlebar=Frame(self,bg=self.tc)#标题栏
      Label(self.titlebar,text=self.title,bg=self.tc,fg='white').place(x=5,y=5)
      self.conbar=Frame(self.titlebar,bg=self.tc)
      self.conbar.pack(side='right')#工具栏
      self.desb=Button(self.conbar,text='×',font=('宋体',15),bg=self.tc,fg='white',activeforeground='white',activebackground='red',relief='flat',command=self.destroy)
      self.desb.pack(side='right')#关闭按钮
      self.desb.bind('<Enter>',lambda event:self.desb.configure(background='red'))
      self.desb.bind('<Leave>',lambda event:self.desb.configure(background=self.tc))#当鼠标划过时有红色样式
      self.expandb=Button(self.conbar,text='□',font=('宋体',15),fg='white',bg=self.tc,activeforeground='white',activebackground=self.tc,relief='flat',command=self.expandwin)
      self.expandb.pack(side='right')#最大化
      self.titlebar.pack(fill='x')
      self.titlebar.bind('<Button-1>',self._startmove,add='+')#移动
      self.titlebar.bind('<B1-Motion>',self._movewin,add='+')

   def show(self,x,y,width,height):#显示窗口
      self.wd=width
      self.hi=height
      self.oralx=x
      self.oraly=y
      self.place(x=x,y=y,width=width,height=height)

   def destroy(self):#销毁窗口
      self.place_forget()

   def _startmove(self,event):#记录开始移动的坐标
      self.startx=event.x
      self.starty=event.y

   def _movewin(self,event):#移动窗口
      self.place(x=self.winfo_x()+(event.x-self.startx),y=self.winfo_y()+(event.y-self.starty))

   def lockwin(self):#禁止窗口移动
      self.titlebar.unbind('<B1-Motion>')

   def activewin(self):#允许窗口移动
      self.titlebar.bind('<B1-Motion>',self._movewin,add='+')

   def backexpandwin(self):#恢复窗口大小
      self.expandb['text']='□'
      self.expandb['command']=self.expandwin
      self.place(x=self.oralx,y=self.oraly,width=self.wd,height=self.hi)
      self.activewin()

   def expandwin(self):#最大化窗口
      #记录窗口的起始位置
      self.oralx=self.winfo_x()
      self.oraly=self.winfo_y()
      self.root.update()
      w=self.root.winfo_width()
      h=self.root.winfo_height()
      self.place(x=0,y=0,width=w,height=h)
      self.expandb['text']='◪'
      self.expandb['command']=self.backexpandwin
      self.lockwin()#最大化不能移动

   def noexpand(self):#是否支持放大
      self.expandb.pack_forget()
   def haveexpand(self):#支持放大
      self.expandb.pack()
root = Tk()
root.resizable(width=False, height=False)
root.geometry('1000x600')
root.title('编译原理')
filename = ''
textPad = Text(root,undo = True,wrap='none')
textPad.tag_add('font','1.0','end')
textPad.tag_config('font',font=(15))

scroll = Scrollbar(textPad)
scroll_bottom = Scrollbar(textPad,orient=HORIZONTAL)
textPad.config(yscrollcommand = scroll.set)
textPad.config(xscrollcommand=scroll_bottom.set)
scroll.config(command = textPad.yview)
scroll_bottom.config(command=textPad.xview)
textPad.place(x=20, y=20,width=400, height=550)
scroll.pack(side=RIGHT,fill=Y)
scroll_bottom.pack(side=BOTTOM,fill=X)


mid_results=Text(root,undo=True,state=DISABLED,bg='#D3D3D3',font=(40))
mid_results.place(x=450,y=20,width=500,height=350)

scroll = Scrollbar(mid_results)
scroll_bottom = Scrollbar(mid_results,orient=HORIZONTAL)
mid_results.config(yscrollcommand = scroll.set)
mid_results.config(xscrollcommand=scroll_bottom.set)
scroll.config(command = mid_results.yview)
scroll_bottom.config(command=mid_results.xview)
scroll.pack(side=RIGHT,fill=Y)
scroll_bottom.pack(side=BOTTOM,fill=X)

results=Text(root,undo=True,state=DISABLED,bg='#D3D3D3')
results.place(x=450,y=390,width=500,height=180)

scroll = Scrollbar(results)
scroll_bottom = Scrollbar(results,orient=HORIZONTAL)
results.config(yscrollcommand = scroll.set)
results.config(xscrollcommand=scroll_bottom.set)
scroll.config(command = results.yview)
scroll_bottom.config(command=results.xview)
scroll.pack(side=RIGHT,fill=Y)
scroll_bottom.pack(side=BOTTOM,fill=X)
menubar = Menu(root)

def new():
    global filename,textPad,root
    root.title('*新文件')
    filename = None
    textPad.delete(1.0,END)


def myopen():
    global filename
    default_dir = r''
    filename = askopenfilename(title = u'选择文件',defaultextension = '.txt',initialdir = (os.path.expanduser(default_dir)))
    if filename == '':
        filename=None
    else:
        root.title("编译器--"+os.path.basename(filename))
        textPad.delete(1.0,END)
        f = open(filename,'r',encoding='utf-8')
        textPad.insert(1.0,f.read())
        f.close()


def save(arg):
    global filename
    try:
        f = open(filename,'w',encoding='utf-8')
        #获取文本中的字符串
        message = textPad.get(1.0,END)
        f.write(message)
        f.close()
    except:
        saveas(arg)

def saveas(arg):
    global filename
    #打开保存文件的文件对话框
    f = asksaveasfilename(initialfile = '未命名.txt',defaultextension = '.txt') #打开文件对话框并获取文件路径保存
    filename = f
    fh = open(f,'w',encoding='utf-8')
    message = textPad.get(1.0,END)
    fh.write(message)
    fh.close()
    root.title("编译器--"+os.path.basename(filename))

def undo():
    global textPad
    textPad.event_generate("<<Undo>>")

def redo():
    global textPad
    textPad.event_generate("<<Redo>>")

def cut():
    global textPad
    textPad.event_generate("<<Cut>>")

def copy():
    global textPad
    textPad.event_generate("<<Copy>>")

def paste():
    global textPad
    textPad.event_generate("<<Paste>>")

def find(self):
    global root
    t = Toplevel(root)
    t.title('查找')
    t.geometry("260x60+200+250")
    t.transient(root) #告诉root新建t窗口是暂时等待
    Label(t,text = '查找').grid(row = 0,column = 0,sticky = W)
    v = StringVar()
    e = Entry(t,width = 20,textvariable = v)
    e.grid(row =0,column = 1,padx = 2,pady = 2,sticky = 'we')
    e.focus_set() #焦点聚集在此输入框
    c = IntVar()
    Checkbutton(t,text = '不区分大小写',variable = c).grid(row = 1,column = 1,sticky = E)
    Button(t,text = '查找所有',command = lambda :search(v.get(),c.get(),textPad,t,e)).grid(row = 0,column = 2,sticky = 'e'+'w',padx = 2,pady =2)
    def close_search():
        textPad.tag_remove('match','1.0',END)
        t.destroy()
    t.protocol('WM_DELETE_WINDOW',close_search)

def search(needle,cssnstv,textPad,t,e):
    textPad.tag_remove('match','1.0',END)
    count = 0
    if needle:
        pos = '1.0'
        while True:
            pos = textPad.search(needle,pos,nocase = cssnstv,stopindex=END)
            if not pos:
                break
            lastpos = pos +str(len(needle))
            textPad.tag_add('match',pos,lastpos)
            count +=1
            pos = lastpos
        textPad.tag_config('match',foreground = 'yellow',background = 'green')
        e.focus_set()
        t.title(str(count)+'个匹配')

#此函数用于鼠标右键显示菜单的
def popup(event):
    global editmenu
    editmenu.tk_popup(event.x_root,event.y_root)



def select_all():
    global textPad
    #tag_add()：为指定的文本添加Tags
    #tag_config()：可以设置Tags的样式
    textPad.tag_add('sel','1.0','end')

def help():
    pass
def others():
    pass

#创建Top文件菜单及其子菜单并绑定函数
filemenu = Menu(menubar,tearoff=False)
filemenu.add_command(label = '新建',accelerator = 'Ctrl + N',command=new)
filemenu.add_command(label = '打开',accelerator = 'Ctrl + O',command = myopen)
filemenu.add_command(label = '保存',accelerator = 'Ctrl + S',command = save)
filemenu.add_command(label = '另存为',accelerator = 'Ctrl + Shift + S',command = saveas)
menubar.add_cascade(label = '文件',menu = filemenu)
#创建Top编辑菜单及其子菜单并绑定函数,同类之间用下分割线
editmenu = Menu(menubar,tearoff=False)
editmenu.add_command(label = '撤销',accelerator = 'Ctrl + Z',command = undo)
editmenu.add_command(label = '重做',accelerator = 'Ctrl + Y',command = redo)
editmenu.add_separator()
editmenu.add_command(label = '剪切',accelerator = 'Ctrl + X',command = cut)
editmenu.add_command(label = '复制',accelerator = 'Ctrl + C',command = copy)
editmenu.add_command(label = '粘贴',accelerator = 'Ctrl + V',command = paste)
editmenu.add_separator()
editmenu.add_command(label = '查找',accelerator = 'Ctrl + F',command = find)
editmenu.add_command(label = '全选',accelerator = 'Ctrl + A',command = select_all)
menubar.add_cascade(label = '编辑',menu = editmenu)

#创建Top文件菜单及其子菜单并绑定函数
pdf_=''
def word():
    save('')
    global pdf_
    if pdf_!='':
        pdf_.destroy()
    code=textPad.get('0.0', END)
    result,error,r,c=RecognizeCode(code)
    mid_results.config(state=NORMAL)
    mid_results.delete(0.0,END)
    mid_results.insert(INSERT,result)
    mid_results.update()
    mid_results.config(state=DISABLED)

    results.config(state=NORMAL)
    results.delete(0.0, END)
    if error=='':
        results.insert(INSERT, '词法分析结束')
    else:
        results.insert(INSERT, error)
    results.update()
    results.config(state=DISABLED)
def Syntax():
    save('')
    global pdf_
    error=''
    try:
        generate_tree(filename)

        v1=pdf.ShowPdf()
        pdf_ = v1.pdf_view(root,
                         pdf_location=f"{filename}.gv.pdf")
        pdf_.place(x=450,y=20,width=500,height=350)
    except:
        error='语法有错，请检查代码！'
    results.config(state=NORMAL)
    results.delete(0.0, END)
    if error=='':
        results.insert(INSERT, '语法分析结束')
    else:
        results.insert(INSERT, error)
    results.update()
    results.config(state=DISABLED)
def Semant():
    save('')
    global pdf_
    if pdf_ != '':
        pdf_.destroy()
    table_str=get_table(filename)
    mid_results.config(state=NORMAL)
    mid_results.delete(0.0, END)
    mid_results.insert(INSERT, table_str)
    mid_results.update()
    mid_results.config(state=DISABLED)

    results.config(state=NORMAL)
    results.delete(0.0, END)
    results.insert(INSERT, '语义分析结束')
    results.update()
    results.config(state=DISABLED)
def Midcode():
    save('')
    global pdf_
    if pdf_ != '':
        pdf_.destroy()
    midcode = get_midcode(filename)

    mid_results.config(state=NORMAL)
    mid_results.delete(0.0, END)
    mid_results.insert(INSERT, midcode)
    mid_results.update()
    mid_results.config(state=DISABLED)

    results.config(state=NORMAL)
    results.delete(0.0, END)
    results.insert(INSERT, '中间代码生成结束')
    results.update()
    results.config(state=DISABLED)
def Target():
    save('')
    global pdf_
    if pdf_ != '':
        pdf_.destroy()
    target_code = get_target_code(filename)+'\n'
    mid_results.config(state=NORMAL)
    mid_results.delete(0.0, END)
    mid_results.insert(INSERT, target_code)
    mid_results.update()
    mid_results.config(state=DISABLED)

    results.config(state=NORMAL)
    results.delete(0.0, END)
    results.insert(INSERT, '目标代码生成结束')
    results.update()
    results.config(state=DISABLED)

def re2dfa():
    def nfa():
        re=re_in.get(0.0,END)[:-1]
        get_nfa(re)
    def dfa():
        re=re_in.get(0.0,END)[:-1]
        get_dfa(re)
    def mindfa():
        re=re_in.get(0.0,END)[:-1]
        get_min_dfa(re)
    def code_():
        re=re_in.get(0.0,END)[:-1]
        textPad.delete(0.0,END)
        textPad.insert(0.0,get_code(re))
    global root
    subwin=ChildFrame(root,'grey')
    subwin.show(x=450,y=20,width=500,height=550)
    re_text=Label(subwin,text='正则表达式:')
    re_text.place(x=0,y=50)
    re_in = Text(subwin, undo=True, wrap='none')
    re_in.tag_add('font', '1.0', 'end')
    re_in.tag_config('font', font=(15))
    re_in.place(x=80,y=50,width=400,height=25)

    re2nfa_bt=Button(subwin,command=nfa,text='正则表达式转NFA')
    re2nfa_bt.place(x=100,y=100,width=300,height=50)
    nfa2dfa_bt = Button(subwin, command=dfa,text='NFA转DFA')
    nfa2dfa_bt.place(x=100, y=175, width=300, height=50)
    dfa2mindfa_bt = Button(subwin, command=mindfa,text='最小化DFA')
    dfa2mindfa_bt.place(x=100, y=250, width=300, height=50)
    dfa2code_bt = Button(subwin, command=code_,text='DFA转词法分析')
    dfa2code_bt.place(x=100, y=325, width=300, height=50)



word_menu = Menu(menubar,tearoff=False)
word_menu.add_command(label = '开始',command=word)
menubar.add_cascade(label = '词法分析',menu = word_menu)

parse_menu = Menu(menubar,tearoff=False)
parse_menu.add_command(label = '开始',command=Syntax)
menubar.add_cascade(label = '语法分析',menu = parse_menu)

meaning_menu = Menu(menubar,tearoff=False)
meaning_menu.add_command(label = '开始',command=Semant)
menubar.add_cascade(label = '语义分析',menu = meaning_menu)

mid_code_menu = Menu(menubar,tearoff=False)
mid_code_menu.add_command(label = '开始',command=Midcode)
menubar.add_cascade(label = '中间代码生成',menu = mid_code_menu)

target_code_menu = Menu(menubar,tearoff=False)
target_code_menu.add_command(label = '开始',command=Target)
menubar.add_cascade(label = '目标代码生成',menu = target_code_menu)

re2dfa_menu = Menu(menubar,tearoff=False)
re2dfa_menu.add_command(label = '开始',command=re2dfa)
menubar.add_cascade(label = '正则表达式转DFA',menu = re2dfa_menu)
#创建Top关于菜单及其子菜单并绑定函数
aboutmenu = Menu(menubar,tearoff=False)
aboutmenu.add_command(label = '帮助',command = help)
aboutmenu.add_command(label = '关于',command = others)
menubar.add_cascade(label = '帮助',menu = aboutmenu)

#将前面的菜单绑定到顶部栏
root.config(menu = menubar)

#热键绑定
textPad.bind("<Control-N>",new)
textPad.bind("<Control-n>",new)
textPad.bind("<Control-O>",myopen)
textPad.bind("<Control-o>",myopen)
textPad.bind("<Control-S>",save)
textPad.bind("<Control-s>",save)
textPad.bind("<Control-A>",select_all)
textPad.bind("<Control-a>",select_all)
textPad.bind("<Control-F>",find)
textPad.bind("<Control-f>",find)

textPad.bind("<Button-3>",popup)
root.mainloop()

