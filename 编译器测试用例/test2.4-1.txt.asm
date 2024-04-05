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
	_j dw 0
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
	mov _n,ax
_seg2:
	call _read
	mov es:[0],ax
_seg3:
	mov ax,es:[0]
	mov _n,ax
_seg4:
	mov ax,0
	mov _i,ax
_seg5:
	mov dx,1
	mov ax,_i
	cmp ax,_n
	jl _gt1
	mov dx,0
_gt1: mov es:[2],dx
_seg6:
	mov ax,es:[2]
	cmp ax,0
	je _ez1
	jmp far ptr _seg8
_ez1: nop
_seg7:
	jmp far ptr _seg34
_seg8:
	mov ax,0
	mov _j,ax
_seg9:
	mov ax,_n
	sub ax,_i
	mov es:[4],ax
_seg10:
	mov ax,es:[4]
	sub ax,1
	mov es:[6],ax
_seg11:
	mov dx,1
	mov ax,_j
	cmp ax,es:[6]
	jl _gt2
	mov dx,0
_gt2: mov es:[8],dx
_seg12:
	mov ax,es:[8]
	cmp ax,0
	je _ez2
	jmp far ptr _seg14
_ez2: nop
_seg13:
	jmp far ptr _seg19
_seg14:
	mov ax,' '
	push ax
_seg15:
	call _write
	mov es:[10],ax
	call dispcrlf
_seg16:
	mov ax,_j
	add ax,1
	mov es:[12],ax
_seg17:
	mov ax,es:[12]
	mov _j,ax
_seg18:
	jmp far ptr _seg11
_seg19:
	mov ax,0
	mov _j,ax
_seg20:
	mov ax,_i
	add ax,1
	mov es:[14],ax
_seg21:
	mov dx,1
	mov ax,_j
	cmp ax,es:[14]
	jl _gt3
	mov dx,0
_gt3: mov es:[16],dx
_seg22:
	mov ax,es:[16]
	cmp ax,0
	je _ez3
	jmp far ptr _seg24
_ez3: nop
_seg23:
	jmp far ptr _seg29
_seg24:
	mov ax,'*'
	push ax
_seg25:
	call _write
	mov es:[18],ax
	call dispcrlf
_seg26:
	mov ax,_j
	add ax,1
	mov es:[20],ax
_seg27:
	mov ax,es:[20]
	mov _j,ax
_seg28:
	jmp far ptr _seg21
_seg29:
	mov ax,'
'
	push ax
_seg30:
	call _write
	mov es:[22],ax
	call dispcrlf
_seg31:
	mov ax,_i
	add ax,1
	mov es:[24],ax
_seg32:
	mov ax,es:[24]
	mov _i,ax
_seg33:
	jmp far ptr _seg5
_seg34:
	mov ax,0
	mov _j,ax
_seg35:
	mov ax,_i
	add ax,1
	mov es:[26],ax
_seg36:
	mov dx,1
	mov ax,_j
	cmp ax,es:[26]
	jl _gt4
	mov dx,0
_gt4: mov es:[28],dx
_seg37:
	mov ax,es:[28]
	cmp ax,0
	je _ez4
	jmp far ptr _seg39
_ez4: nop
_seg38:
	jmp far ptr _seg44
_seg39:
	mov ax,'*'
	push ax
_seg40:
	call _write
	mov es:[30],ax
	call dispcrlf
_seg41:
	mov ax,_j
	add ax,1
	mov es:[32],ax
_seg42:
	mov ax,es:[32]
	mov _j,ax
_seg43:
	jmp far ptr _seg36
_seg44:
	mov ax,'
'
	push ax
_seg45:
	call _write
	mov es:[34],ax
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
    test ax,ax;�ж����㡢��������
    jnz dsiw1;�����㣬��ת
    mov dl,'0'
    mov ah,2
    int 21h
    jmp dsiw5;ת����ʾ
dsiw1:jns dsiw2;����������ת
    mov bx,ax
    mov dl,'-';�Ǹ�������ʾ����
    mov ah,2
    int 21h
    mov ax,bx
    neg ax;�����󲹣�����ֵ��
dsiw2:mov bx,10
    push bx;10ѹ���ջ����Ϊ�˳���־
dsiw3:cmp ax,0  ;���ݣ��̣�Ϊ�㣬ת�򱣴�
    jz dsiw4
    xor dx,dx   ;��չ������ΪDX.AX
    div bx  ;���ݳ���10��DX.AX��10
    add dl,30h  ;������0��9��ת��ΪASCII
    push dx ;�����ȵ�λ���λѹ���ջ
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
    mov dl,0dh  ;����س��ַ�
    mov ah,2
    int 21h
    mov dl, 0ah  ;��������ַ�
    int 21h
    pop dx
    pop ax
    ret
ex: mov al,4ch
    int 21h

code ends
end start