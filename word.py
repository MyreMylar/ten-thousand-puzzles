import csv
import hashlib
import operator
import re
from collections import Counter


class Word:
    def __init__(self, word, wordList, country_codes_database, chemical_symbols_database, short_words_database, state_codes_database, ceaser_translations):

        self.short_words_database = short_words_database
        self.state_codes_database = state_codes_database
        self.country_codes_database = country_codes_database
        self.chemical_symbols_database = chemical_symbols_database
        
        self.ceaser_translations = ceaser_translations
  
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
  
        self.testableValues["length"] = [len(self.word), 1.0]
        self.testableValues["vowels"] = [self.vowelTotal, self.vowelPercentage]
        self.testableValues["consonants"] = [self.consonantTotal, self.consonantPercentage]
        self.testableValues["commonestLetters"] = [self.commonestLettersTotal, self.commonestLettersPercentage]
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
        self.findCountryCodes(self.country_codes_database)
        self.findChemicalCodes(self.chemical_symbols_database)
        self.findCeaserShifts(wordsInSizeRange)
        self.hasCalculatedHardData = True

    def findCeaserShifts(self, wordsInSizeRange):
        for translation in self.ceaser_translations:
            shifted_word = str.translate(self.word, translation)
            for word in wordsInSizeRange[self.length]:
                if word.word == shifted_word:
                    self.foundCeaserShift = True
                    break
                    

    def findDoubleLetters(self):
        doubleLetters = ['aa','bb','cc','dd','ee',
                         'ff','gg','hh','ii','jj',
                         'kk','ll','mm','nn','oo',
                         'pp','qq','rr','ss','tt',
                         'uu','vv','ww','xx','yy',
                         'zz']

        found_double_letters = []
        
        for doubleLetter in doubleLetters:
            found_occurances = [pos.start() for pos in re.finditer(doubleLetter, self.word)]
            for occurance in found_occurances:
                found_double_letters.append(doubleLetter)

        doubleCounter = Counter(found_double_letters)

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

    def isLetterVowel(self, letter):
        vowels = ['a','e','i','o','u']
        return letter in vowels
    
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
        found_country_codes = []
        for code in country_codes_database:
            found_occurances = [pos.start() for pos in re.finditer(code, self.word)]
            for occurance in found_occurances:
                found_country_codes.append([code,occurance])

        country_code_powerset = self.powerset(found_country_codes)

        valid_country_codes = []
        for subset in country_code_powerset:
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
                valid_country_codes.append(subset)    

       
        longestPotentialWord = []
        maxLength = 0
        for subset in valid_country_codes:
            totalWordLength = 0
            for word in subset:
                totalWordLength += len(word[0])
            if totalWordLength > maxLength:
                maxLength = totalWordLength
                longestPotentialWord = subset 
                    
        self.numberOfCountryCodeLetters = maxLength
        self.countryCodesPercentage = self.numberOfCountryCodeLetters / len(self.word)
        self.testableValues["countryCodeLetters"] = [self.numberOfCountryCodeLetters, self.countryCodesPercentage]
               

    def findChemicalCodes(self, chemical_symbols_database):
        found_chemical_codes = []
        for code in chemical_symbols_database:
            found_occurances = [pos.start() for pos in re.finditer(code, self.word)]
            for occurance in found_occurances:
                found_chemical_codes.append([code,occurance])

        chemical_code_powerset = self.powerset(found_chemical_codes)

        valid_chemical_codes = []
        for subset in chemical_code_powerset:
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
                valid_chemical_codes.append(subset)    

       
        longestPotentialWord = []
        maxLength = 0
        for subset in valid_chemical_codes:
            totalWordLength = 0
            for word in subset:
                totalWordLength += len(word[0])
            if totalWordLength > maxLength:
                maxLength = totalWordLength
                longestPotentialWord = subset 
                    
        self.numberOfChemicalCodesLetters = maxLength
        self.chemicalCodesPercentage = self.numberOfChemicalCodesLetters / len(self.word)
        self.testableValues["chemicalCodeLetters"] = [self.numberOfChemicalCodesLetters, self.chemicalCodesPercentage]

        
    def findStateCodes(self, state_codes_database):
        found_state_codes = []
        for code in state_codes_database:
            found_occurances = [pos.start() for pos in re.finditer(code, self.word)]
            for occurance in found_occurances:
                found_state_codes.append([code,occurance])

        state_codes_powerset = self.powerset(found_state_codes)

        valid_state_codes_sets = []
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
                valid_state_codes_sets.append(subset)    

       
        longestPotentialWord = []
        maxLength = 0
        for subset in valid_state_codes_sets:
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

        valid_short_word_sets = []
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
                valid_short_word_sets.append(subset)    

       
        longestPotentialWord = []
        maxLength = 0
        for subset in valid_short_word_sets:
            totalWordLength = 0
            for word in subset:
                totalWordLength += len(word[0])
            if totalWordLength > maxLength:
                maxLength = totalWordLength
                longestPotentialWord = subset 
                    
        self.numberOfShortWordLetters = maxLength
        self.shortWordsPercentage = self.numberOfShortWordLetters / len(self.word)
        self.testableValues["shortWords"] = [self.numberOfShortWordLetters, self.shortWordsPercentage]

