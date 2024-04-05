import statistics
from tqdm import tqdm


# 解决左递归
def left_dg(wf):
    wf_new = []
    for w in wf:
        zd = False
        w0 = w.split('->')[0]

        cnt = 0

        for c in w.split('->')[1].split('|'):
            c = [l for l in c.split(' ') if l != '']
            if w0 == c[0]:
                zd = True
                break
            cnt += 1
        if zd:
            print('存在左递归', w, end=' ')
            k = w.split('->')[1].split('|')[cnt]
            k = [l for l in k.split(' ') if l != '']
            k = ' '.join(k[k.index(w0) + 1:])
            h = ''
            for inde, o in enumerate(w.split('->')[1].split('|')):
                if inde != cnt:
                    h += o
            f1 = w0 + '->' + h + ' ' + w0 + '_'
            f2 = w0 + '_' + '->' + ' ' + k + ' ' + w0 + '_ ' + '| ε'
            wf_new.append(f1)
            wf_new.append(f2)
            print('已经修正为', f1, f2)

        else:
            wf_new.append(w)
    return wf_new


# p = left_dg(['E-> E + T | T', 'T-> T * F | F'])
# print(p)


# 解决回溯
def back_date(wf):
    wf_new = []
    for w in wf:
        l = w.split('->')[1]
        if '|' in l:
            if w.split('->')[0] == 'alphabet':
                sss = 0
            t = [s.split(' ')[1] for s in l.split('|')]
            t2 = list(set(t))
            if len(t2) < len(t):
                print('存在回溯', w, end=' ')
                gz = statistics.mode(t)
                index = 0
                for k in l:
                    if k == gz:
                        break
                    else:
                        index += 1

                f1 = l[:index + 1] + ' ' + w.split('->')[0] + '_'
                r = l[index + 1:]
                r = r.replace(gz, 'ε')
                f2 = w.split('->')[0] + '_' + '->' + r
                wf_new.append(f1)
                wf_new.append(f2)
                print('已经修正为', f1, f2)
            else:
                wf_new.append(w)
        else:
            wf_new.append(w)
    return wf_new


# 获取first集

def get_first(wf, pre):
    ''':arg
    :wf是传入的文法列表，形如 S-> func funcs
    pre 是bool值，若用于预测分析表，就置为True，一般的求first集合就置为false
    '''
    fz = [w.split('->')[0] for w in wf]
    fz_t = list(set(fz))  # 非终结符
    fz_t.sort(key=fz.index)
    fz = fz_t
    first = {}
    zl_cnt = 0
    for s in fz:
        first[s] = {}
        first[s]['zl'] = []
        first[s]['first'] = []
        first[s]['link'] = {}  # 辅助构建预测分析表
        first[s]['re_link'] = {}  # 辅助构建预测分析表
        first[s]['pre'] = {}  # 辅助构建预测分析表
        for w in wf:
            if w.split('->')[0] == s:
                t = [j for j in w.split('->')[1].split(' ') if j != '']
                if '|' not in t:
                    if t[0] not in fz:
                        first[s]['first'].append(t[0])
                        if t[0] not in first[s]['pre'].keys():
                            first[s]['pre'][t[0]] = [w.split('->')[1]]
                        else:
                            if w.split('->')[1] not in first[s]['pre'][t[0]]:
                                first[s]['pre'][t[0]].append(w.split('->')[1])
                    else:

                        if s != t[0] and t[0] not in first[s]['zl']:
                            zl_cnt += 1
                            first[s]['zl'].append(t[0])
                        if t[0] not in first[s]['link'].keys():
                            first[s]['link'][t[0]] = [w.split('->')[1]]
                        else:
                            if w.split('->')[1] not in first[s]['link'][t[0]]:
                                first[s]['link'][t[0]].append(w.split('->')[1])
                else:
                    te = w.split('->')[1].split('|')
                    cr = 0
                    for t in te:
                        if t[0] == ' ':
                            t = t[1:]
                        if t[0] not in fz:
                            first[s]['first'].append(t[0])
                            if t[0] not in first[s]['pre'].keys():
                                first[s]['pre'][t[0]] = [te[cr]]
                            else:
                                first[s]['pre'][t[0]].append(te[cr])
                        else:

                            if s != t[0] and t[0] not in first[s]['zl']:
                                first[s]['zl'].append(t[0])
                                zl_cnt += 1
                            if t[0] not in first[s]['link'].keys():
                                first[s]['link'][t[0]] = te[cr]
                            else:
                                first[s]['link'][t[0]].append(' ' + t)
                        cr += 1

    while True:
        for s in fz:
            for t in set(first[s]['zl'].copy()):
                if len(first[t]['zl']) == 0:

                    if 'ε' in first[t]['first']:
                        k = first[t]['first'].copy()
                        k.remove('ε')
                        re = k
                    else:
                        re = first[t]['first']

                    first[s]['zl'].remove(t)
                    zl_cnt -= 1
                    first[s]['first'].extend(re)
                    first[s]['first'] = list(set(first[s]['first']))
                    for m in set(re):
                        if m not in first[s]['re_link'].keys():
                            first[s]['re_link'][m] = [t]
                            first[s]['re_link'][m].append(t)
        if zl_cnt == 0:
            break
        else:
            pass
            # print(zl_cnt)
    if pre:
        for s in tqdm(first.keys()):
            for j in first[s]['re_link'].keys():
                for m in first[s]['re_link'][j]:
                    if j not in first[s]['pre'].keys():
                        first[s]['pre'][j] = first[s]['link'][m]
                    else:
                        first[s]['pre'][j].extend(first[s]['link'][m])
                        first[s]['pre'][j] = list(set(first[s]['pre'][j]))
    for s in tqdm(first.keys()):
        del first[s]['zl']
        del first[s]['link']
        del first[s]['re_link']
        if not pre:
            del first[s]['pre']
    import gc
    gc.collect()
    return first


# 辅助求follow集合的一个函数
def get_final(first, t, s, fz):
    # if len(t)==1 and t==s:
    Re = False
    if s in t:
        ind = t.index(s)
        for i in range(ind + 1, len(t)):
            if t[i] in fz and 'ε' in first[t[i]]['first']:
                Re = True
            else:
                Re = False
                break
    return Re


# 获取follow集合
def get_follow(wf, first):
    fz = [w.split('->')[0] for w in wf]
    fz_t = list(set(fz))
    fz_t.sort(key=fz.index)
    fz = fz_t

    follow = {}
    for s in fz:
        follow[s] = {}
        follow[s]['h'] = []
        follow[s]['q'] = []
        follow[s]['follow'] = []
        for w in wf:
            t = [j for j in w.split('->')[1].split(' ') if j != '']
            if s in t:
                if '|' not in t:
                    if s == t[-1] and w.split('->')[0] != s:
                        follow[s]['q'].append(w.split('->')[0])
                    ind = t.index(s)
                    if ind <= len(t) - 2:
                        if t[ind + 1] not in fz and t[ind + 1] != ' ' and t[ind + 1] != '_':
                            follow[s]['follow'].append(t[ind + 1])
                        else:
                            for i in range(ind + 1, len(t)):
                                if t[i] in fz and t[i] != s:
                                    follow[s]['h'].append(t[i])
                    if get_final(first, t, s, fz) and w.split('->')[0] != s:
                        follow[s]['q'].append(w.split('->')[0])

                else:
                    te = w.split('->')[1].split('|')
                    for t in te:
                        if s in t:

                            if s == t[-1] and w.split('->')[0] != s:
                                follow[s]['q'].append(w.split('->')[0])
                            if get_final(first, t, s, fz) and w.split('->')[0] != s:
                                follow[s]['q'].append(w.split('->')[0])

                            ind = t.index(s)
                            if ind <= len(t) - 3:
                                if t[ind + 2] not in fz and t[ind + 2] != ' ' and t[ind + 2] != '_':
                                    follow[s]['follow'].append(t[ind + 2])
                                else:
                                    t = [r for r in t.split(' ') if r != '']
                                    ind = t.index(s)
                                    for i in range(ind + 1, len(t)):
                                        if t[i] in fz and t[i] != s:
                                            follow[s]['h'].append(t[i])
    follow[fz[0]]['follow'].append('#')
    while True:
        change = False
        for s in fz:
            for t in set(follow[s]['h'].copy()):
                change = True
                if 'ε' in first[t]['first']:

                    k = first[t]['first'].copy()
                    k.remove('ε')
                    re = k
                else:
                    re = first[t]['first']
                follow[s]['follow'].extend(re)
                follow[s]['follow'] = list(set(follow[s]['follow']))
                follow[s]['h'].remove(t)

            for t in set(follow[s]['q'].copy()):
                if len(follow[t]['q']) == 0 and len(follow[t]['h']) == 0:
                    change = True
                    re = follow[t]['follow']
                    follow[s]['follow'].extend(re)
                    follow[s]['follow'] = list(set(follow[s]['follow']))
                    follow[s]['q'].remove(t)
        if not change:
            break

    return follow


# 判断是否位LL1文法
def is_LL1(first, follow):
    for a, s in first.items():
        x = set(s['first']).intersection(set(follow[a]))
        if 'ε' in s and len(x) != 0:
            print('该文法不满足LL1文法,请重新输入')
            return False
    return True


# 示例
with open('C grammar_') as f:
    wf_source = f.read()
wf = wf_source.split('\n')

first = get_first(wf, False)
follow = get_follow(wf, first)
follow = {f: g['follow'] for f, g in follow.items()}
# print(first)
print(is_LL1(first,follow))