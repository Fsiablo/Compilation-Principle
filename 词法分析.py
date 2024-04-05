num_kh = {'(': 0, '[': 0, '{': 0}
map_kh={')': '(', ']': '[', '}': '{'}
l_kh=[')',']','}']
l_0_7 = [str(i) for i in range(8)]
l_0_9 = [str(i) for i in range(10)]
l_a_f = [chr(i) for i in range(ord('a'), ord('f') + 1)]
l_a_z = [chr(i) for i in range(ord('a'), ord('z') + 1)]
l_sep=['{','}',';',',']
l_blank = ['\t', '\n', '\f', '\v', '\0', ' ']
l_opt = ['(',')','[',']','%','+', '-', '*', '/', '>', '<', '=', '!']
l_spe=['char', 'int', 'float', 'break', 'const', 'return', 'void', 'continue', 'do', 'while', 'if', 'else', 'for']
error=''
def RecognizeID(code,r,c,pos):
    st=pos
    while str.isalpha(code[pos]) or str.isnumeric(code[pos]) or code[pos]=='_':
        pos+=1
        c+=1
    if code[st:pos] in l_spe:
        typ=code[st:pos]
    else:
        typ='ID'
    return r,c,pos,code[st:pos],typ
def RecognizeOpt(code,r,c,pos):
    st=pos
    pos+=1
    c+=1
    if code[pos] in l_0_9 or str.lower(code[pos]) in l_a_z or code[pos]=='_' or code[pos] in l_blank or code[pos] in ['\"','\''] or code[pos] in l_kh or code[pos] in num_kh.keys():
        return r,c,pos,code[st:pos],code[st:pos]
    if code[st] in ['>','<','!','=','-','+']:
        if code[pos]=='=':
            pos+=1
            c+=1
            if code[pos] in l_0_9 or str.lower(code[pos]) in l_a_f or code[pos] == '_' or code[pos] in l_blank or code[pos] in ['\"','\''] or code[pos] in l_kh or code[pos] in num_kh.keys():
                return r, c, pos, code[st:pos], code[st:pos]
            else :
                return r, c, pos, code[st:pos+1],None
        elif code[st] == '+':
            if code[pos] == '+':
                pos += 1
                c += 1
                if code[pos] in l_0_9 or str.lower(code[pos]) in l_a_f or code[pos] == '_' or code[pos] in l_blank or code[pos] in ['\"','\''] or code[pos] in l_kh or code[pos] in num_kh.keys():
                    return r, c, pos, code[st:pos], code[st:pos]
                else:
                    return r, c, pos, code[st:pos+1], None
            else:
                return r, c, pos, code[st:pos+1], None
        elif code[st] == '-':
            if code[pos] == '-':
                pos += 1
                c += 1
                if code[pos] in l_0_9 or str.lower(code[pos]) in l_a_f or code[pos] == '_' or code[pos] in l_blank or code[pos] in ['\"','\''] or code[pos] in l_kh or code[pos] in num_kh.keys():
                    return r, c, pos, code[st:pos], code[st:pos]
                else:
                    return r, c, pos, code[st:pos+1], None
            else:
                return r, c, pos, code[st:pos+1], None
        else:
            return r, c, pos, code[st:pos+1],None
    elif code[st]=='&':
        if code[pos]=='&':
            pos+=1
            c+=1
            if code[pos] in l_0_9 or str.lower(code[pos]) in l_a_f or code[pos] == '_' or code[pos] in l_blank or code[pos] in ['\"','\''] or code[pos] in l_kh or code[pos] in num_kh.keys():
                return r, c, pos, code[st:pos], code[st:pos]
            else :
                return r, c, pos, code[st:pos+1],None
        else :
            return r, c, pos, code[st:pos+1],None
    elif code[st]=='|':
        if code[pos]=='|':
            pos+=1
            c+=1
            if code[pos] in l_0_9 or str.lower(code[pos]) in l_a_f or code[pos] == '_' or code[pos] in l_blank or code[pos] in ['\"','\''] or code[pos] in l_kh or code[pos] in num_kh.keys():
                return r, c, pos, code[st:pos], code[st:pos]
            else :
                return r, c, pos, code[st:pos+1],None
        else :
            return r, c, pos, code[st:pos+1],None
    else :
        return r, c, pos, code[st:pos+1],None
def RecognizeNum(code,r,c,pos):
    global Done
    st = pos
    def st12(code,r,c,st,pos):
        while code[pos] in l_0_9:
            pos += 1
            c += 1
        if code[pos] in l_blank or code[pos] in l_sep or code[pos] in l_opt:
            return r, c, pos, code[st:pos],'FLOAT'
        else:
            return r, c, pos, code[st:pos+1],None
    def st10(code,r,c,st,pos):
        if code[pos] in l_0_9:
            pos+=1
            c+=1
            return st12(code,r,c,st,pos)
        elif code[pos] in ['+','-']:
            pos+=1
            c+=1
            if code[pos] in l_0_9:
                pos+=1
                c+=1
                return st12(code,r,c,st,pos)
            else :
                return r, c, pos, code[st:pos+1],None
        else :
            return r, c, pos, code[st:pos+1],None
    def st8(code,r,c,st,pos):
        if code[pos] in l_0_9:
            pos+=1
            c+=1
            while code[pos] in l_0_9:
                pos+=1
                c+=1
            if str.lower(code[pos])=='e':
                pos+=1
                c+=1
                return st10(code,r,c,st,pos)
            elif code[pos] in l_blank or code[pos] in l_sep or code[pos] in l_opt:
                return r,c,pos,code[st:pos],'FLOAT'
            else:
                return r, c, pos, code[st:pos+1],None
        else :
            return r, c, pos, code[st:pos+1],None
    if code[pos]=='0':
        pos+=1
        c+=1
        while code[pos] in l_0_7:
            pos+=1
            c+=1
        if str.lower(code[pos])=='x':
            pos+=1
            c+=1
            if code[pos] in l_0_9 or str.lower(code[pos]) in l_a_f:
                pos += 1
                c += 1
                while code[pos] in l_0_9 or str.lower(code[pos]) in l_a_f:
                    pos+=1
                    c+=1
                if code[pos] not in l_blank:
                    return r,c,pos,code[st:pos+1],None
                return r,c,pos,code[st:pos],'INT_16'
            else :
                return r, c, pos, code[st:pos+1],None
        elif code[pos]=='.':
            pos+=1
            c+=1
            return st8(code,r,c,st,pos)
        elif code[pos] in l_blank or code[pos] in l_sep or code[pos] in l_opt:
            return r, c, pos, code[st:pos],'INT_8'
        elif str.lower(code[pos])=='e':
            pos += 1
            c += 1
            return st10(code,r,c,st,pos)
        else:
            return r, c, pos, code[st:pos+1],None
    elif code[pos] in l_0_9:
        pos += 1
        c += 1
        while code[pos] in l_0_9:
            pos+=1
            c+=1
        if code[pos] in l_blank or code[pos] in l_sep or code[pos] in l_opt:
            return r, c, pos, code[st:pos],'INT'
        elif str.lower(code[pos])=='e':
            pos += 1
            c += 1
            return st10(code,r,c,st,pos)
        elif code[pos]=='.':
            pos += 1
            c += 1
            return st8(code,r,c,st,pos)
        else :
            return r, c, pos, code[st:pos+1],None
    else :
        return r, c, pos, code[st:pos+1],None
def RecognizeNoteAndDiv(code,r,c,pos):
    st=pos
    pos+=1
    c+=1
    if code[pos]=='/':
        while pos<len(code) and code[pos]!='\n':
            pos+=1
            c+=1
        return r, c, pos, code[st:pos], '//'
    elif code[pos]=='*':
        pos+=1
        c+=1
        end=-1
        rem_r=0
        rem_c=c
        while pos<len(code)-1 :
            if (code[pos]=='*' and code[pos+1]=='/'):
                end=pos
                rem_r = r
                rem_c = c
            if (code[pos]=='/' and code[pos+1]=='*'):
                if end!=-1:
                    break
            pos+=1
            c+=1
            if code[pos]=='\n':
                c=0
                r+=1

        if end==-1:
            return r, c, pos, code[st:pos+1],None
        pos=end
        r=rem_r
        c=rem_c
        pos+=2
        c+=2
        return r, c, pos, code[st:pos], '/*'
    else:
        return r, c, pos, code[st:pos],'/'
def RecognizeChar(code,r,c,pos):
    st=pos
    pos+=1
    c+=1
    if code[pos]=='\'':
        pos+=1
        c+=1
        return r, c, pos, code[st:pos], 'CHAR'
    else:
        pos+=1
        c+=1
        if code[pos] == '\'':
            pos += 1
            c += 1
            return r, c, pos, code[st:pos], 'CHAR'
        else:
            return r, c, pos, code[st:pos+1],None
def RecognizeStr(code,r,c,pos):
    st = pos
    pos += 1
    c += 1
    while pos<len(code) and code[pos] != '\"':
        pos += 1
        c += 1
        if code[pos]=='\n':
            r+=1
            c=0
            pos-=1
            break
    if pos==len(code):
        return r, c, pos, code[st:pos + 1], None
    if code[pos]=='\"':
        pos+=1
        c+=1
        return r, c, pos, code[st:pos], 'STR'
    else:
        return r, c, pos, code[st:pos+1],None
def RecognizeOther(code,r,c,pos):
    st=pos
    r,c,pos,token,type=RecognizeOpt(code,r,c,pos)
    return r, c, pos, token, type
def RemoveBlank(code,r,c,pos):
    global error
    l_blank=['\t','\n','\f','\v','\0',' ']
    while pos<len(code) and code[pos] in l_blank:
        if code[pos]=='\n':
            if num_kh['(']!=0 or num_kh['[']!=0:
                error+=f'无法识别\t{r}行 {c}列\t括号不匹配\n'
            num_kh['(']=0
            num_kh['[']=0
            r += 1
            c = 0
        else:
            c=c+1
        pos=pos+1
    return r,c,pos
def init():
    with open('test.txt','r') as f:
        code=f.read()
    return code
def readFirst(code,r,c,pos):
    r,c,pos=RemoveBlank(code,r,c,pos)
    return r,c,pos
def analysisToken(code,r,c,pos,char):
    token=None
    typ=None
    if str.isalpha(char) or char=='_':
        try:
            r,c,pos,token,typ=RecognizeID(code,r,c,pos)
        except:
            print(f"ERROR:r{r},c{c}")
            return r,c,pos,token, typ
    elif str.isnumeric(char):
        try:
            r,c,pos,token,typ=RecognizeNum(code,r,c,pos)
        except:
            print(f"ERROR:r{r},c{c}")
            return r,c,pos,token, typ
    elif char=='/':
        try:
            r,c,pos,token,typ=RecognizeNoteAndDiv(code,r,c,pos)
        except:
            print(f"ERROR:r{r},c{c}")
            return r,c,pos,token, typ
    elif char=='\'':
        try:
            r, c, pos, token, typ = RecognizeChar(code, r, c, pos)
        except:
            print(f"ERROR:r{r},c{c}")
            return r, c, pos, token, typ
    elif char=='\"':
        try:
            r, c, pos, token, typ = RecognizeStr(code, r, c, pos)
        except:
            print(f"ERROR:r{r},c{c}")
            return r, c, pos, token, typ
    elif char in num_kh.keys():
        num_kh[char]+=1
        c+=1
        pos+=1
        return r,c,pos,char,char
    elif char in l_kh:
        num_kh[map_kh[char]]-=1
        pos+=1
        c+=1
        if num_kh[map_kh[char]]<0:
            return r, c, pos, char, None
        else:
            return r,c,pos,char,char
    else :
        try:
            r, c, pos, token, typ = RecognizeOther(code, r, c, pos)
        except:
            print(f"ERROR:r{r},c{c}")
            return r, c, pos, token, typ
    if typ=='//' or typ=='/*':
        token=typ
    return r,c,pos,token,typ
def RecognizeCode(code):
    global error
    for i in num_kh.keys():
        num_kh[i]=0
    code=code+' '
    results=''
    error=''
    with open('tokens','r') as f:
        tokens={i.split()[0]:i.split()[1] for i in f.read().split('\n')}
    r,c,pos=readFirst(code,0,0,0)
    r,c,pos,token,typ=analysisToken(code,r,c,pos,code[pos])
    try:
        if token=='//' or token=='/*':
            pass
        else:
            results += (f'r{r}\tc{c}\ttoken:{tokens[typ]}\t\t{token}\n')
    except:
        error  +=f'无法识别\t{r}行 {c}列\t{token}\n'
    while pos<len(code)-1:
        r, c, pos = readFirst(code, r, c, pos)
        if pos==len(code):
            break
        r, c, pos, token, typ = analysisToken(code, r, c, pos, code[pos])
        try:
            if token == '//' or token == '/*':
                pass
            else:
                results += (f'r{r}\tc{c}\ttoken:{tokens[typ]}\t\t{token}\n')
        except:
            error += f'无法识别\t{r}行 {c}列\t{token}\n'
    if num_kh['{']>0:
        error+=f'{r}行 {c}列\t括号不匹配\n'
    return results,error,r,c
