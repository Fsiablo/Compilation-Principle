import os
from graphviz import Digraph
import re
Factor_list=['INT','INT_2','INT_8','INT_16','CHAR','STR','ID','FLOAT']
keys_list=['char','int','float','break','const','return','void','continue','do','while','if','else','for','main']
blk=[]
node_num=0
pre_node={}
val_node={}
def create_node(pre,val):
    global node_num
    node_num+=1
    pre_node[node_num]=pre
    val_node[node_num]=val
    return node_num
def alter_node(node,val):
    val_node[node]=val
def getToken(fileName):
    with open('tokens') as f:
        tokens = {i.split()[0]:i.split()[1] for i in f.read().split('\n')}
    param = f"{r'D:/study/pythonProject/编译原理/win_flex_bison-latest/lex.yy.exe'} {fileName}"
    with os.popen(param) as lex:
        msg = lex.buffer.read().decode('utf-8').split('\r\n')[:-1]
    try:
        type=[i.split('@')[-2] for i in msg]
        value=[i.split('@')[-1] for i in msg]
        value_token=[]
        for (i,j) in zip(type,value):
            j=j.replace('\\n','\n')
            j = j.replace('\\t', '\t')
            if j in tokens.keys():
                token=tokens[j]
            else:
                token=tokens[i]
            value_token.append((i,j,token))
    except:
        for i in msg:
            if i[:2]=='错误':
                print(i)
        return
    return value_token
def getNextToken(all=0):
    global ind
    ind += 1
    try:
        if all:
            return type_value_token[ind]
        return type_value_token[ind][0]
    except:
        if all:
            return ('#','#','#')
        return '#'

def back():
    global ind
    ind-=1
def error():
    print('识别时错误:')
    raise 1
def parser():
    node=create_node(None,'Program')
    token=getNextToken(1)[1]
    while token!='main':
        if token=='const':
            CDA(node)
        elif token in ['int','char','float','void']:
            token=getNextToken()
            if token!='ID':
                error()
                return
            token=getNextToken(1)[1]
            if token=='(':
                back()
                back()
                back()
                FDA(node)
            elif token in ['=',',']:
                back()
                back()
                back()
                VDA(node)
            else:
                error()
                return
        else:
            error()
            return
        token=getNextToken(1)[1]
    create_node(node,'main')
    token=getNextToken(1)[1]
    if token!='(':
        error()
        return
    create_node(node,'(')
    token=getNextToken(1)[1]
    if token!=')':
        error()
        return
    create_node(node, ')')
    CSA(node)
    token=getNextToken(1)[1]
    while token in ['int','char','float','void']:
        back()
        FDA(node)
        token=getNextToken()
def Are(pre):#- Factor_list (
    #print(''.join(blk)+'算数表达式识别')
    blk.append('\t')

    def sc_List(pre):
        token = getNextToken(1)[1]
        back()
        if token == ')':
             create_node(pre, ')')
             return
        node = create_node(pre, '函数调用实参列表')
        sc(node)

    def sc(pre):
        node = create_node(pre, '函数调用实参')
        Re(node)
        token = getNextToken(1)[1]
        if token == ',':
            create_node(node, ',')
            sc(node)
        else:
            back()

    def hsdy(pre):
        node = create_node(pre, '函数调用')
        token = getNextToken(1)
        if token[0] != 'ID':
            error()
            return
        create_node(create_node(node,'标识符'),token[1])
        token = getNextToken(1)
        if token[1] != '(':
            error()
            return
        create_node(node, '(')
        sc_List(node)
        token = getNextToken(1)
        if token[1] != ')':
            error()
            return
        create_node(node, ')')

    def E(pre):  # 算术表达式
        node = create_node(pre, 'E')
        T(node)
        E_(node)

    def T(pre):
        node = create_node(pre, 'T')
        F(node)
        T_(node)

    def E_(pre):
        token = getNextToken(1)[1]
        if (token in ['+', '-']):
            create_node(pre, token)
            node = create_node(pre, 'E_')
            T(node)
            E_(node)
        else:
            back()
            return

    def T_(pre):
        token = getNextToken(1)[1]
        if (token in ['/', '*', '%']):
            create_node(pre, token)
            node = create_node(pre, 'T_')
            F(node)
            T_(node)
        else:
            back()
            return

    def F(pre):
        token = getNextToken(1)
        if (token[1] == '-'):
            node = create_node(pre, 'F')
            create_node(node, token[1])
            F(node)
        elif token[1] == '(':
            node = create_node(pre, 'F')
            create_node(node, token[1])
            E(node)
            token = getNextToken(1)[1]
            if token != ')':
                print('括号不匹配')
                return
            create_node(node, token)
        elif token[0] == 'ID':
            token_ = getNextToken(1)
            back()
            if token_[1] == '(':
                node = create_node(pre, 'F')
                back()
                hsdy(node)
            else:
                node = create_node(pre, 'F')
                create_node(node, token[1])
        elif token[0] not in Factor_list:
            error()
        else:
            node = create_node(pre, 'F')
            create_node(node,token[1])
        return

    node = create_node(pre, '算术表达式')
    E(node)


    blk.pop()
    #print(''.join(blk) + '算数表达式识别结束')
def Cre():
    ##关系表达式
    #print(''.join(blk)+'关系表达式识别')
    blk.append('\t')
    def E():
        token=getNextToken(1)[1]
        if token not in ['<','>','<=','>=','!','!=','==']:
            error()
    Are()
    E()
    Are()
    blk.pop()
    #print(''.join(blk)+'关系表达式识别结束')
def Bre():
    #布尔表达式
    #print(''.join(blk)+'布尔表达式识别')
    blk.append('\t')
    def B():
        X()
        B_()
    def B_():
        token=getNextToken(1)[1]
        if token=='||':
            X()
        else:
            back()
            return
    def X():
        Y()
        X_()
    def X_():
        token = getNextToken(1)[1]
        if token == '&&':
            Y()
        else:
            back()
            return
    def Y():
        token=getNextToken(1)[1]
        if token=='!':
            B()
        else:
            back()
            Are()
            Y_()
    def Y_():
        token = getNextToken(1)[1]
        if token in ['<', '>', '<=', '>=', '!', '!=', '==']:
            #print(''.join(blk) + '关系表达式识别')
            blk.append('\t')
            Are()
            blk.pop()
            #print(''.join(blk) + '关系表达式识别结束')
        else:
            back()
            return
    B()
    blk.pop()
    #print(''.join(blk)+'布尔表达式识别结束')
def Fre(pre):#ID
    #赋值表达式
    #print(''.join(blk) + '赋值表达式识别')
    blk.append('\t')
    node=create_node(pre,'赋值表达式')
    token=getNextToken(1)
    if token[0] =='ID':
        create_node(create_node(node,'标识符'),token[1])
        token=getNextToken(1)[1]
        if token=='=':
            create_node(node,token)
            Re(node)
        else:
            error()
    else:
        error()
    blk.pop()
    #print(''.join(blk) + '赋值表达式识别结束')
def bexpr(pre):
    node=create_node(pre,'布尔表达式')
    bterm(node)
    token=getNextToken(1)[1]
    back()
    while token=='||':
        create_node(node, '||')
        bterm(node)
def bterm(pre):
    node=create_node(pre,'bterm')
def Re(pre):
    global ind,node_num
    def Are_(pre):
        def sc_List(pre):
            token = getNextToken(1)[1]
            back()
            if token == ')':
                return
            node=create_node(pre,'函数调用实参列表')
            sc(node)

        def sc(pre):
            node=create_node(pre,'函数调用实参')
            Re(node)
            token = getNextToken(1)[1]
            if token == ',':
                create_node(node,',')
                sc(node)
            else:
                back()
        def hsdy(pre):
            node=create_node(pre,'函数调用')
            token = getNextToken(1)
            if token[0] != 'ID':
                error()
                return
            create_node(create_node(node, '标识符'), token[1])
            token = getNextToken(1)
            if token[1] != '(':
                error()
                return
            create_node(node, '(')
            sc_List(node)
            token = getNextToken(1)
            if token[1] != ')':
                error()
                return
            create_node(node, ')')
        def E(pre):  # 算术表达式
            node=create_node(pre,'E')
            T(node)
            E_(node)
        def T(pre):
            node=create_node(pre,'T')
            F(node)
            T_(node)

        def E_(pre):
            token = getNextToken(1)[1]
            if (token in ['+', '-']):
                create_node(pre,token)
                node = create_node(pre, 'E_')
                T(node)
                E_(node)
            else:
                back()
                return

        def T_(pre):
            token = getNextToken(1)[1]
            if (token in ['/', '*', '%']):
                create_node(pre, token)
                node = create_node(pre, 'T_')
                F(node)
                T_(node)
            else:
                back()
                return

        def F(pre):
            token = getNextToken(1)
            if (token[1] == '-'):
                node=create_node(pre,'F')
                create_node(node,token[1])
                F(node)
            elif token[1] == '(':
                node = create_node(pre, 'F')
                create_node(node, token[1])
                E(node)
                token = getNextToken(1)[1]
                if token != ')':
                    print('括号不匹配')
                    return
                create_node(node, token)
            elif token[0]=='ID':
                token_=getNextToken(1)
                back()
                if token_[1]=='(':
                    node=create_node(pre,'F')
                    back()
                    hsdy(node)
                else:
                    node = create_node(pre, 'F')
                    create_node(node, token[1])
            elif token[0] not in Factor_list:
                error()
            else:
                node = create_node(pre, 'F')
                create_node(node, token[1])
            return
        node=create_node(pre,'算术表达式')
        E(node)
    def B(pre):
        node=create_node(pre,'B')
        X(node)
        B_(node)
    def B_(pre):
        token=getNextToken(1)[1]
        if token=='||':
            node=create_node(pre,'B_')
            create_node(node,'||')
            X(node)
        else:
            back()
            return
    def X(pre):
        node=create_node(pre,'X')
        Y(node)
        X_(node)
    def X_(pre):
        token = getNextToken(1)[1]
        if token == '&&':
            node=create_node(pre,'X_')
            create_node(node,'&&')
            Y(node)
        else:
            back()
            return
    def Y(pre):
        node=create_node(pre,'Y')
        token=getNextToken(1)[1]
        if token=='!':
            create_node(node,token)
            B(node)
        else:
            back()
            Are(node)
            Y_(node)
    def Y_(pre):
        token = getNextToken(1)[1]
        if token in ['<', '>', '<=', '>=', '!', '!=', '==']:
            #print(''.join(blk) + '关系表达式识别')
            blk.append('\t')
            node=create_node(pre,'Y_')
            create_node(node,token)
            Are(node)
            blk.pop()
            #print(''.join(blk) + '关系表达式识别结束')
        else:
            back()
            return
    def E_(pre):
        token=getNextToken(1)
        back()
        if token[1] in ['<', '>', '<=', '>=', '!', '!=', '==']:
            #print(''.join(blk) + '布尔表达式识别')
            blk.append('\t')
            node = create_node(pre, 'E_')
            token=getNextToken(1)[1]
            create_node(node,token)
            Are(node)
            E__(node)
            blk.pop()
            #print(''.join(blk) + '布尔表达式结束')
        elif token[1] in ['&&','||']:
            #print(''.join(blk) + '布尔表达式识别')
            blk.append('\t')
            node = create_node(pre, '布尔表达式')
            X_(node)
            B_(node)
            blk.pop()
            #print(''.join(blk) + '布尔表达式结束')
        else:
            #print(''.join(blk) + '算数表达式识别')
            blk.append('\t')
            # Are_(pre)
            # create_node(pre, token[1])
            blk.pop()
            #print(''.join(blk) + '算数表达式结束')
        return
    def E__(pre):
        token=getNextToken(1)
        back()
        if token[1] in ['&&','||']:
            node=create_node(pre,'E__')
            X_(node)
            B_(node)
        return
    #print(''.join(blk) + '表达式识别')
    blk.append('\t')
    node=create_node(pre,'表达式')
    token=getNextToken(1)
    token2=getNextToken(1)
    back()
    back()
    save_ind=ind
    save_node_num=node_num
    if token[1] in ['(','-'] or (token[0] in Factor_list and token2[1]!='='):
        Are_(node)
        E_(node)
        # token=getNextToken(1)
        # back()
        # if token[1] in ['||','&&']:
        #     ind=save_ind
        #     node_num=save_node_num
        #     bexpr(node)
    elif token[1]=='!':
        #print(''.join(blk) + '布尔表达式识别')
        blk.append('\t')
        node=create_node(pre,'布尔表达式')
        token=getNextToken(1)
        create_node(node,token)
        Y(node)
        X_(node)
        B_(node)
        blk.pop()
        #print(''.join(blk) + '布尔表达式结束')
    elif token[0] in ['ID']:
        Fre(node)
    else:
        error()
    blk.pop()
    #print(''.join(blk) + '表达式识别结束')
def CDA_list(pre):
    #print(''.join(blk) + '常量识别表识别')
    blk.append('\t')
    token=getNextToken(1)
    node=create_node(pre,'常量识别表')
    if token[0]!='ID':
        error()
        return
    create_node(create_node(node,'常量'),token[1])
    token=getNextToken(1)[1]
    if token!='=':
        error()
        return
    create_node(node,'=')
    token=getNextToken(1)
    if token[0] not in Factor_list:
        error()
        return
    create_node(create_node(node, '常量'), token[1])
    token=getNextToken(1)[1]
    if token==';':
        create_node(node, ';')
        return
    elif token==',':
        create_node(node, ',')
        CDA_list(node)
    else:
        error()
        return
    blk.pop()
    #print(''.join(blk) + '常量识别表结束')
def CDA(pre):
    #print(''.join(blk) + '常量识别')
    blk.append('\t')
    token=getNextToken()
    token=getNextToken(1)[1]
    node=create_node(pre,'常量识别')
    if token not in ['int','char','float']:
        error()
        return
    CDA_list(node)
    blk.pop()
    #print(''.join(blk) + '常量识别结束')
def VDA(pre):
    #print(''.join(blk) + '变量声明识别')
    blk.append('\t')
    node=create_node(pre,'变量声明')
    def Sl(pre):
        node=create_node(pre,'变量声明表')
        Ss(node)
        Sl_(node)
    def Sl_(pre):
        token=getNextToken(1)[1]
        if token==';':
            create_node(pre,';')
            return
        elif token==',':
            node=create_node(pre,'变量声明表_')
            create_node(node, ',')
            Sl(node)
        else:
            error()
            back()
            return
    def Ss(pre):
        node=create_node(pre,'单变量声明')
        token=getNextToken(1)
        if token[0]!='ID':
            error()
            back()
            return
        create_node(create_node(node,'变量'),token[1])
        Ss_(node)
    def Ss_(pre):
        token=getNextToken(1)
        if token[1]=='=':
            node=create_node(pre,'=')
            Re(pre)
        else:
            back()
            return
    token=getNextToken(1)
    create_node(create_node(node,'变量类型'),token[1])
    Sl(node)
    blk.pop()
    #print(''.join(blk) + '变量声明结束')
def stc(pre):#语句
    node=create_node(pre,'语句')
    token = getNextToken(1)
    back()
    if token[1]=='{':
        CSA(node)
    elif token[1] == 'const':
        CDA(node)
    elif token[1] in ['int', 'char', 'float']:
        VDA(node)
    elif token[0] == 'ID':
        Exp(node)
    elif token[1] == 'for':
        FOR(node)
    elif token[1] == 'if':
        IF(node)
    elif token[1] == 'while':
        WHILE(node)
    elif token[1] == 'do':
        DOWHILE(node)
    elif token[1] == 'return':
        Return(node)
    else:
        Re(node)
def CSA(pre):
    #print(''.join(blk) +'复合语句识别')
    blk.append('\t')
    node=create_node(pre,'复合语句')

    token=getNextToken(1)[1]
    if token!='{':
        error()
        return
    create_node(node,'{')
    next_=create_node(node,'语句表')
    while True:
        stc(next_)
        token=getNextToken(1)[1]
        if token=='}':
            break
        back()
    create_node(node,'}')
    blk.pop()
    #print(''.join(blk) + '复合语句识别结束')
def FOR(pre):
    #print(''.join(blk) + 'FOR语句识别')
    blk.append('\t')
    node=create_node(pre,'FOR')
    create_node(node,'for')
    token=getNextToken()
    token=getNextToken(1)[1]
    if token!='(':
        error()
        return
    create_node(node, '(')
    Re(node)
    token = getNextToken(1)[1]
    if token != ';':
        error()
        return
    create_node(node, ';')
    Re(node)
    token = getNextToken(1)[1]
    if token != ';':
        error()
        return
    create_node(node, ';')
    Re(node)
    token = getNextToken(1)[1]
    if token != ')':
        error()
        return
    create_node(node, ')')
    loop_stc(node)
    blk.pop()
    #print(''.join(blk) + 'FOR语句识别结束')
def IF(pre):
    #print(''.join(blk) + 'IF语句识别')
    blk.append('\t')
    node=create_node(pre,'IF')
    create_node(node, 'if')
    token=getNextToken()
    token=getNextToken(1)[1]
    if token!='(':
        error()
        return
    create_node(node,token)
    Re(node)
    token=getNextToken(1)[1]
    if token!=')':
        error()
        return
    create_node(node, token)
    stc(node)
    token=getNextToken(1)[1]
    if token=='else':
        create_node(node, token)
        stc(node)
    else:
        back()
    blk.pop()
    #print(''.join(blk) + 'IF语句识别结束')
def loop_if(pre):
    #print(''.join(blk) + '循环用IF语句识别')
    blk.append('\t')
    node=create_node(pre,'循环用IF')
    create_node(node,'if')
    token = getNextToken()
    token = getNextToken(1)[1]
    if token != '(':
        error()
        return
    create_node(node, '(')
    Re(node)
    token = getNextToken(1)[1]
    if token != ')':
        error()
        return
    create_node(node, ')')
    loop_stc(node)
    token = getNextToken(1)[1]
    if token == 'else':
        create_node(node, 'else')
        loop_stc(node)
    else:
        back()
    blk.pop()
    #print(''.join(blk) + '循环用IF语句识别结束')
def Return(pre):
    #print(''.join(blk) + 'Return语句识别')
    blk.append('\t')
    node=create_node(pre,'Return')
    token=getNextToken(1)[1]
    token=getNextToken(1)[1]
    create_node(node,'return')
    if token==';':
        return
    else:
        back()
        Re(node)
        token=getNextToken(1)[1]
        if token!=';':
            error()
    create_node(node, ';')
    blk.pop()
    #print(''.join(blk) + 'Return语句识别结束')
def Break(pre):
    #print(''.join(blk) + 'Break语句识别')
    blk.append('\t')
    node=create_node(pre, 'Break')
    create_node(node, 'break')
    token=getNextToken()
    token=getNextToken(1)[1]
    if token!=';':
        error()
        return
    create_node(node, ';')
    blk.pop()
    #print(''.join(blk) + 'Break语句识别结束')
def Continue(pre):
    #print(''.join(blk) + 'Continue语句识别')
    blk.append('\t')
    node = create_node(pre, 'Continue')
    create_node(node, 'continue')
    token=getNextToken()
    token=getNextToken(1)[1]
    if token!=';':
        error()
        return
    create_node(node, ';')
    blk.pop()
    #print(''.join(blk) + 'Continue语句识别结束')
def loop_exe(pre):
    #print(''.join(blk) + '循环执行语句识别')
    blk.append('\t')
    token=getNextToken(1)[1]
    back()
    node=create_node(pre,'循环执行语句')
    if token=='if':
        loop_if(node)
    elif token=='for':
        FOR(node)
    elif token=='while':
        WHILE(node)
    elif token=='do':
        DOWHILE(node)
    elif token=='return':
        Return(node)
    elif token=='break':
        Break(node)
    elif token=='continue':
        Continue(node)
    else:
        error()
        return
    blk.pop()
    #print(''.join(blk) + '循环执行语句识别结束')
def Ann_stc(pre):
    #print(''.join(blk) + '声明语句识别')
    blk.append('\t')
    token=getNextToken(1)[1]
    back()
    node=create_node(pre,'声明语句')
    if token=='const':
        CDA(node)
    elif token=='void':
        FDA(node)
    else:
        token=getNextToken(1)
        token=getNextToken(1)
        back()
        back()
        if token=='(':
            FDA(node)
        else:
            VDA(node)
    blk.pop()
    #print(''.join(blk) + '声明语句识别结束')
def loop_stc(pre):
    #print(''.join(blk) + '循环语句识别')
    blk.append('\t')
    token=getNextToken(1)
    back()
    node=create_node(pre,'循环语句')
    # print(token)
    # input()
    if token[1] in ['int','float','char','void','const']:
        Ann_stc(node)
    elif token[0]=='ID':
        token = getNextToken(1)[1]
        token=getNextToken(1)[1]
        back()
        back()
        if token=='=':
            fz(node)
        elif token=='(':
            hs(node)
        else:
            error()
            return
    elif token[1] in ['if','for','while','do','return','break','continue']:
        loop_exe(node)
    elif token[1]=='{':
        loop_mutistc(node)
    else:
        error()
        return
    blk.pop()
    #print(''.join(blk) + '循环语句识别结束')
def loop_stc_list(pre):
    #print(''.join(blk) + '循环语句表识别')
    blk.append('\t')
    node=create_node(pre,'循环语句表')
    loop_stc(node)
    token=getNextToken(1)[1]
    back()
    while token!='}' and token!='#':
        # print(token)/
        # input()
        loop_stc_list(node)
        token=getNextToken(1)[1]
        back()
    if token=='#':
        error()
        return
    blk.pop()
    #print(''.join(blk) + '循环语句表识别结束')
def loop_mutistc(pre):
    #print(''.join(blk) + '循环复合语句识别')
    blk.append('\t')
    token=getNextToken(1)[1]
    node=create_node(pre,'循环复合语句')
    if token!='{':
        error()
        return
    create_node(node,'{')
    loop_stc_list(node)
    token = getNextToken(1)[1]
    if token != '}':
        error()
        return
    create_node(node, '}')
    blk.pop()
    #print(''.join(blk) + '循环复合语句识别结束')
def WHILE(pre):
    #print(''.join(blk) + 'WHILE语句识别')
    blk.append('\t')
    node=create_node(pre,'WHILE')
    create_node(node, 'while')
    token=getNextToken()
    token=getNextToken(1)[1]
    if token!='(':
        error()
        return
    create_node(node,'(')
    Re(node)
    token=getNextToken(1)[1]
    if token!=')':
        error()
        return
    create_node(node, ')')
    loop_stc(node)
    blk.pop()
    #print(''.join(blk) + 'WHILE语句识别结束')
def DOWHILE(pre):
    #print(''.join(blk) + 'DO WHILE语句识别')
    blk.append('\t')
    node=create_node(pre,'DO WHILE')
    create_node(node, 'do')
    token=getNextToken()
    loop_mutistc(node)
    token=getNextToken(1)[1]
    if token!='while':
        error()
        return
    create_node(node,'while')
    token = getNextToken(1)[1]
    if token != '(':
        error()
        return
    create_node(node, '(')
    Re(node)
    token = getNextToken(1)[1]
    if token != ')':
        error()
        return
    create_node(node, ')')
    token = getNextToken(1)[1]
    if token != ';':
        error()
        return
    create_node(node, ';')
    blk.pop()
    #print(''.join(blk) + 'DO WHILE语句识别结束')
def fz(pre):#赋值语句
    #print(''.join(blk) + '赋值语句识别')
    blk.append('\t')
    node=create_node(pre,'赋值语句')
    Fre(node)
    token = getNextToken(1)
    if token[1] != ';':
        error()
    create_node(node,';')
    blk.pop()
    #print(''.join(blk) + '赋值语句识别结束')
def hs(pre):
    #print(''.join(blk) + '函数调用识别')
    blk.append('\t')
    node=create_node(pre,'函数调用')

    def sc_List(pre):
        token = getNextToken(1)[1]
        back()
        if token == ')':
            return
        node = create_node(pre, '函数调用实参列表')
        sc(node)

    def sc(pre):
        node = create_node(pre, '函数调用实参')
        Re(node)
        token = getNextToken(1)[1]
        if token == ',':
            create_node(node, ',')
            sc(node)
        else:
            back()

    def hsdy(pre):
        node = create_node(pre, '函数调用')
        token = getNextToken(1)
        if token[0] != 'ID':
            error()
            return
        create_node(create_node(node,'标识符'),token[1])
        token = getNextToken(1)
        if token[1] != '(':
            error()
            return
        create_node(node, '(')
        sc_List(node)
        token = getNextToken(1)
        if token[1] != ')':
            error()
            return
        create_node(node, ')')
    hsdy(node)
    token=getNextToken(1)
    if token[1]!=';':
        error()
    create_node(node,';')
    blk.pop()
    #print(''.join(blk) + '函数调用识别结束')
def Exp(pre):
    node=create_node(pre,'Exp')
    token=getNextToken(1)
    token=getNextToken(1)[1]
    back()
    back()
    if token =='=':
        fz(node)
    elif token=='(':
        hs(node)
    else:
        error()
def hs_v_list(pre):
    token=getNextToken(1)[1]
    is_def=0
    is_ann=0
    node=create_node(pre,'函数声明形参列表')
    while token!=')':
        if token not in ['int','float','char']:
            error()
            return
        create_node(node, token)
        token=getNextToken(1)
        if token[1]==')':
            break
        if token[0]=='ID':
            create_node(node,token[1])
            if is_ann:
                error()
                return
            if not is_def:
                #print(''.join(blk) + '函数定义识别')
                blk.append('\t')
            is_def=1
            token=getNextToken(1)[1]
            if token==')':
                break
            if token!=',':
                error()
                return
            create_node(node, ',')
        elif token[1]==',':
            if is_def:
                error()
                return
            is_ann=1
            create_node(node, ',')
        token=getNextToken(1)[1]
    if is_def:
        alter_node(node,'函数定义形参列表')
        alter_node(pre_node[node],'函数定义')
        blk.pop()
        #print(''.join(blk) + '函数定义识别结束')
    back()
def FDA(pre):
    #print(''.join(blk) + '函数声明识别')
    blk.append('\t')
    token=getNextToken(1)[1]
    node=create_node(pre,'函数声明')
    if token not in ['int','char','float','void']:
        error()
        return
    create_node(node,token)
    token=getNextToken(1)
    if token[0]!='ID':
        error()
        return
    create_node(create_node(node,'函数名'), token[1])
    token=getNextToken(1)
    if token[1]!='(':
        error()
        return
    create_node(node,'(')
    hs_v_list(node)
    token=getNextToken(1)
    if token[1]!=')':
        error()
        return
    create_node(node, ')')
    token = getNextToken(1)
    if token[1]=='{':
        back()
        CSA(node)
    elif token[1] != ';':
        error()
        return
    create_node(node, ';')
    blk.pop()
    #print(''.join(blk) + '函数声明识别结束')
def get_tree(filename):
    # print(pre_node)
    # print(val_node)
    dot = Digraph(comment=filename,node_attr={'fontname':"Microsoft YaHei"})
    for (i,j) in val_node.items():
        # print(i,j)
        # print(pre_node[i])
        dot.node(str(i),j)
    for (i,j) in pre_node.items():
        if j==None:
            continue
        dot.edge(str(j),str(i))
    dot.render(f'{filename}.gv',view=False)
    return (val_node,pre_node)
def generate_tree(filename=None):
    global type_value_token,ind,node_num,pre_node,val_node
    if filename==None:
        for i in os.listdir('编译器测试用例/')[:-2]:
            if '.txt' in i:
                try:
                    node_num = 0
                    pre_node = {}
                    val_node = {}
                    type_value_token = getToken(f'/编译器测试用例/{i}')
                    ind = -1
                    parser()
                    get_tree(i)
                except:
                    print(i)
    else:
        type_value_token = getToken(filename)
        ind = -1
        parser()
        return get_tree(filename)