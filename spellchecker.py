import time, re

def intialmenu(): #Starting menu to allow user to choose how they want to use the program

	while True:
		try:
			print("\n 1. Spellcheck a sentence"\
				"\n 2. Spellcheck a file" \
				"\n 0. Quit program")
			time.sleep(0.5)
			prompt = int(input("\nPlease select an option by entering its corresponding number: "))
			#Input validation
			if prompt in set([0, 1, 2]):

				break

			else:

				time.sleep(0.5)
				input("\nThis is not a valid option. Press enter to try again...")
				time.sleep(0.5)

		except ValueError:

			time.sleep(0.5)
			input("\nYou did not enter a number. Press enter to try again...")
			time.sleep(0.5)

	optionselect(prompt)

def optionselect(option): #Prompts the user for either the sentence or file depending on the option chosen

	if option == 1:

		sentence = input("\nPlease enter your sentence: ")
		spellcheck(sentence)

	elif option == 2:

		while True:

			try:

				time.sleep(0.5)
				filename = input("\nPlease enter the filename: ")
				f = open(filename, "r") #Open the given file to read
				file=f.read()
				f.close() #Close the file as it is now not in use
				break
				#More input validation
			except FileNotFoundError:

				time.sleep(0.5)
				print("\nCannot find the file with filename " + filename + ".")
				time.sleep(0.5)
				#Another menu to either try again or return to start menu
				while True:

					try:

						option = int(input("\n1. To try another filename"\
							"\n2. To return to initial menu"\
							"\nPlease enter an option by entering its corresponding number: "))

						if option == 1:

							break

						elif option == 2:

							intialmenu()

						else:

							time.sleep(0.5)
							input("\nThis is not a valid option. Press enter to try again...")
							time.sleep(0.5)

					except ValueError:

						time.sleep(0.5)
						input("\nYou did not enter a number. Press enter to try again...")
						time.sleep(0.5)

		time.sleep(0.5)
		spellcheck(file)

def spellcheck(checkstring):

	checkstring = checkstring.lower() #Makes everything lowercase
	checkstring = re.sub(r"[^\w\s]|[\b\d+\b]", " ", checkstring) #Removes punctuation and numbers from text	
	checklist = checkstring.split() #Splits the words in the text into items of a list

	f = open("EnglishWords.txt", "r") #Open EnglishWords.txt to read, this will be used to check spelling.
	words = f.read()
	f.close() #Close the file as it is now not in use
	wordslist = words.splitlines() #Splits the words in the file by line into items of a list

	#Assigning variables for statistics
	totalwordcount, correctwordcount, incorrectwordcount = 0, 0, 0

	for x in checklist: #Loops through each word of the list that we are spellchecking

		if (x in wordslist) == False: #Checks if the word is in the EnglishWords.txt

			print(x + " is spelt incorrectly")
			incorrectwordcount = incorrectwordcount + 1

		else: 

			print(x)
			correctwordcount = correctwordcount + 1

		totalwordcount = totalwordcount + 1 #Counter

	print("\nSummary:"\
		"\nTotal number of words: " + str(totalwordcount) + \
		"\nCorrectly spelt words: " + str(correctwordcount) + \
		"\nIncorrectly spelt words: " + str(incorrectwordcount)) #Wordcount


intialmenu() #Starts the program
