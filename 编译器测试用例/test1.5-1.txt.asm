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
	_sum dw 0
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
	mov ax,0
	mov _sum,ax
_seg2:
	mov ax,1
	mov _x,ax
_seg3:
	mov dx,1
	mov ax,_x
	cmp ax,10
	jle _le1
	mov dx,0
_le1: mov es:[0],dx
_seg4:
	mov ax,es:[0]
	cmp ax,0
	je _ez1
	jmp far ptr _seg6
_ez1: nop
_seg5:
	jmp far ptr _seg11
_seg6:
	mov ax,_sum
	add ax,_x
	mov es:[2],ax
_seg7:
	mov ax,es:[2]
	mov _sum,ax
_seg8:
	mov ax,_x
	add ax,1
	mov es:[4],ax
_seg9:
	mov ax,es:[4]
	mov _x,ax
_seg10:
	jmp far ptr _seg3
_seg11:
	mov ax,_x
	push ax
_seg12:
	call _write
	mov es:[6],ax
	call dispcrlf
_seg13:
	mov ax,_sum
	push ax
_seg14:
	call _write
	mov es:[8],ax
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