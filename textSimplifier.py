## import os
import pandas as pd

txtString = "The Acts of Adjournal are important" # ['act', 'and', 'warrant','act', 'and', 'warrant', 'extra']

txtString = "The Adult Support and Protection 2007 Act is designed to protect those adults who are unable to safeguard their own interests and are at risk of harm because they are affected by"

txtString = txtString.lower()
cleanString = re.sub('\W+','', txtString )
txt = txtString.split(" ")

df_legalTerms = pd.read_csv("legalWordsExplained.csv")
df_legalTerms['legalWords'] = df_legalTerms['legalWords'].replace({':':''}, regex=True)
df_legalTerms['legalWords'] = df_legalTerms['legalWords'].str.lower()
#print(len(df_legalTerms['legalWords'][0]))
for idx, elem in enumerate(df_legalTerms['legalWords']):
    df_legalTerms['legalWords'][idx] = df_legalTerms['legalWords'][idx].split() #make this tuple

legalWordsList_l = df_legalTerms['legalWords'].tolist()

legalWordsList_p = []
for legWord in legalWordsList_l:
    legalWordsList_p.append(tuple(legWord))
    
legalWordsDict = {val: idx + 1 for idx, val in enumerate(legalWordsList_p)}
copy = txt.copy()

def find_sub_list(sl,l):
    results=[]
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            x = (ind,ind+sll-1)
            if len(x)!=0:
                results.append(x)
    return results

positions = []
for lst in legalWordsList_l:
    e = find_sub_list(lst, txt)
    if e != []:
        positions.append(e)

pos = []
for meaningGroup in positions:
    for positiongrp in meaningGroup:
        pos.append(positiongrp)

#mapping positions with values
for p in pos:
    start = p[0]
    end = p[-1]
    meaning = legalWordsDict[tuple(txt[start:(end+1)])]
    meaningValue = "(" + df_legalTerms['definitions'][meaning-1] +")"
    copy.insert(end+1,meaningValue)

outputText = ""
for simplifiedTextElem in copy:
    outputText += ((simplifiedTextElem + " "))
    
print(outputText)
    
