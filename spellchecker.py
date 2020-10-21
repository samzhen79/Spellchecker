import time, re
def spellcheck(checkstring):

	checkstring = checkstring.lower() #Makes everything lowercase
	checkstring = re.sub(r"[^\w\s]|[\b\d+\b]", " ", checkstring) #Removes punctuation and numbers from text	
	checklist = checkstring.split() #Splits the words in the text into items of a list

	f = open("EnglishWords.txt", "r") #Open EnglishWords.txt to read, this will be used to check spelling.
	words = f.read()
	f.close() #Close the file as it is now not in use
	wordslist = words.splitlines() #Splits the words in the file by line into items of a list

	wordcount = 0

	for x in checklist: #Loops through each word of the list that we are spellchecking

		if (x in wordslist) == False: #Checks if the word is in the EnglishWords.txt
			print(x + " is spelt incorrectly")
		else: 
			print(x)
			
		wordcount = wordcount + 1 #Counter

	print(wordcount) #Wordcount


def intialmenu(): #Starting menu to allow user to choose how they want to use the program
	print("\n1. Spellcheck a sentence \n2. Spellcheck a file \n0. Quit program")

	while True:
		try:
			prompt = int(input("\nPlease select an option by entering its corresponding number: "))
			#Input validation
			if prompt in set([0, 1, 2]):
				break
			else:
				print("\nPlease try again.")
				time.sleep(0.5)
		except ValueError:
			print("\nPlease try again.")
			time.sleep(0.5)
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
				f.close() #Close the file as it is now not in use
				break
				#More input validation
			except FileNotFoundError:
				print("\nCannot find the file with filename " + filename + ".")
				time.sleep(0.5)
				#Another menu to either try again or return to start menu
				while True:
					try:
						option = int(input("\nEnter\n1. To try another filename\n2. To return to initial menu\n: "))
						if option == 1:
							break
						elif option == 2:
							intialmenu()
					except ValueError:
						print("\nPlease try again")
						time.sleep(0.5)
		spellcheck(file)

intialmenu() #Starts the program
