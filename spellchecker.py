import time, re, datetime, sys, os
from difflib import SequenceMatcher

def title(text="Spellchecker"):
	"""Resets the terminal, and places the title at the top of the terminal"""

	os.system('cls' if os.name == 'nt' else 'clear') #Clears the terminal, This also enables VT100 escape sequences for Windows 10 (This may be a bug with os.system)

	border(text, "title")

def border(text, style="default"): 
	"""Puts a border around given text and then prints, also has different style options"""

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

def optionsmenu (options, num, menutext=""):
	"""Prints out the available options, also validates the options."""
	
	title()

	if menutext != "": #For any additional text above the list of options
		border(menutext)

	border(options, "options")

	while True:
		try:

			sys.stdout.write('\x1b[1A'+'\x1b[2K')	#This effectively replaces the previous line, to the user this means the terminal stays in the same place.

			prompt = int(input(" Please choose an option by entering its corresponding number: "))

			if prompt in set (num):

				title()

				return(prompt)
			
			else: #If any integer that is not a valid option is inputted

				time.sleep(0.5)
				sys.stdout.write('\x1b[1A'+'\x1b[2K')
				input(" This is not one of the options. Press \x1b[41mENTER\x1b[0m to try again... ") #\x1b[41m \x1b[0m Colours the text with a red background
				time.sleep(0.5)

		except ValueError: #If any non-integer is inputted

			time.sleep(0.5)
			sys.stdout.write('\x1b[1A'+'\x1b[2K')
			input(" You did not enter an integer. Press \x1b[41mENTER\x1b[0m to try again...")
			time.sleep(0.5)

def initialmenu():
	"""Main menu"""
	
	option = optionsmenu(["1. Spellcheck a sentence", "2. Spellcheck a file", "0. Quit program"], [1,2,0])

	if option == 1:

		border("Spellcheck a sentence")

		sentence = input("\n Please enter your sentence: ")
		time.sleep(0.5)
		string, summary = spellcheck(sentence)

	elif option == 2:
		while True:
			try:

				border("Spellcheck a file")

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

			title()
			border("Spellcheck Complete.")
			filewrite = input("\n Please enter a filename to create: ")

			f = open(filewrite, "x")
			loglist = string.split() #Technically don't need to do this as we could instead return a list from the spellcheck function,
									 #But this retains the previous functionality of the code if I wanted to change it back in the future.
			logstring = ""

			for word in loglist: #This formats the text file as a vertical list of words
				logstring = (logstring + "\n" + word)

			f.write(summary + logstring)
			f.close()
			break

		except FileExistsError:

			sys.stdout.write('\x1b[1A'+'\x1b[2K')

			time.sleep(0.5)
			input(" A file with the name \x1b[41m" + filewrite + "\x1b[0m already exists. Press \x1b[41mENTER\x1b[0m to try again...")
			time.sleep(0.5)

		except (ValueError, PermissionError, OSError): #OS does not allow certain characters or filenames. e.g. "con", /, ? etc.

			sys.stdout.write('\x1b[1A'+'\x1b[2K')

			if filewrite == "":

				time.sleep(0.5)
				input(" No input detected. Press \x1b[41mENTER\x1b[0m to try again...")
				time.sleep(0.5)

			else:

				time.sleep(0.5)
				input(" Cannot use \x1b[41m" + filewrite + "\x1b[0m as a file name. Press \x1b[41mENTER\x1b[0m to try again...")
				time.sleep(0.5)

	option = optionsmenu(["1. Return to main menu", "0. Quit program"], {1, 0}, "File created")

	if option == 1:

		initialmenu()

	else:
		return

def spellcheck(checkstring):

	starttime = datetime.datetime.now() #Gets the current system date and time.
	startcounter = time.perf_counter() #Gets the current counter value. This will be used later to find the total elapsed time in seconds.

	cleanstring = re.sub(r"[^\w\s]|[\b\d+\b]", "", checkstring.lower()) #Removes punctuation and numbers from text. Also makes everything lowercase.
	checklist = cleanstring.split()
	string = cleanstring #Will be used for the new file after spellcheck, not neccesary for this current implementation but is useful for restoring some previous functionality

	f = open("EnglishWords.txt", "r")
	wordslist = (f.read()).splitlines()
	f.close()

	totalwordcount, correctwordcount, incorrectwordcount, addDictionary, suggestionCount = 0, 0, 0, 0, 0

	title()

	for word in checklist:

		border(word, "check")

		sys.stdout.write('\x1b[4A'+'\x1b[0J') #Removes the last 4 lines. Could use title() instead but this may be less taxing

		time.sleep(0.3)
		if (word in wordslist) == False:

			option = optionsmenu(["1. Ignore", "2. Mark", "3. Add to dictionary", "4. Suggest a word"], {1, 2, 3, 4}, word + " is spelt incorrectly")

			if option == 1: 

				incorrectwordcount += 1

			elif option == 2: 

				string = string.replace(word, "?" + word + "?", 1)	#Marks the word with ?around? it
				incorrectwordcount += 1
			
			elif option == 3:

				f = open("EnglishWords.txt", "a")
				f.write("\n" + word) #Adds the word to the end of the dictionary
				f.close()

				wordslist.append(word)#Also updates the list we are currently checking against so it is not flagged again
				addDictionary += 1
			
			elif option == 4:

				suggestionRatio = float(0)
				border("Loading...")

				for x in wordslist: #Loops through the list of english words and compares it with the mispelt word, may be a more efficient method.

					test = SequenceMatcher(None, word, x).ratio() #Produces a ratio based on how similar the words are

					if test >= suggestionRatio: #This replaces the suggestion everytime a word with a higher ratio is found

						suggestionRatio = test
						suggestion = x

				sys.stdout.write('\x1b[1A'+'\x1b[2K')

				option = optionsmenu(["1. Use suggestion", "2. Reject suggestion"], {1, 2}, "Suggestion: " + suggestion)

				if option == 1:

					string = string.replace(word, suggestion, 1)
					correctwordcount += 1
					suggestionCount += 1

				else:

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