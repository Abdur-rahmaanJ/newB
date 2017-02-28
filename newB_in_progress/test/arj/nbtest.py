#.*.F means function #see line 28 adding to dict not working

import re

operators = ['+','-']
conditionals = ['if','when'] #then replaces the : as in if x=3 :

with open('txt.nub','r+') as f:
	filecontent = f.read()+' <EOF> '

values={} #global so as to be accessible from funcs

def parseF(textlist):
	data=textlist
	incr_var = 0
	while incr_var < len(data) :
		forwardIndex = incr_var + 1
		backwardIndex = incr_var - 1
		if forwardIndex >= len(data): #preventing out of bounds in array
			forwardIndex = incr_var

		cur_token = data[incr_var]
		next_token = data[forwardIndex]
		previous_token = data[backwardIndex]
		index=data.index(cur_token)

		if cur_token == 'ASSIGN':
			values[previous_token]=next_token #adding to dict not working

		elif cur_token == 'output':
			if next_token in values :
				print(values[next_token]) #printing the var by fetching the value
			else :
				print(next_token.replace('STRING','').replace('NUM','').strip())

		incr_var+=1


def tokenF(load):
	data = load #takes in a list
	t_var=''
	incr_var=0
	#num = ['0','1','2','3','4','5','6','7','8','9'] not needed checked in isdigit()

	while incr_var < len(data):
		cur_char = data[incr_var]
		index=data.index(cur_char) #get index of current char

		pattern=r"'(.)*'" #regex for string
		match= re.search(pattern,cur_char) #cur_char is not only one char but can also be 20 for example

		if cur_char in conditionals :
			data[index] = 'COND ' #
#cur_char.isdigit()==True:    # or unicode.isNumeric()

		elif cur_char in operators:
			data[index] = 'OPER '+data[index]

		elif cur_char == '=' and data[incr_var+1] != '=' and data[incr_var-1] != '=':
			data[index] = 'ASSIGN'

		elif cur_char == '=' and data[incr_var+1] == '=':
			data[index] = 'EQUAL'
			data.remove('=')

		elif match is not None:
			data[index] = 'STRING '+data[index]

		incr_var+=1

	return data
	#print(values)

def splitF(feed):
	raw = feed
	rawChar = ['(',')','+','-','*','/','&','%','=',' ','\n',';','/*','*/','==']
	formattedChar = [' ( ',' ) ',' + ',' - ',' * ',' / ',' & ',' % ',' = ','  ',' NEWLINE ',' ; ',' /* ',' */ ','dequal'] #replace with space
	incr_var = 0
	while incr_var < len(rawChar):
		raw =''+raw.replace(rawChar[incr_var],formattedChar[incr_var])
		incr_var +=1
	#print(raw)
	return raw.split()


print(splitF(filecontent))                                    #debug
print(tokenF(splitF(filecontent)))
print(values)
print(' ')
print(parseF(tokenF(splitF(filecontent))))                    #real
