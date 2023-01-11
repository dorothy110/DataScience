# Loan Analysis

## Overview

Sadly, there is a long history of lending discrimination based on race
in the United States.  Lenders have literally drawn red
lines on a map around certain neighbourhoods where they would not
offer loans, based on the racial demographics of those neighbourhoods
(read more about redlining here: https://en.wikipedia.org/wiki/Redlining).
In 1975, congress passed the Home Mortgage Disclosure Act (HDMA) to
bring more transparency to this injustice
(https://en.wikipedia.org/wiki/Home_Mortgage_Disclosure_Act).  The
idea is that banks must report details about loan applications and
which loans they decided to approve.

The public HDMA dataset spans all the states and many years, and is documented here:
* https://www.ffiec.gov/hmda/pdf/2020guide.pdf
* https://cfpb.github.io/hmda-platform/#hmda-api-documentation

In this project, I will analyze every loan application made in Wisconsin in
2020.

Things I will practice:
* classes
* large datasets
* trees
* testing
* writing modules

## Results

Results will be in 4 files:
* p2.ipynb
* loans.py 
* module_tester.py
* search.py 

## First Home Bank Analysis

```
import search
import loans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
```

For the following questions, created a `Bank` object for the bank named "First Home Bank".
```
fhb = loans.Bank("First Home Bank")

```
### Q1: what is the average interest rate for the bank?

Skip missing loans where the interest rate is not specified in your calculation.

```
total = 0
count = 0
for r in fhb:
    if r.interest_rate == -1:
        pass
    else:
        total += r.interest_rate
        count +=1
                
total/count

```

### Q2: how many applicants are there per loan, on average?
```
total = 0
count = 0
for app in fhb:
    total += len(app.applicants)
    count +=1
    
total/count
```

### Q3: what is the distribution of ages?



Answer with a dictionary, like this:

```
{'65-74': 21, '45-54': 21, ...}
```
```
dic1 = {}
for app in fhb:
    for i in app.applicants:
         dic1[i.age] = dic1.get(i.age,0)+1 
   
dic1
```
### Tree of Loans for Q4 and Q5

For the following questions, create a `BST` tree.  Loop over every loan in the bank, adding each to the tree.  The `key` passed to the `add` call should be the `.interest_rate` of the `Loan` object, and the `val` passed to `add` should be the `Loan` object itself.

### Q4: how many interest rate values are missing?

Don't loop over every loan to answer.  Use your tree to get and count loans with missing rates (that is, `-1`).
```
fhb = loans.Bank("First Home Bank")
a = search.BST()
for i in fhb:
    a.add(i.interest_rate, i)


len(a.__getitem__(-1))

```

### Q5: how tall is the tree?

The height is the number of nodes in the path from the root to the deepest node.  Write a recursive function or method to answer.
```
def h(node):
    if node == None:
        return 0
    lH = h(node.left)
    rH = h(node.right)
    maxH = max(rH, lH)
    return maxH + 1

int(h(a.root))
```


## Part 4: University of Wisconsin Credit Union Analysis

Build a new `Bank` and corresponding `BST` object as before, but now for "University of Wisconsin Credit Union".
```
uwcunew = loans.Bank("University of Wisconsin Credit Union")
```


### Q6: how long does it take to add the loans to the tree?

Answer with a plot, where the x-axis is how many loans have been added so far, and the y-axis is the total time that has passed so far.  You'll need to measure how much time has elapsed (since the beginning) after each `.add` call using `time.time()`.

**Note:** performance and the amount of noise will vary from one virtual machine to another, so your plot probably won't be identical (this applies to the other performance plots too).

<img src="q6.png">

```

b = search.BST()

t = []

t1 = time.time()
for i in range(len(uwcunew)):
        b.add(uwcunew[i].interest_rate, uwcunew[i])
        t2 = time.time()
        t.append((t2-t1)*1000)
    


df = pd.DataFrame(t, columns=["Time"])
df.plot.line()    
plt.xlabel("BST Adds")
plt.ylabel("Total Elapsed Milliseconds")
plt.show()
```

### Q7: how fast are tree lookups?

Create a bar plot with two bars:
1. time to find missing `interest_rate` values (`-1`) by looping over every loan and keeping a counter
2. time to compute `len(NAME_OF_YOUR_BST_OBJECT[-1])`

<img src="q7.png">

```
t = []
tt = []

t1 = time.time()
count = 0 
for i in uwcunew:   
    if i.interest_rate == -1:
        count +=1
t2 = time.time()
t.append((t2-t1)*1000)
    
    
t3 = time.time()
len(b[-1])
t4 = time.time()
tt.append((t4-t3)*1000)
        
        
df = pd.DataFrame([t,tt])
df.index= [ "LOOP", "BST"]
df.plot.bar()    
plt.xlabel("BST Adds")
plt.ylabel("Total Elapsed Milliseconds")
plt.legend('', frameon=False)
plt.show()
```

### Q8: How many applicants indicate multiple racial identities?

Answer with a bar graph, where the y axis should represent the number of applicants with the corresponding x-axis represents number of race selections.

```

b = search.BST()

# for i in uwcunew:   
#     # len(i.applicants)
#     print(i.applicants)
        

list8 = []
# #get race
for i in uwcunew:
    for j in i.applicants:
        # print(len(j.race))
        list8.append(len(j.race))
# print(list8)
# The value_counts() function is used to get a Series containing counts of unique values. 
here = pd.Series(list8).value_counts() 



df = pd.DataFrame(here)
print(type(df))

df.plot.bar()    
plt.xlabel("Race Count")
plt.ylabel("Applicants")
plt.legend('', frameon=False)
plt.show()
```

### Q9: How many leaf nodes are in the tree?
Write a recursive function or method to count the number of leaf nodes present in the given BST.

```

b = search.BST()

for i in uwcunew:
    b.add(i.interest_rate, i)


def findingnode(node):
    if node == None:
        return 0
    elif node.left == None and node.right == None:
        return 1
    else :
        return findingnode(node.left) + findingnode(node.right)
    

int(findingnode(b.root))   
```

### Q10: What is the second largest interest rate in the Bank BST?

**Hint:** you could write a recursive function or method that can return the top 2 (or N) keys for any subtree.

```
def second(node):
    if node == None:
        return []
    # if node.left == None and node.right == None:
    #     return node.__getitem__()
    s = sorted([node.key] + second(node.left) +second(node.right))
    return s

second(b.root)[-2]
```

### Search.py
```

```

### Search.py
```

```
