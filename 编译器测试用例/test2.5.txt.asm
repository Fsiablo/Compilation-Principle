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
	_i dw 0
	_j dw 0
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
	mov _n,ax
_seg2:
	mov ax,0
	mov _i,ax
_seg3:
	mov ax,0
	mov _j,ax
_seg4:
	call _read
	mov es:[0],ax
_seg5:
	mov ax,es:[0]
	mov _n,ax
_seg6:
	mov ax,_n
	push ax
_seg7:
	call _write
	mov es:[2],ax
	call dsp
_seg8:
	mov ax,2
	mov _i,ax
_seg9:
	mov dx,1
	mov ax,_i
	cmp ax,_n
	jl _gt1
	mov dx,0
_gt1: mov es:[4],dx
_seg10:
	mov ax,es:[4]
	cmp ax,0
	je _ez1
	jmp far ptr _seg12
_ez1: nop
_seg11:
	jmp far ptr _seg32
_seg12:
	mov ax,2
	mov _j,ax
_seg13:
	mov dx,1
	mov ax,_j
	cmp ax,_i
	jl _gt2
	mov dx,0
_gt2: mov es:[6],dx
_seg14:
	mov ax,es:[6]
	cmp ax,0
	je _ez2
	jmp far ptr _seg16
_ez2: nop
_seg15:
	jmp far ptr _seg24
_seg16:
	mov ax,_i
	mov dx,0
	mov bx,_j
	div bx
	mov es:[8],dx
_seg17:
	mov dx,1
	mov ax,es:[8]
	cmp ax,0
	je _eq1
	mov dx,0
_eq1: mov es:[10],dx
_seg18:
	mov ax,es:[10]
	cmp ax,0
	je _ez3
	jmp far ptr _seg20
_ez3: nop
_seg19:
	jmp far ptr _seg21
_seg20:
	jmp far ptr _seg24
_seg21:
	mov ax,_j
	add ax,1
	mov es:[12],ax
_seg22:
	mov ax,es:[12]
	mov _j,ax
_seg23:
	jmp far ptr _seg13
_seg24:
	mov dx,1
	mov ax,_j
	cmp ax,_i
	je _eq2
	mov dx,0
_eq2: mov es:[14],dx
_seg25:
	mov ax,es:[14]
	cmp ax,0
	je _ez4
	jmp far ptr _seg27
_ez4: nop
_seg26:
	jmp far ptr _seg29
_seg27:
	mov ax,_i
	push ax
_seg28:
	call _write
	mov es:[16],ax
	call dsp
_seg29:
	mov ax,_i
	add ax,1
	mov es:[18],ax
_seg30:
	mov ax,es:[18]
	mov _i,ax
_seg31:
	jmp far ptr _seg9
_seg32:
	mov dx,1
	mov ax,_j
	cmp ax,_i
	je _eq3
	mov dx,0
_eq3: mov es:[20],dx
_seg33:
	mov ax,es:[20]
	cmp ax,0
	je _ez5
	jmp far ptr _seg35
_ez5: nop
_seg34:
	jmp far ptr quit
_seg35:
	mov ax,_i
	push ax
_seg36:
	call _write
	mov es:[22],ax
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

code ends
end start