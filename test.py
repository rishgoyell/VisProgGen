validlist = []
def genparenthesis(openp, closep, currstr=""):
    if openp == 0:
        temp = ""
        for i in range(closep):
            temp = temp + ')'
        validlist.append(currstr+temp) 
        return
    elif currstr.count(")") > currstr.count("("):
        return
    genparenthesis(openp-1, closep, currstr+'(')
    genparenthesis(openp, closep-1, currstr+')')
    return
genparenthesis(0, 0)
for i in validlist:
    print(i)