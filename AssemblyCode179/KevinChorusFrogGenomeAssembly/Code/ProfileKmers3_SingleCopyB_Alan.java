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

//java -Xmx700g ProfileKmers3_SingleCopyB /pool/KevinChorusFrogGenomeAssembly/Examples/WholeGenome_RC_HiC_Connections_August_5/KmerMatrixObj ../CCS/ccs1.2bit__../CCS/ccs2.2bit ../CCS/ccs1_RC.2bit__../CCS/ccs2_RC.2bit SCKmers_POS.txt SCKmers_COV.txt


public class ProfileKmers3_SingleCopyB_Alan{

	public static void main(String[] args){
		try{

			String inputObjectPath = args[0];			//Byte Array Location

			String inputPBFiles = args[1];				//e.g. ccs1.2bit__ccs2.2bit
			String inputPBFilesRC = args[2];			//e.g. ccs1_RC.2bit__ccs2_RC.2bit

			String outputSingleCopy = args[3];			//OutputFile position of SC Kmers
			String outputSingleCopy_Cov = args[4];		//OutputFile coverage of SC Kmers

			String expCovL_S = args[5];
			String expCovH_S = args[6];
			String coverageJump_S = args[7];
			String delta_Low_S = args[8];
			String delta_High_S = args[9];
			String numLinesToProcess_S = args[10];

			int K1 = 4;
			int K2 = 15;
			int K=K1+K2;
			int B1=K1*2;
			int B2=K2*2;
			int nBits=2*(K1+K2);

			//Load Byte Array			
			System.out.println("Loading Object byte array...");
			ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream(inputObjectPath));
			byte[][] countArray = (byte[][])inputStream.readObject();
			System.out.println("Done");


			String[] lstInputPBFiles = inputPBFiles.split("__");
			String[] lstInputPBFilesRC = inputPBFilesRC.split("__");


			BufferedWriter bw = new BufferedWriter(new FileWriter(new File(outputSingleCopy)));
			BufferedWriter bw2 = new BufferedWriter(new FileWriter( new File(outputSingleCopy_Cov)));
			BufferedReader br = null;
			BufferedReader brRC = null;

			int readID=0;
			String tempS,tempS2,tempSRC;
			int readLength;
			int readBits;
			int covProfile[]=new int[50000];	//set to above maximum length
			int covProfileRC[]=new int[50000];	//set to above maximum length
			int covProfileB[]=new int[50000];	//set to above maximum length		both combined

			//int expCovL=4;
			int expCovL = Integer.parseInt(expCovL_S);
			//int expCovH = 11;
			int expCovH = Integer.parseInt(expCovH_S);
			//double delta_Low =1.0;
			double delta_Low = Double.parseDouble(delta_Low_S);
			//double delta_High = 0.0;			
			double delta_High_Thresh = Double.parseDouble(delta_High_S);
			double delta_High;
			//double coverageJump = 2.0;
			double coverageJump = Double.parseDouble(coverageJump_S);
			double avgMiddle = 0.0;
			int numLinesToProcess = Integer.parseInt(numLinesToProcess_S);
			int startCoverage = 0;

			if(numLinesToProcess == -1){
				numLinesToProcess = 99999999;
			}

			

			int begA,endA,begB,endB,begC,endC;
			int widthA,widthB,widthC;

			int imer1,imer2,imerRC1,imerRC2;	//integer representations of kmer

			//Outer loop going through all input sequence files

			for(int j=0; j<lstInputPBFiles.length; j++){

				br = new BufferedReader(new FileReader(new File(lstInputPBFiles[j])));
				brRC = new BufferedReader(new FileReader(new File(lstInputPBFilesRC[j])));	//avoid having to RC each sequence

				tempS=br.readLine();
				tempSRC=brRC.readLine();

				//SLIDE WINDOW ACROSS 2BIT REPRESENTATION OF SEQUENCE AND LOOKUP COVERAGE
				while(tempS!=null){
					readID++;

					//if( readID < 0){
                                        //	tempS=br.readLine();
                                        //	tempSRC=brRC.readLine();
					//	continue;
					//}


					//if(readID > 20){
					//	break;
					//}

					//if(readID%1000==0){System.out.print("\r"+readID+" reads processed... ");}
					readBits=tempS.length();
					readLength=readBits/2;

					//covProfile= new int[readLength-K+1];		avoid re-initializing array		
																//not info from previous read will be overwritten, but only until readlen, be careful when writing to file

					//LOOKUP COVERAGE CORRESPONDING TO EACH POSITION IN SEQUENCE
							//i refers to position of bit in bitstring
					for(int i=0; i<readBits-nBits+2; i+=2){ //<=SHOULD BE +=2, BUT COULD BE +=1
						imer1=Integer.parseInt(tempS.substring(i,i+B1),2);			//e.g. 11010100 => 212
						imer2=Integer.parseInt(tempS.substring(i+B1,i+nBits),2);	//e.g. 010011010101010010011010101001 => 324347561
						imerRC1=Integer.parseInt(tempSRC.substring(readBits-nBits-i,readBits-i-B2),2);		
						imerRC2=Integer.parseInt(tempSRC.substring(readBits-i-B2,readBits-i),2);	
						covProfile[i/2]=(int)countArray[imer1][imer2];
						covProfileRC[i/2]=(int)countArray[imerRC1][imerRC2];
						covProfileB[i/2]=covProfile[i/2]+covProfileRC[i/2];
						//System.out.println(covProfile[i/2]+"\t"+covProfileRC[i/2]+"\t"+covProfileB[i/2]);
					}

							//i refers to position of character in sequence
					for(int i=0; i<readLength-K+1; i++){
						if(covProfileB[i] >= expCovL && covProfileB[i] <= expCovH ){	//found candidate region

							//find endpoints of lower coverage stretch
							begB=i;
							endB=i;
							avgMiddle = 0.0;

							startCoverage = covProfileB[i];

							while((covProfileB[endB] > (startCoverage - delta_Low)) && (covProfileB[endB] < (startCoverage + delta_Low))){
								avgMiddle = avgMiddle + covProfileB[endB];
								endB++;
								if(endB>=readLength-K+1){break;}
								
							}
							endB--;
							widthB=endB-begB+1;
							avgMiddle = avgMiddle/widthB;
							if(delta_High_Thresh == -1){
								delta_High = avgMiddle/coverageJump;
							}else{
								delta_High = delta_High_Thresh;
							}

							//verify length (and position relative to end of sequence)
							if(widthB < 19 || begB<10 || begB>readLength-K-10){
								i=endB;	//lower coverage stretch too short advance and continue
								continue;
							}

							//find endpoints of left flank
							endA=begB-1;
							begA=endA;
							//System.out.println("Potential Range: ");
							//System.out.println(coverageJump*avgMiddle-delta_High);
							//System.out.println(coverageJump*avgMiddle+delta_High);
							while(covProfileB[begA] >= (coverageJump*avgMiddle-delta_High) && covProfileB[begA] <= (coverageJump*avgMiddle+delta_High)){
								begA--;
								if(begA<0){break;}
							}
							begA++;
							widthA=endA-begA+1;

							//verify length
							if(widthA < 10){
								i=endB;	//lower coverage stretch too short advance and continue
								continue;
							}

							//find endpoints of right flank
							begC=endB+1;
							endC=begC;
							while(covProfileB[endC]>=(coverageJump*avgMiddle-delta_High) && covProfileB[endC]<=(coverageJump*avgMiddle+delta_High)){
								endC++;
								if(endC>=readLength-K+1){break;}
							}
							endC--;
							widthC=endC-begC+1;

							//verify length
							if(widthC < 10){
								i=endC;	//lower coverage stretch too short advance and continue
								continue;
							}							

							//passed tests, write center stretch information
							//System.out.println("Passed tests writing kmer");
							//System.out.println(readBits);
							//System.out.println(endB);
							if(endB*2 >= readBits){
								System.out.println("Failed: ");
								System.out.println(readID);
							}
							for(int k=begB; k<=endB; k++){
								bw.write(k+"\t");
								bw2.write(covProfileB[k]+"\t");
							}
							i=endC;	//advance
						}
					}
					bw.write("\n");
					bw2.write("\n");
					tempS=br.readLine();
					tempSRC=brRC.readLine();

					if(readID >= numLinesToProcess){
						break;
					};

				}
				br.close(); 
				brRC.close();
				if(readID >= numLinesToProcess){
					break;
				}
			}
			bw.flush();
			bw.close();
			bw2.flush();
			bw2.close();
System.out.println();

/*
					String lineCoverage = "";

					//bw.write("-1");
					lineCoverage = lineCoverage + "-1";
					for(int i=0; i<=tempS.length()-2*(K1+K2); i+=2){
// !! THE NEXT LINE WILL BE EXPENSIVE
//		MANY SUBSTRINGS

						tempS2=tempS.substring(i,i+2*(K1+K2));
						String binKmer = tempS2;
						if(tempS2.indexOf("N")>=0){
							//bw.write("\t0");
							lineCoverage = lineCoverage + "\t0";

						}else{

							//Get indexes of SC kmer from byte array both forward and reverse add them together

							int kmer1=Integer.parseInt(tempS.substring(i,i+2*K1),2);			//two bits per character
							int kmer2=Integer.parseInt(tempS.substring(i+2*K1,i+2*(K1+K2)),2);	//two bits per character
							//bw.write("\t"+(int)countArray[kmer1][kmer2]);

							String binKmerRC="";
							for(int x=binKmer.length()-2; x>=0; x-=2){
// !! THE NEXT LINE WILL BE EXPENSIVE
//		MANY SUBSTRINGS
				        			switch(binKmer.substring(x,x+2)){
				                			case "00": binKmerRC+="11";             break; //convert A to T
				                			case "11": binKmerRC+="00";             break; //convert T to A
				                			case "01": binKmerRC+="10";             break; //convert C to G
				                			case "10": binKmerRC+="01";             break; //convert G to C
				                			default: System.out.println("SHOULD NOT HAVE ENCOUNTERED DEFAULT IN SWITCH: "+binKmer.substring(x,x+2));
				        			}
							}
							//System.out.println(binKmerRC);
							//System.out.println(K1+"\t"+K2+"\t"+0+"\t"+2*K1+"\t"+2*(K1+K2));
				                        //GET SPLIT INTEGER KMER CORRESPONDING TO REV COMP
				                        int iRC=Integer.parseInt(binKmerRC.substring(0,2*K1),2);                    //two bits per character
				                        int jRC=Integer.parseInt(binKmerRC.substring(2*K1,2*(K1+K2)),2);    //two bits per character
							int coverage = (int)countArray[kmer1][kmer2] + (int)countArray[iRC][jRC];
// !! THE NEXT LINE WILL BE EXPENSIVE
//		REPEATEDLY CONCATENATING STRING WILL COST A LOT OF TIME
//		MAY BE BETTER TO CREATE FILE
							lineCoverage = lineCoverage + "\t"+Integer.toString(coverage);

						}
					}



					//Select single copies from the string representing coverage level from on PB read







					String[] sline = lineCoverage.split("\t");
					ArrayList<ArrayList<Integer>> singleCopy = getSingleCopy(sline);

					ArrayList<Integer> singleCopy_Index = singleCopy.get(0);
					ArrayList<Integer> singleCopy_Cov = singleCopy.get(1);

					for(int i = 0; i < singleCopy_Index.size(); i++){
						bw.write(singleCopy_Index.get(i) + "\t");
						bw2.write(singleCopy_Cov.get(i) + "\t");
					}


					bw.write("\n");
					bw2.write("\n");
					tempS=br.readLine();
				}
				br.close();

			}

                        bw.flush();
                        bw.close();
                        bw2.flush();
                        bw2.close();
*/


		}catch(IOException ioe){
			System.out.println(ioe.getMessage());
		}catch(ClassNotFoundException e){
			System.out.println(e);
		}
	}

	public static ArrayList<ArrayList<Integer>> getSingleCopy(String[] sline){



			//Threshold Values

			int numBefore = 10;
			int numAfter = 10;
			double thresholdHigh = 1.0;

			int numMiddle = 19;
			double thresholdLow = 1.0;


//Low=4
//delta=4
//High=Low*2

//Low1=Low-delta
//Low2=Low+delta

//High1=High-delta
//High2=High+delta

			int acceptalbeHighCoverage_UpperB = 17;
			int acceptableHighCoverage_LowerB = 8;

			int acceptalbeLowerCoverage_UpperB = 6;
			int acceptableLowerCoverage_LowerB = 2;



			ArrayList<Integer> lstReliable = new ArrayList<>();
			ArrayList<Integer> lstReliableCoverage = new ArrayList<>();
			int flagEndOfLine = 0;
			

			//Iterate through the lst of coverages

			for(int j = 0; j < (sline.length - (numBefore+numMiddle+numAfter)); j++){
				

				//Check that x% fall inbetween normal high coverage
				int count = 0;

				for(int k = 0; k < numBefore; k++){
					int temp = Integer.parseInt(sline[j+k]);
			        if ((temp <= acceptalbeHighCoverage_UpperB) && (temp >= acceptableHighCoverage_LowerB)){
			        	count++;
			        }
				}

				if((count*1.0)/(numBefore*1.0) >= thresholdHigh){
					//pass;
			    }else{
					continue;
			    }


				//Check x% fall inbetween lower coverage  out of next 5
				count = 0;
				for(int k = 0; k < numMiddle; k++){
				        int temp = Integer.parseInt(sline[j + numBefore + k]);
				        if ((temp <= acceptalbeLowerCoverage_UpperB) && (temp >= acceptableLowerCoverage_LowerB)){
				        	count++;
				        }
				}
				if ((count*1.0)/(numMiddle*1.0) >= thresholdLow){
				        //pass;
				}else{
				        continue;
				}

			    //While maintaining this x% coverage continue
			    int countextra = 0;
			    while((count*1.0)/((numMiddle+countextra)*1.0) >= thresholdLow){
			            int index = j + numBefore + numMiddle + countextra;
			            if(index >= sline.length){
			                    flagEndOfLine = 1;
			                    break;
			            }
			            int temp = Integer.parseInt(sline[index]);
			            if((temp <= acceptalbeLowerCoverage_UpperB) && (temp >= acceptableLowerCoverage_LowerB)){
			                    count++;
			            }
			            countextra++;

			    }


			    //Check x% fall inbetween normal coverage after lower coverage for next 10
      			    countextra = countextra-1;
   			    count = 0;
			    for(int k = 0; k < numAfter; k++){
			            int index = j + numBefore + numMiddle + countextra+k;
			            if(index >= sline.length){
			                    flagEndOfLine = 1;
			                    break;
			            }
			            int temp = Integer.parseInt(sline[index]);
			            if(temp <= acceptalbeHighCoverage_UpperB && temp >= acceptableHighCoverage_LowerB){
			                    count++;
			            }
			    }


			    //Check if end of file has been reached
			    if(flagEndOfLine ==1){
			            continue;
			    }

			    if((count*1.0)/(numAfter*1.0) >= thresholdHigh){
			            //pass;
			    }else{
			            continue;
			    }

			    int startIndex = j + numBefore;
			    int stopIndex = j + numBefore + numMiddle + countextra;



			    //ArrayList<Integer> lstTemp = new ArrayLst<Integer>();

			    for(int k = startIndex; k < stopIndex; k++){
			            //int temp = Integer.parseInt(sline[k]);
			            lstReliable.add(k);
			            lstReliableCoverage.add(Integer.parseInt(sline[k]));
			    }


		

			}

			ArrayList<ArrayList<Integer>> ret = new ArrayList<ArrayList<Integer>>();
			ret.add(lstReliable);
			ret.add(lstReliableCoverage);	
			return ret;
	}

}

