#The purpose of this bash script is to scaffold contigs with HiC linking data

#Input Files
inputSAM=../ExampleData/merged_dedup_testdata.sam
inputMergeNoDups=../ExampleData/OldMergeNoDups_testdata.txt
workingDirectory=../WorkingDirectory/
originalContigFastaFile=../ExampleData/PferFiltered.fasta
keepReadsWithinThisDistanceFromTheEndOfContig=40000

#Intermediate Files
contigLengthsFile="${workingDirectory}contigLengths.txt"
samGrepXAZ="samGrepXAZ.sam"
samGrepXAZPlusDirc="${workingDirectory}samGrepXAZ.sam"
multiMapDict="${workingDirectory}MultiMapDictionary.pickle"
chicagoJuicerMergedNoDups="${workingDirectory}CHI_merged_nodups_PurgedMM.txt"
chicagoJuicerMergedNoDupsRemoveSelfMappingReads="${workingDirectory}CHI_merged_nodups_PurgedMM_RemoveSelf.txt"
newNoDups="${workingDirectory}CHI_merged_nodups_PurgedMM_RemoveSelf_Trimm40kb.txt"
nameOfDictionaryObjectWithConnectionCountsBetweenContigs="${workingDirectory}CHI_purgedups_Trimmed_Connections.pickle"
nameOfDictionaryObjectWithConnectionLocationsBetweenContigs="${workingDirectory}CHI_purgedups_Trimmed_Connections_Locations.pickle"
chicagoConnections="${workingDirectory}MyChicagoConnections.txt"
chicagoConnectionsInJuiceBoxFormat="${workingDirectory}JuiceBoxMyChicagoScaffolds.assembly"
contigIndexNumbers="${workingDirectory}JuiceBoxChicagoNames.txt"
blackListContigIfMoreThanTwoConnections="${workingDirectory}ChicagoBlackListContigs.pickle"

#Output Files
chicagoScaffolds="${workingDirectory}MyChicagoScaffolds_TestExample.fasta"
chicagoScaffoldsKey="${workingDirectory}MyChicagoScaffoldsKey_TestExample.fasta"

mkdir $workingDirectory

echo "Calculating Contig Lengths"
python3 GetFastaLengths.py $originalContigFastaFile $contigLengthsFile

echo "Filtering out reads which map to more than one place"
grep "A:Z:" $inputSAM > $samGrepXAZPlusDirc

echo "Add multimapping reads to a python dictionary"
python3 DoubleMappedReadsDictionary.py $workingDirectory $samGrepXAZ $multiMapDict

echo "Remove multimapping reads from juicer merge no dups file"
python3 RemoveMultiMapFromNoDups.py $inputMergeNoDups $multiMapDict $chicagoJuicerMergedNoDups

echo "Filtering Self matching Reads"
awk '$2 != $6' $chicagoJuicerMergedNoDups > $chicagoJuicerMergedNoDupsRemoveSelfMappingReads

echo "Filtering further to keep only reads at the ends of contigs"
#filter out reads > 40k from the ends of contigs. No much "real" interaction happens past this range
python3 FilterChicagoReadsWhichDoNotMapToEnds.py $keepReadsWithinThisDistanceFromTheEndOfContig $contigLengthsFile $chicagoJuicerMergedNoDupsRemoveSelfMappingReads $newNoDups

echo "Counting Chicago Connections Between Contigs"
#Count chicago connections between contigs (if both reads have a mapq score of 0 ignore)
python3 CountConnectionsInNoDups.py $newNoDups $nameOfDictionaryObjectWithConnectionCountsBetweenContigs

echo "Storing locations of Chicago Connections"
#Store locations of Chicago connections in dictionary if the number of connections are >= 8
python3 NoDupsConnectionsGreaterThan10Positions.py $newNoDups $nameOfDictionaryObjectWithConnectionCountsBetweenContigs $nameOfDictionaryObjectWithConnectionLocationsBetweenContigs

echo "Making Connections with Chicago Data"
#Create Chicago connections
python3 ChicagoScaffolding_Connections.py $nameOfDictionaryObjectWithConnectionLocationsBetweenContigs $contigLengthsFile $chicagoConnections $keepReadsWithinThisDistanceFromTheEndOfContig $blackListContigIfMoreThanTwoConnections

echo "Creating Juicer style .assembly file"
#Create Juicer style .assembly file
python3 GroupMyChicagoConnections_Clean.py $chicagoConnections $contigLengthsFile $chicagoConnectionsInJuiceBoxFormat $contigIndexNumbers $blackListContigIfMoreThanTwoConnections

echo "Creating the new Chicago Scaffolds fasta file"
#Actually create the new Chicago Scaffolds fasta file
python3 TransformScaffoldsIntoSequence.py $chicagoConnectionsInJuiceBoxFormat $originalContigFastaFile $contigIndexNumbers $chicagoScaffolds $chicagoScaffoldsKey

echo "Scaffold fasta written to $chicagoScaffolds"
echo "Scaffold key written to $chicagoScaffoldsKey"
