import sys
import math
import os

def calcBleuScore(candidate, references):
    prec_mult = 1
    pLen = 0
    precList = []
    xs=0
    while xs<4:
        totalClipCount = 0
        nc = 0
        bestRefLenSum = 0
        candWordLenSum = 0
        for cdit in range(len(candidate)):
            refDictList = []
            refLenList = []
            candDict = {}
            candWords = candidate[cdit].split()
            candWordsLen = len(candWords)
            for reference in references:
                ngramDict = {}
                refWords = reference[cdit].split()
                refLenList.append(len(refWords))
                for i in range(len(refWords) - xs):
                    cut = 1+i+xs
                    ng = ' '.join(refWords[i:cut])
                    if ng in ngramDict.keys():
                        ngramDict[ng] = 1 + ngramDict[ng]
                    else:
                        ngramDict[ng] = 1
                refDictList.append(ngramDict)
            for i in range(0, candWordsLen-xs):
                cut = 1+i+xs
                ng = ' '.join(candWords[i:cut])
                if ng in candDict:
                    candDict[ng] = 1 + candDict[ng]
                else:
                    candDict[ng] = 1
            totalClipCount += getClipCount(candDict, refDictList)
            nc += candWordsLen - xs
            minDiff = abs(candWordsLen - refLenList[0])
            similar_length = refLenList[0]
            for r in refLenList:
                if abs(r - candWordsLen) < minDiff:
                    similar_length = r
                    minDiff = abs(similar_length - candWordsLen)
            bestRefLenSum += similar_length
            candWordLenSum += candWordsLen
        if totalClipCount == 0:
            prec = 0
        else:
            prec = totalClipCount/nc
        if candWordLenSum > bestRefLenSum:
            brevPen = 1
        else:
            brevPen = math.exp((candWordLenSum - bestRefLenSum) / candWordLenSum)
        precList.append(prec)
        xs+=1
    for p in precList:
        prec_mult = prec_mult* p
        pLen+=1
    bleu=brevPen*(prec_mult **(1 / pLen))
    return bleu

def getClipCount(candDict, refDictList):
    clipCount = 0
    for ck in candDict.keys():
        minVal = candDict[ck]
        maxRef = 0
        for ref in refDictList:
            if ck in ref:
                maxRef = max(maxRef, ref[ck])
        minVal = min(minVal, maxRef)
        clipCount += minVal
    return clipCount

candDir = sys.argv[1]
refDir = sys.argv[2]
reference = []
if os.path.isdir(refDir):#reference is directory
    for r, d, fs in os.walk(refDir):
        for filename in fs:
            fileReader = open(os.path.join(r, filename), 'r', encoding='utf-8')
            lines = fileReader.readlines()
            reference.append(lines)
else:#is txt
    fileReader = open(refDir, 'r', encoding='utf-8')
    lines = fileReader.readlines()
    reference.append(lines)
fileReader = open(candDir, 'r', encoding='utf-8')
candidate= fileReader.readlines()
fileReader.close()
outFile = open('bleu_out.txt', 'w', encoding='utf-8')
outFile.write(str(calcBleuScore(candidate, reference)))
outFile.close()