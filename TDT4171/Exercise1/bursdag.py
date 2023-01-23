

import random


def birthday(n):
    personsInGroup = 1
    allBirthdays = []
    for i in range(n):
        randomBirthday = random.randint(1, 365)
        if randomBirthday in allBirthdays:
            return True
        allBirthdays.append(randomBirthday)
    return False

def birthdayGroup():
    personsInGroup = 0
    allBirthdays = []
    while len(allBirthdays) <= 365:
        randomBirthday = random.randint(1, 365)
        
        if randomBirthday in allBirthdays:
            personsInGroup += 1
            if len(allBirthdays) == 365:
                return personsInGroup
            continue
        
        allBirthdays.append(randomBirthday)
        personsInGroup += 1
    return personsInGroup

def simulateBirthdays(n, iterations):
    count = 0
    for i in range(iterations):
        if birthday(n):
            count += 1
    return count / iterations


def main():
    # for i in range (50):      
    #     res = simulateBirthdays(50, 100000)
    #     print(res)
    resSum = 0
    for i in range(100000):
        res = birthdayGroup()
        resSum += res
        
    print("GJENNOMSNITT GRUPPESTØRRELSE: ", resSum/10000) 
    
main()





