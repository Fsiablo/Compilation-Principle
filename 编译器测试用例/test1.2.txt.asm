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
	mov ax,3
	neg ax
	mov es:[0],ax
_seg2:
	mov ax,es:[0]
	mov _x,ax
_seg3:
	mov dx,1
	mov ax,_x
	cmp ax,0
	jl _gt1
	mov dx,0
_gt1: mov es:[2],dx
_seg4:
	mov ax,es:[2]
	cmp ax,0
	je _ez1
	jmp far ptr _seg6
_ez1: nop
_seg5:
	jmp far ptr _seg9
_seg6:
	mov ax,_x
	neg ax
	mov es:[4],ax
_seg7:
	mov ax,es:[4]
	mov _x,ax
_seg8:
	jmp far ptr _seg15
_seg9:
	mov dx,1
	mov ax,_x
	cmp ax,0
	je _eq1
	mov dx,0
_eq1: mov es:[6],dx
_seg10:
	mov ax,es:[6]
	cmp ax,0
	je _ez2
	jmp far ptr _seg12
_ez2: nop
_seg11:
	jmp far ptr _seg14
_seg12:
	mov ax,_x
	mov _x,ax
_seg13:
	jmp far ptr _seg15
_seg14:
	mov ax,_x
	mov _x,ax
_seg15:
	mov ax,_x
	push ax
_seg16:
	call _write
	mov es:[8],ax
	call dsp
quit:
	mov ah,4ch
	int 21h
_write:
    push ax
    push bx
    push dx
    test ax,ax
    jnz sign_
    mov dl,'0'
    mov ah,2
    int 21h
    jmp dsiw5
sign_:jns sign_2
    mov bx,ax
    mov dl,'-'
    mov ah,2
    int 21h
    mov ax,bx
    neg ax
sign_2:mov bx,10
    push bx
sign_3:cmp ax,0
    jz sign_4
    xor dx,dx
    div bx
    add dl,30h
    push dx
    jmp sign_3
sign_4:pop dx
    cmp dl,10
    je dsiw5
    mov ah,2;
    int 21h
    jmp sign_4
dsiw5:pop dx
    pop bx
    pop ax
    ret
dsp:
    push ax
    push dx
    mov dl,0dh
    mov ah,2
    int 21h
    mov dl, 0ah
    int 21h
    pop dx
    pop ax
    ret
ex: mov al,4ch
    int 21h

code ends
end start