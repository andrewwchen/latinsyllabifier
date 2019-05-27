from random import randint
cost = 0
n = randint(300, 1001)
d = randint(3, 10)
g = randint(96, 100)
k = randint(88, 93)
w = randint(78, 85)
m = randint(50, 101)
s = randint(2, 7)
masterMechanic = False

print('n = ' + str(n))
print('d = ' + str(d))
print('g = ' + str(g))
print('k = ' + str(k))
print('w = ' + str(w))
print('m = ' + str(m))
print('s = ' + str(s))

adjustments = randint(1, 101)
if adjustments in range(1, 81):
    goodAdjustments = 2
elif adjustments in range(81, 96):
    goodAdjustments = 1
else:
    goodAdjustments = 0


# Strategies
print("""
Please choose a strategy:
#1: call a master mechanic at a cost of ${0} (m)
#2: do nothing and hope for the best
#3: run a sample of parts at a cost of ${1} (s) per part
    and call the master mechanic if any part is defective
""".format(m, s))
strategy = input('Which strategy do you wish to use? Choose 1, 2, or 3')
if strategy == '1':
    print("You've chosen strategy #1: call a master mechanic at a cost of ${0} (m).".format(m))
    masterMechanic = True
    cost += m
elif strategy == '2':
    print("You've chosen strategy #2: do nothing and hope for the best.")
elif strategy == '3':
    print("""
You've chosen strategy #3: run a sample of parts at a cost of ${0} (s) per part
                           and call the master mechanic if any part is defective
    """.format(s))
    samples = int(input('How many parts do you wish to sample? Choose a number > 0'))
    assert (samples > 0), '{0} is not a number > 0'.format(strategy)
    for x in range(5):
        cost += samples * s
        if goodAdjustments == 2:
            if randint(1, 101) in range(1, 100 - g):
                masterMechanic = True
        elif goodAdjustments == 1:
            if randint(1, 101) in range(1, 100 - k):
                masterMechanic = True
        else:
            if randint(1, 101) in range(1, 100 - w):
                masterMechanic = True
    if masterMechanic == True:
        print('Master mechanic was called')
else:
    raise Exception('{0} is not a viable strategy. Choose 1, 2, or 3'.format(strategy))
    
if masterMechanic == True:
    goodAdjustments = 2


# cost of hand fitting defective parts:
if goodAdjustments == 2:
    goodParts = n * (g/100)
elif goodAdjustments == 1:
    goodParts = n * (k/100)
else:
    goodParts = n * (w/100)
badParts = n - goodParts
cost += d * badParts
print('The total cost is ${0}'.format(cost))