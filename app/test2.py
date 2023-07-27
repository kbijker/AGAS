

def checknaam(naamschepse):
    check = True
    for letter in naamschepse:
        if letter in 'abcdefghijklmnopqrstuvwxyz ':
            continue
        else: 
            check = False
            return check
    return check

vw = checknaam('Ijsvogel')
if vw: print('goed')
else: print('fout') 