import time, re
def spellcheck(test):

	test = test.lower() #Makes everything lowercase
	test = re.sub(r"[^\w\s]", " ", test) #Removes punctuation from text	
	test = re.sub(r"[\b\d+\b]", " ", test) #Removes numbers from the text
	list = test.split() #Splits the words in the text into items of a list
	print(list)

def intialmenu():
	print("\n1. Spellcheck a sentence \n2. Spellcheck a file \n0. Quit program")

	while True:
		try:
			prompt = int(input("\nPlease select an option by entering its corresponding number: "))
			#Input validation
			if prompt in set([0, 1, 2]):
				break
			else:
				print("Please try again.")
		except ValueError:
			print("Please try again.") 
	optionselect(prompt)

def optionselect(option):

	if option == 1:
		sentence = input("\nPlease enter your sentence: ")
		spellcheck(sentence)
	elif option == 2:
		while True:
			try:
				filename = input("\nPlease enter the filename: ")
				f = open(filename, "r")
				file=f.read()
				break
				#More input validation
			except FileNotFoundError:
				print("\nCannot find the file with filename " + filename + ".")
				#Another menu to either try again or return to start menu
				while True:
					try:
						option = int(input("\nEnter\n1. To try another filename\n2. To return to initial menu\n: "))
						if option == 1:
							break
						elif option == 2:
							intialmenu()
					except ValueError:
						print("Please try again")
		spellcheck(file)

intialmenu()
