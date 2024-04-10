#curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_017654675.1/download?include_annotation_type=GENOME_FASTA,SEQUENCE_REPORT&filename=GCF_017654675.1.zip" -H "Accept: application/zip"

#organism = ["XenTrop", "hourglasstreefrog"]
#lstgenBankID = ["GCF_000004195.3", "GCF_027789725.1"]

organism = ["Musmusculus"]
lstgenBankID = ["GCF_000001635.27"]


for item in lstgenBankID:

	genbankID = item
	start = 'curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/'

	middle = "/download?include_annotation_type=GENOME_FASTA,SEQUENCE_REPORT&filename="

	end = '.zip" -H "Accept: application/zip"'

	command = start + genbankID + middle + genbankID + end

	print(command)
