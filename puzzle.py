import helper_funcs as Helper

class Puzzle:
    def __init__(self, row, col, clueInfo):
        self.row = row
        self.col = col
        self.clueInfo = clueInfo

        self.hasProperty = ""
        self.hasPropertyValue = []

        self.viableWords = []

        self.hasSumTotalTest = False
        self.sumTotal = 0
        self.hasRangeTotalTest = False
        self.rangeTotal = []
        self.sumDivisibleTests = []
        self.sumNotDivisibleTests =[]

        self.base26Test = []
        self.base26DivisibleTests = []
        self.base26NotDivisibleTests = []

        self.hasScrabbleTotalTest = False
        self.scrabbleTotal = 0
        self.hasScrabbleRangeTest = False
        self.scrabbleRange = []

        self.commonestLettersSubTest = []
        self.commonestVowelsSubTest = []
        self.commonestConsonantsSubTest = []
        self.vowelSubTest = []
        self.consonantSubTest = []
        self.countryCodesSubTest = []
        self.chemicalCodesSubTest = []
        self.smallWordsSubTest = []
        self.qwertyTopRowSubTest = []
        self.qwertyMiddleRowSubTest = []
        self.qwertyBottomRowSubTest = []
        self.startsWithTest = []
        self.endsWithTest = []
        self.shaHashTest = []
        self.lengthTest = []

        self.base26UintTest = []
        self.base26IntTest = []
        self.base26FloatTest = []
        self.base26DoubleTest = []

        self.distinctVowelTest = []
        self.distinctConsonantTest = []
        self.distinctLetterTest = []

        self.atLeastOneDLTest = []
        self.atLeastTwoSameDLTest = []
        self.atLeastTwoDiffDLTest = []

        self.oneOffAnagTest = []
        self.twoOffAnagTest = []
        self.fullAnagTest = []

        self.stateCodesSubTest = []

        self.ceaserCipherTest = []

        self.contains = ""


def parsePuzzleData( lines, puzzleFileName, onlyClues, onlyHasPropertyPuzzles, puzzleRowToRecord = -1 ):
    puzzle = None
    
    rowNumber = puzzleFileName.split('.')[0].split('_')[0].strip('row')
    colNumber = puzzleFileName.split('.')[0].split('_')[1].strip('col')
    answerClue = ""
    shouldClueNextLine = False
    hasProperty = ""
    hasPropertyValue = []
    hasSumTotalTest = False
    sumTotal = 0
    hasRangeTotalTest = False
    rangeTotal = []
    sumDivisibleTests = []
    sumNotDivisibleTests = []
    base26Test = []
    base26DivisibleTests = []
    base26NotDivisibleTests = []
    
    
    hasScrabbleTotalTest = False
    scrabbleTotal = 0
    hasScrabbleRangeTest = False
    scrabbleRange = []
    
    commonestLettersSubTest = []
    commonestVowelsSubTest = []
    commonestConsonantsSubTest = []
    vowelSubTest = []
    consonantSubTest = []
    countryCodesSubTest = []
    chemicalCodesSubTest = []
    smallWordsSubTest = []
    qwertyTopRowSubTest = []
    qwertyMiddleRowSubTest = []
    qwertyBottomRowSubTest = []
    startsWithTest = []
    endsWithTest = []
    shaHashTest = []
    lengthTest = []

    base26UintTest = []
    base26IntTest = []
    base26FloatTest = []
    base26DoubleTest = []

    distinctVowelTest = []
    distinctConsonantTest = []
    distinctLetterTest = []

    atLeastOneDLTest = []
    atLeastTwoSameDLTest = []
    atLeastTwoDiffDLTest = []

    oneOffAnagTest = []
    twoOffAnagTest = []
    fullAnagTest = []

    stateCodesSubTest = []

    ceaserCipherTest = []
    
    contains = ""
    
    for line in lines:
        
        if shouldClueNextLine:
            shouldClueNextLine = False
            answerClue = line
            
        if line == "":
            shouldClueNextLine = True
            
        if not shouldClueNextLine and answerClue == "":
            if line.find("Has property") != -1:
                hasProperty = line.split(':')[0].split()[-1]
                if line.split(':')[1].split()[0] == "YES":
                    hasPropertyValue = [True]
                elif line.split(':')[1].split()[0] == "NO":
                    hasPropertyValue = [False]
            elif line.find("Contains:") != -1:
                contains = line.split(':')[1].split()[0].lower()
            elif line.find("Sum of letters") != -1:
                
                if line.find("divisible") != -1:
                    yesOrNoString = line.split(':')[1].split()[0]
                    value = int(line.split(':')[0].split()[-1])
                    if yesOrNoString == "YES":
                        sumDivisibleTests.append(value)
                    else:
                        sumNotDivisibleTests.append(value)
                else:
                    rangeString = line.split(':')[1]
                    if rangeString.find("between") != -1:
                        hasRangeTotalTest = True
                        startStr = line.split(':')[1].split()[1]
                        endStr = line.split(':')[1].split()[3]
                        rangeTotal = [int(startStr), int(endStr)]
                    else:
                        hasSumTotalTest = True
                        sumTotal = int(line.split(':')[1].split()[0])

            elif line.find("Word interpreted as a base 26 number") != -1:
                if line.find("divisible") != -1:
                    yesOrNoString = line.split(':')[1].split()[0]
                    value = int(line.split(':')[0].split()[-1])
                    if yesOrNoString == "YES":
                        base26DivisibleTests.append(value)
                    else:
                        base26NotDivisibleTests.append(value)
                else:
                    rangeString = line.split(':')[1]
                    if rangeString.find("between") != -1:
                        base26Test = [int(line.split(':')[1].split()[1]), int(line.split(':')[1].split()[3])]
                    elif line.find("representable as an unsigned 32-bit integer") != -1:
                        if line.split(':')[1].split()[0] == "YES":
                            base26UintTest = [True]
                        elif line.split(':')[1].split()[0] == "NO":
                            base26UintTest = [False]
                    elif line.find("representable as an unsigned 64-bit integer") != -1:
                        if line.split(':')[1].split()[0] == "YES":
                            base26IntTest = [True]
                        elif line.split(':')[1].split()[0] == "NO":
                            base26IntTest = [False]
                    elif line.find("exactly representable in IEEE 754 single-precision floating point format") != -1:
                        if line.split(':')[1].split()[0] == "YES":
                            base26FloatTest = [True]
                        elif line.split(':')[1].split()[0] == "NO":
                            base26FloatTest = [False]
                    elif line.find("exactly representable in IEEE 754 double-precision floating point format") != -1:
                        if line.split(':')[1].split()[0] == "YES":
                            base26DoubleTest = [True]
                        elif line.split(':')[1].split()[0] == "NO":
                            base26DoubleTest = [False]
                    else:
                        print(line)
                        base26Test = [int(line.split(':')[1].split()[0])]
                
            elif line.find("Scrabble") != -1:
                if line.find("between") != -1:
                    hasScrabbleRangeTest = True
                    startStr = line.split(':')[1].split()[1]
                    endStr = line.split(':')[1].split()[3]
                    scrabbleRange = [int(startStr), int(endStr)]
                else:
                    hasScrabbleTotalTest = True
                    scrabbleTotal = int(line.split(':')[1].split()[0])

            elif line.find("Most common") != -1:
                if line.find("Most common vowel") != -1:
                    commonestVowelsSubTest = Helper.determineSubTestType(line)
                elif line.find("Most common consonant") != -1:
                    commonestConsonantsSubTest = Helper.determineSubTestType(line)
                elif line.find("letter") != -1:
                    commonestLettersSubTest = Helper.determineSubTestType(line)
            elif line.find("Consonant") != -1:
                consonantSubTest = Helper.determineSubTestType(line)
            elif line.find("Vowels") != -1:
                vowelSubTest = Helper.determineSubTestType(line)
            elif line.find("If you marked nonoverlapping officially-assigned ISO 3166-1 alpha-2 country codes, you could mark at most") != -1:
                countryCodesSubTest = Helper.determineSubTestType(line)
            elif line.find("If you marked nonoverlapping chemical element symbols (atomic number 112 or below)") != -1:
                chemicalCodesSubTest = Helper.determineSubTestType(line)
            elif line.find("If you marked nonoverlapping occurrences of words in the word list that are 3 or fewer letters long, you could mark at most") != -1:
                smallWordsSubTest = Helper.determineSubTestType(line)
            elif line.find("QWERTY") != -1:
                if line.find("top row") != -1:
                    qwertyTopRowSubTest = Helper.determineSubTestType(line)
                if line.find("middle row") != -1:
                    qwertyMiddleRowSubTest = Helper.determineSubTestType(line)
                if line.find("bottom row") != -1:
                    qwertyBottomRowSubTest = Helper.determineSubTestType(line)
            elif line.find("Starts with") != -1:
                if line.find("a vowel") != -1:
                    yesOrNoString = line.split(':')[1].split()[0]
                    if yesOrNoString == "YES":
                        startsWithTest = ["vowel", True]    
                    else:
                        startsWithTest = ["vowel", False]
                else:
                    startsWithTest = [line.split(':')[1].split()[0].lower()]
            elif line.find("Ends with") != -1:
                if line.find("a vowel") != -1:
                    yesOrNoString = line.split(':')[1].split()[0]
                    if yesOrNoString == "YES":
                        endsWithTest = ["vowel", True]    
                    else:
                        endsWithTest = ["vowel", False]
                else:
                    endsWithTest = [line.split(':')[1].split()[0].lower()]
            elif line.find("SHA-1 hash") != -1:
                if line.find("starts with") != -1:
                    shaHashTest = ["starts", line.split(':')[1].split()[0]]
                elif line.find("ends with") != -1:
                    shaHashTest = ["ends", line.split(':')[1].split()[0]]
                elif line.find("contains") != -1:
                    shaHashTest = ["contains", line.split(':')[1].split()[0]]
            elif line.find("Length:") != -1:
                lengthTest = Helper.determineSubTestType(line)
            elif line.find("anagram") != -1:
                
                if line.find("Can be combined with one additional") != -1:
                    if line.split(':')[1].split()[0] == "YES":
                        oneOffAnagTest = [True]
                    elif line.split(':')[1].split()[0] == "NO":
                        oneOffAnagTest = [False]
                elif line.find("Can be combined with two additional") != -1:
                    if line.split(':')[1].split()[0] == "YES":
                        twoOffAnagTest = [True]
                    elif line.split(':')[1].split()[0] == "NO":
                        twoOffAnagTest = [False]
                else:
                    if line.split(':')[1].split()[0] == "YES":
                        fullAnagTest = [True]
                    elif line.split(':')[1].split()[0] == "NO":
                        fullAnagTest = [False]
            elif line.find("Distinct") != -1:
                if line.find("vowels") != -1:
                    distinctVowelTest = Helper.determineSubTestType(line)
                elif line.find("consonants") != -1:
                    distinctConsonantTest = Helper.determineSubTestType(line)
                elif line.find("letters") != -1:
                    distinctLetterTest = Helper.determineSubTestType(line)

            elif line.find("Contains at least one doubled letter") != -1:
                if line.split(':')[1].split()[0] == "YES":
                    atLeastOneDLTest = [True]
                elif line.split(':')[1].split()[0] == "NO":
                    atLeastOneDLTest = [False]
            elif line.find("Contains at least two different doubled letters") != -1:
                if line.split(':')[1].split()[0] == "YES":
                    atLeastTwoDiffDLTest = [True]
                elif line.split(':')[1].split()[0] == "NO":
                    atLeastTwoDiffDLTest = [False]
            elif line.find("Contains at least two nonoverlapping occurrences of the same doubled letter") != -1:
                if line.split(':')[1].split()[0] == "YES":
                    atLeastTwoSameDLTest = [True]
                elif line.split(':')[1].split()[0] == "NO":
                    atLeastTwoSameDLTest = [False]
            elif line.find("If you marked nonoverlapping US state postal abbreviations") != -1:
                stateCodesSubTest = Helper.determineSubTestType(line)

            elif line.find("Can be Caesar shifted to produce another word in the word list") != -1:
                if line.split(':')[1].split()[0] == "YES":
                    ceaserCipherTest = [True]
                elif line.split(':')[1].split()[0] == "NO":
                    ceaserCipherTest = [False]
            else:
                if not onlyClues:
                    print(line)
            
    shouldAddPuzzle = True
    if onlyClues:
        shouldAddPuzzle = answerClue != ""

    if onlyHasPropertyPuzzles:
        shouldAddPuzzle = hasProperty != ""

    if puzzleRowToRecord != -1:
        if puzzleRowToRecord == int(rowNumber):
            shouldAddPuzzle = True
        else:
            shouldAddPuzzle = False

    if shouldAddPuzzle:
        puzzle = Puzzle(int(rowNumber),int(colNumber),answerClue)

        puzzle.hasProperty = hasProperty
        puzzle.hasPropertyValue = hasPropertyValue
        
        puzzle.hasSumTotalTest = hasSumTotalTest
        puzzle.sumTotal = sumTotal
        puzzle.hasRangeTotalTest = hasRangeTotalTest
        puzzle.rangeTotal = rangeTotal
        puzzle.sumDivisibleTests = sumDivisibleTests
        puzzle.sumNotDivisibleTests = sumNotDivisibleTests

        puzzle.base26Test = base26Test
        puzzle.base26DivisibleTests = base26DivisibleTests
        puzzle.base26NotDivisibleTests = base26NotDivisibleTests
        
        puzzle.hasScrabbleTotalTest = hasScrabbleTotalTest
        puzzle.scrabbleTotal = scrabbleTotal
        puzzle.hasScrabbleRangeTest = hasScrabbleRangeTest
        puzzle.scrabbleRange = scrabbleRange

        puzzle.commonestLettersSubTest = commonestLettersSubTest
        puzzle.commonestVowelsSubTest = commonestVowelsSubTest
        puzzle.commonestConsonantsSubTest = commonestConsonantsSubTest
        puzzle.vowelSubTest = vowelSubTest
        puzzle.consonantSubTest = consonantSubTest
        puzzle.countryCodesSubTest = countryCodesSubTest
        puzzle.chemicalCodesSubTest = chemicalCodesSubTest
        puzzle.smallWordsSubTest = smallWordsSubTest
        puzzle.qwertyTopRowSubTest = qwertyTopRowSubTest
        puzzle.qwertyMiddleRowSubTest = qwertyMiddleRowSubTest
        puzzle.qwertyBottomRowSubTest = qwertyBottomRowSubTest
        puzzle.startsWithTest = startsWithTest
        puzzle.endsWithTest = endsWithTest
        puzzle.shaHashTest = shaHashTest
        puzzle.lengthTest = lengthTest

        puzzle.base26UintTest = base26UintTest
        puzzle.base26IntTest = base26IntTest
        puzzle.base26FloatTest = base26FloatTest
        puzzle.base26DoubleTest = base26DoubleTest

        puzzle.distinctVowelTest = distinctVowelTest
        puzzle.distinctConsonantTest = distinctConsonantTest
        puzzle.distinctLetterTest = distinctLetterTest

        puzzle.atLeastOneDLTest = atLeastOneDLTest
        puzzle.atLeastTwoSameDLTest = atLeastTwoSameDLTest
        puzzle.atLeastTwoDiffDLTest = atLeastTwoDiffDLTest

        puzzle.oneOffAnagTest = oneOffAnagTest
        puzzle.twoOffAnagTest = twoOffAnagTest
        puzzle.fullAnagTest = fullAnagTest

        puzzle.stateCodesSubTest = stateCodesSubTest

        puzzle.ceaserCipherTest = ceaserCipherTest

        puzzle.contains = contains

    return puzzle
