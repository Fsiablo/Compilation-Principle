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
	_a dw 0
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
	mov _m,ax
_seg3:
	call _read
	mov es:[2],ax
_seg4:
	mov ax,es:[2]
	mov _k,ax
_seg5:
	mov ax,_k
	push ax
_seg6:
	mov ax,_m
	push ax
_seg7:
	call _comp
	mov es:[4],ax
_seg8:
	mov ax,es:[4]
	mov _result,ax
_seg9:
	mov ax,_result
	push ax
_seg10:
	call _write
	mov es:[6],ax
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

_comp:push bp
	mov bp,sp
	sub sp,2
_seg12:
	mov dx,1
	mov ax,ss:[bp+4]
	cmp ax,ss:[bp+6]
	je _eq1
	mov dx,0
_eq1: mov es:[8],dx
_seg13:
	mov dx,1
	mov ax,ss:[bp+6]
	cmp ax,0
	je _eq2
	mov dx,0
_eq2: mov es:[10],dx
_seg14:
	mov dx,1
	mov ax,es:[8]
	cmp ax,0
	jne _or1
	mov ax,es:[10]
	cmp ax,0
	jne _or1
	mov dx,0
_or1: mov es:[12],dx
_seg15:
	mov ax,es:[12]
	cmp ax,0
	je _ez1
	jmp far ptr _seg17
_ez1: nop
_seg16:
	jmp far ptr _seg18
_seg17:
	mov ax,1
	mov sp,bp
	pop bp
	ret
_seg18:
	mov ax,ss:[bp+4]
	sub ax,1
	mov es:[14],ax
_seg19:
	mov ax,ss:[bp+6]
	push ax
_seg20:
	mov ax,es:[14]
	push ax
_seg21:
	call _comp
	mov es:[16],ax
_seg22:
	mov ax,ss:[bp+4]
	sub ax,1
	mov es:[18],ax
_seg23:
	mov ax,ss:[bp+6]
	sub ax,1
	mov es:[20],ax
_seg24:
	mov ax,es:[20]
	push ax
_seg25:
	mov ax,es:[18]
	push ax
_seg26:
	call _comp
	mov es:[22],ax
_seg27:
	mov ax,es:[16]
	add ax,es:[22]
	mov es:[24],ax
_seg28:
	mov ax,es:[24]
	mov _a,ax
_seg29:
	mov ax,_a
	mov sp,bp
	pop bp
	ret
code ends
end start