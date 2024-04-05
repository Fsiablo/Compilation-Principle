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
data ends
code segment
start: mov ax,extended
	mov es,ax
	mox ax,stack
	mov ss,ax
	mov sp,1024
	mov bp,sp
	mov ax,data
	mov ds,ax
	mov a,1
	call read
	mov N,temp1
	call read
	mov M,temp2
	mov dx,1
	mov ax,M
	cmp ax,0
	je _not1
	mov dx,0
	mov dx,1
	mov ax,temp3
	cmp ax,N
	jnb _ge1
	mov dx,0
	mov ax,temp4
	cmp ax,0
	je _ez1
	jmp far ptr 10
	jmp far ptr 12
	mov result,M
	jmp far ptr 13
	mov result,N
	mov ax,result
	add ax,100
	mov temp5,ax
	mov a,temp5
	mov ax,a
	push ax
	call write
quit: mov,ah,4ch
	int 21h
_not1: mov temp3,dx
_ge1: mov temp4,dx
_ez1: nop
code ends
end start