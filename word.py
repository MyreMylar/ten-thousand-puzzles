import csv
import hashlib
import operator
import re
from collections import Counter


class Word:
    def __init__(self, word, wordList, country_codes_database, chemical_symbols_database, short_words_database, state_codes_database, ceaser_translations):

        self.short_words_database = short_words_database
        self.state_codes_database = state_codes_database
        self.ceaser_translations = ceaser_translations
        #start debug variables
        self.sorted_codes = []
        self.found_country_codes = []
        self.countryCodes = []
        self.chemicalCodes = []
        self.sorted_chemical_codes = []
        self.sorted_short_words = []
        self.valid_short_word_sets = []
        self.valid_state_codes_sets = []
        self.fullAnagrams = []
        self.twoOffAnagrams = []
        self.found_double_letters = []
        #end debug variables

        self.wordList = wordList
        self.word = word.lower()
        self.counterWord = Counter(self.word)
        self.length = len(self.word)
        self.sortedWord = sorted(self.word)
        self.sh1Hash = hashlib.sha1(self.word.encode()).hexdigest().upper()
        self.sum = self.sumSelf()
        self.base26Interp = self.base26Self()
        self.scrabbleValue = self.scrabbleValue()

        self.testableValues = {}
        
        self.vowelTotal = 0
        self.vowelPercentage = 0.0
        
        self.consonantTotal = 0
        self.consonantPercentage = 0.0
        
        self.commonestLettersTotal = 0
        self.commonestLettersPercentage = 0.0

        self.numberOfCountryCodeLetters = 0
        self.countryCodesPercentage = 0.0

        self.numberOfChemicalCodesLetters = 0
        self.chemicalCodesPercentage = 0

        self.numberOfShortWordLetters = 0
        self.shortWordsPercentage = 0

        self.distinctConsonants = 0
        self.distinctLetters = 0
        self.distinctVowels = 0

        self.atLeastOneDoubleLetter = False
        self.atLeastTwoDoubleLetters = False
        self.twoOfTheSameDoubleLetter = False

        self.foundCeaserShift = False
        
        self.findDoubleLetters()
        self.calculateLetterPercentagesAndTotals() 
        self.findCountryCodes(country_codes_database)
        self.findChemicalCodes(chemical_symbols_database)
        
        self.testableValues["length"] = [len(self.word), 1.0]
        self.testableValues["vowels"] = [self.vowelTotal, self.vowelPercentage]
        self.testableValues["consonants"] = [self.consonantTotal, self.consonantPercentage]
        self.testableValues["commonestLetters"] = [self.commonestLettersTotal, self.commonestLettersPercentage]
        self.testableValues["countryCodeLetters"] = [self.numberOfCountryCodeLetters, self.countryCodesPercentage]
        self.testableValues["chemicalCodeLetters"] = [self.numberOfChemicalCodesLetters, self.chemicalCodesPercentage]
        self.testableValues["distinctVowels"] = [self.distinctVowels, self.distinctVowels/self.length]
        self.testableValues["distinctConsonants"] = [self.distinctConsonants, self.distinctConsonants/self.length]
        self.testableValues["distinctLetters"] = [self.distinctLetters, self.distinctLetters/self.length]
        

        self.calculateQWERTYValues()

        self.hasFullAnag = False
        self.hasOneOffAnag = False
        self.hasTwoOffAnag = False
        self.hasCalculatedHardData = False

    def calculateHardData(self, wordsInSizeRange):
        self.calculateHasAnagrams(wordsInSizeRange)
        self.findShortWords()
        self.findStateCodes(self.state_codes_database)
        self.findCeaserShifts(wordsInSizeRange)
        self.hasCalculatedHardData = True

    def findCeaserShifts(self, wordsInSizeRange):
        for translation in self.ceaser_translations:
            shifted_word = str.translate(self.word, translation)
            for word in wordsInSizeRange[self.length]:
                if word == shifted_word:
                    self.foundCeaserShift = True
                    break
                    

    def findDoubleLetters(self):
        doubleLetters = ['aa','bb','cc','dd','ee',
                         'ff','gg','hh','ii','jj',
                         'kk','ll','mm','nn','oo',
                         'pp','qq','rr','ss','tt',
                         'uu','vv','ww','xx','yy',
                         'zz']

        for doubleLetter in doubleLetters:
            found_occurances = [pos.start() for pos in re.finditer(doubleLetter, self.word)]
            for occurance in found_occurances:
                self.found_double_letters.append(doubleLetter)

        doubleCounter = Counter(self.found_double_letters)

        self.atLeastOneDoubleLetter = len(doubleCounter) > 0
        self.atLeastTwoDoubleLetters = len(doubleCounter) > 1
        if len(doubleCounter) > 0:
            self.twoOfTheSameDoubleLetter = (doubleCounter.most_common(1)[0][1] > 1)

        
    def powerset(self, seq):
        """
        Returns all the subsets of this set. This is a generator.
        """
        if len(seq) <= 1:
            yield seq
            yield []
        else:
            for item in self.powerset(seq[1:]):
                yield [seq[0]]+item
                yield item

    def calculateHasAnagrams(self, wordsInSizeRange):
        hasFullAnag = False
        hasOneOffAnag = False
        hasTwoOffAnag = False

        for word in wordsInSizeRange[self.length]:
            if hasFullAnag:
                break
            elif word.word != self.word:
                hasFullAnag = not (self.counterWord - word.counterWord)
                if hasFullAnag:
                    self.fullAnagrams.append(word)
 
        if self.length+1 < len(wordsInSizeRange):
            for word in wordsInSizeRange[self.length+1]:
                if hasOneOffAnag:
                    break
                else:
                    hasOneOffAnag = not(self.counterWord - word.counterWord)
            
        if self.length+2 < len(wordsInSizeRange):
            for word in wordsInSizeRange[self.length+2]:
                
                if hasTwoOffAnag: 
                    break
                else:
                    hasTwoOffAnag = not(self.counterWord - word.counterWord)
                    if hasTwoOffAnag:
                        self.twoOffAnagrams.append(word)

        self.hasFullAnag = hasFullAnag
        self.hasOneOffAnag = hasOneOffAnag
        self.hasTwoOffAnag = hasTwoOffAnag
        
            
    def calculateQWERTYValues(self):
        letterCounts = self.counterWord
        
        bottomQWERTY = ['z','x','c','v','b','n','m']
        middleQWERTY = ['a','s','d','f','g','h','j','k','l']
        topQWERTY = ['q','w','e','r','t','y','u','i','o','p']

        bottomQWERTYTotal = 0
        for key in letterCounts:
            if key in bottomQWERTY:
                bottomQWERTYTotal += letterCounts[key]

        middleQWERTYTotal = 0
        for key in letterCounts:
            if key in middleQWERTY:
                middleQWERTYTotal += letterCounts[key]

        topQWERTYTotal = 0
        for key in letterCounts:
            if key in topQWERTY:
                topQWERTYTotal += letterCounts[key]

        bottomQWERTYPercentage = bottomQWERTYTotal / len(self.word)
        middleQWERTYPercentage = middleQWERTYTotal / len(self.word)
        topQWERTYPercentage = topQWERTYTotal / len(self.word)
        
        self.testableValues["bottomQWERTY"] = [bottomQWERTYTotal, bottomQWERTYPercentage]
        self.testableValues["middleQWERTY"] = [middleQWERTYTotal, middleQWERTYPercentage]
        self.testableValues["topQWERTY"] = [topQWERTYTotal, topQWERTYPercentage]

    def sumSelf(self):
        total = 0       
        for letter in self.word:
            total += ord(letter) - 96      
        return total

    def base26Self(self):
        letters = []      
        for letter in self.word:
            letter26 = str(ord(letter) - 97)
            letters.append(letter26)
        number26 = [int(i) for i in reversed(letters)]
        for i in range(len(number26)):
            number26[i] = number26[i] * (26 ** i)
 
        return sum(number26)

    def scrabbleValue(self):
        value_list = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 
                      'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 
                      'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 
                      'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}
        return sum(value_list[char] for char in self.word)

    def calculateLetterPercentagesAndTotals(self):
        vowels = ['a','e','i','o','u']
        self.distinctLetters = len(self.counterWord)
        most_common_value = self.counterWord.most_common(1)[0][1]
        
        numberOfVowels = 0
        foundVowels = [letter for letter in self.word if letter in vowels]
        foundConsonants = [letter for letter in self.word if letter not in vowels]
        self.distinctVowels = 0
        for key in self.counterWord:
            if key in vowels:
                self.distinctVowels += 1
                numberOfVowels += self.counterWord[key]

        self.distinctConsonants = self.distinctLetters - self.distinctVowels
        most_common_consonant_value = 0
        if len(foundConsonants) > 0:
            most_common_consonant_value = Counter(foundConsonants).most_common(1)[0][1]

        most_common_vowel_value = 0
        if len(foundVowels) > 0:
            most_common_vowel_value = Counter(foundVowels).most_common(1)[0][1]     

        self.vowelTotal = numberOfVowels
        self.consonantTotal = len(self.word) - numberOfVowels
        self.vowelPercentage = numberOfVowels / len(self.word)
        self.consonantPercentage = 1.0 - self.vowelPercentage
        self.commonestLettersTotal = most_common_value
        self.commonestLettersPercentage = most_common_value / len(self.word)

        self.testableValues["commonestVowels"] = [most_common_vowel_value, most_common_vowel_value / len(self.word)]
        self.testableValues["commonestConsonants"] = [most_common_consonant_value, most_common_consonant_value / len(self.word)]

    def findCountryCodes(self, country_codes_database):
        
        for code in country_codes_database:
            found_occurances = [pos.start() for pos in re.finditer(code, self.word)]
            for occurance in found_occurances:
                self.found_country_codes.append([code,occurance])


        overlap_dict = []
        for code in self.found_country_codes:
            overlaps = []
            for other_code in self.found_country_codes:
                if code[1] != other_code[1]:
                    if abs(code[1] - other_code[1]) == 1:
                        overlaps.append(other_code[0])
            overlap_dict.append([code[0],overlaps,len(overlaps), -len(code[0])])

        self.sorted_codes = sorted(overlap_dict, key=operator.itemgetter(3,2))

        self.countryCodes = []
        for code in self.sorted_codes:
            if code[2] == 0:
                self.countryCodes.append(code[0])
            else:
                hasNoOverlaps = True
                for overlapCode in code[1]:
                    for otherCode in self.countryCodes:
                        if overlapCode == otherCode:
                            hasNoOverlaps = False
                if hasNoOverlaps:
                    self.countryCodes.append(code[0])
        joinedString = ""
        for code in self.countryCodes:
            joinedString += code
        self.numberOfCountryCodeLetters = len(joinedString)
        self.countryCodesPercentage = self.numberOfCountryCodeLetters / len(self.word)               

    def findChemicalCodes(self, chemical_symbols_database):
        found_chemical_codes = []
        for code in chemical_symbols_database:
            found_occurances = [pos.start() for pos in re.finditer(code, self.word)]
            for occurance in found_occurances:
                found_chemical_codes.append([code,occurance])


        overlap_dict = []
        for code in found_chemical_codes:
            overlaps = []
            for other_code in found_chemical_codes:
                if code[0] == other_code[0] and code[1] == other_code[1]:
                    pass #don't add self to overlaps
                else:
                    if code[1] == other_code[1]:
                        overlaps.append(other_code[0])
                    if len(other_code[0]) == 2 and code[1] - other_code[1] == 1:
                        overlaps.append(other_code[0])
                    if len(code[0]) == 2 and other_code[1] - code[1] == 1:
                        overlaps.append(other_code[0])
            overlap_dict.append([code[0],overlaps,len(overlaps), -len(code[0])])

        
        self.sorted_chemical_codes = sorted(overlap_dict, key=operator.itemgetter(3,2))

        chemicalCodes = []
        for code in self.sorted_chemical_codes:
            if code[2] == 0:
                chemicalCodes.append(code[0])
            else:
                hasNoOverlaps = True
                for overlapCode in code[1]:
                    for otherCode in chemicalCodes:
                        if overlapCode == otherCode:
                            hasNoOverlaps = False
                if hasNoOverlaps:
                    chemicalCodes.append(code[0])
        self.chemicalCodes = chemicalCodes
        joinedString = ""
        for code in chemicalCodes:
            joinedString += code
        self.numberOfChemicalCodesLetters = len(joinedString)
        self.chemicalCodesPercentage = self.numberOfChemicalCodesLetters / len(self.word)
        
    def findStateCodes(self, state_codes_database):
        found_state_codes = []
        for code in state_codes_database:
            found_occurances = [pos.start() for pos in re.finditer(code, self.word)]
            for occurance in found_occurances:
                found_state_codes.append([code,occurance])

        state_codes_powerset = self.powerset(found_state_codes)

        
        for subset in state_codes_powerset:
            noOverlaps = True
            for occuranceA in subset:
                if noOverlaps:
                    for occuranceB in subset:
                        if noOverlaps:
                            if occuranceA[0] == occuranceB[0] and occuranceA[1] == occuranceB[1]:
                                pass
                            else:
                                posDiff = occuranceA[1] - occuranceB[1]
                                if posDiff == 0:
                                    noOverlaps = False
                                elif posDiff < 0 and len(occuranceA[0]) > abs(posDiff):
                                    noOverlaps = False
                                elif posDiff > 0 and len(occuranceB[0]) > posDiff:
                                    noOverlaps = False
                        else:
                            break
                else:
                    break
            if noOverlaps:
                self.valid_state_codes_sets.append(subset)    

       
        longestPotentialWord = []
        maxLength = 0
        for subset in self.valid_state_codes_sets:
            totalWordLength = 0
            for word in subset:
                totalWordLength += len(word[0])
            if totalWordLength > maxLength:
                maxLength = totalWordLength
                longestPotentialWord = subset 
                    
        self.testableValues["stateCodes"] = [maxLength, maxLength / len(self.word)]
    
    def findShortWords(self):
        found_short_words = []
        for code in self.short_words_database:
            found_occurances = [pos.start() for pos in re.finditer(code, self.word)]
            for occurance in found_occurances:
                found_short_words.append([code,occurance])

        short_word_powerset = self.powerset(found_short_words)

        
        for subset in short_word_powerset:
            noOverlaps = True
            for occuranceA in subset:
                if noOverlaps:
                    for occuranceB in subset:
                        if noOverlaps:
                            if occuranceA[0] == occuranceB[0] and occuranceA[1] == occuranceB[1]:
                                pass
                            else:
                                posDiff = occuranceA[1] - occuranceB[1]
                                if posDiff == 0:
                                    noOverlaps = False
                                elif posDiff < 0 and len(occuranceA[0]) > abs(posDiff):
                                    noOverlaps = False
                                elif posDiff > 0 and len(occuranceB[0]) > posDiff:
                                    noOverlaps = False
                        else:
                            break
                else:
                    break
            if noOverlaps:
                self.valid_short_word_sets.append(subset)    

       
        longestPotentialWord = []
        maxLength = 0
        for subset in self.valid_short_word_sets:
            totalWordLength = 0
            for word in subset:
                totalWordLength += len(word[0])
            if totalWordLength > maxLength:
                maxLength = totalWordLength
                longestPotentialWord = subset 
                    
        self.numberOfShortWordLetters = maxLength
        self.shortWordsPercentage = self.numberOfShortWordLetters / len(self.word)
        self.testableValues["shortWords"] = [self.numberOfShortWordLetters, self.shortWordsPercentage]

