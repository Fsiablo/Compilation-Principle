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
	_N dw 0
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
	mov ax,1
	mov _a,ax
_seg2:
	call _read
	mov es:[0],ax
_seg3:
	mov ax,es:[0]
	mov _N,ax
_seg4:
	mov ax,3
	push ax
_seg5:
	mov ax,4
	push ax
_seg6:
	call _sum
	mov es:[2],ax
_seg7:
	mov ax,es:[2]
	push ax
_seg8:
	mov ax,_N
	push ax
_seg9:
	call _sum
	mov es:[4],ax
_seg10:
	mov ax,es:[4]
	mov _a,ax
_seg11:
	mov ax,_a
	push ax
_seg12:
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

_sum:push bp
	mov bp,sp
	sub sp,2
_seg14:
	mov ax,ss:[bp+4]
	add ax,ss:[bp+6]
	mov es:[8],ax
_seg15:
	mov ax,es:[8]
	mov _result,ax
_seg16:
	mov ax,_result
	mov sp,bp
	pop bp
	ret
code ends
end start