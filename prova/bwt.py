
def bwt(stringa):
    stringa+="$"
    matrice = []
    for i in range(len(stringa)):
        matrice.append(stringa)
        stringa = stringa[1:] + stringa[0]
    matrice.sort()
    result = ""
    for i in range(len(stringa)):
        result+=matrice[i][len(stringa)-1]
    return result
    
stringa=input()
bwtransform = bwt(stringa)
print(bwtransform)