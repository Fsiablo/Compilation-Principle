import os
import pandas as pd
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
mid_codes=[]
tokens=[]
Factor_list=['INT','INT_2','INT_8','INT_16','CHAR','ID','FLOAT']
fun_table=[]
tmp_num=0
def get_stc_end(code,i):
    while code[i]!=';':
        i+=1
    return i
def get_bool_end(i):
    while tokens[i]!='{':
        i+=1
    return i-1
def generate_code(a,b,c,d):
    if a =='&&':
        code_pos_1_t=generate_code('jnz',b,'',None)
        code_pos_1_f=generate_code('j','', '', None)
        code_pos_2_t=generate_code('jnz',c,'',None)
        code_pos_2_f=generate_code('j','','',None)
        code_pos_t=generate_code('=','1','',d)
        generate_code('j', '', '', get_code_pos() + 2)
        code_pos_f = generate_code('=', '0', '', d)
        mid_codes[code_pos_2_t][3]=code_pos_t
        mid_codes[code_pos_1_t][3] = code_pos_2_t
        mid_codes[code_pos_2_f][3] = code_pos_f
        mid_codes[code_pos_1_f][3] = code_pos_f
    elif a=='||':
        code_pos_1_t = generate_code('jnz', b, '', None)
        code_pos_2_t = generate_code('jnz', c, '', None)
        code_pos_2_f = generate_code('j', '', '', None)
        code_pos_t = generate_code('=', '1', '', d)
        generate_code('j', '', '', get_code_pos() + 2)
        code_pos_f = generate_code('=', '0', '', d)
        mid_codes[code_pos_2_t][3] = code_pos_t
        mid_codes[code_pos_1_t][3] = code_pos_t
        mid_codes[code_pos_2_f][3] = code_pos_f
    elif a in ['>','>=','<','<=','==','!=']:
        generate_code(f'j{a}', b, c, get_code_pos()+2)
        generate_code('j', '', '', get_code_pos()+3)
        generate_code('=', '1', '', d)
        generate_code('j', '', '', get_code_pos() + 2)
        generate_code('=', '0', '', d)
    else:
        mid_codes.append([a,b,c,d])
    # mid_codes.append([a, b, c, d])
    return len(mid_codes)-1
def getPlace():
    global tmp_num,tmp_fun_num,in_fun
    if in_fun:
        tmp_fun_num+=1
        return f'temp_fun{tmp_fun_num}'
    else:
        tmp_num+=1
        return f'temp{tmp_num}'
def get_code_pos():
    return len(mid_codes)
def Expr(tokens):
    pre_dict = {'(':-1,
                '!':4,
                '*':3,'/':3,'%':3,
                '+':2,'-':2,
                '>':1,'>=':1,'<':1,'<=':1,'==':1,'!=':1,
                '&&':0,'||':0,
                }
    operator_stack = []
    operand_stack = []
    st=0
    end=len(tokens)
    if tokens[st]=='-':
        place=getPlace()
        if tokens[st+1] in fun_table:
            ind=st+3
            code,ind=get_para_code(tokens,ind)
            return_val=call_func(tokens[st+1:ind])
            generate_code('@',return_val,'',place)
            st=ind
        else:
            generate_code('@',tokens[st+1],'',place)
            st+=2
        operand_stack.append(place)
    i=st
    while i<end:
        token=tokens[i]
        if token=='(':
            operator_stack.append(token)
        elif token==')':
            top=operator_stack.pop()
            while top!='(':
                op2=operand_stack.pop()
                op1=operand_stack.pop()
                place=getPlace()
                operand_stack.append(place)
                generate_code(top,op1,op2,place)
                top=operator_stack.pop()
        elif token in pre_dict.keys():
            while operator_stack and pre_dict[operator_stack[-1]] >= pre_dict[token]:
                top = operator_stack.pop()
                if top=='!':
                    op=operand_stack.pop()
                    place = getPlace()
                    operand_stack.append(place)
                    generate_code(top, op, '', place)
                    continue
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                place = getPlace()
                operand_stack.append(place)
                generate_code(top, op1, op2, place)
            operator_stack.append(token)
        else:
            if token in fun_table:
                ind = i+ 2
                code, ind = get_para_code(tokens, ind)
                return_val = call_func(tokens[i: ind])
                operand_stack.append(return_val)
                i=ind-1
            else:
                operand_stack.append(token)
        i+=1
    while operator_stack:
        top = operator_stack.pop()
        if top == '!':
            op = operand_stack.pop()
            place = getPlace()
            operand_stack.append(place)
            generate_code(top, op, '', place)
            continue
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        place = getPlace()
        operand_stack.append(place)
        generate_code(top, op1, op2, place)
    return operand_stack[0]
def call_func(tokens):
    func=tokens[0]
    paras=tokens[2:-1]
    per_para=[]
    tmp=[]
    lbrk=0
    rbrk=0
    for i in paras:
        if i==',':
            if lbrk!=rbrk:
                per_para.append(i)
            else:
                tmp.append(Expr(per_para))
                per_para = []
        else:
            per_para.append(i)
            if i=='(':
                lbrk+=1
            elif i==')':
                rbrk+=1
    if per_para:
        tmp.append(Expr(per_para))
    tmp.reverse()
    for i in tmp:
        generate_code('para', i, '', '')
    place=getPlace()
    generate_code('call', func, '', place)
    return place
def get_block_code(tokens,ind):
    l_bkt_num = 1
    r_bkt_num = 0
    r_bkt_ind = ind
    while l_bkt_num != r_bkt_num:
        if tokens[r_bkt_ind] == '}':
            r_bkt_num += 1
        if tokens[r_bkt_ind] == '{':
            l_bkt_num += 1
        r_bkt_ind += 1
    return (tokens[ind:r_bkt_ind-1],r_bkt_ind)
def get_para_code(tokens,ind):
    l_bkt_num = 1
    r_bkt_num = 0
    r_bkt_ind = ind
    while l_bkt_num != r_bkt_num:
        if tokens[r_bkt_ind] == ')':
            r_bkt_num += 1
        if tokens[r_bkt_ind] == '(':
            l_bkt_num += 1
        r_bkt_ind += 1
    return (tokens[ind:r_bkt_ind-1],r_bkt_ind)
def check_control(in_code_pos,out_code_pos):
    for i in range(len(mid_codes)):
        if mid_codes[i][3]=='break':
            mid_codes[i][3]=out_code_pos
        elif mid_codes[i][3]=='continue':
            mid_codes[i][3]=in_code_pos
def analyze_code(tokens):
    global in_fun,tmp_fun_num
    i=0
    while i <len(tokens):
        if tokens[i] == '=':
            end=get_stc_end(tokens,i)
            code = tokens[i + 1:end]
            generate_code('=', Expr(code), '', tokens[i - 1])
            i=end
        elif tokens[i] == 'if':
            Bexpr_result = Expr(tokens[i + 2:tokens[i:].index('{') + i-1])
            generate_code('jnz', Bexpr_result, '', get_code_pos() + 2)
            ind = tokens[i:].index('{') + i + 1
            tc_code,ind=get_block_code(tokens,ind)
            if 'else' in tokens[i:]:
                ind = tokens[i:].index('else') + i+2
                fc_code,ind = get_block_code(tokens,ind)
                code_pos_1 = generate_code('j', '', '', -1)
                analyze_code(tc_code)
                code_pos_2 = generate_code('j', '', '', -1)
                mid_codes[code_pos_1][3] = get_code_pos()
                analyze_code(fc_code)
                mid_codes[code_pos_2][3] = get_code_pos()

                i=ind
            else:
                code_pos=generate_code('j','','',-1)
                analyze_code(tc_code)
                mid_codes[code_pos][3]=get_code_pos()

                i=ind
        elif tokens[i] =='while':
            Bexpr_result = Expr(tokens[i + 2:tokens[i:].index('{') + i-1])
            st_code_pos=generate_code('jnz', Bexpr_result, '', get_code_pos() + 2)-1

            ind=tokens[i:].index('{') + i + 1
            tc_code,ind = get_block_code(tokens,ind)
            code_pos = generate_code('j', '', '', -1)
            analyze_code(tc_code)
            generate_code('j', '', '', st_code_pos)
            mid_codes[code_pos][3] = get_code_pos()

            check_control(st_code_pos,get_code_pos())

            i = ind
        elif tokens[i] =='do':
            code_pos=get_code_pos()
            ind = tokens[i:].index('{') + i + 1
            tc_code, ind = get_block_code(tokens, ind)
            analyze_code(tc_code)
            Bexpr_result = Expr(tokens[ind + 2:tokens[ind:].index(';') + ind-1])
            st_code_pos=generate_code('jnz', Bexpr_result, '', code_pos)

            check_control(st_code_pos, get_code_pos())

            i = tokens[ind:].index(';') + ind
        elif tokens[i]=='for':
            end = get_stc_end(tokens, i)
            code = tokens[i + 4:end]
            generate_code('=', Expr(code), '', tokens[i+2])


            Bexpr=tokens[end+1:get_stc_end(tokens,end+1)]
            Bexpr_result = Expr(Bexpr)
            code_pos_t=generate_code('jnz', Bexpr_result, '', get_code_pos()+2)
            code_pos_f=generate_code('j', Bexpr_result, '', -1)

            ind=tokens[i:].index('{') + i + 1
            tc_code,ind = get_block_code(tokens,ind)
            analyze_code(tc_code)

            end=get_stc_end(tokens,end+1)
            e3=tokens[end+3:tokens[end+1:].index('{')+end]
            st_code_pos=get_code_pos()
            generate_code('=', Expr(e3), '', tokens[end+1])
            generate_code('j', '', '', code_pos_t-1)

            mid_codes[code_pos_f][3]=get_code_pos()

            check_control(st_code_pos, get_code_pos())

            i = tokens[i:].index('}') + i
        elif tokens[i] in ['int','float','char','void'] and tokens[i+2]=='(' :
            try:
                tmp=tokens[i:].index(';')+i+1
                ind=tokens[i:tmp].index('{')+i+1
            except:
                fun_table.append(tokens[i+1])
                i=tokens[i:].index(';')+i+1
                continue
            in_fun=1
            tmp_fun_num=0
            code,ind=get_block_code(tokens,ind)
            generate_code(tokens[i+1],'','','')
            analyze_code(code)
            fun_table.append(tokens[i+1])
            i=ind
            in_fun=0
        elif tokens[i].isalpha() and tokens[i+1]=='(' and tokens[i] !='main' and tokens[i-1] not in ['int','float','char','void']:
            ind=i+2
            code,ind=get_para_code(tokens,ind)
            call_func(tokens[i:ind])
            i=ind
        elif tokens[i]=='return':
            end=tokens[i:].index(';')+i
            expr=tokens[i+1:end]
            if expr:
                generate_code('ret', '', '', Expr(expr))
            else:
                generate_code('ret', '', '', '')
            i=end+1
        elif tokens[i] in ['break','continue']:
            generate_code('j', '', '', tokens[i])
            i+=1
        else:
            i+=1
def get_mid(tokens):
    generate_code('main','','','')
    analyze_code(tokens)
    generate_code('sys', '', '', '')
def build_sign_table():
    def getNextToken(all=0):
        global ind
        ind += 1
        try:
            if all:
                return type_value_token[ind]
            return type_value_token[ind][1]
        except:
            if all:
                return ('#', '#', '#')
            return '#'
    def back():
        global ind
        ind -= 1
    global type_value_token
    const_table = []
    var_table = {}
    func_table = []
    str_table = []
    continue_table=[]
    break_table=[]
    return_table=[]
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
            item['value']=0
            var_table[item['name']]=var_table.get(item['name'], [])
            var_table[item['name']].append(item)
            while token!=';':
                item = {}
                item['block'] = now_block()
                item['name'] = getNextToken()
                item['type'] = type_
                item['value'] = 0
                var_table[item['name']] = var_table.get(item['name'], [])
                var_table[item['name']].append(item)
                token=getNextToken()
        else:
            item['value']=getNextToken()
            if item['value']=='-':
                item['value']+=getNextToken()
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
            # tmp=getNextToken()
            # if tmp not in [',',')',';']:
            #     back()
            #     item_v = {}
            #     item_v['block'] = now_block()
            #     item_v['name'] = getNextToken()
            #     item_v['type'] = token
            #     item_v['value'] = 0
            #     var_table[item_v['name']] = var_table.get(item_v['name'], [])
            #     var_table[item_v['name']].append(item_v)
            token=getNextToken()
            if token==';':
                break
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
def token_2_mid(type_value_token):
    global ind, mid_codes, tmp_num, fun_table, tokens,in_fun,tmp_fun_num
    in_fun=0
    mid_codes = []
    tokens = []
    fun_table = ['read','write']
    tmp_num = 0
    tmp_fun_num=0
    ind = -1
    tokens=[i[1] for i in type_value_token]
    get_mid(tokens)
    return mid_codes
def get_midcode(filename):
    global type_value_token, ind,mid_codes,tmp_num,func_table,tokens
    type_value_token = getToken(filename)
    midcode=''
    num=0
    for i in token_2_mid(type_value_token):
        midcode+=(str(num)+'\t'+'\t'.join([str(j) for j in i])+'\n')
        num+=1
    return midcode
def get_table(filename,raw=0):
    global type_value_token,ind
    ind = -1
    type_value_token=getToken(filename)
    tables=build_sign_table()
    table_str=""
    for i in tables:
        table_str+=i+'\n'
        if i=='var_table':
            table_str+=(pd.DataFrame([j[0] for j in tables[i].values()]).to_string())+'\n'+'\n'
        elif tables[i]:
            table_str+=(pd.DataFrame(tables[i]).to_string())+'\n'+'\n'
    # print(pd.DataFrame(tables))
    if raw:
        return tables
    return table_str