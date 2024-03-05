import re

keyWords = "acadena|alogico|anumero|leer|limpiar|caso|cierto|verdadero|defecto|otro|desde|elegir|error|escribir|imprimir|poner|falso|fin|funcion|fun|hasta|imprimirf|mientras|nulo|osi|repetir|retorno|retornar|ret|romper|si|sino|tipo|rango|si|sino|fun|funcion|para|en"

operators = {"(&&)": "and", "(\|\|)": "or", "(..)": "concat", "(\.)": "period", "(\,)": "comma", "(;)": "semicolon","(:)": "colon", "(\{)": "opening_key", "(\})": "closing_key", "(\[)": "opening_bra", "(\])": "closing_bra", "(\()": "opening_par", "(\))": "closing_par", "(\++)": "increment", "(--)": "decrement", "(%=)": "mod_assign", "(/=)": "div_assign", "(\*=)": "times_assign", "(-=)": "minus_assign", "(\+=)": "plus_assign", "(\+)": "plus", "(-)": "minus", "(\*)": "times", "(/)": "div", "(\^)": "power", "(%)": "mod", "(<=)": "leq", "(>=)": "geq", "(==)": "equal", "(!=)": "neq", "(<)": "less", "(>)": "greater", "(=)": "assign", "(!)": "not", "(~=)": "regex"}
operatorsKeys = "|".join(operators.keys())


file = open('example.txt', 'r')
lines = file.readlines()
file.close()

def maximalToken(line, flag, j):
    if (j+2 == len(line)):
        return True
    elif (line[j+1] == " "):
        return True
    if (re.match(operatorsKeys, line[j+1])):
        print(re.match(operatorsKeys, line[j+1]))
        return True
    else:
        return False
    

for i in range(len(lines)):
    flag = 0
    line = lines[i]
    #print(i,line)
    if not line.strip():
        continue
    for j in range(0,len(line)):
        ##print(line[flag:j], flag, j, len(line))
        if (re.match(keyWords, line[flag:j+1])):
            print(line[flag:j+1], flag, j, len(line))
            if (maximalToken(line, flag, j)):
                print("<"+line[flag:j+1]+","+str(i+1)+","+str(flag+1)+">")
                flag = j+1
            else:
                continue
            
            
        elif (line[j] == " "):
            flag = j+1
        ##elif(re.match)


       