import java.io.*;
import java.util.*;

public class TestRC{
	
	public static void main(String args[]){

		//CAGCAGGGAACTGGATCCG 540529 806221 824000 2763735
		//TGTGATATCCAGACAGGGA 934548 1209195 3052427 3161462
		//ACCTCCACTGCTGAGCAGA 254543 537659 712310 1520287 1759050 3101727
		//CTAATGACCGCCGGGCCCT 872534 1365245 1469791 1474348

// GGCTGCGGGGTAGTCTGAA 119886 200452 791726 984144 1189942 1803041 1827153 1936018 2139911 2511933 2636648 2745422 2815184 2923909 3251076 3303597 3351527
// ACAATACTGCAATACTATA 182593 718576 1294126 1385832 1671392 3075325 3097870 3174487
// GGAACAGGGCAATCACCAA 2206901 2220013 2258112 2530921
// ATGCCTGATCCCATGGTAC 74768 93448 542013 948483 1078340 1183681 1214839 1324947 1912585 2244711 2550354 3322518




		String inputObjectPath = "/pool/KevinChorusFrogGenomeAssembly/Examples/WholeGenome_RC_HiC_Connections_August_5/KmerMatrixObj";

		//String[] lstKmers = {"CAGCAGGGAACTGGATCCG", "TGTGATATCCAGACAGGGA", "ACCTCCACTGCTGAGCAGA", "CTAATGACCGCCGGGCCCT"};

		String[] lstKmers = {"GGCTGCGGGGTAGTCTGAA","ACAATACTGCAATACTATA","GGAACAGGGCAATCACCAA","ATGCCTGATCCCATGGTAC"};

		try{


			ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream(inputObjectPath));
			byte[][] countArray = (byte[][])inputStream.readObject();
			
			for(int p = 0; p < lstKmers.length; p++){

				String kmer = lstKmers[p];
				int K1 = 4;
				int K2 = 15;

				String binKmer = "";
				for(int i = 0; i< kmer.length(); i++){
					switch(kmer.charAt(i)){
						case 'A': 
								binKmer = binKmer + "00";
								break;
						case 'T': 
								binKmer = binKmer + "11";
								break;
						case 'C': 
								binKmer = binKmer + "01";
								break;
						case 'G': 
								binKmer = binKmer + "10";
								break;
				        default: 
				        	System.out.println("SHOULD NOT HAVE ENCOUNTERED DEFAULT IN SWITCH: ");
				        	System.out.println(kmer.charAt(i));
				        	break;
					}
					
				}




				int kmer1=Integer.parseInt(binKmer.substring(0,2*K1),2);                    //two bits per character
				int kmer2=Integer.parseInt(binKmer.substring(2*K1,2*(K1+K2)),2);

				                                        //GET BINARY KMER (STRING REPRESENTATION) FROM SPLIT INT KMER
				                                         //concatenate 2 strings
				                                        //NOTE: K determines maximum number of positions needed to store integer
				                                        //To ensure the correct length is represented in string, leading 0's are sometimes needed
				                                        //binKmer1=String.format("%"+2*K1+"s",Integer.toBinaryString(i)).replace(" ","0");
				                                        //binKmer2=String.format("%"+2*K2+"s",Integer.toBinaryString(j)).replace(" ","0");

				//example with K1=4 and K2=15

				//A A A A A A A A A G G G C G T  A G T C
				//000000000000000000101010011011 00101101

				//10000111 000110010101111111111111111111
				//G A C T  A C G C C C T T T T T T T T T

				//System.out.println(i+"\t"+binKmer1);
				//System.out.println(j+"\t"+binKmer2);

				                                        //binKmer=binKmer1+binKmer2;

				//System.out.println(binKmer);

				                                        //GET REVERSE COMPLEMENT OF BINARY KMER
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
				System.out.println(kmer);
				System.out.println(binKmer);
				System.out.println(kmer1);
				System.out.println(kmer2);
				System.out.println(countArray[kmer1][kmer2]);
				System.out.println(iRC);
				System.out.println(jRC);
				System.out.println(countArray[iRC][jRC]);

			}
		}catch(IOException e){
			System.out.println(e);
		}catch(ClassNotFoundException e){
			System.out.println(e);
		}

	}
}

