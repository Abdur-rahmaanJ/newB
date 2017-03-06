# nameF is the format used for functions

import re
import configparser

conf = configparser.ConfigParser()

conf.read('custom.conf')

if1 = conf['KEYWORDS']['if1_setting']
if2 = conf['KEYWORDS']['if2_setting']
then = conf['KEYWORDS']['then_setting']
endcon = conf['KEYWORDS']['endcon_setting']
ask = conf['KEYWORDS']['ask_setting']
store = conf['KEYWORDS']['store_setting']
in1 = conf['KEYWORDS']['in_setting']
output = conf['KEYWORDS']['output_setting']

execfile = conf['FILE']['filename']

prim_operators =['+','-','/','*']
cond_operators = ['>','<','EQUAL']
conditionals = [if1,if2]

values={} 

def parseF(textlist):
    data=textlist
    incr_var = 0
    while incr_var < len(data) :
        def printF(nextRequiredToken,table):
            if nextRequiredToken in table :
                print( table[nextRequiredToken] )#printing the var by fetching the value
            elif 'STRING' or 'NUM' in nextRequiredToken :
                print( nextRequiredToken.replace('STRING','').replace('NUM','').strip() )
                
        def sanitiseF(inprog):
            inprog.replace('STRING','').replace("'",'').strip()

        
        def condopF(prev,nextt,cur_tok):
            if isinstance(prev,str) == True: 
                    sanitiseF(prev)
            if isinstance(nextt,str) == True:
                    sanitiseF(nextt)
        
            if prev in values :
                prev = values[prev] #fetching from dict
            elif prev.isdigit() == True :
                prev = float(prev)
            elif any (ext in prev for ext in prim_operators):
                prev=eval(prev)
                
            if nextt in values :
                nextt = values[nextt]
            elif nextt.isdigit() == True :
                nextt = float(nextt)
                
            if cur_tok == 'EQUAL':
                if prev == nextt :
                    if data[index+3] == 'OUTPUT':
                        printF(data[index+4],values)
            elif cur_tok == '>':
                if isinstance(prev,str) == True:
                    if prev.isdigit() == True:
                        prev=float(prev)
                if isinstance(nextt,str) == True:
                    if nextt.isdigit() == True:
                        nextt=float(nextt)
                if prev > nextt :
                    if data[index+3] == 'OUTPUT':
                        printF(data[index+4],values)
                        
            elif cur_tok == '<':
                if isinstance(prev,str) == True:
                    if prev.isdigit() == True:
                        prev=float(prev)
                if isinstance(nextt,str) == True:
                    if nextt.isdigit() == True:
                        nextt=float(nextt)
                if prev < nextt :
                    if data[index+3] == 'OUTPUT':
                        printF(data[index+4],values)
                    

        forwardIndex = incr_var + 1
        backwardIndex = incr_var - 1
        if forwardIndex >= len(data): #preventing out of bounds in array
            forwardIndex = incr_var

        cur_token = data[incr_var]
        next_token = data[forwardIndex]
        previous_token = data[backwardIndex]
        index=data.index(cur_token)
        #print('analysing :',cur_token) #debug

        part1_cond = '' #cond stands for conditional
        part2_cond = ''

        if cur_token == 'ASSIGN':
            values[previous_token] = next_token #adding to dict if x= 2 then output x

        elif cur_token in cond_operators:
                condopF(previous_token,next_token,cur_token)
                
        elif cur_token == 'PROMPT':            #ask 'gerg' store in x
                                               #x=input(next_token.replace('STRING','').replace("'",'').strip())
            x = input(sanitiseF(next_token))   #else appears with ''
            values[data[incr_var+4]] = x
            
        elif cur_token in prim_operators :
            cur_token = eval(cur_token) 

        elif cur_token == 'OUTPUT' and previous_token != 'THEN': #dealing with print
            if any (ext in next_token for ext in prim_operators):
                print( eval(next_token) )
            else:
                 printF(next_token,values)
                 
        elif any (ext in next_token for ext in prim_operators):
            print( eval(next_token) )
        
          
        incr_var+=1
        

            

def tokenF(load):
    data = load #takes in a list
    t_var=''
    incr_var=0


    while incr_var < len(data):
        cur_char = data[incr_var]
        index=data.index(cur_char)                  #get index of current char

        pattern=r"'(.)*'" #regex for string
        match= re.search(pattern,cur_char)
        
        if cur_char in conditionals :
            data[index] = 'COND '                    #
                                                     #cur_char.isdigit()==True:    # or unicode.isNumeric()
        elif cur_char == '=' and data[incr_var+1] != '=' and data[incr_var-1] != '=':
            data[index] = 'ASSIGN'

        elif cur_char == '=' and data[incr_var+1] == '=': #dealing with ==
            data[index] = 'EQUAL'
            data.remove('=')

        elif cur_char == endcon:
            data[index] = 'ENDCOND'

        elif cur_char == then :
            data[index] = 'THEN'

        elif cur_char == ask:
            data[index] = 'PROMPT'
            
        elif cur_char == output:
            data[index] = 'OUTPUT'
    
        elif match is not None:
            data[index] = 'STRING '+data[index]

        incr_var+=1

    return data

def splitF(feed):
    raw = feed
    rawChar = ['(',')','&','%','=',' ','\n',';','/*','*/','==','\t','>']
    formattedChar = [' ( ',' ) ',' & ',' % ',' = ','  ',' NEWLINE ',' ; ',' /* ',' */ ','dequal',' TAB ',' > '] #replace with space
    incr_var = 0
    while incr_var < len(rawChar):
        raw =''+raw.replace(rawChar[incr_var],formattedChar[incr_var])
        incr_var +=1
    return raw.split()

n = 0
print(' >welcome to the newB version 1 Interactive Prompt')
print(' >newB allows you to customise your own syntax, \nthus making the language your own')
while 1:
    n+=1
    #try:
    filecontent = input(str(n)+' >')
    #print('debug',splitF(filecontent))
    #print('debug',tokenF(splitF(filecontent)))
    parseF(tokenF(splitF(filecontent)))
    print('')
    #except:
        #print('terminated')                #real
#print(values)
#debug
