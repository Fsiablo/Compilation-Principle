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
	_n dw 0
	_s dw 0
	_a dw 0
	_b dw 0
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
	call _read
	mov es:[0],ax
_seg2:
	mov ax,es:[0]
	mov _n,ax
_seg3:
	mov ax,_n
	push ax
_seg4:
	call _seq
	mov es:[2],ax
_seg5:
	mov ax,es:[2]
	push ax
_seg6:
	call _write
	mov es:[4],ax
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
    test ax,ax
    jnz dsiw1
    mov dl,'0'
    mov ah,2
    int 21h
    jmp dsiw5
dsiw1:jns dsiw2
    mov bx,ax
    mov dl,'-'
    mov ah,2
    int 21h
    mov ax,bx
    neg ax
dsiw2:mov bx,10
    push bx
dsiw3:cmp ax,0
    jz dsiw4
    xor dx,dx
    div bx
    add dl,30h
    push dx
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

_seq:push bp
	mov bp,sp
	sub sp,2
_seg8:
	mov dx,1
	mov ax,ss:[bp+4]
	cmp ax,2
	jle _le1
	mov dx,0
_le1: mov ss:[bp+76],dx
_seg9:
	mov ax,ss:[bp+76]
	cmp ax,0
	je _ez1
	jmp far ptr _seg11
_ez1: nop
_seg10:
	jmp far ptr _seg13
_seg11:
	mov ax,1
	mov _s,ax
_seg12:
	jmp far ptr _seg21
_seg13:
	mov ax,ss:[bp+4]
	sub ax,1
	mov ss:[bp+72],ax
_seg14:
	mov ax,ss:[bp+72]
	push ax
_seg15:
	call _seq
	mov ss:[bp+68],ax
_seg16:
	mov ax,ss:[bp+4]
	sub ax,2
	mov ss:[bp+64],ax
_seg17:
	mov ax,ss:[bp+64]
	push ax
_seg18:
	call _seq
	mov ss:[bp+60],ax
_seg19:
	mov ax,ss:[bp+68]
	add ax,ss:[bp+60]
	mov ss:[bp+56],ax
_seg20:
	mov ax,ss:[bp+56]
	mov _s,ax
_seg21:
	mov ax,_s
	mov sp,bp
	pop bp
	ret
code ends
end start