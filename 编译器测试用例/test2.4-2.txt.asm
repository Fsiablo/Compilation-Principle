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
	_N dw 0
	_count dw 0
	_nprime dw 0
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
	call _read
	mov es:[0],ax
_seg2:
	mov ax,es:[0]
	mov _N,ax
_seg3:
	mov ax,0
	mov _count,ax
_seg4:
	mov ax,2
	mov _i,ax
_seg5:
	mov dx,1
	mov ax,_i
	cmp ax,_N
	jle _le1
	mov dx,0
_le1: mov es:[2],dx
_seg6:
	mov ax,es:[2]
	cmp ax,0
	je _ez1
	jmp far ptr _seg8
_ez1: nop
_seg7:
	jmp far ptr _seg25
_seg8:
	mov ax,0
	mov _nprime,ax
_seg9:
	mov ax,2
	mov ss:[bp+4],ax
	push ss:[bp+4]
_seg10:
	mov dx,1
	mov ax,ss:[bp+4]
	cmp ax,_i
	jl _gt1
	mov dx,0
_gt1: mov es:[4],dx
_seg11:
	mov ax,es:[4]
	cmp ax,0
	je _ez2
	jmp far ptr _seg13
_ez2: nop
_seg12:
	jmp far ptr _seg22
_seg13:
	mov ax,_i
	mov dx,0
	mov bx,ss:[bp+4]
	div bx
	mov es:[6],dx
_seg14:
	mov dx,1
	mov ax,es:[6]
	cmp ax,0
	je _eq1
	mov dx,0
_eq1: mov es:[8],dx
_seg15:
	mov ax,es:[8]
	cmp ax,0
	je _ez3
	jmp far ptr _seg17
_ez3: nop
_seg16:
	jmp far ptr _seg19
_seg17:
	mov ax,_nprime
	add ax,1
	mov es:[10],ax
_seg18:
	mov ax,es:[10]
	mov _nprime,ax
_seg19:
	mov ax,ss:[bp+4]
	add ax,1
	mov es:[12],ax
_seg20:
	mov ax,es:[12]
	mov ss:[bp+4],ax
	push ss:[bp+4]
_seg21:
	jmp far ptr _seg10
_seg22:
	mov ax,_i
	add ax,1
	mov es:[14],ax
_seg23:
	mov ax,es:[14]
	mov _i,ax
_seg24:
	jmp far ptr _seg5
_seg25:
	mov dx,1
	mov ax,_nprime
	cmp ax,0
	je _eq2
	mov dx,0
_eq2: mov es:[16],dx
_seg26:
	mov ax,es:[16]
	cmp ax,0
	je _ez4
	jmp far ptr _seg28
_ez4: nop
_seg27:
	jmp far ptr _seg32
_seg28:
	mov ax,_i
	push ax
_seg29:
	call _write
	mov es:[18],ax
	call dsp
_seg30:
	mov ax,_count
	add ax,1
	mov es:[20],ax
_seg31:
	mov ax,es:[20]
	mov _count,ax
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

code ends
end start