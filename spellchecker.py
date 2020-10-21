print("1. Spellcheck a sentence \n2. Spellcheck a file \n0. Quit program")
option = 10
while True:
	try:
		option = int(input("Please select an option by entering its corresponding number: "))
		if option in set([0, 1, 2]):
			break
		else:
			print("Please try again.")
	except ValueError:
		print("Please try again")

	