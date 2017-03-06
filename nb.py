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
conditionals = [if1,if2] #then replaces the : as in if x=3 :

with open(execfile,'r+') as f:
	filecontent = f.read()+' eof'

values={} #global so as to be accessible from funcs

def parseF(textlist):
	data=textlist
	#new_data = textlist.remove('NEWLINE')
	incr_var = 0
	while incr_var < len(data) :
		if incr_var == 0: #start message
			print('*** newB execution started')
			print('*** taking commands from',execfile,'\n')
			

		def printF(nextRequiredToken,table):
			if nextRequiredToken in table :
				print(table[nextRequiredToken]) #printing the var by fetching the value
			else :
				print(nextRequiredToken.replace('STRING','').replace('NUM','').strip())
				
		def sanitiseF(inprog):
			return inprog.replace('STRING','').replace("'",'').strip()

		
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
				print(eval(next_token))
			else:
				 printF(next_token,values)
		
		if incr_var == len(data)-1: #ending message et maquille bug which happens due to print(print())
			print('\n*** newB execution ended')
			print('Tip of the day: \nWhen something returns nothing it returns:')	
		incr_var+=1
		

			

def tokenF(load):
	data = load #takes in a list
	t_var=''
	incr_var=0
	#num = ['0','1','2','3','4','5','6','7','8','9'] not needed checked in isdigit()

	while incr_var < len(data):
		cur_char = data[incr_var]
		index=data.index(cur_char)                  #get index of current char

		   #cur_char is not only one char but can also be 20 for example
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
	#print(values)

def splitF(feed):
	raw = feed
	rawChar = ['(',')','&','%','=',' ','\n',';','/*','*/','==','\t','>']
	formattedChar = [' ( ',' ) ',' & ',' % ',' = ','  ',' NEWLINE ',' ; ',' /* ',' */ ','dequal',' TAB ',' > '] #replace with space
	incr_var = 0
	while incr_var < len(rawChar):
		raw =''+raw.replace(rawChar[incr_var],formattedChar[incr_var])
		incr_var +=1
	#print(raw)
	return raw.split()

#print(splitF(filecontent))
#print(tokenF(splitF(filecontent)))
#print(' ')
try:
	print(parseF(tokenF(splitF(filecontent))))
except:
	print('oh oh, you did something crazy')                    #real
#print(values)
#debug


