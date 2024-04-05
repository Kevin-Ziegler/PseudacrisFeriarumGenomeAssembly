import java.io.*;
import java.util.*;



public class ClusterFaster{
	
	public static void main(String args[]){

		String input_SingleCopy = args[0];
		String output = args[1];


		ArrayList<ArrayList<Integer>> clusters = new ArrayList<ArrayList<Integer>>();
		HashMap<Integer, ArrayList<Integer>> kmercluster_ids = new HashMap<Integer, ArrayList<Integer>>();
		HashMap<Integer, Integer> usedLine = new HashMap<Integer, Integer>();
		ArrayList<ArrayList<Integer>> newclusters = new ArrayList<ArrayList<Integer>>();




		try{

			FileReader fr = new FileReader(input_SingleCopy);
			BufferedReader br = new BufferedReader(fr);

			String line = br.readLine();
			int lineNum = 0;

			while(line != null){

				String[] sline = line.split(" ");

				String kmer = sline[0];

				ArrayList<Integer> tempArrayList = new ArrayList<Integer>();

				for(int i = 1; i < sline.length; i++){
					int key = Integer.parseInt(sline[i]);
					tempArrayList.add(key);
					if(kmercluster_ids.containsKey(key)){
						ArrayList<Integer> tempAL = kmercluster_ids.get(key);
						tempAL.add(lineNum);

					}else{
						ArrayList<Integer> tempAL = new ArrayList<Integer>();
						tempAL.add(lineNum);
						kmercluster_ids.put(key, tempAL);
					}
					//kmercluster_ids.put(Integer.parseInt(sline[i]), lineNum);
				}

				clusters.add(tempArrayList);



				lineNum++;
				line = br.readLine();

			}

			System.out.println("Loaded");


			for(int i =0; i < clusters.size(); i++){
				if(usedLine.containsKey(i)){
					continue;
				}
				ArrayList<Integer> linesInCluster = new ArrayList<Integer>();
				linesInCluster.add(i);
				usedLine.put(i, 1);

				ArrayList<Integer> listPBIds = clusters.get(i);


				ArrayList<Integer> currentLines = new ArrayList<Integer>();

				for(int j = 0; j < listPBIds.size(); j++){

					ArrayList<Integer> lstLinesKmer = kmercluster_ids.get(listPBIds.get(j));

					for(int k = 0; k < lstLinesKmer.size(); k++){
						if(usedLine.containsKey(lstLinesKmer.get(k))){
							continue;
						}
						currentLines.add(lstLinesKmer.get(k));
						usedLine.put(lstLinesKmer.get(k), 1);
						linesInCluster.add(lstLinesKmer.get(k));
					}

				}

				while(currentLines.size() > 0){

					ArrayList<Integer> lines = currentLines;


					currentLines = new ArrayList<Integer>();

					for(int j = 0; j < lines.size(); j++){

						ArrayList<Integer> lstLinesKmer = clusters.get(lines.get(j));

						for(int k = 0; k < lstLinesKmer.size(); k++){

							ArrayList<Integer> tempLines = kmercluster_ids.get(lstLinesKmer.get(k));

							for(int l = 0; l < tempLines.size(); l++){


								if(usedLine.containsKey(tempLines.get(l))){
									continue;
								}
								currentLines.add(tempLines.get(l));
								usedLine.put(tempLines.get(l), 1);
								linesInCluster.add(tempLines.get(l));
							}
						}

					}


				}



				newclusters.add(linesInCluster);
				// System.out.println("Cluster: ");
				// System.out.println(i);
				// for(int j = 0; j < linesInCluster.size(); j++){
				// 	System.out.println(linesInCluster.get(j));
				// }

			}

			System.out.println(newclusters.size());
			FileWriter f = new FileWriter(output);
			double avgSize = 0;
			HashMap<Integer, Integer> usedPB = new HashMap<Integer, Integer>();



			for(int i = 0; i < newclusters.size(); i++){
				ArrayList<Integer> temp = newclusters.get(i);


				avgSize = avgSize + temp.size();

				f.write("Cluster: " + Integer.toString(i) + " \n");

				for(int j = 0; j < temp.size(); j++){

					ArrayList<Integer> PBIDS = clusters.get(temp.get(j));

						for(int k = 0; k < PBIDS.size(); k++){

							if(usedPB.containsKey(PBIDS.get(k))){
								//pass
							}else{
								f.write(Integer.toString(PBIDS.get(k)) + " ");
								usedPB.put(PBIDS.get(k), 1);
							}
						}
				}
				f.write("\n");

			}





		}catch(FileNotFoundException e){
			System.out.println(e);
		}catch(IOException e){
			System.out.println(e);
		}


	}
}
