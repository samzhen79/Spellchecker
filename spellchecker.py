import time, re, datetime, sys, os
from difflib import SequenceMatcher

def title(text="Spellchecker"): #Produces a title for the terminal. 

	os.system('cls' if os.name == 'nt' else 'clear') #Clears the terminal, This also enables VT100 escape sequences for Windows 10 (This may be a bug with os.system)

	border(text, "title")

def border(text, style="default"): #Puts a border around given text, also has different style options

	if style == "title": #Title style border. Double line border.
		print("\n\u2554"+"\u2550"*(len(text)+2)+"\u2557"
			"\n\u2551 " + text + " \u2551"
			"\n\u255a"+"\u2550"*(len(text)+2)+"\u255d")

	elif style == "check": #Border for spellchecking. Has a nice little separation between checking and the word.
		print("\n\u250c"+"\u2500"*11+"\u252c"+"\u2500"*(len(text)+2)+"\u2510"
			"\n\u2502 Checking: \u2502 " + text + " \u2502"
			"\n\u2514"+"\u2500"*11+"\u2534"+"\u2500"*(len(text)+2)+"\u2518")

	elif style == "options": #Dashed border for a set of options
		print("")
		for option in text:

			print(" "+"\u254c"*25+
				"\n "+option)

		print(" "+"\u254c"*25+"\n\n")

	else: #Default case. Default single line border.
		print("\n\u250c"+"\u2500"*(len(text)+2)+"\u2510"
			"\n\u2502 " + text + " \u2502"
			"\n\u2514"+"\u2500"*(len(text)+2)+"\u2518")

def optionsmenu (options, num, menutext=""):	#Prints out the available options, also validates the options.
	
	title()

	if menutext != "": #For any text above the list of options
		border(menutext)

	border(options, "options")

	while True:
		try:

			#This effectively replaces the previous line, to the user this means the terminal stays in the same place.
			sys.stdout.write('\x1b[1A'+'\x1b[2K')

			prompt = int(input(" Please choose an option by entering its corresponding number: "))

			if prompt in set (num): #If prompt is part of the given options then it will return the value of the chosen option

				title()

				return(prompt)
			
			else: #If any integer that is not a valid option is inputted

				time.sleep(0.5)
				sys.stdout.write('\x1b[1A'+'\x1b[2K')
				input(" This is not one of the options. Press \x1b[41mENTER\x1b[0m to try again... ") #\x1b[41m \x1b[0m Colours the text with a red background
				time.sleep(0.5)

		except ValueError: #If any none integer is inputted

			time.sleep(0.5)
			sys.stdout.write('\x1b[1A'+'\x1b[2K')
			input(" You did not enter an integer. Press \x1b[41mENTER\x1b[0m to try again...")
			time.sleep(0.5)

def initialmenu(): #Starting menu to allow user to choose how they want to use the program
	
	option = optionsmenu(["1. Spellcheck a sentence", "2. Spellcheck a file", "0. Quit program"], [1,2,0])

	if option == 1:

		sentence = input("\n Please enter your sentence: ")

		time.sleep(0.5)
		string, summary = spellcheck(sentence)

	elif option == 2:
		while True:
			try:


				filename = input("\n Please enter the filename: ")
				f = open(filename, "r") 
				file = f.read()
				f.close()

				break
			
			except FileNotFoundError:

				sys.stdout.write('\x1b[1A'+'\x1b[2K')
				
				time.sleep(0.5)
				input(" A file with the name \x1b[41m" + filename + "\x1b[0m does not exist. Press \x1b[41mENTER\x1b[0m to continue...")
				time.sleep(0.5)

				option = optionsmenu(["1. Try another file name", "2. Return to menu"], {1,2})

				if option == 1:

					break

				elif option == 2:

					initialmenu()

		string, summary = spellcheck(file)

	else:
		return

	while True:
		try:

			time.sleep(0.5)
			title()
			border("Spellcheck Complete.")
			filewrite = input("\n Please enter a filename to create: ")

			f = open(filewrite, "x")
			loglist = string.split() #Technically don't need to do this as we could instead return a list from the spellcheck function,
									 #But this retains the previous functionality of the code if I wanted to change it back in the future.
			logstring = ""

			for word in loglist: #This formats the text file as a long list of words
				logstring = (logstring + "\n" + word)

			f.write(summary + logstring)
			f.close()
			break
			
		except FileExistsError:

			sys.stdout.write('\x1b[1A'+'\x1b[2K')

			time.sleep(0.5)
			input(" A file with the name \x1b[41m" + filewrite + "\x1b[0m already exists. Press \x1b[41mENTER\x1b[0m to try again...")
			time.sleep(0.5)

	option = optionsmenu(["1. Return to starting menu", "0. Quit program"], {1, 0}, "File created")

	if option == 1:

		initialmenu()

	else:
		return

def spellcheck(checkstring):

	starttime = datetime.datetime.now() #Gets the current date and time.
	startcounter = time.perf_counter() #Gets the current counter value. This will be used later to find the total elapsed time in seconds.

	cleanstring = re.sub(r"[^\w\s]|[\b\d+\b]", "", checkstring.lower()) #Removes punctuation and numbers from text. Also makes everything lowercase.
	checklist = cleanstring.split() #Splits the words in the text into items of a list
	string = cleanstring #Will be used for the new file after spellcheck

	f = open("EnglishWords.txt", "r")
	wordslist = (f.read()).splitlines() #Splits the words in the file by line into items of a list
	f.close()

	title()

	#Assigning variables for statistics

	totalwordcount, correctwordcount, incorrectwordcount, addDictionary, suggestionCount = 0, 0, 0, 0, 0

	for word in checklist: #Loops through each word of the list that we are spellchecking

		#Shows the word that is currently being checked
		border(word, "check")

		sys.stdout.write('\x1b[4A'+'\x1b[0J') #Removes the last 4 lines. Could use title() instead but this may be less taxing

		time.sleep(0.3)
		if (word in wordslist) == False: #Checks if the word is in the EnglishWords.txt list

			option = optionsmenu(["1. Ignore", "2. Mark", "3. Add to dictionary", "4. Suggest a word"], {1, 2, 3, 4}, word + " is spelt incorrectly")

			if option == 1: #This will ignore the current word but increase the incorrect word count

				incorrectwordcount += 1

			elif option == 2: #This will replace the word with itself with question marks around it

				string = string.replace(word, "?" + word + "?", 1) #Adds question marks around the word in the string
				incorrectwordcount += 1
			

			elif option == 3: #This will add the word to the dictionary and also the list of english words so it does not get flagged again during the loop

				f = open("EnglishWords.txt", "a")
				f.write("\n" + word) #Adds the word to the end of the dictionary
				f.close()
				wordslist.append(word)#Also updates the list we are currently checking against
				addDictionary += 1
			

			elif option == 4: #This will suggest a word to replace the mispelt word and gives the user and option to accept or reject the word

				suggestionRatio = float(0)
				border("Loading...")
				#Loops through the list of english words and compares it with the mispelt word, absolutely not the most efficient method
				for x in wordslist: 

					test = SequenceMatcher(None, word, x).ratio()

					if test >= suggestionRatio: #This replaces the suggestion everytime a word with a better ratio is found

						suggestionRatio = test
						suggestion = x

				sys.stdout.write('\x1b[1A'+'\x1b[2K')

				option = optionsmenu(["1. Use suggestion", "2. Reject suggestion"], {1, 2}, "Suggestion: " + suggestion)

				if option == 1: #Replace the word with the suggestion

					string = string.replace(word, suggestion, 1)
					correctwordcount += 1
					suggestionCount += 1

				else: #Mark as incorrect, with the question marks

					string = string.replace(word, "?" + word + "?", 1)
					incorrectwordcount += 1

		else:

			correctwordcount += 1

		totalwordcount += 1 

	summary = ("Summary:" +
			"\nDate and time of spellcheck: " + starttime.strftime("D%d-M%m-Y%Y H%H:M%M:S%S")+
			"\nSeconds elapsed during spellcheck: " + str(round((time.perf_counter() - startcounter),1)) + "s" +
			"\nTotal number of words: " + str(totalwordcount)+
			"\nCorrectly spelt words: " + str(correctwordcount)+
			"\nIncorrectly spelt words: " + str(incorrectwordcount)+
			"\nWords added to dictionary: " + str(addDictionary)+
			"\nWords replaced by suggestion: " + str(suggestionCount)+
			"\n")

	return(string, summary)

initialmenu()
os.system('cls' if os.name == 'nt' else 'clear')