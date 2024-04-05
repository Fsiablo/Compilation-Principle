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
	_z dw 0
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
	mov ax,9
	mov _x,ax
_seg2:
	mov ax,3
	mov _y,ax
_seg3:
	mov ax,_y
	mov bx,_y
	mul bx
	mov es:[0],ax
_seg4:
	mov ax,_x
	sub ax,es:[0]
	mov es:[2],ax
_seg5:
	mov ax,_x
	mov dx,0
	mov bx,3
	div bx
	mov es:[4],dx
_seg6:
	mov ax,es:[2]
	sub ax,es:[4]
	mov es:[6],ax
_seg7:
	mov ax,es:[6]
	mov _z,ax
_seg8:
	mov ax,_x
	push ax
_seg9:
	call _write
	mov es:[8],ax
	call dsp
_seg10:
	mov ax,_y
	push ax
_seg11:
	call _write
	mov es:[10],ax
	call dsp
_seg12:
	mov ax,_z
	push ax
_seg13:
	call _write
	mov es:[12],ax
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