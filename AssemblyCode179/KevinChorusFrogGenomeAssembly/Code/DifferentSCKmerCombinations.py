#thresholdCoverageSCLow=2
#thresholdCoverageSCHigh=10
#thresholdCoverageJump=2
#thresholdDeltaLow=1
#thresholdDeltaHigh=-1
#numberLinesToProcess=1000
#numberSCKmers=100
#folderName=/pool/KevinChorusFrogGenomeAssembly/Examples/TestDifferentSCKmerThresholds/CovL_2_CovH_10_CovJump_2_DeltaLow_1_DeltaHigh_-1/


lst_thresholdCoverageSCLow=[2,2,2,2,2,2,2,2]
lst_thresholdCoverageSCHigh=[10,8,6,10,10,10,10,10]
lst_thresholdCoverageJump=[2,2,2,2,2,2,2,2]
lst_thresholdDeltaLow=[1,1,1,2,3,1,1,1]
lst_thresholdDeltaHigh=[-1,-1,-1,-1,-1,1,2,3]


print(len(lst_thresholdCoverageSCLow))
print(len(lst_thresholdCoverageSCHigh))
print(len(lst_thresholdCoverageJump))
print(len(lst_thresholdDeltaLow))
print(len(lst_thresholdDeltaHigh))


numberLinesToProcess=10000
numberSCKmers=1000
folderNameBase = "/pool/KevinChorusFrogGenomeAssembly/Examples/TestDifferentSCKmerThresholds/"

#CovL_2_CovH_10_CovJump_2_DeltaLow_1_DeltaHigh_-1/"


for i in range(0, len(lst_thresholdCoverageSCLow)):
	SCLow = str(lst_thresholdCoverageSCLow[i])
	SCHigh = str(lst_thresholdCoverageSCHigh[i])
	jump = str(lst_thresholdCoverageJump[i])
	deltaLow = str(lst_thresholdDeltaLow[i])
	deltaHigh = str(lst_thresholdDeltaHigh[i])

	folderName = folderNameBase + "CovL_" + SCLow + "_CovH_" + SCHigh + "_CovJump_" + jump + "_DeltaLow_" + deltaLow + "_DeltaHigh_" + deltaHigh + "/" 
	tempMafftScriptCmd = "./DiffSCKmersScript.sh " + SCLow + " " + SCHigh + " " + jump + " " + deltaLow + " " + deltaHigh + " " + str(numberLinesToProcess) + " " + str(numberSCKmers) + " " + folderName

	print(tempMafftScriptCmd)

