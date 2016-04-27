import os
import csv
import hashlib
import numpy
from operator import attrgetter

import word as WordCode
import puzzle as PuzzleCode
import helper_funcs as Helper

ceaser_translations = []
alphabet = 'abcdefghijklmnopqrstuvwxyz'
for offset in range(1,26):
    enc_alphabet = (alphabet[alphabet.index(alphabet[offset]):len(alphabet)])+ alphabet[0:offset]
    translation = str.maketrans(alphabet,enc_alphabet)
    ceaser_translations.append(translation)

short_words_database = []
with open("words.txt", "r") as puzzleFile:
    for line in puzzleFile:
        word = line.rstrip()
        if len(word) < 4:
            short_words_database.append(word)

country_codes_database = []
with open('country_codes.csv',"r") as countriesDataFile:
    csvread=csv.DictReader(countriesDataFile)
    for row in csvread:
        country_codes_database.append(row['Code'].lower())

chemical_symbols_database = []
with open('elementlist.csv',"r") as elementsDataFile:
    csvread=csv.DictReader(elementsDataFile)
    for row in csvread:
        code = row['Code'].lower()
        chemical_symbols_database.append(code)

state_codes_database = []
with open('states.csv',"r") as statesDataFile:
    csvread=csv.DictReader(statesDataFile)
    for row in csvread:
        state_codes_database.append(row['Abbreviation'].lower())

print("Started loading words...")
sizeOfWords = 108286
words = []
wordsByCompareLength = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 15: [], 16: [], 17: [], 18: [], 19: [], 20: [], 21: [], 22: [], 23: [], 24: [], 25: [], 26: [], 27: [], 28: []}
with open("words.txt", "r") as wordsFile:
    counter = 0
    percentageComplete = 0.0
    for line in wordsFile:
        if (counter / sizeOfWords) > percentageComplete:
            print(str(round((counter / sizeOfWords),2) * 100) + "% complete")
            percentageComplete += 0.05
        word = WordCode.Word(line.rstrip(), words, country_codes_database, chemical_symbols_database, short_words_database, state_codes_database, ceaser_translations )
        words.append(word)
        wordsByCompareLength[word.length].append(word)

        counter += 1
        
    
print("finished parsing word dictionary...")
cluePuzzles = []
puzzle_folder = "pyramid/" #"test_case/"#
for folder in os.listdir(puzzle_folder):
    for puzzleFileName in os.listdir(puzzle_folder + folder):
        fullFilePath = puzzle_folder + folder + "/" + puzzleFileName
        with open(fullFilePath, "r") as puzzleFile:
            lines = []
            for line in puzzleFile:
                lines.append(line.rstrip())

            puzzle = PuzzleCode.parsePuzzleData( lines, puzzleFileName, True, False )

            if puzzle != None:
                cluePuzzles.append(puzzle)
  
cluePuzzles.sort(key=attrgetter('row'))

print("finished gathering puzzle info...")
print("testing puzzles...")
counter = 0
percentageComplete = 0.0
sizeOfPuzzles = len(cluePuzzles)
for puzzle in cluePuzzles:
    if (counter / sizeOfPuzzles) > percentageComplete:
        print(str(round((counter / sizeOfPuzzles),2) * 100) + "% complete")
        percentageComplete += 0.05
    for word in words:
                   
        viableWord = True
        
        if viableWord and puzzle.hasSumTotalTest:
            if word.sum != puzzle.sumTotal:
                viableWord = False
        if viableWord and  puzzle.hasRangeTotalTest:
            if word.sum < puzzle.rangeTotal[0] or word.sum > puzzle.rangeTotal[1]:
                viableWord = False

        if viableWord:
            for test in puzzle.sumDivisibleTests:
                if word.sum % test != 0:
                    viableWord = False
            for test in puzzle.sumNotDivisibleTests:
                if word.sum % test == 0:
                    viableWord = False
                
        if viableWord and len(puzzle.base26Test) > 0:
            if len(puzzle.base26Test) == 1:
                if word.base26Interp != puzzle.base26Test[0]:
                    viableWord = False
            if len(puzzle.base26Test) == 2:
                if word.base26Interp < puzzle.base26Test[0] or word.base26Interp > puzzle.base26Test[1]:
                    viableWord = False
                    
        if viableWord:            
            for test in puzzle.base26DivisibleTests:
                if word.base26Interp % test != 0:
                    viableWord = False
            for test in puzzle.base26NotDivisibleTests:
                if word.base26Interp % test == 0:
                    viableWord = False       

        if viableWord and puzzle.hasScrabbleTotalTest:
            if word.scrabbleValue != puzzle.scrabbleTotal:
                viableWord = False
        if viableWord and viableWord and puzzle.hasScrabbleRangeTest:
            if word.scrabbleValue < puzzle.scrabbleRange[0] or word.scrabbleValue > puzzle.scrabbleRange[1]:
                viableWord = False
                
        if viableWord and Helper.runFailTest(word, "length", puzzle.lengthTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "commonestLetters", puzzle.commonestLettersSubTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "commonestVowels", puzzle.commonestVowelsSubTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "commonestConsonants", puzzle.commonestConsonantsSubTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "vowels", puzzle.vowelSubTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "consonants", puzzle.consonantSubTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "countryCodeLetters", puzzle.countryCodesSubTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "chemicalCodeLetters", puzzle.chemicalCodesSubTest):
            viableWord = False                          
        if viableWord and Helper.runFailTest(word, "bottomQWERTY", puzzle.qwertyBottomRowSubTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "middleQWERTY", puzzle.qwertyMiddleRowSubTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "topQWERTY", puzzle.qwertyTopRowSubTest):
            viableWord = False
        

        if viableWord and len(puzzle.startsWithTest) > 0:
            if len(puzzle.startsWithTest) == 1:
                if word.word.find(puzzle.startsWithTest[0]) != 0:
                    viableWord = False
            elif len(puzzle.startsWithTest) == 2:
                vowels = ['a','e','i','o','u']
                if ((word.word[0] in vowels) != puzzle.startsWithTest[1]):
                    viableWord = False

        if viableWord and len(puzzle.endsWithTest) > 0:
            if len(puzzle.endsWithTest) == 1:
                if (word.length >= len(puzzle.endsWithTest[0])):
                    if word.word.rfind(puzzle.endsWithTest[0]) != (len(word.word) - len(puzzle.endsWithTest[0])):
                        viableWord = False
                else:
                    viableWord = False
            elif len(puzzle.endsWithTest) == 2:
                vowels = ['a','e','i','o','u']
                if ((word.word[-1] in vowels) != puzzle.endsWithTest[1]):
                    viableWord = False
                    
        if viableWord and len(puzzle.shaHashTest) == 2:
            if puzzle.shaHashTest[0] == "starts":
                if word.sh1Hash.find(puzzle.shaHashTest[1]) != 0:
                    viableWord = False
            elif puzzle.shaHashTest[0] == "ends":
                if word.sh1Hash.rfind(puzzle.shaHashTest[1]) != (len(word.sh1Hash) - len(puzzle.shaHashTest[1])):
                    viableWord = False
            elif puzzle.shaHashTest[0] == "contains":
                if word.sh1Hash.find(puzzle.shaHashTest[1]) == -1:
                    viableWord = False
       
        if viableWord and len(puzzle.contains) > 0:
            if word.word.find(puzzle.contains) == -1:
                viableWord = False

        if viableWord and Helper.runFailTest(word, "distinctVowels", puzzle.distinctVowelTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "distinctConsonants", puzzle.distinctConsonantTest):
            viableWord = False
        if viableWord and Helper.runFailTest(word, "distinctLetters", puzzle.distinctLetterTest):
            viableWord = False
                    

        if viableWord and len(puzzle.base26UintTest) > 0:
            if (word.base26Interp < 4294967295) != puzzle.base26UintTest[0]:
                viableWord = False
        if viableWord and len(puzzle.base26IntTest) > 0:
            if (word.base26Interp < 18446744073709551615) != puzzle.base26IntTest[0]:
                viableWord = False
        if viableWord and len(puzzle.base26FloatTest) > 0:
            if (word.base26Interp == int(numpy.float32(word.base26Interp))) != puzzle.base26FloatTest[0]:
                viableWord = False
        if viableWord and len(puzzle.base26DoubleTest) > 0:
            if (word.base26Interp == int(float(word.base26Interp))) != puzzle.base26DoubleTest[0]:
                viableWord = False

        if viableWord and len(puzzle.atLeastOneDLTest)> 0:
            if (word.atLeastOneDoubleLetter != puzzle.atLeastOneDLTest[0]):
                viableWord = False
        if viableWord and len(puzzle.atLeastTwoDiffDLTest)> 0:
            if (word.atLeastTwoDoubleLetters != puzzle.atLeastTwoDiffDLTest[0]):
                viableWord = False
        if viableWord and len(puzzle.atLeastTwoSameDLTest)> 0:
            if (word.twoOfTheSameDoubleLetter != puzzle.atLeastTwoSameDLTest[0]):
                viableWord = False        

        if viableWord:
            if not word.hasCalculatedHardData:
                word.calculateHardData(wordsByCompareLength)

            if viableWord and len(puzzle.oneOffAnagTest) > 0:
                if word.hasOneOffAnag != puzzle.oneOffAnagTest[0]:
                    viableWord = False
                    
            if viableWord and len(puzzle.twoOffAnagTest) > 0:
                if word.hasTwoOffAnag != puzzle.twoOffAnagTest[0]:
                    viableWord = False
                    
            if viableWord and len(puzzle.fullAnagTest) > 0:
                if word.hasFullAnag != puzzle.fullAnagTest[0]:
                    viableWord = False
                    
            if viableWord and Helper.runFailTest(word, "shortWords", puzzle.smallWordsSubTest):
                viableWord = False
                             
            if viableWord and Helper.runFailTest(word, "stateCodes", puzzle.stateCodesSubTest):
                viableWord = False
                
            if viableWord and len(puzzle.ceaserCipherTest) > 0:
                if puzzle.ceaserCipherTest[0] != word.foundCeaserShift:
                    viableWord = False
                    

        if viableWord:
            puzzle.viableWords.append(word)

    counter +=1


print("finished checking viable words...")

concept_pharoahs = {}
color_pharoahs = {}
has_property_pharoahs = {}
has_not_property_pharoahs = {}

for puzzle in cluePuzzles:
    pharoahName = puzzle.clueInfo.split()[-1].split('.')[0]
    puzzleLocation = "row: " + str(puzzle.row) + ", col: " + str(puzzle.col) + " = "

    if puzzle.clueInfo.find("concept") != -1 :
        if pharoahName in concept_pharoahs:
            concept_pharoahs[pharoahName].append([puzzleLocation,puzzle.viableWords])
        else:
            concept_pharoahs[pharoahName] = [[puzzleLocation,puzzle.viableWords]]

    if puzzle.clueInfo.find("color") != -1 :
        if pharoahName in color_pharoahs:
            color_pharoahs[pharoahName].append([puzzleLocation,puzzle.viableWords])
        else:
            color_pharoahs[pharoahName] = [[puzzleLocation,puzzle.viableWords]]

    if puzzle.clueInfo.find("NOT") == -1 and puzzle.clueInfo.find("color") == -1 and puzzle.clueInfo.find("concept") == -1:
        if pharoahName in has_not_property_pharoahs:
            has_property_pharoahs[pharoahName].append([puzzleLocation,puzzle.viableWords])
        else:
            has_property_pharoahs[pharoahName] = [[puzzleLocation,puzzle.viableWords]]

    if puzzle.clueInfo.find("NOT") != -1 :
        if pharoahName in has_property_pharoahs:
            has_not_property_pharoahs[pharoahName].append([puzzleLocation,puzzle.viableWords])
        else:
            has_not_property_pharoahs[pharoahName] = [[puzzleLocation,puzzle.viableWords]]

errors_list = []
print("Concepts")
print("---------------------------\n")
for pharoah in concept_pharoahs:
    associated_words = []
    for viableWordList in concept_pharoahs[pharoah]:
        if len(viableWordList[1]) == 1:
            for word in viableWordList[1]:
                associated_words.append(word.word.upper())
        else:
            errors_list.append([pharoah,viableWordList])

    print("[B]" + pharoah.upper() + "[\\B]: " + str(associated_words) + "\n")
    

print("Colors")
print("---------------------------\n")
for pharoah in color_pharoahs:
    associated_words = []
    for viableWordList in color_pharoahs[pharoah]:
        if len(viableWordList[1]) == 1:
            for word in viableWordList[1]:
                associated_words.append(word.word.upper())
        else:
            errors_list.append([pharoah,viableWordList])

    print("[B]" + pharoah.upper() + "[\\B]: " + str(associated_words) + "\n")

print("Has property:")
print("---------------------------\n")
for pharoah in has_property_pharoahs:
    associated_words = []
    for viableWordList in has_property_pharoahs[pharoah]:
        if len(viableWordList[1]) == 1:
            for word in viableWordList[1]:
                associated_words.append(word.word.upper())
        else:
            errors_list.append([pharoah,viableWordList])

    print("[B]" + pharoah.upper() + "[\\B]: " + str(associated_words) + "\n")

print("Does not Have property:")
print("---------------------------\n")
for pharoah in has_not_property_pharoahs:
    associated_words = []
    for viableWordList in has_not_property_pharoahs[pharoah]:
        if len(viableWordList[1]) == 1:
            for word in viableWordList[1]:
                associated_words.append(word.word.upper())
        else:
            errors_list.append([pharoah,viableWordList])

    print("[B]" + pharoah.upper() + "[\\B]: " + str(associated_words) + "\n")

print("/n/nErrors")
print("---------------------------\n")

for error in errors_list:
        print(error[0] + " : " + error[1][0] + " - " + str([word.word.upper() for word in error[1][1]]))


