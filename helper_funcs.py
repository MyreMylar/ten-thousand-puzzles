
def determineSubTestType(line):
    subTest = []
    if line.find("between") != -1 and line.find("%") != -1:
        startStr = line.split(':')[1].split()[1][:-1]
        endStr = line.split(':')[1].split()[3][:-1]
        subTest = ["percentage",float(startStr)/100.0, float(endStr)/100.0]
    elif line.find("between") != -1:
        startStr = line.split(':')[1].split()[1]
        endStr = line.split(':')[1].split()[3]
        subTest = ["total",int(startStr), int(endStr)]
    elif line.find("exactly") != -1:
        subTest = ["percentage", float(line.split(':')[1].split()[1][:-1])/100.0]
    else:
        subTest = ["total", int(line.split(':')[1].split()[0])]

    return subTest

def runFailTest(word, valueName, subTest):
    wordValues = word.testableValues[valueName]
    unviableWord = False
    if len(subTest) > 0:
        if len(subTest) == 3:
            if subTest[0] == "percentage":
                if wordValues[1] < subTest[1] or wordValues[1] > subTest[2]:
                    unviableWord = True
            else:
                if wordValues[0] < subTest[1] or wordValues[0] > subTest[2]:
                    unviableWord = True
        elif len(subTest) == 2:
            if subTest[0] == "percentage":
                if wordValues[1] != subTest[1]:
                    unviableWord = True
            else:
                if wordValues[0] != subTest[1]:
                    unviableWord = True

    return unviableWord
