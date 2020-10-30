import time, re, datetime
from difflib import SequenceMatcher
string = "" #Global variable

def options (num):	#Alot of menus in this code, might aswell make a function for it. When given any a number of options, it will ensure a valid option is selected.

	while True:
		try:

			prompt = int(input("\nPlease choose an option by entering its corresponding number: "))

			if prompt in set (num): #If prompt is part of the given options then it will return the value of the chosen option

				return(prompt)
			
			else: #If any integer that is not a valid option is inputted

				time.sleep(0.5)
				input("\nThis is not a valid option. Press enter to try again...")
				time.sleep(0.5)

		except ValueError: #If any none integer is inputted

			time.sleep(0.5)
			input("\nYou did not enter a number. Press enter to try again...")
			time.sleep(0.5)

def initialmenu(): #Starting menu to allow user to choose how they want to use the program

	print("\n 1. Spellcheck a sentence"
		"\n 2. Spellcheck a file" 
		"\n 0. Quit program")
	time.sleep(0.5)

	option = options({1, 2, 0})

	global string, summary

	if option == 1:

		sentence = input("\nPlease enter your sentence: ")

		time.sleep(0.5)
		spellcheck(sentence)

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
				print("\nCannot find the file with filename " + filename + ".\n")
				time.sleep(0.5)
				#Another menu to either try again or return to start menu

				print("\n1. To try another filename"
					"\n2. To return to initial menu")

				option = options(1, 2)

				if option == 1:

					break

				elif option == 2:

					initialmenu()

		spellcheck(file)

	else:
		return

	while True:
		try:

			time.sleep(0.5)
			filewrite = input("\nPlease enter a filename to create: ")
			f = open(filewrite, "x") #Open the given file to read
			f.write(summary + "\n" + string)
			f.close()
			break
			#More input validation
		except FileExistsError:

			time.sleep(0.5)
			input("\nA file with the name " + filename + " already exists. Press enter to try again...")
			time.sleep(0.5)

	print("\n 1. Return to starting menu" 
		"\n 0. Quit program")

	option = options({1, 0})

	if option == 1:

		initialmenu()

	else:

		return

def spellcheck(checkstring):

	starttime=datetime.datetime.now()
	startcounter = time.perf_counter()

	global string #Will be used across functions
	string = checkstring
	cleanstring = checkstring.lower() #Makes everything lowercase
	cleanstring = re.sub(r"[^\w\s]|[\b\d+\b]", "", cleanstring) #Removes punctuation and numbers from text	
	checklist = cleanstring.split() #Splits the words in the text into items of a list

	f = open("EnglishWords.txt", "r") #Open EnglishWords.txt to read, this will be used to check spelling.
	words = f.read()
	f.close() #Close the file as it is now not in use
	wordslist = words.splitlines() #Splits the words in the file by line into items of a list

	#Assigning variables for statistics

	totalwordcount, correctwordcount, incorrectwordcount, addDictionary, suggestionCount = 0, 0, 0, 0, 0

	for word in checklist: #Loops through each word of the list that we are spellchecking
		if (word in wordslist) == False: #Checks if the word is in the EnglishWords.txt

			print("\n" + word + " is spelt incorrectly")
			time.sleep(0.5)

			print("\n 1. Ignore"
			"\n 2. Mark" 
			"\n 3. Add to dictionary"
			"\n 4. Suggest likely correct spelling")
			time.sleep(0.5)

			option = options({1, 2, 3, 4})

			if option == 1: #This will ignore the current word but increase the incorrect word count

				incorrectwordcount += 1

			elif option == 2: #This will replace the word with itself with question marks around it

				string = string.replace(word, "?" + word + "?", 1) #Adds question marks to the word in the string
				incorrectwordcount += 1
			

			elif option == 3: #This will add the word to the dictionary and also the list of english words so it does not get flagged again during the loop

				f = open("EnglishWords.txt", "a") #Opens the file to add the word to the end
				f.write("\n" + word)
				f.close()
				wordslist.append(word)
				addDictionary += 1
			

			elif option == 4: #This will suggest a word to replace the mispelt word and gives the user and option to accept or reject the word

				suggestionRatio = float(0)

				#Loops through the list of english words and compares it with the mispelt word
				for x in wordslist: 
					test = SequenceMatcher(None, word, x).ratio()

					if test >= suggestionRatio: #This replaces the suggestion everytime a word with a better ratio is found

						suggestionRatio = test
						suggestion = x

				print("\nSuggestion: " + suggestion)
				time.sleep(0.5)

				print("\n 1. Use suggestion"
					"\n 2. Reject suggestion")
				time.sleep(0.5)

				option = options({1, 2})

				if option == 1: #Replaces the word with the suggestion

					string = string.replace(word, suggestion, 1)
					correctwordcount += 1
					suggestionCount += 1

				else:
					string = string.replace(word, "?" + word + "?", 1) #Adds question marks to the word in the string
					incorrectwordcount += 1

		else: 

			print(word) #Shows the checked word, this should always output a word which is correctly spelt

			correctwordcount += 1

		totalwordcount += 1 #Counter

	global summary
	summary = ("Summary:" + 
		"\nDate and time of spellcheck: " + starttime.strftime("D%d-M%m-Y%Y H%H:M%M:S%S") +
		"\nSeconds elapsed during spellcheck: " + str(round((time.perf_counter() - startcounter),1)) + "s" + 
		"\nTotal number of words: " + str(totalwordcount) + 
		"\nCorrectly spelt words: " + str(correctwordcount) + 
		"\nIncorrectly spelt words: " + str(incorrectwordcount) +
		"\nWords added to dictionary: " + str(addDictionary) +
		"\nWords replaced by suggestion: " + str(suggestionCount) + 
		"\n") #Summary

initialmenu()