import time, re
def spellcheck(test):

	test = test.lower() #Makes everything lowercase
	test = re.sub(r"[^\w\s]|[\b\d+\b]", " ", test) #Removes punctuation from text	

	testlist = test.split() #Splits the words in the text into items of a list
	print(testlist)

	f1 = open("EnglishWords.txt", "r") #Open EnglishWords.txt to read, this will be used to check spelling.
	words = f1.read()
	wordslist = words.splitlines() #Splits the words in the file by line into items of a list


def intialmenu(): #Starting menu to allow user to choose how they want to use the program
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

def optionselect(option): #Prompts the user for either the sentence or file depending on the option chosen

	if option == 1:
		sentence = input("\nPlease enter your sentence: ")
		spellcheck(sentence)
	elif option == 2:
		while True:
			try:
				filename = input("\nPlease enter the filename: ")
				f = open(filename, "r") #Open the given file to read
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

intialmenu() #Starts the program
