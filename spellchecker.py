import time, re
from difflib import SequenceMatcher
string = ""

def intialmenu(): #Starting menu to allow user to choose how they want to use the program

	while True:
		try:

			print("\n 1. Spellcheck a sentence"
				"\n 2. Spellcheck a file" 
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

	global string

	if option == 1:

		sentence = input("\nPlease enter your sentence: ")

		time.sleep(0.5)
		spellcheck(sentence)
		print("Here is the processed sentence: \n" +\
			 string)

	elif option == 2:
		while True:
			try:

				time.sleep(0.5)
				filename = input("\nPlease enter the filename: ")
				f = open(filename, "r") #Open the given file to read
				file = f.read()
				f.close()

				break
				#More input validation
			except FileNotFoundError:

				time.sleep(0.5)
				print("\nCannot find the file with filename " + filename + ".")
				time.sleep(0.5)
				#Another menu to either try again or return to start menu
				while True:
					try:

						option = int(input("\n1. To try another filename"
							"\n2. To return to initial menu"
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
		#Rewrites the file with the marked words
		file = open(filename, "w")
		file.write(string)
		file.close()


def spellcheck(checkstring):

	global string, wordslist #Will be used across functions
	string = checkstring
	cleanstring = checkstring.lower() #Makes everything lowercase
	cleanstring = re.sub(r"[^\w\s]|[\b\d+\b]", " ", cleanstring) #Removes punctuation and numbers from text	
	checklist = cleanstring.split() #Splits the words in the text into items of a list

	f = open("EnglishWords.txt", "r") #Open EnglishWords.txt to read, this will be used to check spelling.
	words = f.read()
	f.close() #Close the file as it is now not in use
	wordslist = words.splitlines() #Splits the words in the file by line into items of a list

	#Assigning variables for statistics
	global incorrectwordcount, addDictionary, correctwordcount, suggestionCount#incorrectwordcount will be used across functions
	totalwordcount, correctwordcount, incorrectwordcount, addDictionary, suggestionCount = 0, 0, 0, 0, 0

	for word in checklist: #Loops through each word of the list that we are spellchecking
		if (word in wordslist) == False: #Checks if the word is in the EnglishWords.txt

			print("\n" + word + " is spelt incorrectly")

			while True: #This menu will show up when a mispelt word is found
				try:

					print("\n 1. Ignore"
					"\n 2. Mark" 
					"\n 3. Add to dictionary"
					"\n 4. Suggest likely correct spelling")
					time.sleep(0.5)
					prompt = int(input("\nPlease select an option by entering its corresponding number: "))

					if prompt in set([1, 2, 3, 4]):

						break

					else:

						time.sleep(0.5)
						input("\nThis is not a valid option. Press enter to try again...")
						time.sleep(0.5)


				except ValueError:

					time.sleep(0.5)
					input("\nYou did not enter a number. Press enter to try again...")
					time.sleep(0.5)
			spellcheckOption(prompt, word)
		else: 

			print(word) #Shows the checked word, this should always output a word which is correctly spelt

			correctwordcount =+ 1

		totalwordcount =+ 1 #Counter

	print("\nSummary:"\
		"\nTotal number of words: " + str(totalwordcount) + 
		"\nCorrectly spelt words: " + str(correctwordcount) + 
		"\nIncorrectly spelt words: " + str(incorrectwordcount) +
		"\nWords added to dictionary: " + str(addDictionary) +
		"\nWords replaced by suggestion: " + str(suggestionCount)) #Summary


def spellcheckOption(option, word):

	global string, incorrectwordcount, correctwordcount, addDictionary, suggestionCount	

	if option == 1: #This will ignore the current word but increase the incorrect word count

		incorrectwordcount =+ 1
		return

	elif option == 2: #This will replace the word with itself with question marks around it

		string.replace(word, "?" + word + "?", 1) #Makes changes to the original string
		incorrectwordcount =+ 1
		return

	elif option == 3: #This will add the word to the dictionary and also the list of english words so it does not get flagged again during the loop

		f = open("EnglishWords.txt", "a") #Opens the file to add the word to the end
		f.write("\n" + word)
		f.close()
		wordslist.append(word)
		addDictionary =+ 1
		return

	elif option == 4: #This will suggest a word to replace the mispelt word and gives the user and option to accept or reject the word

		suggestionRatio = float(0)

		#Loops through the list of english words and compares it with the mispelt word
		for x in wordslist: 
			test = SequenceMatcher(None, word, x).ratio()

			if test >= suggestionRatio: #This replaces the suggestion everytime a word with a better ratio is found

				suggestionRatio = test
				suggestion = x

		print("\nSuggestion: " + suggestion)

		while True: #Another menu, might have to make this into a function?
			try:

				print("\n 1. Use suggestion"
					"\n 2. Reject suggestion")
				time.sleep(0.5)
				prompt = int(input("\nPlease select an option by entering its corresponding number: "))
				#Input validation
				if prompt in set([1, 2]):

					break

				else:

					time.sleep(0.5)
					input("\nThis is not a valid option. Press enter to try again...")
					time.sleep(0.5)

			except ValueError:

				time.sleep(0.5)
				input("\nYou did not enter a number. Press enter to try again...")
				time.sleep(0.5)
			return

		if prompt == 1: #Replaces the word with the suggestion

			string.replace(word, suggestion, 1)
			correctwordcount =+ 1
			suggestionCount =+ 1

		else:

			incorrectwordcount =+ 1





intialmenu() #Starts the program
