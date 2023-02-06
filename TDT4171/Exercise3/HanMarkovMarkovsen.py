#!/usr/bin/python
import numpy as np

#HAN MARKOV MARKOVSEN AKA HMM
#TDT4171 - Exercise 3

#Hidden Markov Model
#Umbrella problem med en fremoverlent algoritme

#State 0 = Regn
#State 1 = Ikke regn
#Evidence 0 = Umbrella
#Evidence 1 = No umbrella

#Transisjonsmatrise
#   0.7     0.3 True
#   0.3     0.7 False

#Observasjonsmatrise
#   0.9     0.2 True
#   0.1     0.8 False

TransitionMatrix = np.array([[0.7, 0.3], [0.3, 0.7]])
ObservationMatrix = np.array([[0.9, 0.2], [0.1, 0.8]])

initialProbability = np.array([0.5, 0.5])

def normalize(arr):
    return arr / np.sum(arr)

def forwardAlgorithm(evidenceArray, currentProbability):
    
    #Indicates that we've reached the end of the evidence array
    if len(evidenceArray) == 0:
        return currentProbability
    
    #Is true if the umbrella is used at the current time (evidence 0: true)
    if evidenceArray[0] == 0:
        r1 = TransitionMatrix[0] * currentProbability[0] + TransitionMatrix[1] * currentProbability[1]
        r1u1 = ObservationMatrix[0] * r1
        newCurrentProbability = normalize(r1u1)
        print("Umbrella is used, probability for rain at current time, NORMALIZED VALUE:", newCurrentProbability)
        return forwardAlgorithm(evidenceArray[1:], newCurrentProbability)
    
    #Should probably have been switched evidence 0 and 1 as it would indicate that the umbrella is used in a normal boolean sense
    
    #Is true if the umbrella is not used at the current time (evidence 1: false)
    if evidenceArray[0] == 1:
        r1 = TransitionMatrix[0] * currentProbability[0] + TransitionMatrix[1] * currentProbability[1]
        r1u1 = ObservationMatrix[1] * r1
        newCurrentProbability = normalize(r1u1)
        print("Umbrella is not used, probability for rain at current time, NORMALIZED VALUE:", newCurrentProbability)        
        return forwardAlgorithm(evidenceArray[1:], newCurrentProbability)
    
def main():
    # 0 = Evidence observes umbrella
    # 1 = Evidence observes no umbrella 

    # DEL 1 - TEST
    # Verifification of the algorithm given the exercise where Umbrella is true first 2 days
    print("PART 1 - VERIFICATION OF THE ALGORITHM")
    verifyImplementation = forwardAlgorithm([0,0], initialProbability)
    print("Probability for rain array", verifyImplementation)
    print("Probability for rain in the present is", verifyImplementation[0]*100,"%")

    print("----------------------------")
    print("PART 2 - 5 DAYS WITH BOTH RAIN AND NO RAIN")
    # DEL 2 - 5 dager med både regn og ikke regn
    # Answer to the final part of the task, U1 = True, U2 = True, U3 = False, U4 = True, U5 = True
    partTwo = forwardAlgorithm([0,0,1,0,0], initialProbability)
    print("Probability for rain array", partTwo)
    print("Probability for rain in the present is", partTwo[0]*100,"%")
    

main()