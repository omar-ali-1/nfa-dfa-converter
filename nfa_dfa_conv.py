### Omar Ali
### HW 4 NFA DFA Conversion
### Theory of Computation


def replaceComma(line):
    inSet = False
    for i in range(len(line)):
        if inSet:
            if line[i] == ',':
                line = line[:i] + '#' + line[i+1:]
        if line[i] == '{':
            inSet = True
        if line[i] == '}':
            inSet = False
    return line.strip('\r\n')
        

def populateMap(stateMap, line):
    items = line.split(',')
    state = items[0]
    toState0 = items[1]
    toState1 = items[2]
    if toState0 != '' and toState0[0] == '{':
        toState0 = toState0.strip('}{')
        toState0 = toState0.split('#')
    if toState1 != '' and toState1[0] == '{':
        toState1 = toState1.strip('}{')
        toState1 = toState1.split('#')
    stateMap[state] = [toState0, toState1]


def getStateConcat(toState):
    if toState == '' or not isinstance(toState, list):
        return toState
    else:
        return ''.join(sorted(list(set(toState))))


def getStateCombo(multiState, stateMap, pos):
    if isinstance(multiState, list):
        comboState = []
        for state in multiState:
            newStates = stateMap[state][pos]
            if isinstance(newStates, list):
                comboState.extend(newStates)
            else:
                comboState.append(newStates)
        if len(''.join(comboState)) == 2:
            return comboState[0]
        if len(''.join(comboState)) == 0:
            return ''
        comboState = set(comboState)
        if '' in comboState:
            comboState.remove('')
        return sorted(list(comboState))
    return stateMap[multiState][pos]


def convert(inputFileName, outputFileName):
    outputList = []
    toDef = []
    stateMap = {}
    defined = set()
    with open(inputFileName) as f:
        for line in f.readlines():
            line = replaceComma(line)
            populateMap(stateMap, line)

    # first state should be included no matter what
    toDef.append(sorted(stateMap.keys())[0])
    defined.add(sorted(stateMap.keys())[0])

    while toDef:
        state = toDef.pop(0)
        if not isinstance(state, list) and state in stateMap:
            toState0 = stateMap[state][0]
            toState1 = stateMap[state][1]
        else:
            toState0 = getStateCombo(state, stateMap, 0)
            toState1 = getStateCombo(state, stateMap, 1)
        if getStateConcat(toState0) not in defined:
            defined.add(getStateConcat(toState0))
            toDef.append(toState0)
        if getStateConcat(toState1) not in defined:
            defined.add(getStateConcat(toState1))
            toDef.append(toState1)
        outputList.append([getStateConcat(state), getStateConcat(toState0), getStateConcat(toState1)])

    with open(outputFileName, 'w') as f:
        f.write('state,0,1\r\n')
        for line in outputList:
            f.write(line[0]+','+line[1]+','+line[2]+'\r\n')


if __name__ == "__main__":
    convert('nfa-page873.csv', 'outputFile.csv')

