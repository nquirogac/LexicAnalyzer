import re
import sys

keyWords = "acadena|alogico|anumero|leer|limpiar|caso|cierto|verdadero|defecto|otro|desde|elegir|error|escribir|imprimir|poner|falso|fin|funcion|fun|hasta|imprimirf|mientras|nulo|osi|repetir|retorno|retornar|ret|romper|tipo|rango|si|sino|fun|funcion|para|en|regresar"

operators = {"&&": "and", "\|\|": "or", "\.\.": "concat", "\.": "period", "\,": "comma", ";": "semicolon",":": "colon", "\{": "opening_key", "\}": "closing_key", "\[": "opening_bra", "\]": "closing_bra", "\(": "opening_par", "\)": "closing_par", "(\+\+)": "increment", "\-\-": "decrement", "%=": "mod_assign", "/=": "div_assign", "\*=": "times_assign", "-=": "minus_assign", "\+=": "plus_assign", "\+": "plus", "-": "minus", "\*": "times", "/": "div", "\^": "power", "%": "mod", "<=": "leq", ">=": "geq", "==": "equal", "!=": "neq", "<": "less", ">": "greater", "=": "assign", "!": "not", "~=": "regex"}
operatorsKeys = "|".join(operators.keys())

idsRegex = "^[a-zA-Z_][a-zA-Z0-9_]*" 
commentsRegex = "//|#"
multiLineCommentsRegex = r'/\*(.*?)\*/' 
numbersRegex = "\d+(\.\d+)?"
stringRegex = r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\''

linesAsText = sys.stdin.read()
lines = linesAsText.split("\n")

def maximalToken(line, flag, j, num=False):
    if (j+1 == len(line)):
        return True
    elif (j+1 < len(line) ):              #if the token is a space
        if (line[j+1] == " "): 
            return True
        elif (line[j+1] == "\n"): 
            return True     
        elif ((re.match(operatorsKeys, line[j+1]) or re.match(commentsRegex, line[j+1:j+2])) and not num):
            return True
        elif(num):
                
            if (re.match("\d", line[j+1])):
                return False
            elif (re.match("\.", line[j+1])) and maximalToken(line, flag, j+1, True):
                return True 
            elif (re.fullmatch(numbersRegex, line[flag:j+3]))==None:
                return True
        else:
                
            if (re.match("\w", line[j+1])) and (re.match(r'[^\WñçáéíóúÁÉÍÓÚüÜ]', line[j+1])):
                return False
            else:
                return True
    else:
        return False

def findOperators(line, flag, j):
    for key in operators:
        if(re.fullmatch(key, line[flag:j+1])):
            print("<tkn_"+operators[key]+","+str(i+1)+","+str(flag+1)+">")
              
def defineOperators(line, flag, j):
    
    if (j+1 == len(line)):
        findOperators(line, flag, j)
        return True
    elif (j+1 <= len(line) and ((line[j+1] == " ") or (line[j+1] == "\n") or (j+1 == len(line)))):              #if the token is a space
       
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

def defineMultiLineComments(line, flag, j):
    comentarios = re.findall(multiLineCommentsRegex, linesAsText, re.DOTALL)
    if len(comentarios) == 0:    
        return False
    elif '/*' in comentarios[0] or '*/' in comentarios[0]:     
        return False
    return True

ignore = False
romper = False
for i in range(len(lines)):
    flag = 0
    line = lines[i]
    contador = 0
    
    if not line.strip():
        continue
    
    for j in range(0,len(line)):    
        
        if (re.fullmatch(keyWords, line[flag:j+1])):           #if the token is a keyword
            
            if ignore:
                continue 
            elif (maximalToken(line, flag, j)):
                print("<"+line[flag:j+1]+","+str(i+1)+","+str(flag+1)+">")
                flag = j+1
                
            else:
                continue  
        elif (re.match(commentsRegex, line[flag:j+2])):         #if the token is a comment
            if ignore:
                continue 
            
            else:
                break
        elif(re.match(operatorsKeys, line[flag:j+1]) or re.match(operatorsKeys, line[flag:j+2]) or ignore):     #if the token is an operator or special character
            
            if (re.match(r'/\*', line[flag:j+2])) and not ignore:
                if(not defineMultiLineComments(line, flag, j)):
                    
                    print(">>> Error lexico (linea:", str(i+1)+ ", posicion:", str(flag+1)+")")
                    romper = True
                    break
                else:
                    
                    linesAsText = '\n'.join(linesAsText.split("\n")[1:])
                    ignore = True
                    flag = j+1
            elif (re.search('\*/', line[flag:j+1])) and ignore:
                ignore = False
                flag = j+1
            #elif (re.match(r'\*/', line[flag:j+2])) and not ignore:
                
                #romper = True
                #break
            elif not ignore:
                if defineOperators(line, flag, j):
                    flag = j+1
            else:
                
                continue        
        
        elif (re.match(idsRegex, line[flag:j+1])):                  #if the token is an identifier
            
            if ignore:
                continue      
            elif (maximalToken(line, flag, j)):
                
                print("<id,"+line[flag:j+1]+","+str(i+1)+","+str(flag+1)+">")
                flag = j+1
            else:
                continue
        elif (re.match(numbersRegex, line[flag:j+1])):     #if the token is a number
            
            if ignore:
                continue 
            elif(maximalToken(line, flag, j, True)):
                print("<tkn_real,"+line[flag:j+1]+","+str(i+1)+","+str(flag+1)+">")
                flag = j+1
        
        elif len(re.findall(stringRegex, line[flag:len(line)])) > 0 and re.match((r'"|\''), line[flag]) and not ignore:  #if the token is a string
            
            if ignore:
                continue                                          
            elif contador==0 :
                
                if re.match((r'"|\''), line[j]) and j!=flag:
                    flag = flag + len(foundStrings[0])
                else:
                    foundStrings = re.findall(stringRegex, line[flag:len(line)])
                    cadena = foundStrings[0]
                    
                    if re.match('"', line[flag]):
                        cadena = re.sub(r'\\\'', "'", cadena)
                    elif re.match('\'', line[flag]):
                        cadena = re.sub(r'\\\"', '"', cadena)
                    cadena = cadena[1:-1]
                    contador = len(foundStrings[0])-2
                    print("<tkn_str,"+cadena+","+str(i+1)+","+str(flag+1)+">")

            else:
                contador = contador - 1
                
        
        elif (j+1 <= len(line)) and ((line[j] == " ") or (line[j] == "\t") or (line[j] == "\n")):                           #if the token is a space
            
            flag = j+1
        
        else:
            
            if not ignore:
                print(">>> Error lexico (linea:", str(i+1)+ ", posicion:", str(flag+1)+")")
                romper = True
                break
    linesAsText = '\n'.join(linesAsText.split("\n")[1:])
    if linesAsText.split("\n")[0] == "" or linesAsText.split("\n")[0] == "\n":
        linesAsText = '\n'.join(linesAsText.split("\n")[1:])

    if romper:
        break