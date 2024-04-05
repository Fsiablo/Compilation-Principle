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
	_a dw 0
	_b dw 0
	_c dw 0
	_d dw 0
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
	mov ax,2
	mov _x,ax
_seg2:
	mov ax,3
	mov _y,ax
_seg3:
	mov dx,0
	mov ax,_x
	cmp ax,0
	je _and1
	mov ax,_y
	cmp ax,0
	je _and1
	mov dx,1
_and1: mov es:[0],dx
_seg4:
	mov ax,es:[0]
	mov _a,ax
_seg5:
	mov ax,_x
	add ax,2
	mov es:[2],ax
_seg6:
	mov ax,0
	mov bx,2
	mul bx
	mov es:[4],ax
_seg7:
	mov dx,0
	mov ax,es:[2]
	cmp ax,0
	je _and2
	mov ax,es:[4]
	cmp ax,0
	je _and2
	mov dx,1
_and2: mov es:[6],dx
_seg8:
	mov dx,1
	mov ax,2
	cmp ax,ss:[bp+4]
	je _eq1
	mov dx,0
_eq1: mov es:[8],dx
_seg9:
	mov dx,1
	mov ax,es:[6]
	cmp ax,0
	jne _or1
	mov ax,es:[8]
	cmp ax,0
	jne _or1
	mov dx,0
_or1: mov es:[10],dx
_seg10:
	mov ax,es:[10]
	mov _b,ax
_seg11:
	mov dx,1
	mov ax,_x
	cmp ax,0
	jne _or2
	mov ax,_y
	cmp ax,0
	jne _or2
	mov dx,0
_or2: mov es:[12],dx
_seg12:
	mov ax,es:[12]
	mov _c,ax
_seg13:
	mov dx,1
	mov ax,_x
	cmp ax,0
	jne _or3
	mov ax,0
	cmp ax,0
	jne _or3
	mov dx,0
_or3: mov es:[14],dx
_seg14:
	mov ax,es:[14]
	mov _d,ax
_seg15:
	mov ax,_a
	push ax
_seg16:
	call _write
	mov es:[16],ax
	call dispcrlf
_seg17:
	mov ax,_b
	push ax
_seg18:
	call _write
	mov es:[18],ax
	call dispcrlf
_seg19:
	mov ax,_c
	push ax
_seg20:
	call _write
	mov es:[20],ax
	call dispcrlf
_seg21:
	mov ax,_d
	push ax
_seg22:
	call _write
	mov es:[22],ax
	call dispcrlf
quit:
	mov ah,4ch
	int 21h
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