
dircFiles=../WorkingDirectory/
inputJuicerMappingFile=../ExampleData/testdata_Example.sam
inputFasta=../ExampleData/PferFiltered_Heterozygosity.fasta
outputFasta=../WorkingDirectory/HeterozygosityRemoved.fasta


#Used for publication
#numReadsRequired=3000

#Used for example
numReadsRequired=300

#Intermediate Files
dictionaryConnectionCounts="${dircFiles}connectionCountsBetweenContigs.pickle"
dictionaryConnectionCoordinates="${dircFiles}dataCoords.pickle"
candidateRegionsToRemove="${dircFiles}ListOfRegionsToRemove_PurgeMultiMap.txt"
candidateRegionsToRemoveFilterSmall="${dircFiles}ListOfRegionsToRemove_PurgeMultiMap_FilterSmall.txt"
contigLengths="${dircFiles}ContigLengths.txt"
newName="DoubleMapped.sam"

mkdir $dircFiles

if [[ $inputFasta == *"PferFiltered_Heterozygosity.fasta" ]]; then
echo "Using default contig lengths and maxContig value"
cp ../ExampleData/ContigLengths.txt ../WorkingDirectory/ContigLengths.txt
maxContigs=90000
else
echo "Generating List of contigs lengths for input assembly"
maxContigs=$(python3 GetFastaLengths_Sorted.py $inputFasta $contigLengths)

fi


echo "Filtering Reads with Two Mappings: Double Mapped"
#Filter out reads with only one other connection (XA:Z ensures at least one alternate and -v ;tig ensures only one alternate)
grep "XA:Z:tig" $inputJuicerMappingFile | grep -v ";tig" > "$dircFiles$newName"

echo "Count the number of Double Mapped reads connecting each contig pair"
#The purpose of this file is to take a filter juicer sam file with only reads that map to two places, and create a dictionary object that counts the number of Chicago connections between contigs
python CountDoubleMappedReads.py $dircFiles "$newName" $maxContigs $dictionaryConnectionCounts

echo "For contig pairs which are connected with Double Mapped Read, record the location of the mappings"
#The purpose of this file is to take the dictionary of connection counts from CountDoubleMappedReads.py and filter for contigs pairs which have over a certain number of connections
#A new lst object is created where lst[i] is a dictionary of connections for the ith contig. The key for this dictionary is the number of the contig its connection to and the value is a "coordinate" list of locations where the mappings actually are
python FindDoubleMappedContigs.py $dircFiles "$newName" $maxContigs $numReadsRequired $dictionaryConnectionCounts $dictionaryConnectionCoordinates

echo "Generating Candidate regions to remove"
#The purpose of this file is to generate candidate regions of heterozygosity to remove, given mappings of Double mapped reads and specific parameters to check
#The parameters check that there are many Double Mapped reads which span a continuous region
python MultiMapRemove.py $contigLengths $dictionaryConnectionCoordinates $candidateRegionsToRemove

echo "Ensure small fragments <= 15 kbp are not removed"
#The purpose of this file is to take the list of candidate areas to remove and modify them.
#The modification is ensuring small segmenets are not removed.
python RepurgeMM.py $candidateRegionsToRemove $candidateRegionsToRemoveFilterSmall

echo "Re-write fasta file with locations to remove"
#Rewrite fasta files with list of contigs to remove
python PurgeContigs_WithList_DoublesEdit.py $inputFasta $outputFasta $candidateRegionsToRemoveFilterSmall

echo "Results written to $outputFasta"
