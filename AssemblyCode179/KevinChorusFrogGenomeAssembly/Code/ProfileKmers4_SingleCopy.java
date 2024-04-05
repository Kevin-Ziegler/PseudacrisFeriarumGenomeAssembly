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


public class ProfileKmers3_SingleCopy{

	public static void main(String[] args){
		try{

			String inputObjectPath = args[0];			//Byte Array Location
			String inputPBFiles = args[1];				//e.g. ccs1.fasta__ccs.fasta or 2bit
			String outputSingleCopy = args[2];			//OutputFile position of SC Kmers
			String outputSingleCopy_Cov = args[3];			//OutputFile coverage of SC Kmers

			//int numlines = 100000;


			//int nReadsProfiled = Integer.parseInt(args[4]);	//e.g. 1000
			//int nReadsProfiled = 100;

			//int maxKmerID1=(int)(Math.pow(4,K1));

			int K1 = 4;
			int K2 = 15;
			


			//Load Byte Array			

			System.out.println("Loading Object byte array...");
			//byte countArray[][] = new byte[maxKmerID1][maxKmerID2];
			ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream(inputObjectPath));
			byte[][] countArray = (byte[][])inputStream.readObject();

			

			System.out.println("Done");

			String[] lstInputPBFiles = inputPBFiles.split("__");

			BufferedWriter bw = new BufferedWriter(new FileWriter(new File(outputSingleCopy)));
			BufferedWriter bw2 = new BufferedWriter(new FileWriter( new File(outputSingleCopy_Cov)));
			BufferedReader br = null;
			int readID=0;
			String tempS2;


			//Outer loop going through all input sequence files

			for(int j = 0; j < lstInputPBFiles.length; j++){

				br = new BufferedReader(new FileReader(new File(lstInputPBFiles[j])));
				String tempS=br.readLine();

	
				//Loop through each character of PB read create string representing coverage of each kmer				

				while(tempS!=null){
					readID++;
					//if(readID>nReadsProfiled){break;}
					String lineCoverage = "";

					//bw.write("-1");
					lineCoverage = lineCoverage + "-1";
					for(int i=0; i<=tempS.length()-2*(K1+K2); i+=2){
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



		}catch(IOException ioe){
			System.out.println(ioe.getMessage());
		}catch(ClassNotFoundException e){
			System.out.println(e);
		}
	}

	public static ArrayList<ArrayList<Integer>> getSingleCopy(String[] sline){



			//Threshold Values
			
			double startVarianceThreshold = 1.0;
			double midVarianceThreshold = 1.0;
			double endVarianceThreshold = 1.0;
			
			double minStartThreshold = 6.0;
			double maxStartThreshold = 30.0;
			double delta_FromDouble = 2.0;
			double factor = 2.0;
			
			int numBefore = 10;
			int numAfter = 10;
			int numMiddle = 19;
			
			



			ArrayList<Integer> lstReliable = new ArrayList<>();
			ArrayList<Integer> lstReliableCoverage = new ArrayList<>();
			int flagEndOfLine = 0;
			

			//Iterate through the lst of coverages
			//This version is a updated version of the hardcoded threshold ranges
			//This version focuses on finding jumps between coverage that is 2x -> x -> 2x
			//The range of x varied so much (based on understanding visual plots) that creating a threshold for low and high could not account for all values of x 

			for(int j = 0; j < (sline.length - (numBefore+numMiddle+numAfter)); j++){
				

				//Check that the first numBefore are within the thresholds, compute the average, and check if the variance is less than the threshold
				double startAvg = 0;

				for(int k = 0; k < numBefore; k++){
					int temp = Integer.parseInt(sline[j+k]);
					startAvg = startAvg + temp;			
				}

				startAvg = startAvg/numBefore;

				//Check that the starting avg is not unreasonablely high

				if(startAvg >= minStartThreshold & startAvg <= maxStartThreshold){
					//pass
				}else{
					continue;
				} 

				//Compute Variance
				double startVariance = 0.0;

				for(int k = 0; k < numBefore; k++){
                                        int temp = Integer.parseInt(sline[j+k]);
                                        startVariance = startVaraince + Math.pow((temp - startAvg), 2);
                                }

				startVariance = startVariance/numBefore;

				//Check that the starting sequence has a variance less than the threshold hold (stable coverage)				

				if( startVariance <= startVarianceThreshold){
					//pass;
				    }else{
					continue;
			   	}


				//Check next numMiddle. Compute average and variance. If the average is approximately half of the startAvg and the variance is low move on
				count = 0;
				double middleAvg = 0.0;
			
				for(int k = 0; k < numMiddle; k++){
				        int temp = Integer.parseInt(sline[j + numBefore + k]);
				        middleAvg = middleAvg + temp;
				}
				middleAvg = middleAvg/numMiddle;
				
				//Check that the average is half 
				if (startAvg/2 + delta >= thresholdLow){
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

