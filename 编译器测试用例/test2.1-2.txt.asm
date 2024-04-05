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
	_max dw 0
	_min dw 0
	_sum dw 0
	_i dw 0
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
	mov _a,ax
_seg2:
	mov ax,0
	mov _max,ax
_seg3:
	mov ax,0
	mov _min,ax
_seg4:
	mov ax,0
	mov _sum,ax
_seg5:
	mov ax,0
	mov _i,ax
_seg6:
	mov dx,1
	mov ax,_i
	cmp ax,5
	jl _gt1
	mov dx,0
_gt1: mov es:[0],dx
_seg7:
	mov ax,es:[0]
	cmp ax,0
	je _ez1
	jmp far ptr _seg9
_ez1: nop
_seg8:
	jmp far ptr _seg30
_seg9:
	call _read
	mov es:[2],ax
_seg10:
	mov ax,es:[2]
	mov _a,ax
_seg11:
	mov dx,1
	mov ax,_i
	cmp ax,0
	je _eq1
	mov dx,0
_eq1: mov es:[4],dx
_seg12:
	mov ax,es:[4]
	cmp ax,0
	je _ez2
	jmp far ptr _seg14
_ez2: nop
_seg13:
	jmp far ptr _seg17
_seg14:
	mov ax,_a
	mov _max,ax
_seg15:
	mov ax,_a
	mov _min,ax
_seg16:
	jmp far ptr _seg25
_seg17:
	mov dx,1
	mov ax,_a
	cmp ax,_max
	jg _lt1
	mov dx,0
_lt1: mov es:[6],dx
_seg18:
	mov ax,es:[6]
	cmp ax,0
	je _ez3
	jmp far ptr _seg20
_ez3: nop
_seg19:
	jmp far ptr _seg21
_seg20:
	mov ax,_a
	mov _max,ax
_seg21:
	mov dx,1
	mov ax,_a
	cmp ax,_min
	jl _gt2
	mov dx,0
_gt2: mov es:[8],dx
_seg22:
	mov ax,es:[8]
	cmp ax,0
	je _ez4
	jmp far ptr _seg24
_ez4: nop
_seg23:
	jmp far ptr _seg25
_seg24:
	mov ax,_a
	mov _min,ax
_seg25:
	mov ax,_sum
	add ax,_a
	mov es:[10],ax
_seg26:
	mov ax,es:[10]
	mov _sum,ax
_seg27:
	mov ax,_i
	add ax,1
	mov es:[12],ax
_seg28:
	mov ax,es:[12]
	mov _i,ax
_seg29:
	jmp far ptr _seg6
_seg30:
	mov ax,'
'
	push ax
_seg31:
	call _write
	mov es:[14],ax
	call dispcrlf
_seg32:
	mov ax,_max
	push ax
_seg33:
	call _write
	mov es:[16],ax
	call dispcrlf
_seg34:
	mov ax,'
'
	push ax
_seg35:
	call _write
	mov es:[18],ax
	call dispcrlf
_seg36:
	mov ax,_min
	push ax
_seg37:
	call _write
	mov es:[20],ax
	call dispcrlf
_seg38:
	mov ax,'
'
	push ax
_seg39:
	call _write
	mov es:[22],ax
	call dispcrlf
_seg40:
	mov ax,_sum
	mov dx,0
	mov bx,5
	div bx
	mov es:[24],ax
_seg41:
	mov ax,es:[24]
	mov _sum,ax
_seg42:
	mov ax,_sum
	push ax
_seg43:
	call _write
	mov es:[26],ax
	call dispcrlf
_seg44:
	mov ax,'
'
	push ax
_seg45:
	call _write
	mov es:[28],ax
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