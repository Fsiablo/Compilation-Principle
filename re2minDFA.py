from graphviz import Digraph
import numpy as np
from collections import deque
class nfa_edge(object):
    num=0
    def __init__(self):
        self.value='#'
        self.ind=nfa_edge.num
        self.v=None
        self.epsCls=set()
        nfa_edge.num+=1
class nfa_node(object):
    def __init__(self,pre,next):
        self.pre=pre
        self.next=next
def re2nfa(re):
    global nfa_edges
    re=list(re)
    a_z_list=[chr(i) for i in range(ord("a"),ord("z")+1)]
    def init(re):
        i=0
        while i<len(re)-1:
            if (re[i] in a_z_list or re[i] in ['+','*',')']) and (re[i+1] in a_z_list or re[i+1]=='('):
                re.insert(i+1,'&')
            i+=1
        return ''.join(re)
    def in2post(re):
        opt = {
            '*': 3, '+': 3,
            '&': 2,
            '|': 1,
            '(': 0
        }
        postfix=[]
        stk=[]
        for i in re:
            if i in a_z_list:
                postfix.append(i)
            elif len(stk)==0:
                stk.append(i)
            elif i=='(':
                stk.append(i)
                continue
            elif i==')':
                while (stk[-1] != '('):
                    postfix.append(stk.pop())
                stk.pop()
            elif len(stk) > 0 and opt[i] > opt[stk[-1]]:
                stk.append(i)
            else:
                while (len(stk) > 0 and opt[i] <= opt[stk[-1]]):
                    postfix.append(stk.pop())
                stk.append(i)
        while (len(stk) != 0):
            postfix.append(stk.pop())
        return ''.join(postfix)
    def link(a,b,w):
        a.value=w
        a.v=b.ind
    def link_eps(a,b):
        a.epsCls.add(b.ind)
    def post2nfa(post):
        stk=[]
        cls=set()
        nfa_edges=[]
        for i in post:
            if i in a_z_list:
                a=nfa_edge()
                b=nfa_edge()
                n=nfa_node(a,b)
                nfa_edges.append(a)
                nfa_edges.append(b)

                link(n.pre,n.next,i)
                cls.add(i)
                stk.append(n)
            elif i=='+':
                a = nfa_edge()
                b = nfa_edge()
                n = nfa_node(a, b)
                nfa_edges.append(a)
                nfa_edges.append(b)

                t=stk.pop()
                link_eps(t.next, n.pre)
                link_eps(t.next, n.next)
                link_eps(n.pre, t.pre)
                stk.append(n)
            elif i == '*':
                a = nfa_edge()
                b = nfa_edge()
                n = nfa_node(a, b)
                nfa_edges.append(a)
                nfa_edges.append(b)

                n1 = stk.pop()
                link_eps(n1.next, n.pre)
                link_eps(n1.next, n.next)
                link_eps(n.pre, n1.pre)
                link_eps(n.pre, n.next)
                stk.append(n)
            elif i == '&':
                n = nfa_node(None, None)
                n1 = stk.pop()
                n2 = stk.pop()
                link_eps(n2.next, n1.pre)
                n.pre = n2.pre
                n.next = n1.next
                stk.append(n)
            elif i == '|':
                a = nfa_edge()
                b = nfa_edge()
                n = nfa_node(a, b)
                nfa_edges.append(a)
                nfa_edges.append(b)

                n1 = stk.pop()
                n2 = stk.pop()
                link_eps(n.pre, n1.pre)
                link_eps(n.pre, n2.pre)
                link_eps(n1.next, n.next)
                link_eps(n2.next, n.next)
                stk.append(n)
        nfa = stk.pop()
        return nfa,cls,nfa_edges
    re=init(re)
    postfix=in2post(re)
    nfa,cls,nfa_edges=post2nfa(postfix)
    return nfa,nfa_edges,cls
def plot_nfa(nfa,nfa_edges,cls):
    d=Digraph('nfa',graph_attr={'rankdir':'LR'},format='png')
    for i in range(len(nfa_edges)):
        if i == nfa.pre.ind:
            d.node(str(i), color='orange')
        if i == nfa.next.ind:
            d.node(str(i), color='red')
    for i in range(len(nfa_edges)):
        if len(nfa_edges[i].epsCls)!=0:
            for j in nfa_edges[i].epsCls:
                d.edge(str(nfa_edges[i].ind),str(j),label='ε')
        if nfa_edges[i].value in cls:
            d.edge(str(nfa_edges[i].ind), str(nfa_edges[i].v), label=nfa_edges[i].value)
    d.view(filename='nfa.png')

class dfa_edge:
    ind = 0

    def __init__(self):
        self.is_end = False
        self.ind = dfa_edge.ind
        self.cls = set()
        self.Edges = []
        dfa_edge.ind += 1


class dfa_node:
    def __init__(self):
        self.startState = 0  # 开始状态为0
        self.endStates = set()
        self.terminator = set()
        self.trans = np.array([[-1 for j in range(26)] for i in range(128)])
def cloure(s):
    global nfa_edges
    eps_stk = []
    s_list = list(s)
    for item in s_list:
        eps_stk.append(item)
    while (len(eps_stk) > 0):
        temp = eps_stk.pop()
        for item in list(nfa_edges[temp].epsCls):
            if item not in s:
                s.add(item)
                eps_stk.append(item)
    return s


def move(s, ch):
    temp = set()
    for item in s:
        if nfa_edges[item].value == ch:
            temp.add(nfa_edges[item].v)
    temp = cloure(temp)
    return temp


def is_end(n, s):
    for item in s:
        if n.next.ind == item:
            return True
    return False



def plot_dfa(dfa,dfanum):
    d = Digraph('dfa', graph_attr={'rankdir': 'LR'}, format='png')
    for i in range(dfanum):
        if i == dfa.startState:
            d.node(name=str(i), color='orange')
        elif dfa_edges[i].is_end == True:
            d.node(name=str(i), color='red')
        elif i == dfa.startState and dfa_edges[i].is_end == True:
            d.node(name=str(i), color='purple')
        else:
            d.node(name=str(i))
    for i in range(dfanum):
        for edge in dfa_edges[i].Edges:
            d.edge(str(dfa_edges[i].ind), str(edge[1]), label=str(edge[0]))
    d.view(filename='dfa.png')
def nfa2dfa(nfa, exp):
    global dfa_edges
    dfa_edges=[dfa_edge() for i in range(128)]
    dfanum = 0
    d = dfa_node()
    q = deque()
    exp = list(exp)
    exp.sort()
    stateSet = set()
    for ch in exp:
        if ch >= 'a' and ch <= 'z':
            d.terminator.add(ch)

    tempSet = set()
    tempSet.add(nfa.pre.ind)
    dfa_edges[0].cls = cloure(tempSet)  # 得到初态的ε闭包
    dfa_edges[0].is_end = is_end(nfa, dfa_edges[0].cls)
    dfanum += 1

    q.append(d.startState)

    while len(q) > 0:
        num = q.popleft()
        dt = list(d.terminator)
        dt.sort()
        for ch in dt:
            temp = move(dfa_edges[num].cls, ch)  # 对每个终止符号进行move运算
            if len(temp) > 0 and tuple(temp) not in stateSet:  # 如果当前闭包未出现过，则进栈
                stateSet.add(tuple(temp))
                dfa_edges[dfanum].cls = temp
                dfa_edges[num].Edges.append([ch, dfanum])
                d.trans[num][ord(ch) - ord('a')] = dfanum
                dfa_edges[dfanum].is_end = is_end(nfa, dfa_edges[dfanum].cls)
                q.append(dfanum)

                dfanum += 1
            else:
                for i in range(dfanum):
                    if temp == dfa_edges[i].cls:
                        dfa_edges[num].Edges.append([ch, i])
                        d.trans[num][ord(ch) - ord('a')] = i
                        break
    for item in dfa_edges:
        if item.is_end == True:
            d.endStates.add(item)
    return d, dfanum, len(dt)

class stateSet:
    def __init__(self):
        self.ind = -1  # 能转换到的状态集标号
        self.s = set()  # 该状态集中的dfa状态号



def plot_minDFA(mindfa,numstate):
    d = Digraph('mindfa', graph_attr={'rankdir': 'LR'}, format='png')
    for i in range(numstate):
        if i == mindfa.startState:
            d.node(name=str(i), color='orange')
        elif min_dfa_edges[i].is_end == True:
            d.node(name=str(i), color='red')
        elif i == mindfa.startState and min_dfa_edges[i].is_end == True:
            d.node(name=str(i), color='purple')
        else:
            d.node(name=str(i))
    for i in range(numstate):
        for edge in min_dfa_edges[i].Edges:
            d.edge(str(min_dfa_edges[i].ind - 128), str(edge[1]), label=str(edge[0]))
    d.view(filename='mindfa.png')
def minDFA(dfa, dfanum):
    global min_dfa_edges
    min_dfa_edges=[dfa_edge() for i in range(128)]
    s = [set() for i in range(128)]
    minDFA = dfa_node()
    minDFA.terminator = dfa.terminator

    # 下面将DFA状态分为终态和非终态
    endFlag = 1  # 判断是否DFA状态全为终态，若为1则是，为0则否
    for i in range(dfanum):
        if dfa_edges[i].is_end == True:
            s[0].add(dfa_edges[i].ind)
        else:
            endFlag = 0
            s[1].add(dfa_edges[i].ind)
            numstateSet = 2  # 初始的状态数
    if endFlag == 1:
        numstateSet = 1  # DFA状态全为终态，所以只有一个状态集合

    cutFlag = True  # 上一次是否产生新的划分的标志
    while (cutFlag):  # 若上一次产生新的划分则继续循环
        cutCount = 0
        for statenum in range(numstateSet):
            for ch in dfa.terminator:  # 对每个终结符做move
                setNum = 0  # 当前划分的个数
                temp = [stateSet() for i in range(20)]  # 初始化缓冲区用于存储当前move操作的划分集合

                for item in s[statenum]:
                    epFlag = True  # 判断该集合是否存在没有此终结符对应的边
                    for edge in dfa_edges[item].Edges:
                        if edge[0] == ch:
                            epFlag = False
                            transNum = -1
                            for i in range(numstateSet):
                                s_temp = list(s[i])
                                for j in range(len(s_temp)):
                                    if edge[1] == s_temp[j]:
                                        transNum = i
                                        break
                            curSetNum = 0
                            while temp[curSetNum].ind != transNum and curSetNum < setNum:
                                curSetNum += 1
                            if curSetNum == setNum:
                                temp[setNum].ind = transNum
                                temp[setNum].s.add(item)
                                setNum += 1
                            else:
                                temp[curSetNum].s.add(item)
                    if epFlag == True:
                        curSetNum = 0
                        while temp[curSetNum].ind != -1 and curSetNum < setNum:
                            curSetNum += 1
                        if curSetNum == setNum:
                            temp[setNum].ind = -1
                            temp[setNum].s.add(item)
                            setNum += 1
                        else:
                            temp[curSetNum].s.add(item)

                if setNum > 1:
                    cutCount += 1
                    for i in range(setNum):
                        differ = False
                        for item in temp[i].s:
                            if item in s[i]:
                                s[i].remove(item)
                                s[numstateSet].add(item)
                                differ = True
                        if differ == True:
                            numstateSet += 1

        if cutCount == 0:
            cutFlag = False
            # 遍历每个划分好的状态集
    for i in range(numstateSet):
        for item in s[i]:
            if item == dfa.startState:  # 如果当前状态为初态，则最小化DFA状态也为初态
                minDFA.startState = i
            endStates = [state.ind for state in dfa.endStates]
            if item in endStates:  # 如果当前状态为终态，则最小化DFA状态也为终态
                min_dfa_edges[i].is_end = True
                minDFA.endStates.add(i)

            for edge in dfa_edges[item].Edges:
                for t in range(numstateSet):
                    if edge[1] in s[t]:
                        haveEdge = False
                        for m_edge in min_dfa_edges[i].Edges:
                            if m_edge[0] == edge[0] and m_edge[1] == edge[1]:
                                haveEdge = True
                        if haveEdge == False:
                            if [edge[0], t] not in min_dfa_edges[i].Edges:
                                min_dfa_edges[i].Edges.append([edge[0], t])
                            minDFA.trans[i][ord(edge[0]) - ord('a')] = t
    return minDFA, numstateSet


def dfa2code(minDFA, numstateSet):
    state = minDFA.startState
    code = ''
    code += 'int startState = ' + str(state) + ';\n'
    code += 'int state = startState;\n'
    code += 'bool quit = false;\n'

    code += 'while(quit == false)\n{\n'
    code += '    char ch = cin.get();\n'
    code += '    switch(state)\n    {\n'
    for i in range(numstateSet):
        code += '    case ' + str(min_dfa_edges[i].ind - 128) + ':\n'
        if min_dfa_edges[i].is_end == True:
            code += '        switch(ch)\n        {\n'
            for edge in min_dfa_edges[i].Edges:
                code += "            case '" + str(edge[0]) + "':\n"
                code += '                state = ' + str(edge[1]) + ';\n'
                code += '                break;\n'
            code += '            default:\n'
            code += '                quit = true;\n                cout<<"SUCCESS"<<endl;\n                break;\n'
            code += '        }\n'
            code += '        break;\n'

        else:
            code += '        switch(ch)\n        {\n'
            for edge in min_dfa_edges[i].Edges:
                code += "            case '" + str(edge[0]) + "':\n"
                code += '                state = ' + str(edge[1]) + ';\n'
                code += '                break;\n'
            code += '            default:\n'
            code += '                cout<<"ERROR"<<endl;\n'
            code += '                quit = true;\n'
            code += '                break;\n'
            code += '        }\n'
            code += '        break;\n'

    code += '    }\n'
    code += '}\n'
    return code
def get_nfa(re):
    global nfa_edges,dfa_edges,min_dfa_edges
    nfa_edge.num = 0
    dfa_edge.ind = 0
    nfa_edges=[]
    dfa_edges=[]
    min_dfa_edges=[]
    nfa, nfa_edges, cls=re2nfa(re)
    plot_nfa(nfa, nfa_edges, cls)
def get_dfa(re):
    global nfa_edges, dfa_edges, min_dfa_edges
    nfa_edge.num=0
    dfa_edge.ind=0
    nfa_edges = []
    dfa_edges = []
    min_dfa_edges = []
    nfa, nfa_edges, cls = re2nfa(re)
    dfa, dfanum, _ = nfa2dfa(nfa, cls)
    plot_dfa(dfa,dfanum)
def get_min_dfa(re):
    global nfa_edges, dfa_edges, min_dfa_edges
    nfa_edge.num = 0
    dfa_edge.ind = 0
    nfa_edges = []
    dfa_edges = []
    min_dfa_edges = []
    nfa, nfa_edges, cls = re2nfa(re)
    dfa, dfanum, _ = nfa2dfa(nfa, cls)
    mindfa,numstate=minDFA(dfa,dfanum)
    plot_minDFA(mindfa,numstate)
def get_code(re):
    global nfa_edges, dfa_edges, min_dfa_edges
    nfa_edge.num = 0
    dfa_edge.ind = 0
    nfa_edges = []
    dfa_edges = []
    min_dfa_edges = []
    nfa, nfa_edges, cls = re2nfa(re)
    dfa, dfanum, _ = nfa2dfa(nfa, cls)
    mindfa, numstate = minDFA(dfa, dfanum)
    return dfa2code(mindfa, numstate)
# nfa,postfix=re2nfa('(a|b)*abb')
# dfa,dfanum,_=nfa2dfa(nfa,postfix)
# mindfa,numstate=minDFA(dfa,dfanum)
# code=dfa2code(mindfa, numstate)
# print(code)