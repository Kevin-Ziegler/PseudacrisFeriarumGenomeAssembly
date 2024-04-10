#/pool/Kevin81/NeuronProject/Blast/ncbi-blast-2.15.0+/bin/blastn -query GabaTranscripts.fasta -db /pool/Kevin81/NeuronProject/Data/PferDataBase/my_local_Pfer_db -out results.txt

blast = "/home/alanlemmonlab/NeuronProject/Blast/ncbi-blast-2.15.0+/bin/tblastn"
#query = "/home/alanlemmonlab/NeuronProject/SearchGaba/NCBI_XenTrop_Gaba-a_transcripts.fasta"
dataBasedirc = "/home/alanlemmonlab/NeuronProject/Data/DataBases/"

#DataBases = ["PferTranscriptDataBase/local_Pfer_Transcript_db", "PferDataBase/my_local_Pfer_db", "HourGlassTreeFrog/my_local_HourGlassTreeFrog_db", "XenTropDataBase/my_local_XenTrop_db", "MouseDataBase/local_Mouse_db"]
#OutDirc = "/home/alanlemmonlab/NeuronProject/Data/BlastResults/XenTropGaba-A_NCBI_transcripts_AminoAcid/"
#OutNames = ["Pfer_Transcript", "Pfer_Genome", "HourGlass_Genome", "XenTrop_Genome", "Mouse_Genome"]

DataBases = ["PferTranscriptDataBase/local_Pfer_Transcript_db", "PferDataBase/my_local_Pfer_db"]
OutDirc = "/home/alanlemmonlab/NeuronProject/Data/BlastResults/XenTropGaba-A_NCBI_transcripts_AminoAcid_2/"
OutNames = ["Pfer_Transcript", "Pfer_Genome"]



#/home/alanlemmonlab/NeuronProject/Blast/ncbi-blast-2.15.0+/bin/blastn -query /home/alanlemmonlab/NeuronProject/SearchGaba/NCBI_XenTrop_Gaba-a_transcripts.fasta -db  -out results.txt
#searchFasta = "/home/alanlemmonlab/NeuronProject/SearchGaba/NCBI_XenTrop_Gaba-a_transcripts.fasta"
#searchFasta = "NCBI_XenTrop_Gaba-a_transcripts_AminoAcid.fasta"

searchFasta = "/home/alanlemmonlab/NeuronProject/Data/QuerySequences/Gaba-A_Subunits_NCBI_Orthologs/CombinedGabaXenTrop.fasta"

for i in range(0, len(DataBases)):
	#cmd = blast + " -query " + searchFasta + " -db " + dataBasedirc + DataBases[i] + " -out " + OutDirc + OutNames[i] + ".txt"
	cmd = blast + " -query " + searchFasta + " -db " + dataBasedirc + DataBases[i] + " -out " + OutDirc + OutNames[i] + "_AminoAcid.txt"
	print(cmd)
