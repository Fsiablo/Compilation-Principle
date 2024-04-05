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
	_m dw 0
	_k dw 0
	_result dw 0
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
	mov ax,666
	mov _result,ax
_seg2:
	call _read
	mov es:[0],ax
_seg3:
	mov ax,es:[0]
	mov _m,ax
_seg4:
	call _read
	mov es:[2],ax
_seg5:
	mov ax,es:[2]
	mov _k,ax
_seg6:
	mov dx,1
	mov ax,_m
	cmp ax,_k
	jl _gt1
	mov dx,0
_gt1: mov es:[4],dx
_seg7:
	mov dx,1
	mov ax,_m
	cmp ax,0
	jne _ne1
	mov dx,0
_ne1: mov es:[6],dx
_seg8:
	mov dx,1
	mov ax,es:[4]
	cmp ax,0
	jne _or1
	mov ax,es:[6]
	cmp ax,0
	jne _or1
	mov dx,0
_or1: mov es:[8],dx
_seg9:
	mov dx,1
	mov ax,_k
	cmp ax,1
	je _eq1
	mov dx,0
_eq1: mov es:[10],dx
_seg10:
	mov dx,0
	mov ax,es:[8]
	cmp ax,0
	je _and1
	mov ax,es:[10]
	cmp ax,0
	je _and1
	mov dx,1
_and1: mov es:[12],dx
_seg11:
	mov ax,es:[12]
	cmp ax,0
	je _ez1
	jmp far ptr _seg13
_ez1: nop
_seg12:
	jmp far ptr quit
_seg13:
	mov ax,_result
	push ax
_seg14:
	call _write
	mov es:[14],ax
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