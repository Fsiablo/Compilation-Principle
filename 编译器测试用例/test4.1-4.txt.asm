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
	_b dw 0
	_c dw 0
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
	mov ax,_a
	push ax
_seg2:
	call _read
	mov es:[0],ax
_seg3:
	mov ax,es:[0]
	mov _a,ax
_seg4:
	mov ax,_b
	push ax
_seg5:
	call _read
	mov es:[2],ax
_seg6:
	mov ax,es:[2]
	mov _b,ax
_seg7:
	mov ax,_b
	push ax
_seg8:
	mov ax,_a
	push ax
_seg9:
	call _gcd
	mov es:[4],ax
_seg10:
	mov ax,es:[4]
	mov _c,ax
_seg11:
	mov ax,_c
	push ax
_seg12:
	call _write
	mov es:[6],ax
	call dsp
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

_gcd:push bp
	mov bp,sp
	sub sp,2
_seg14:
	mov ax,ss:[bp+4]
	push ax
_seg15:
	call _write
	mov ss:[bp-2],ax
	call dsp
	push ss:[bp-2]
_seg16:
	mov ax,ss:[bp+6]
	push ax
_seg17:
	call _write
	mov ss:[bp-4],ax
	call dsp
	push ss:[bp-4]
_seg18:
	mov dx,1
	mov ax,ss:[bp+6]
	cmp ax,0
	je _eq1
	mov dx,0
_eq1: mov ss:[bp-6],dx
	push ss:[bp-6]
_seg19:
	mov ax,ss:[bp-6]
	cmp ax,0
	je _ez1
	jmp far ptr _seg21
_ez1: nop
_seg20:
	jmp far ptr _seg23
_seg21:
	mov ax,ss:[bp+4]
	mov sp,bp
	pop bp
	ret
	push ss:[bp+4]
_seg22:
	jmp far ptr _seg30
_seg23:
	mov ax,ss:[bp+4]
	mov dx,0
	mov bx,ss:[bp+6]
	div bx
	mov ss:[bp-8],ax
	push ss:[bp-8]
_seg24:
	mov ax,ss:[bp-8]
	mov bx,ss:[bp+6]
	mul bx
	mov ss:[bp-10],ax
	push ss:[bp-10]
_seg25:
	mov ax,ss:[bp+4]
	sub ax,ss:[bp-10]
	mov ss:[bp-12],ax
	push ss:[bp-12]
_seg26:
	mov ax,ss:[bp-12]
	push ax
_seg27:
	mov ax,ss:[bp+6]
	push ax
_seg28:
	call _gcd
	mov ss:[bp-14],ax
	push ss:[bp-14]
_seg29:
	mov ax,ss:[bp-14]
	mov sp,bp
	pop bp
	ret
	push ss:[bp-14]
_seg30:
	mov ax,0
	mov sp,bp
	pop bp
	ret
code ends
end start