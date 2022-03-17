# Spellchecker
This is a simple terminal based spelling checker written in Python 3.8.

## General Information
This spellchecker was a coursework task given in my first year of my computer science course. This was also my first ever programming project.

In the spell checking process the input string is cleaned of any non-alpha characters and any capitalisation is removed. The words are checked against a list of english words given by EnglishWords.txt.

## Features

* A text based menu.

  ![image](https://user-images.githubusercontent.com/75619220/158750539-913b5688-0732-458a-a411-083e0f0bc498.png)


* When checking the spelling of the words, the program will prompt the user on how they wish to deal with misspelt words.

  ![image](https://user-images.githubusercontent.com/75619220/158751059-933f26b8-0019-46fb-b0b0-1b8484f91655.png)

* The program can find a similar word to the misspelt word

   ![image](https://user-images.githubusercontent.com/75619220/158751894-efe72824-ae67-4da3-b55a-dc77106d4761.png)

* After the checking is complete, the user will be prompted for a filename for the program to output its result to.
In the result will be a summary of various statistics and a processed form of the input text with markers or the suggested words added.

  ![image](https://user-images.githubusercontent.com/75619220/158753076-80b0f199-b891-4705-9ff5-b77aeefe4d12.png)

## Usage

You can run the program from any terminal using:

`python3 spellchecker.py`
