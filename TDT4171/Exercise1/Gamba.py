

import random
import statistics

def gambaMachine(iterations, amount):
    symbolArray = ["cherry","lemon", "bar", "bell"]
    print("Welcome to the Gamba Machine!")
    
    timesPlayed = 0
    for i in range(iterations):
        if amount == 0:
            print("You have no money, please insert money")
                
            return timesPlayed
        
        amount -= 1
        timesPlayed += 1
        
        if i%5 == 0:
            print( "Amount: ", amount)

        res = []
        for j in range(3):
            res.append(random.choice(symbolArray))

        match res:
            case ["lemon","lemon", "lemon"]:
                amount += 5
            case ["bar","bar", "bar"]:
                amount += 20
            case ["bell","bell", "bell"]:
                amount += 15
            case _:
                if res.count("cherry") == 3:
                    amount += 3
                elif res[0] == ("cherry") and res[1] == ("cherry"):
                    amount += 2
                elif res[0] == ("cherry"):
                    amount += 1
                continue


def main():
    print("Hello World!")
    timesPlayedArray = []
    for i in range (100000):
        timesPlayed = gambaMachine(100000, 10)
        timesPlayedArray.append(timesPlayed)


    summer = 0
    for i in range(len(timesPlayedArray)):
        summer += timesPlayedArray[i]
    avg = summer/1000

    print("Average number of times played: ", avg)
    print("Max number of times played: ", max(timesPlayedArray))
    print("Min number of times played: ", min(timesPlayedArray))
    print("Mean number of times played: ", statistics.mean(timesPlayedArray))
    print("Median number of times played: ", statistics.median(timesPlayedArray))

    
main()