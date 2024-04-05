import java.util.*;
import java.io.*;

public class HiC_Connections_Filter_Print{
	

	public static void main(String args[]){

		// String inputFile_HiC = "test_R1_001.fastq";
		// String inputFile_SingleCopyKmers_PBs = "outputPB.txt";
		// String output_HiC_Connections = "ouputHiC_Connections.txt";

		String inputFiles_HiC = args[0];
		String inputFile_SingleCopyKmers_PBs = args[1];
		String output_HiC_Connections_Overlap = args[2];
		String output_HiC_Connections_Spaced = args[3];
		//String output_HiC_Connections_Overlap_Lines = args[4];
		//String output_HiC_Connections_Spaced_Lines = args[5];
		String output_HiC_Connections_Log = args[4];

		int lengthKmer = 19;
		int maxPB_per_Kmer = 20;

		try{

			FileReader scF = new FileReader(inputFile_SingleCopyKmers_PBs);
			BufferedReader scBR = new BufferedReader(scF);



			HashMap<String, ArrayList<Integer>> map = new HashMap<>();
			HashMap<String, ArrayList<Integer>> rCmap = new HashMap<>();


			String line = scBR.readLine();

			while(line!=null){

				String[] sline = line.split(" ");
				
				//Skip if Kmer has to many PB reads tied to it
				if((sline.length-1) >= maxPB_per_Kmer){
					line = scBR.readLine();
					continue;
				}
				ArrayList<Integer> temp = new ArrayList<Integer>();

				String key = sline[0];
				for(int i = 1; i < sline.length; i++){
					int pbid = Integer.parseInt(sline[i]);
					temp.add(pbid);
				}
				String rCKey = createReverseCompliment(key);

				map.put(key, temp);
				rCmap.put(rCKey, temp);



				line = scBR.readLine();
			}


			scF.close();
			scBR.close();


			FileWriter output_Overlap = new FileWriter(output_HiC_Connections_Overlap);
			FileWriter output_Spaced = new FileWriter(output_HiC_Connections_Spaced);
			FileWriter output_Log = new FileWriter(output_HiC_Connections_Log);
			//FileWriter overlapLines = new FileWriter(output_HiC_Connections_Overlap_Lines);

			String[] files = inputFiles_HiC.split("__");
			int lineNum = 0;


			for(int f = 0; f < files.length; f++){


				FileReader hiCF = new FileReader(files[f]);
				BufferedReader hicBR = new BufferedReader(hiCF);
			

				line = hicBR.readLine();
				line = hicBR.readLine();

				while(line != null){


					ArrayList<ArrayList<Integer>> tempPbIds = new ArrayList<ArrayList<Integer>>();
					ArrayList<Integer> locationTempPbIds = new ArrayList<Integer>();
					ArrayList<Integer> locationTempPbIds_RC = new ArrayList<Integer>();

					for(int i = 0; i < (line.length()-19); i++){
						String tempKmer = line.substring(i, i+19);
						//System.out.println(tempKmer);
						if(map.containsKey(tempKmer)){
							ArrayList<Integer> tempAL = map.get(tempKmer);
							tempPbIds.add(tempAL);
							//System.out.println(tempAL);
							locationTempPbIds.add(i);
						}
						if(rCmap.containsKey(tempKmer)){
							ArrayList<Integer> tempAL = rCmap.get(tempKmer);
							tempPbIds.add(tempAL);
							//System.out.println(tempAL);
							locationTempPbIds_RC.add(i);
						}					
					}


					if(tempPbIds.size() <= 1){
						//nothing
					}else{

						//System.out.println(tempPbIds);
						int numSpaced = 0;
						int numOverlap = 0;
						int indexKmer = -1;
						HashMap<String, Integer> currentConnections = new HashMap<String, Integer>();


						for(int i = 0; i < (tempPbIds.size()-1); i++){

							ArrayList<Integer> one = tempPbIds.get(i);
							ArrayList<Integer> two = tempPbIds.get(i+1);
							int numDifferences  = 0;

							if(two.size() > one.size()){
								ArrayList<Integer> tempL = one;
								one = two;
								two = one;
							}

							for(int j = 0; j < one.size(); j++){

								int temp = one.get(j);

								if(two.contains(temp) == true){
									numDifferences++;
								}
							}

							FileWriter output = null;
							

							if(numDifferences == 0){
								output = output_Spaced;
								numSpaced++;
							}else{
								output = output_Overlap;
								numOverlap++;
							}

							indexKmer = i;					

							ArrayList<Integer> kmer1pb = tempPbIds.get(indexKmer);
							ArrayList<Integer> kmer2pb = tempPbIds.get(indexKmer+1);	
							String connection;
							for(int k = 0; k < kmer1pb.size(); k++){

								for(int j = 0; j < kmer2pb.size(); j++){
									connection = kmer1pb.get(k) + "_" + kmer2pb.get(j);
									if(currentConnections.containsKey(connection)){
                                                        			continue;
                                               	 			}else{
										currentConnections.put(connection, 1);
										output.write(connection + " \n");
										//output2.write(Integer.toString(lineNum) + " \n");
									}
								}
							}

						
						}
                                                //Log of SC Kmers found in HiC reads
                                                //HiC read id
						String readId = Integer.toString(lineNum);
						String singleCopy = Integer.toString(tempPbIds.size());
						String posF = "";
						String posR = "";
						String numSpaced_S = Integer.toString(numSpaced);
						String numOverlap_S = Integer.toString(numOverlap);
						
						for(int l = 0; l < locationTempPbIds.size(); l++){
							posF = posF + locationTempPbIds.get(l) + ",";
						}
						for(int l = 0; l < locationTempPbIds_RC.size(); l++){
							posR = posR + locationTempPbIds_RC.get(l) + ",";
						}

						
						 
                                                output_Log.write(readId + " " + singleCopy + " " + posF + "_" + posR + " " + numSpaced_S + " " + numOverlap_S + " \n");

						

					}

					line = hicBR.readLine();
					line = hicBR.readLine();
					line = hicBR.readLine();
					line = hicBR.readLine();
					lineNum++;

				}
			}

			output_Overlap.close();
			output_Spaced.close();
			output_Log.close();



		}catch(IOException e){
			System.out.println(e);
		}
	}

	public static String createReverseCompliment(String x){

		String reverse = "";
		String reverseCompliment = "";

		for(int i = 0; i < x.length(); i++){

			reverse = reverse + x.charAt((x.length()-1)- i);

		}

		for(int i = 0; i < reverse.length(); i++){

			String temp = "";

			if(reverse.charAt(i) == 'A'){
				temp = "T";
			}
			if(reverse.charAt(i) == 'T'){
				temp = "A";
			}
			if(reverse.charAt(i) == 'C'){
				temp = "G";
			}
			if(reverse.charAt(i) == 'G'){
				temp = "C";
			}	

			reverseCompliment = reverseCompliment + temp;					

		}

		return reverseCompliment;
	}	
}
