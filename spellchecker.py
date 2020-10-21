def spellcheck(test):
	pass

def intialmenu():
	print("\n1. Spellcheck a sentence \n2. Spellcheck a file \n0. Quit program")

	while True:
		try:
			prompt = int(input("\nPlease select an option by entering its corresponding number: "))
			if prompt in set([0, 1, 2]):
				break
			else:
				print("Please try again.")
		except ValueError:
			print("Please try again.")
	optionselect(prompt)

def optionselect(option):

	if option == 1:
		sentence = input("Please enter your sentence: ")
		spellcheck(sentence)
	elif option == 2:
		while True:
			try:
				filename = input("Please enter the filename: ")
				file = open(filename, "r")
				break
			except FileNotFoundError:
				print("\nCannot find the file with filename " + filename + ".")
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
