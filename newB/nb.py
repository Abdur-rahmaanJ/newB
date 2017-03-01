

#.*.F means function

import re

operators = ['+','-']
conditionals = ['if','when'] #then replaces the : as in if x=3 :

with open('txt.nub','r+') as f:
	filecontent = f.read()+' <EOF> '

values={} #global so as to be accessible from funcs

def parseF(textlist):
	data=textlist
	new_data = textlist.remove('NEWLINE')
	incr_var = 0
	while incr_var < len(data) :

		def printF(nextRequiredToken,table):
			if nextRequiredToken in table :
				print(table[nextRequiredToken]) #printing the var by fetching the value
			else :
				print(nextRequiredToken.replace('STRING','').replace('NUM','').strip())

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
			values[previous_token]=next_token #adding to dict if x= 2 then output x

		elif cur_token == 'EQUAL':

			prev = previous_token
			nextt = next_token
			if prev in values :
				prev = values[prev] #fetching from dict
			if nextt in values :
				nextt = values[prev]

			if prev == nextt :
				#print(prev == nextt ) #print(data[index+3])
				if data[index+3] == 'output':
					printF(data[index+4],values)


		elif cur_token == 'output' and previous_token != 'THEN': #dealing with print
			printF(next_token,values)

##2morrow ia write print func
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

		elif cur_char == '=' and data[incr_var+1] == '=': #dealing with ==
			data[index] = 'EQUAL'
			data.remove('=')

		elif cur_char == 'only':
			data[index] = 'ENDCOND'

		elif cur_char == 'then':
			data[index] = 'THEN'

		elif match is not None:
			data[index] = 'STRING '+data[index]

		incr_var+=1

	return data
	#print(values)

def splitF(feed):
	raw = feed
	rawChar = ['(',')','+','-','*','/','&','%','=',' ','\n',';','/*','*/','==','\t']
	formattedChar = [' ( ',' ) ',' + ',' - ',' * ',' / ',' & ',' % ',' = ','  ',' NEWLINE ',' ; ',' /* ',' */ ','dequal',' TAB '] #replace with space
	incr_var = 0
	while incr_var < len(rawChar):
		raw =''+raw.replace(rawChar[incr_var],formattedChar[incr_var])
		incr_var +=1
	#print(raw)
	return raw.split()


print(splitF(filecontent))                                    #debug
print(tokenF(splitF(filecontent)))
print(' ')
print(parseF(tokenF(splitF(filecontent))))                    #real
print(' ')
print(values)
