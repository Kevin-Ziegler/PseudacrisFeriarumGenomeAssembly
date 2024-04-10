import numpy as np
import bisect

#inputHIC_AGP = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/scaffolds_HIC_v2.agp"
#inputHIC_AGP = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/VisualizeHIC/Try2GATC/scaffolds_HIC_v2_GATC.agp"
#inputHIC_AGP = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/VisualizeHIC/Try2GATC/scaffolds_CHI_v2_GATC.agp"

#inputHIC_AGP = "/home/alanlemmonlab/YetAnotherHiCScaffolder/run1/yahs.out_scaffolds_final.agp"


inputHIC_AGP = "/home/alanlemmonlab/HiCData/Scaffolding/ScaffoldingFolder/mapping_pipeline/PurgedChicago_v2_GATC/scaffolds_FINAL.agp"

#inputHIC_AGP = "ChicagoAGP.txt"


fin = open(inputHIC_AGP, 'r')

scaf = ""
tempChicName = []
tempChicLength = []
tempChicStartPos = []

masterName = []
masterChicName = []
masterChicLength = []
masterChicStartPos = []

lstSplit = []

for line in fin:
        sline = line.split()
        #new scaf write lists to master, and clear them
        if scaf != sline[0]:
                masterName.append(scaf)
                masterChicName.append(tempChicName)
                masterChicLength.append(tempChicLength)
                masterChicStartPos.append(tempChicStartPos)
                tempChicName = []
                tempChicLength = []
                tempChicStartPos = []

        scaf = sline[0]


        if sline[4] == "W":
                tempChicName.append(sline[5])
                tempChicLength.append(int(sline[7]))
                tempChicStartPos.append(int(sline[1]))
                num_ = 0
                for char in sline[5]:
                        if char == "_":
                                num_+=1
                if num_ == 2:
                        baseName = sline[5][:-2]
                        if baseName in lstSplit:
                                pass
                        else:
                                lstSplit.append(baseName)


fin.close()


masterName.append(scaf)
masterChicName.append(tempChicName)
masterChicLength.append(tempChicLength)
masterChicStartPos.append(tempChicStartPos)
tempChicName = []
tempChicLength = []
tempChicStartPos = []


def find2DList(lst, item):
        for i in range(0, len(lst)):
                for j in range(0, len(lst[i])):
                        if lst[i][j] == item:
                                return [i,j]
        return "not found"

def replaceWithHIC(ChiScaffold, ChiPos):
        if ChiScaffold in lstSplit:
                index = find2DList(masterChicName, ChiScaffold + "_1")
                split1 = masterChicLength[index[0]][index[1]]
                #first one
                if ChiPos <= split1:
                        ChiScaffold = ChiScaffold+"_1"
                else:
                        #must be in second split
                        ChiScaffold = ChiScaffold + "_2"

        index = find2DList(masterChicName, ChiScaffold)
        newScafName = masterName[index[0]]
        newScafPos = int(masterChicStartPos[index[0]][index[1]]) + int(ChiPos)

        return [newScafName, str(newScafPos)]

def createDic(ChiScaffold):

        index = find2DList(masterChicName, ChiScaffold)
        newScafName = masterName[index[0]]


        return newScafName

def indexOf(lst, item):
        for x in range(0,len(lst)):
                if lst[x] == item:
                        return x
        return -1


#pairsFileName = "VisCHIScafwHIC2.bsorted.pairs"
#pairsFileName = "temp"
#pairsFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/VisualizeHIC/Try2GATC/VisCHIScafwHICGATC.bsorted.pairs"
pairsFileName = "/home/alanlemmonlab/HiCData/Scaffolding/ScaffoldingData/Pfer_purged_bed_HIC_Sorted_v2_GATC.bed"
#pairsFileName = "HicToChicago.txt"

fpairIn = open(pairsFileName, 'r')
fpairOut = open("HicToCanu_v2.bed", 'w')


# print(masterName)
# print(masterChicName)
# print(masterChicLength)
# print(masterChicStartPos)
# print(lstSplit)



dictScaffolds = {}
#bisect.bisect_left(x, 3)

for i in range(0, len(masterName)):
        dictScaffolds[masterName[i]] = i



counter = 0
for line in fpairIn:
        if counter%1000000 == 0:
                print(counter)
        counter+=1

        sline = line.split()
        if len(sline) < 6:
                continue

        scaff = sline[0]
        start = int(sline[1])
        end = int(sline[2])

        # print(scaff)
        # print(masterName)

        #index = indexOf(masterName, scaff)
        index = dictScaffolds[scaff]


        if index == -1:
                continue

        lstContigsOfScaffold = masterChicStartPos[index]

        startContig = -1
        indexStart = -1

        #for i in range(0, len(lstContigsOfScaffold)):
                # if start >= int(lstContigsOfScaffold[i]):
                #         startContig = int(lstContigsOfScaffold[i])
                #         indexStart = i
                #         break
        #print(lstContigsOfScaffold)
        #print(start)
        indexStart = bisect.bisect_left(lstContigsOfScaffold, start) - 1
        #print(indexStart)
        startContig = int(lstContigsOfScaffold[indexStart])

        if startContig == -1:
                print("Did not find contig")
                print(line)
                continue

        nameCanuContig = masterChicName[index][indexStart]

        locationofHiCRead_Start = start-startContig
        locationofHiCRead_End = end-startContig

        fpairOut.write(nameCanuContig + "\t" + str(locationofHiCRead_Start) + "\t" + str(locationofHiCRead_End) + "\t" + sline[3] + "\t" + sline[4] + "\t" + sline[5] + " \n")

fpairOut.close()
fpairIn.close()


