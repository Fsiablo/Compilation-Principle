assume cs:code,ds:data,ss:stack,es:extended
extended segment
	db 1024 dup (0)
extended ends
stack segment
	db 1024 dup (0)
stack ends
data segment
	t_buff_p db 256 dup (24h)
	t_buff_s db 256 dup (0)
	t_w db 0ah,'Output:',0
	t_r db 0ah,'Input:',0
	_x dw 0
	_y dw 0
	_a dw 0
	_b dw 0
	_c dw 0
	_d dw 0
data ends
code segment
start:
	mov ax,extended
	mov es,ax
	mov ax,stack
	mov ss,ax
	mov sp,1024
	mov bp,sp
	mov ax,data
	mov ds,ax
_seg1:
	mov ax,1
	mov _x,ax
_seg2:
	mov ax,2
	neg ax
	mov es:[0],ax
_seg3:
	mov ax,es:[0]
	mov _y,ax
_seg4:
	mov dx,1
	mov ax,_x
	cmp ax,_y
	jg _lt1
	mov dx,0
_lt1: mov es:[2],dx
_seg5:
	mov ax,es:[2]
	mov _a,ax
_seg6:
	mov dx,1
	mov ax,_x
	cmp ax,_y
	jl _gt1
	mov dx,0
_gt1: mov es:[4],dx
_seg7:
	mov ax,es:[4]
	mov _b,ax
_seg8:
	mov dx,1
	mov ax,_x
	cmp ax,_y
	je _eq1
	mov dx,0
_eq1: mov es:[6],dx
_seg9:
	mov ax,es:[6]
	mov _c,ax
_seg10:
	mov dx,1
	mov ax,_x
	cmp ax,_y
	jne _ne1
	mov dx,0
_ne1: mov es:[8],dx
_seg11:
	mov ax,es:[8]
	mov _d,ax
_seg12:
	mov ax,_a
	push ax
_seg13:
	call _write
	mov es:[10],ax
	call dispcrlf
_seg14:
	mov ax,_b
	push ax
_seg15:
	call _write
	mov es:[12],ax
	call dispcrlf
_seg16:
	mov ax,_c
	push ax
_seg17:
	call _write
	mov es:[14],ax
	call dispcrlf
_seg18:
	mov ax,_d
	push ax
_seg19:
	call _write
	mov es:[16],ax
	call dispcrlf
quit:
	mov ah,4ch
	int 21h
_write:
    push ax
    push bx
    push dx
    test ax,ax;判断是零、正数或负数
    jnz dsiw1;不是零，跳转
    mov dl,'0'
    mov ah,2
    int 21h
    jmp dsiw5;转向显示
dsiw1:jns dsiw2;是正数，跳转
    mov bx,ax
    mov dl,'-';是负数，显示负号
    mov ah,2
    int 21h
    mov ax,bx
    neg ax;数据求补（绝对值）
dsiw2:mov bx,10
    push bx;10压入堆栈，作为退出标志
dsiw3:cmp ax,0  ;数据（商）为零，转向保存
    jz dsiw4
    xor dx,dx   ;扩展被除数为DX.AX
    div bx  ;数据除以10：DX.AX÷10
    add dl,30h  ;余数（0～9）转换为ASCII
    push dx ;数据先低位后高位压入堆栈
    jmp dsiw3
dsiw4:pop dx
    cmp dl,10
    je dsiw5
    mov ah,2;
    int 21h
    jmp dsiw4
dsiw5:pop dx
    pop bx
    pop ax
    ret
dispcrlf:
    push ax
    push dx
    mov dl,0dh  ;输出回车字符
    mov ah,2
    int 21h
    mov dl, 0ah  ;输出换行字符
    int 21h
    pop dx
    pop ax
    ret
ex: mov al,4ch
    int 21h

code ends
end start