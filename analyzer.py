import re

keyWords = "acadena|alogico|anumero|leer|limpiar|caso|cierto|verdadero|defecto|otro|desde|elegir|error|escribir|imprimir|poner|falso|fin|funcion|fun|hasta|imprimirf|mientras|nulo|osi|repetir|retorno|retornar|ret|romper|si|sino|tipo|rango|si|sino|fun|funcion|para|en"

operators = {"&&": "and", "\|\|": "or", "\.\.": "concat", "\.": "period", "\,": "comma", ";": "semicolon",":": "colon", "\{": "opening_key", "\}": "closing_key", "\[": "opening_bra", "\]": "closing_bra", "\(": "opening_par", "\)": "closing_par", "(\+\+)": "increment", "\-\-": "decrement", "%=": "mod_assign", "/=": "div_assign", "\*=": "times_assign", "-=": "minus_assign", "\+=": "plus_assign", "\+": "plus", "-": "minus", "\*": "times", "/": "div", "\^": "power", "%": "mod", "<=": "leq", ">=": "geq", "==": "equal", "!=": "neq", "<": "less", ">": "greater", "=": "assign", "!": "not", "~=": "regex"}
operatorsKeys = "|".join(operators.keys())

idsRegex = "^[a-zA-Z_][a-zA-Z0-9_]*" 
commentsRegex = "//|#"
multiLineCommentsRegex = "^(/*)."


file = open('example.txt', 'r')
lines = file.readlines()
file.close()

def maximalToken(line, flag, j):
    if (j+1 == len(line)):
        return True
    elif (j+1 < len(line) ):              #if the word is a space
            if (line[j+1] == " "): 
                return True
            elif (line[j+1] == "\n"): 
                return True     
            elif (re.match(operatorsKeys, line[j+1])):
                return True
    else:
        return False

def findOperators(line, flag, j):
    for key in operators:
        if(re.match(key, line[flag:j+1])):
            print("<tkn_"+operators[key]+","+str(i+1)+","+str(flag+1)+">")
              
def defineOperators(line, flag, j):
    #print(1,line[flag:j+1], flag, j, len(line))
    if (j+1 <= len(line) and ((line[j+1] == " ") or (line[j+1] == "\n") or (j+1 == len(line)))):              #if the word is a space
        findOperators(line, flag, j)
        return True
    elif (re.match(commentsRegex, line[flag:j+2])): 
        print("comentario")  
        return False  
    elif  re.match("\w+", line[j+1]):
        findOperators(line, flag, j) 
        return True  
    elif (re.fullmatch(operatorsKeys, line[flag:j+2])==None):
        findOperators(line, flag, j) 
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
        #print(line[flag:j+1], flag, j, len(line))
        if (re.match(keyWords, line[flag:j+1])):                 #if the word is a keyword
            #print(line[flag:j+1], flag, j, len(line))
            if (maximalToken(line, flag, j)):
                print("<"+line[flag:j+1]+","+str(i+1)+","+str(flag+1)+">")
                flag = j+1
                
                #print(flag,j, len(line))
            else:
                continue  
        elif (re.match(commentsRegex, line[flag:j+2])):
            print("comentario")
            break
        elif(re.match(operatorsKeys, line[flag:j+1])):            #if the word is an operator or special character
            #print("ddd")
            if(defineOperators(line, flag, j)):
                flag = j+1
            else:
                continue 
        
        elif (re.match(idsRegex, line[flag:j+1])):              #if the word is an identifier
            if (maximalToken(line, flag, j)):
                #print("dfs",line[flag:j+1], flag, j, len(line))
                print("<id,"+line[flag:j+1]+","+str(i+1)+","+str(flag+1)+">")
                flag = j+1
            else:
                continue
        elif (j+1 < len(line) ):              #if the word is a space
            if (line[j] == " "):  
                flag = j+1
        