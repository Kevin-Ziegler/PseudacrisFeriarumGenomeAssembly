import java.io.*;
import java.util.*;
import java.text.NumberFormat;

//THIS PROGRAM COUNTS THE NUMBER OF TIMES KMERS FOUND IN A SEQUENCE FILE ARE FOUND, THEN REPORTS THE COUNT DISTRIBUTION FOR EACH SEQUENCE
//kmer is hashed as a int, via two bit represented as a string, type casted to an int
//in this version, the kmer is split into two pieces. counts are stored in a 2-d byte array...
//with first index corresponding to first portion of kmer (K1), and second corresponding to second portion (K2)
//use of 2-d array is forced by constraint on length of byte array being Integer.MAXVALUE
//kmers can only contain A T C or G

//THIS PROGRAM DOES NOT HANDLE REVERSE COMPLEMENT DIRECTLY: YOU SHOULD INCLUDE IN YOUR FILE LIST FORWARD AND REVERSE COMPLEMENT VERSIONS OF THE SAME SEQUENCES


public class ProfileKmerCounts3_MatrixObject{

	public static void main(String[] args){
		try{

			String inFiles=args[0];				//../CCS/ccs1.2bit__../CCS/ccs2.2bit__../CCS/ccs1_RC.2bit__../CCS/ccs2_RC.2bit
			String outStem=args[1];				//ccs
			int K1 = Integer.parseInt(args[2]);	//e.g. 4
			int K2 = Integer.parseInt(args[3]);	//e.g. 15
			String outputFileObj = args[4];

			//int nReadsProfiled = Integer.parseInt(args[4]);	//e.g. 1000

			int maxKmerID1=(int)(Math.pow(4,K1));
			int maxKmerID2=(int)(Math.pow(4,K2));
			
			System.out.println(maxKmerID1);
			System.out.println(maxKmerID2);

			System.out.println("Allocating byte array...");
			byte countArray[][] = new byte[maxKmerID1][maxKmerID2];
			System.out.println("Done");

			String inFileList[] = inFiles.split("__");

			BufferedReader br;
			int kmer1;
			int kmer2;
			int kmerRC1;
			int kmerRC2;
			String binKmer="";
			StringBuilder binKmerRC;

			Integer value;
			String tempS;
			int readID=0;
			int nKmers=0;
			int attempts=0;
			int totalBases=0;
			String tempA[];

			for(int f=0; f<inFileList.length; f++){
				System.out.println("\nReading "+inFileList[f]);
				br = new BufferedReader(new FileReader(new File(inFileList[f])));

				kmer1=-1;
				kmer2=-1;

				value=0;

				//Get counts of kmers found in the Sequenes
				tempS=br.readLine();
				while(tempS!=null){
					totalBases+=tempS.length()/2;
					readID++;
					System.out.print("\rEvaluating kmers in read "+readID);

					if(readID%10000==0){
						Runtime runtime = Runtime.getRuntime();

						NumberFormat format = NumberFormat.getInstance();

						StringBuilder sb = new StringBuilder();
						long allocatedMemory = runtime.totalMemory();

						System.out.println();
						System.out.println("allocated memory: " + format.format(allocatedMemory / 1073741824));
					}

					tempA=tempS.split("N"); //split sequence into word array by presence of N's
					for(int w=0; w<tempA.length; w++){ 	//for each word in array
						for(int i=0; i<=tempA[w].length()-2*(K1+K2); i+=2){	//two char in this string corresponds to one nucleotide
							attempts++;
							binKmer=tempS.substring(i,i+2*(K1+K2));

							//note, this will skip over words with length less than 2K
							kmer1=Integer.parseInt(binKmer.substring(0,2*K1),2);			//two bits per character
							kmer2=Integer.parseInt(binKmer.substring(2*K1,2*(K1+K2)),2);	//two bits per character

//							kmer1=Integer.parseInt(tempS.substring(i,i+2*K1),2);			//two bits per character
//							kmer2=Integer.parseInt(tempS.substring(i+2*K1,i+2*(K1+K2)),2);	//two bits per character

							if(countArray[kmer1][kmer2]==0){
								nKmers++;
							}

							if(countArray[kmer1][kmer2]<100){ //counts max out at 100
								countArray[kmer1][kmer2]=(byte)(countArray[kmer1][kmer2]+1);
							}

							//////
							//PROCESS REVERSE COMPLEMENT
							binKmerRC = new StringBuilder(binKmer).reverse();
							kmerRC1=Integer.parseInt(binKmerRC.substring(0,2*K1),2);			//two bits per character
							kmerRC2=Integer.parseInt(binKmerRC.substring(2*K1,2*(K1+K2)),2);	//two bits per character
							if(countArray[kmerRC1][kmerRC2]==0){
								nKmers++;
							}
							if(countArray[kmerRC1][kmerRC2]<100){ //counts max out at 100
								countArray[kmerRC1][kmerRC2]=(byte)(countArray[kmerRC1][kmerRC2]+1);
							}


						}
					}
					tempS=br.readLine();
				}
				br.close();
			}


			System.out.println();
			System.out.println(readID+" sequence reads were processed.");
			System.out.println(totalBases+" bases were processed.");
			System.out.println(attempts+" (non-unique) Kmers encountered.");			
			System.out.println(nKmers+" unique Kmers were recorded.");

			//Writes Obj to file
			ObjectOutputStream outputStream = new ObjectOutputStream(new FileOutputStream(outputFileObj));
			outputStream.writeObject(countArray);

		}catch(IOException ioe){System.out.println(ioe.getMessage());}
	}

}
