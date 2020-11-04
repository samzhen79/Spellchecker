import time, re, datetime, sys
from difflib import SequenceMatcher

def title():

	#Nice looking title + border thing.
	print("\n\u2554"+"\u2550"*14+"\u2557"
	"\n\u2551 Spellchecker \u2551"
	"\n\u255a"+"\u2550"*14+"\u255d")

def options (num):	#Alot of menus in this code, might aswell make a function for it. When given any a number of options, it will ensure a valid option is selected.

	while True:
		try:

			#This effectively replaces the previous line, to the user this means the terminal stays in the same place.
			sys.stdout.write('\x1b[1A'+'\x1b[2K')

			prompt = int(input(" Please choose an option by entering its corresponding number: "))

			if prompt in set (num): #If prompt is part of the given options then it will return the value of the chosen option

				#This clears the terminal 
				sys.stdout.write('\x1bc')

				title()

				return(prompt)
			
			else: #If any integer that is not a valid option is inputted

				time.sleep(0.5)
				sys.stdout.write('\x1b[1A'+'\x1b[2K')
				input(" This is not a one of the options. Press \x1b[41mENTER\x1b[0m to try again... ") #\x1b[41m \x1b[0m Colours the text with a red background
				time.sleep(0.5)

		except ValueError: #If any none integer is inputted

			time.sleep(0.5)
			sys.stdout.write('\x1b[1A'+'\x1b[2K')
			input(" You did not enter an integer. Press \x1b[41mENTER\x1b[0m to try again...")
			time.sleep(0.5)

def initialmenu(): #Starting menu to allow user to choose how they want to use the program
	
	sys.stdout.write('\x1bc')
	
	
	title()

	print("\n "+"\u254c"*25+
		"\n 1. Spellcheck a sentence"
		"\n "+"\u254c"*25+
		"\n 2. Spellcheck a file" 
		"\n "+"\u254c"*25+
		"\n 0. Quit program"
		"\n "+"\u254c"*25+"\n\n")

	option = options({1, 2, 0})

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

				time.sleep(0.5)

				sys.stdout.write('\x1b[1A'+'\x1b[2K')

				print("\u250c"+"\u2500"*(39+len(filename))+"\u2510"
					"\n\u2502 Cannot find the file with file name " + "\x1b[41m"+filename+"\x1b[0m" + ". \u2502"
					"\n\u2514"+"\u2500"*(39+len(filename))+"\u2518")

				print("\n "+"\u254c"*25+
					"\n 1. Try another file name"
					"\n "+"\u254c"*25+
					"\n 2. Return to menu"
					"\n "+"\u254c"*25+"\n\n")

				option = options({1, 2})

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
			sys.stdout.write('\x1bc')
			title()
			filewrite = input("\n\u250c"+"\u2500"*22+"\u2510"
							"\n\u2502 Spellcheck Complete. \u2502"
							"\n\u2514"+"\u2500"*22+"\u2518"
							"\n\n Please enter a filename to create: ")

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
			input(" A file with the name " + filewrite + " already exists. Press \x1b[41mENTER\x1b[0m to try again...")
			time.sleep(0.5)

	print("\n "+"\u254c"*25+
		"\n 1. Return to starting menu" 
		"\n "+"\u254c"*25+
		"\n 0. Quit program"
		"\n "+"\u254c"*25+"\n\n")

	option = options({1, 0})

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

	print("\n")

	#Assigning variables for statistics

	totalwordcount, correctwordcount, incorrectwordcount, addDictionary, suggestionCount = 0, 0, 0, 0, 0

	for word in checklist: #Loops through each word of the list that we are spellchecking

		sys.stdout.write('\x1b[3A'+'\x1b[0J') #Clears the last three lines

		#Shows the word that is currently being checked
		print("\u250c"+"\u2500"*11+"\u252c"+"\u2500"*(len(word)+2)+"\u2510"
			"\n\u2502 Checking: \u2502 " + word + " \u2502"
			"\n\u2514"+"\u2500"*11+"\u2534"+"\u2500"*(len(word)+2)+"\u2518")

		time.sleep(0.3)
		if (word in wordslist) == False: #Checks if the word is in the EnglishWords.txt list

			sys.stdout.write('\x1b[3A'+'\x1b[0J')

			print("\u250c"+"\u2500"*(23+len(word))+"\u2510"
				"\n\u2502 " + word + " is spelt incorrectly \u2502"
				"\n\u2514"+"\u2500"*(23+len(word))+"\u2518")

			print("\n "+"\u254c"*25+
				"\n 1. Ignore"
				"\n "+"\u254c"*25+
				"\n 2. Mark" 
				"\n "+"\u254c"*25+
				"\n 3. Add to dictionary"
				"\n "+"\u254c"*25+
				"\n 4. Suggest a word"
				"\n "+"\u254c"*25+"\n\n")

			option = options({1, 2, 3, 4})

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
				print("\nLoading...")
				#Loops through the list of english words and compares it with the mispelt word, absolutely not the most efficient method
				for x in wordslist: 

					test = SequenceMatcher(None, word, x).ratio()

					if test >= suggestionRatio: #This replaces the suggestion everytime a word with a better ratio is found

						suggestionRatio = test
						suggestion = x

				sys.stdout.write('\x1b[1A'+'\x1b[2K')

				print(" Suggestion: " + suggestion)

				print("\n "+"\u254c"*25+
					"\n 1. Use suggestion"
					"\n "+"\u254c"*25+
					"\n 2. Reject suggestion"
					"\n "+"\u254c"*25+"\n\n")

				option = options({1, 2})

				if option == 1: #Replace the word with the suggestion

					string = string.replace(word, suggestion, 1)
					correctwordcount += 1
					suggestionCount += 1

				else: #Mark as incorrect, with the question marks

					string = string.replace(word, "?" + word + "?", 1)
					incorrectwordcount += 1

			print("\n") #Keeps the checking line on the same line of the terminal by repositioning it.

			correctwordcount += 1

		totalwordcount += 1 

	summary = ("Summary:" + 
		"\nDate and time of spellcheck: " + starttime.strftime("D%d-M%m-Y%Y H%H:M%M:S%S") +
		"\nSeconds elapsed during spellcheck: " + str(round((time.perf_counter() - startcounter),1)) + "s" + 
		"\nTotal number of words: " + str(totalwordcount) + 
		"\nCorrectly spelt words: " + str(correctwordcount) + 
		"\nIncorrectly spelt words: " + str(incorrectwordcount) +
		"\nWords added to dictionary: " + str(addDictionary) +
		"\nWords replaced by suggestion: " + str(suggestionCount) + 
		"\n")

	return(string, summary)

initialmenu()