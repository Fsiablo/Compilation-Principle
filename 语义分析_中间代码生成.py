from 递归下降_语法分析 import getToken,get_tree,parser,generate_tree
from networkx.drawing.nx_pydot import read_dot
import pandas as pd
import numpy as np
ind=-1
place=0
mid_code=[]
def getNextToken(all=0):
    global ind
    ind += 1
    try:
        if all:
            return type_value_token[ind]
        return type_value_token[ind][1]
    except:
        if all:
            return ('#','#','#')
        return '#'
def back():
    global ind
    ind-=1
def build_sign_table():
    global type_value_token
    const_table = []
    var_table = {}
    func_table = []
    str_table = []
    continue_table=[]
    break_table=[]
    return_table=[]
    type_value_token = getToken('tmp')
    def append_const():
        item={}
        type_=getNextToken()
        item['in']=len(const_table)+1
        item['type']=type_
        item['name']=getNextToken()
        getNextToken()
        item['value']=getNextToken()
        const_table.append(item)
        while getNextToken()==',':
            item={}
            item['in'] = len(const_table)+1
            item['type'] = type_
            item['name'] = getNextToken()
            getNextToken()
            item['value'] = getNextToken()
            const_table.append(item)
    def append_var():
        item = {}
        type_ = getNextToken()
        item['block']=now_block()
        item['name'] = getNextToken()
        item['type'] = type_
        token=getNextToken()
        if token==',' or token==';':
            item['value']=None
            var_table[item['name']]=var_table.get(item['name'], [])
            var_table[item['name']].append(item)
            while token!=';':
                item = {}
                item['block'] = now_block()
                item['name'] = getNextToken()
                item['type'] = type_
                item['value'] = None
                var_table[item['name']] = var_table.get(item['name'], [])
                var_table[item['name']].append(item)
                token=getNextToken()
        else:
            item['value']=getNextToken()
            var_table[item['name']] = var_table.get(item['name'], [])
            var_table[item['name']].append(item)
            while getNextToken()==',':
                item = {}
                item['block'] = now_block()
                item['name'] = getNextToken()
                item['type'] = type_
                getNextToken()
                item['value'] = getNextToken()
                var_table[item['name']] = var_table.get(item['name'], [])
                var_table[item['name']].append(item)
    def append_func():
        item = {}
        type_ = getNextToken()
        item['in']=len(func_table)+1
        item['name'] = getNextToken()
        item['type'] = type_
        item['args']=[]
        getNextToken()
        token=getNextToken()
        while token!=')':
            item['args'].append(token)
            getNextToken()
            token=getNextToken()
            if token==',':
                token=getNextToken()
        func_table.append(item)
    def now_block():
        return '/'.join(blocks)
    token=getNextToken(1)
    block=0
    blocks=[]
    blocks.append(str(block))
    while token[0]!='#':
        if token[1]=='{':
            block+=1
            blocks.append(str(block))
        if token[1]=='}':
            blocks.pop()
        if token[1] == 'const':
            append_const()
        if token[1] in ['int','float','char','void']:
            getNextToken()
            token_ = getNextToken()
            back()
            back()
            back()
            if token_=='(':
                append_func()
            else:
                append_var()
        if token[0]=='STR':
            str_table.append(token[1])
        if token[1]=='continue':
            continue_table.append({'block':now_block()})
        if token[1]=='break':
            break_table.append({'block':now_block()})
        if token[1]=='return':
            return_table.append({'block':now_block()})
        token=getNextToken(1)
    return {'var_table':var_table,
            "func_table":func_table,
            'str_table':str_table,
            "continue_table":continue_table,
            "break_table":break_table,
            "return_table":return_table}
class node(object):
    def __init__(self,name,in_,type,value,place,parameters,para,returntype,silbings):
        self.name=name
        self.in_=in_
        self.type=type
        self.value=value
        self.place=place
        self.parameters=parameters
        self.para=para
        self.returntype=returntype
        self.silbings=silbings
    def __str__(self):
        return f"name:{self.name},in_:{self.in_},type:{self.type}," \
               f"value:{self.value},place:{self.place},parameters:{self.parameters}," \
               f"para:{self.para},returntype:{self.returntype},edges:{self.silbings}\n"
class per_mid_code(object):
    def __init__(self,p1,p2,p3,p4):
        self.p1=p1
        self.p2=p2
        self.p3=p3
        self.p4=p4
    def __str__(self):
        return f'({self.p1},{self.p2},{self.p3},{self.p4})'
def gencode(a='',b='',c='',d=''):
    global mid_code
    mid_code.append(per_mid_code(a,b,c,d))
    return len(mid_code)-1
def showcode():
    for i in mid_code:
        print(i)
def insertVartable(id):
    pass
def insertFunction(id):
    pass
def newtemp():
    global place
    place+=1
    return f'temp{place}'
def generate_mid():
    def Exp(root,reverse=None):
        if root.name=='赋值表达式':
            id=nodes[nodes[root.silbings[0]].silbings[0]]
            e=nodes[root.silbings[2]]
            Exp(e)
            gencode('=',e.place,'',id.name)
        elif root.name=='表达式':
            aexp=nodes[root.silbings[0]]
            Exp(aexp)
            root.place=aexp.place
        elif root.name=='算术表达式':
            e=nodes[root.silbings[0]]
            Exp(e)
            root.place=e.place
        elif root.name in ['E','E_']:
            if len(root.silbings)==1:
                t=nodes[root.silbings[0]]
                Exp(t)
                if reverse:
                    tmp = newtemp()
                    gencode('@', t.place, '', tmp)
                    t.place = tmp
                root.place=t.place
            else:
                t=nodes[root.silbings[0]]
                opt=nodes[root.silbings[1]]
                e_=nodes[root.silbings[2]]
                Exp(t)
                if opt.name=='-':
                    Exp(e_,True)
                else:
                    Exp(e_)
                root.place = newtemp()
                if reverse:
                    tmp = newtemp()
                    gencode('@', t.place, '', tmp)
                    t.place = tmp
                gencode('+', t.place, e_.place, root.place)

        elif root.name in ['T','T_']:
            if len(root.silbings)==1:
                f=nodes[root.silbings[0]]
                Exp(f)
                if reverse:
                    tmp = newtemp()
                    gencode('/', '1', f.place, tmp)
                    f.place = tmp
                root.place=f.place
            else:
                f = nodes[root.silbings[0]]
                opt = nodes[root.silbings[1]]
                t_ = nodes[root.silbings[2]]
                Exp(f)
                if opt.name == '/':
                    Exp(t_, True)
                else:
                    Exp(t_)
                root.place = newtemp()
                if reverse:
                    tmp=newtemp()
                    gencode('/','1',f.place,tmp)
                    f.place=tmp
                gencode('*', f.place, t_.place, root.place)
        elif root.name=='F':
            if len(root.silbings)==1:
                root.place=nodes[root.silbings[0]].name
            elif len(root.silbings)==2:
                root.place=newtemp()
                f=nodes[root.silbings[1]]
                Exp(f)
                gencode('@',f.place,'',root.place)
            else:
                f = nodes[root.silbings[1]]
                Exp(f)
                root.place=f.place

    def Var_ann(root):
        if root.name=='变量声明':
            VarType=nodes[root.silbings[0]]
            ids = nodes[root.silbings[1]]
            Var_ann(VarType)
            ids.in_=VarType.type
            Var_ann(ids)
        elif root.name=='变量类型':
            root.type=nodes[root.silbings[0]].name
        elif root.name=='变量声明表':
            temp=nodes[root.silbings[1]]
            if temp.name==';':
                sids= nodes[root.silbings[0]]
                sids.in_=root.in_
                Var_ann(sids)
            else:
                sids = nodes[root.silbings[0]]
                ids=nodes[nodes[root.silbings[1]].silbings[1]]
                sids.in_=root.in_
                ids.in_=root.in_
                Var_ann(sids)
                Var_ann(ids)
        elif root.name=='单变量声明':
            id=nodes[nodes[root.silbings[0]].silbings[0]]
            insertVartable(id)
            id.type=root.in_
            if len(root.silbings)>1:
                expr=nodes[root.silbings[2]]
                Exp(expr)
                id.value=expr.place
    def Func_ann(root):
        if root.name=='函数声明':
            ft=nodes[root.silbings[0]]
            id=nodes[nodes[root.silbings[1]].silbings[0]]
            ffpl=nodes[root.silbings[3]]

            ft.type=ft.name
            Func_ann(ffpl)

            insertFunction(id)
            id.returntype=ft.type
            id.parameters=ffpl.parameters
            id.para=ffpl.para
        elif root.name=='函数声明形参列表':
            root.parameters=0
            root.para=[]
            for i in root.silbings:
                if nodes[i].name!=',':
                    nodes[i].type=nodes[i].name
                    root.para.append(nodes[i].name)
                    root.parameters+=1
            root.para=','.join(root.para)
    def dfs(root:node):
        if root.name=='变量声明':
            Var_ann(root)
            return
        if root.name=='函数声明':
            Func_ann(root)
            return
        if root.name=='赋值表达式':
            Exp(root)
            return
        if root.silbings!=None:
            for i in root.silbings:
                dfs(nodes[i])
    gencode('main')
    dfs(nodes[1])
    gencode('sys')
if __name__=='__main__':
    build_sign_table()
    val_node,pre_node=generate_tree('test0.2.txt')
    edges={}
    for (i,j) in pre_node.items():
        if j==None:
            continue
        edges[j]=edges.get(j,[])
        edges[j].append(i)
    nodes={}
    for i in val_node.keys():
        nodes[i]=node(val_node[i],None,None,None,None,None,None,None,edges.get(i,None))
    generate_mid()
    showcode()
    # for i in nodes.keys():
    #     print(nodes[i])