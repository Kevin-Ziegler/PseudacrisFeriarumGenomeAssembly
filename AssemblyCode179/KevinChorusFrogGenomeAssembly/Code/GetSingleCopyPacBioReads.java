import java.util.*;
import java.io.*;


public class GetSingleCopyPacBioReads{
	

	public static void main(String args[]){



		// String inputFile_SingleCopyKmers = "output.txt";
		// String inputFile_PacBioFasta = "ccs1_4Mb.fasta";

		// String output_KmersPacBio = "outputPB.txt";

		String inputFile_SingleCopyKmers = args[0];
		String inputFile_PacBioFasta_Files = args[1];

		String output_KmersPacBio = args[2];
		
		//int numLinesToProcess = 999999999;
		//if(args.length >= 4){
		//	String numLinesToProcess_S = args[3];
		//	numLinesToProcess = Integer.parseInt(numLinesToProcess_S);
		//}
		



		int lengthKmer = 19;

		try{

			FileReader scF = new FileReader(inputFile_SingleCopyKmers);
			BufferedReader scBR = new BufferedReader(scF);

			FileWriter fw = new FileWriter(output_KmersPacBio);

			String line = scBR.readLine();


			HashMap<String, ArrayList<Integer>> map = new HashMap<>();
			HashMap<String, ArrayList<Integer>> rCmap = new HashMap<>();



			while(line!=null){

				String sline[] = line.split(" ");

				String key = sline[0];
				int pacBioId = Integer.parseInt(sline[1]);

				String rC = createReverseCompliment(key);

				if(map.containsKey(key)){
					//ArrayList<Integer> temp = map.get(key);
					//temp.add(pacBioId);
				}else{
					ArrayList<Integer> intitalizeAL = new ArrayList<Integer>();
					ArrayList<Integer> intitalizeAL2 = new ArrayList<Integer>();

					//intitalizeAL.add(pacBioId);

					map.put(key, intitalizeAL);
					rCmap.put(rC, intitalizeAL2);

				}




				line = scBR.readLine();
			}


  			
  			scF.close();
  			scBR.close();
			System.out.println("Finished Loading Kmers into HashMap");

  			String[] files = inputFile_PacBioFasta_Files.split("__");
  			int pbId = 0;


  			for(int f = 0; f < files.length; f++){


				FileReader pbF = new FileReader(files[f]);
				BufferedReader pbBR = new BufferedReader(pbF);  			


				line = pbBR.readLine();
				line = pbBR.readLine();


				while(line != null){

					// System.out.println(line.length());
					// System.out.println(line);

					int cap = line.length() - 19;

					for(int i = 0; i < cap; i++){

						//System.out.println(i);

						String tempKmer = line.substring(i, i+19);

						//String tempKmer = line.substring(10, 29);


						if(map.containsKey(tempKmer)){
							ArrayList<Integer> tempAL = map.get(tempKmer);
							tempAL.add(pbId);
							String rC = createReverseCompliment(tempKmer);
							ArrayList<Integer> tempAL2 = rCmap.get(rC);
							tempAL2.add(pbId);
						}
						if(rCmap.containsKey(tempKmer)){
							ArrayList<Integer> tempAL = rCmap.get(tempKmer);
							tempAL.add(pbId);
							String rC = createReverseCompliment(tempKmer);
							ArrayList<Integer> tempAL2 = map.get(rC);
							tempAL2.add(pbId);
						}						
					}

					pbId++;
					line = pbBR.readLine();
					line = pbBR.readLine();
										
					//if(pbId >= numLinesToProcess){
					//	break;
					//}

					if(pbId % 10000 == 0){
						System.out.println(pbId);
					}					

				}
			}


			// System.out.println("Size of map is: " + map.size());
			// System.out.println(map);


			Iterator hmIterator = map.entrySet().iterator();
  
	        // Iterate through the hashmap
	        // and add some bonus marks for every student
	  
	        while (hmIterator.hasNext()) {
	            Map.Entry mapElement = (Map.Entry)hmIterator.next();
	            ArrayList<Integer> pbIds = (ArrayList<Integer>)mapElement.getValue();
	            String kmer = (String)mapElement.getKey();

	           	fw.write(kmer + " ");
		        for(int i = 0; i < pbIds.size(); i++){
		        	int temp = pbIds.get(i);
		        	fw.write(Integer.toString(temp) + " ");

		        }
		        fw.write("\n");


	        }

			fw.close();	


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

		//System.out.println(reverse);

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

