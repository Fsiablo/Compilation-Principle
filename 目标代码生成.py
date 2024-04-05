import os

from 中间代码生成 import token_2_mid,getToken,get_table
func_code=[]
func_num={}
segNum=-1
var=[]
read=0
write=0
para_num=0
id_dict={}
def generate_func(name,code):
    func_num[name]=func_num.get(name,0)+1
    return (name+f'{func_num[name]}'+': '+code)
def getNum(name):
    return name+f'{func_num.get(name,0)+1}'
def form_id(id):
    global vars_,funcs_,para_num,id_dict,is_func,is_cmp
    tmp = str(id)
    if tmp.isidentifier():
        if 'temp' in tmp:
            if 'fun' in tmp:
                id=f'ss:[bp-{int(tmp[8:])*2}]'
            else:
                id = f'es:[{int(tmp[4:]) * 2 - 2}]'
        elif tmp not in vars_ and tmp not in funcs_:
            if tmp in id_dict:
                id = id_dict[tmp]
            else:
                id_dict[tmp]=id_dict.get(tmp,f'ss:[bp+{4+2*para_num}]')
                id=id_dict[tmp]
                para_num+=1
        else:
            id = f'_{id}'
    return id
def generate_code(i):
    global func_code,segNum,var,read,write,para_num,is_func,is_cmp
    code=''
    opt=i[0]
    a=form_id(i[1])
    b=form_id(i[2])
    t=form_id(i[3])
    is_cmp = 0
    is_seg=1
    if opt=='+':
        code=f'\tmov ax,{a}\n' \
             f'\tadd ax,{b}\n' \
             f'\tmov {t},ax'
    elif opt=='-':
        code = f'\tmov ax,{a}\n' \
               f'\tsub ax,{b}\n' \
               f'\tmov {t},ax'
    elif opt=='@':
        code = f'\tmov ax,{a}\n' \
               f'\tneg ax\n' \
               f'\tmov {t},ax'
    elif opt=='*':
        code = f'\tmov ax,{a}\n' \
               f'\tmov bx,{b}\n' \
               f'\tmul bx\n' \
               f'\tmov {t},ax'
    elif opt=='/':
        code = f'\tmov ax,{a}\n' \
               f'\tmov dx,0\n' \
               f'\tmov bx,{b}\n' \
               f'\tdiv bx\n' \
               f'\tmov {t},ax'
    elif opt=='%':
        code = f'\tmov ax,{a}\n' \
               f'\tmov dx,0\n' \
               f'\tmov bx,{b}\n' \
               f'\tdiv bx\n' \
               f'\tmov {t},dx'
    elif opt == '>':
        code = f'\tmov dx,1\n' \
               f'\tmov ax,{a}\n' \
               f'\tcmp ax,{b}\n' \
               f'\tjg {getNum("_lt")}\n' \
               f'\tmov dx,0\n'
        is_cmp=1
        code+=generate_func('_lt', f'mov {t},dx')
    elif opt == '>=':
        code = f'\tmov dx,1\n' \
               f'\tmov ax,{a}\n' \
               f'\tcmp ax,{b}\n' \
               f'\tjge {getNum("_ge")}\n' \
               f'\tmov dx,0\n'
        is_cmp = 1
        code+=generate_func('_ge', f'mov {t},dx')
    elif opt == '<':
        code = f'\tmov dx,1\n' \
               f'\tmov ax,{a}\n' \
               f'\tcmp ax,{b}\n' \
               f'\tjl {getNum("_gt")}\n' \
               f'\tmov dx,0\n'
        is_cmp = 1
        code+=generate_func('_gt', f'mov {t},dx')
    elif opt == '<=':
        code = f'\tmov dx,1\n' \
               f'\tmov ax,{a}\n' \
               f'\tcmp ax,{b}\n' \
               f'\tjle {getNum("_le")}\n' \
               f'\tmov dx,0\n'
        is_cmp = 1
        code+=generate_func('_le', f'mov {t},dx')
    elif opt == '==':
        code = f'\tmov dx,1\n' \
               f'\tmov ax,{a}\n' \
               f'\tcmp ax,{b}\n' \
               f'\tje {getNum("_eq")}\n' \
               f'\tmov dx,0\n'
        is_cmp = 1
        code+=generate_func('_eq', f'mov {t},dx')
    elif opt == '!=':
        code = f'\tmov dx,1\n' \
               f'\tmov ax,{a}\n' \
               f'\tcmp ax,{b}\n' \
               f'\tjne {getNum("_ne")}\n' \
               f'\tmov dx,0\n'
        is_cmp = 1
        code+=generate_func('_ne', f'mov {t},dx')
    elif opt == '&&':
        code = f'\tmov dx,0\n' \
               f'\tmov ax,{a}\n' \
               f'\tcmp ax,0\n' \
               f'\tje {getNum("_and")}\n' \
               f'\tmov ax,{b}\n' \
               f'\tcmp ax,0\n' \
               f'\tje {getNum("_and")}\n' \
               f'\tmov dx,1\n'
        is_cmp = 1
        code+=generate_func('_and', f'mov {t},dx')
    elif opt == '||':
        code = f'\tmov dx,1\n' \
               f'\tmov ax,{a}\n' \
               f'\tcmp ax,0\n' \
               f'\tjne {getNum("_or")}\n' \
               f'\tmov ax,{b}\n' \
               f'\tcmp ax,0\n' \
               f'\tjne {getNum("_or")}\n' \
               f'\tmov dx,0\n'
        is_cmp = 1
        code+=generate_func('_or', f'mov {t},dx')
    elif opt == '!':
        code = f'\tmov dx,1\n' \
               f'\tmov ax,{a}\n' \
               f'\tcmp ax,0\n' \
               f'\tje {getNum("_not")}\n' \
               f'\tmov dx,0\n'
        is_cmp = 1
        code+=generate_func('_not', f'mov {t},dx')
    elif opt=='=':
        code=f'\tmov ax,{a}\n' \
             f'\tmov {t},ax'
    elif opt=='j':
        code=f'\tjmp far ptr _seg{t}'
    elif opt=='jnz':
        code=f'\tmov ax,{a}\n' \
             f'\tcmp ax,0\n' \
             f'\tje {getNum("_ez")}\n' \
             f'\tjmp far ptr _seg{t}\n'
        is_cmp = 1
        code+=generate_func('_ez', f'nop')
    elif opt=='para':
        code=f'\tmov ax,{a}\n' \
             f'\tpush ax'
    elif opt=='call':
        if a=='_read':
            read=1
        if a=='_write':
            write=1
        code=f'\tcall {a}\n' \
             f'\tmov {t},ax'
        if a=='_write':
            code+=f'\n\tcall dsp'
    elif opt=='ret':
        v=f'\tmov ax,{t}\n'
        code=f'\tmov sp,bp\n' \
             f'\tpop bp\n' \
             f'\tret'
        if t!='':
            code=v+code
    elif opt=='main':
        is_seg=0
        code='assume cs:code,ds:data,ss:stack,es:extended\n' \
             'extended segment\n' \
             '\tdb 1024 dup (0)\n' \
             'extended ends\n' \
             'stack segment\n' \
             '\tdb 1024 dup (0)\n' \
             'stack ends\n' \
             'data segment\n' \
             '\tt_buff_p db 256 dup (24h)\n' \
             '\tt_buff_s db 256 dup (0)\n' \
             '\tt_w db 0ah,\'Output:\',0\n' \
             '\tt_r db 0ah,\'Input:\',0\n'+''.join(var)+'data ends\n' \
             'code segment\n' \
             'start:\n\tmov ax,extended\n' \
             '\tmov es,ax\n' \
             '\tmov ax,stack\n' \
             '\tmov ss,ax\n' \
             '\tmov sp,1024\n' \
             '\tmov bp,sp\n' \
             '\tmov ax,data\n' \
             '\tmov ds,ax'
    elif opt=='sys':
        is_seg=0
        code='quit:\n\tmov ah,4ch\n' \
             '\tint 21h'
        if read:
            code+='''
_read:
    push bp
    mov bp,sp
    mov bx,offset t_r
    call _print
    mov bx,offset t_buff_s
    mov di,0
_print:mov si,0
	mov di,offset t_buff_p
_r_lp_1:
    mov ah,1
    int 21h
    cmp al,0dh
    je _r_brk_1
    mov ds:[bx+di],al
    inc di
    jmp short _r_lp_1
_r_brk_1:
    mov ah,2
    mov dl,0ah
    int 21h
    mov ax,0
    mov si,0
    mov cx,10
_r_lp_2:
    mov dl,ds:[bx+si]
    cmp dl,30h
    jb _r_brk_2
    cmp dl,39h
    ja _r_brk_2
    sub dl,30h
    mov ds:[bx+si],dl
    mul cx
    mov dl,ds:[bx+si]
    mov dh,0
    add ax,dx
	inc si
	jmp short _r_lp_2
_r_brk_2:
    mov cx,di
	mov si,0
_r_lp_3:
    mov byte ptr ds:[bx+si],0
	loop _r_lp_3
	mov sp,bp
	pop bp
	ret'''
        if write:
            code+='''
_write:	push bp
	mov bp,sp
	mov bx,offset _msg_p
	call _print
	mov ax,ss:[bp+4]
	mov bx,10
	mov cx,0
_w_lp_1:	mov dx,0
	div bx
	push dx
	inc cx
	cmp ax,0
	jne _w_lp_1
	mov di ,offset _buff_p
_w_lp_2:	pop ax
	add ax,30h
	mov ds:[di],al
	inc di
	loop _w_lp_2
	mov dx,offset _buff_p
	mov ah,09h
	int 21h
	mov cx,di
	sub cx,offset _buff_p
	mov di,offset _buff_p
_w_lp_3:	mov al,24h
	mov ds:[di],al
	inc di
	loop _w_lp_3
	mov ax,di
	sub ax,offset _buff_p
	mov sp,bp
	pop bp
	ret 2
_print:	mov si,0
	mov di,offset _buff_p
_p_lp_1:	mov al,ds:[bx+si]
	cmp al,0
	je _p_brk_1
	mov ds:[di],al
	inc si
	inc di
	jmp short _p_lp_1
_p_brk_1:	mov dx,offset _buff_p
	mov ah,09h
	int 21h
	mov cx,si
	mov di,offset _buff_p
_p_lp_2:	mov al,24h
	mov ds:[di],al
	inc di
	loop _p_lp_2
	ret'''
#             code+='''
# _write:
#     push ax
#     push bx
#     push dx
#     test ax,ax
#     jnz sign_
#     mov dl,'0'
#     mov ah,2
#     int 21h
#     jmp dsiw5
# sign_:jns sign_2
#     mov bx,ax
#     mov dl,'-'
#     mov ah,2
#     int 21h
#     mov ax,bx
#     neg ax
# sign_2:mov bx,10
#     push bx
# sign_3:cmp ax,0
#     jz sign_4
#     xor dx,dx
#     div bx
#     add dl,30h
#     push dx
#     jmp sign_3
# sign_4:pop dx
#     cmp dl,10
#     je dsiw5
#     mov ah,2;
#     int 21h
#     jmp sign_4
# dsiw5:pop dx
#     pop bx
#     pop ax
#     ret
# dsp:
#     push ax
#     push dx
#     mov dl,0dh
#     mov ah,2
#     int 21h
#     mov dl, 0ah
#     int 21h
#     pop dx
#     pop ax
#     ret
# ex: mov al,4ch
#     int 21h
# '''
    else:
        is_seg=0
        para_num=0
        is_func=1
        code=f'_{opt}:push bp\n' \
             f'\tmov bp,sp\n' \
             f'\tsub sp,2'
    segNum+=1
    if is_seg:
        code=f'_seg{segNum}:\n'+code
    if 'ss' in str(t):
        code+=f'\n\tpush {t}'
    return code
def mid_2_target(mid_code):
    global is_func,segNum
    target_code=[]
    is_func=0
    segNum=-1
    func_code=[]
    for i in mid_code:
        code=generate_code(i)
        if f'_seg{len(mid_code)-1}' in code:
            code=code.replace(f'_seg{len(mid_code)-1}','quit')
        if i[0]=='sys':
            is_func=0
        if is_func:
            func_code.append(code)
        else:
            target_code.append(code)
    target_code.extend(func_code)
    target_code.append('code ends\nend start')
    return target_code
def get_target_code(filename):
    global func_code,func_num,var,read,write,vars_,funcs_,id_dict
    id_dict={}
    table=get_table(filename,raw=1)
    var=[]
    read=0
    write=0
    vars_=table['var_table']
    funcs_=set([i['name'] for i in table['func_table']])
    funcs_.add('read')
    funcs_.add('write')
    for i in vars_:
        tmp_code=vars_[i][0]
        var.append(f'\t_{tmp_code["name"]} dw 0\n')
    func_code = []
    func_num = {}
    type_value_token=getToken(filename)
    mid_code=token_2_mid(type_value_token)
    # for i in range(len(mid_code)):
    #     print(i,mid_code[i])
    target=mid_2_target(mid_code)
    target_code_asm='\n'.join(target)
    with open(f'{filename}.asm','w') as f:
        f.write(target_code_asm)
    return target_code_asm
# for i in os.listdir(r'D:\study\pythonProject\编译原理\编译器测试用例'):
#     if '.txt'==i[-4:]:
#         print(i)
#         get_target_code(rf'D:\study\pythonProject\编译原理\编译器测试用例\{i}')
# get_target_code(rf'D:\study\pythonProject\编译原理\编译器测试用例\test5.1.txt')