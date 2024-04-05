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
	_a dw 0
	_i dw 0
	_sum dw 0
	_N dw 0
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
	mov _a,ax
_seg2:
	mov ax,1
	mov _i,ax
_seg3:
	call _read
	mov ES:[0],ax
_seg4:
	mov ax,ES:[0]
	mov _N,ax
_seg5:
	mov dx,1
	mov ax,_i
	cmp ax,_N
	jb _lt1
	mov dx,0
_lt1: mov ES:[2],dx
_seg6:
	mov ax,ES:[2]
	cmp ax,0
	je _ez1
	jmp far ptr _seg8
_ez1: nop
_seg7:
	jmp far ptr _seg17
_seg8:
	mov ax,_i
	mov dx,0
	mov bx,2
	div bx
	mov ES:[4],dx
_seg9:
	mov dx,1
	mov ax,ES:[4]
	cmp ax,0
	je _eq1
	mov dx,0
_eq1: mov ES:[6],dx
_seg10:
	mov ax,ES:[6]
	cmp ax,0
	je _ez2
	jmp far ptr _seg12
_ez2: nop
_seg11:
	jmp far ptr _seg14
_seg12:
	mov ax,_sum
	add ax,_i
	mov ES:[8],ax
_seg13:
	mov ax,ES:[8]
	mov _sum,ax
_seg14:
	mov ax,_i
	add ax,1
	mov ES:[10],ax
_seg15:
	mov ax,ES:[10]
	mov _i,ax
_seg16:
	jmp far ptr _seg5
_seg17:
	mov ax,_sum
	push ax
_seg18:
	call _write
	mov ES:[12],ax
	call dispcrlf
quit:
	mov ah,4ch
	int 21h
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
	ret
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