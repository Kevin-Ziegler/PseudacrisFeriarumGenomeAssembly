import java.io.*;
import java.util.*;

public class ClusterSingleCopyPB{
	
	public static void main(String args[]){
		String inputPB = args[0];
		String outputClusters = args[1];

		try{

		FileReader fr = new FileReader(inputPB);
		BufferedReader br = new BufferedReader(fr);
		FileWriter f = new FileWriter(outputClusters);

		ArrayList<HashMap<Integer, Integer>> clusters = new ArrayList<HashMap<Integer, Integer>>();

		String line = br.readLine();
		int lineNum = 0;

		while(line != null){
			//System.out.println(line);
			String[] sline = line.split(" ");
			ArrayList<Integer> clustersForKmer = new ArrayList<Integer>();
			ArrayList<Integer> pbIds = new ArrayList<Integer>();


			for(int i = 1; i < sline.length; i++){
				int pbId = Integer.parseInt(sline[i]);
				pbIds.add(pbId);


				//Find clusters for PB ID
				for(int j = 0; j < clusters.size(); j++){
					if(clusters.get(j).containsKey(pbId)){
						if(clustersForKmer.contains(j) != true){
							clustersForKmer.add(j);
						}
					}
				}
			}

			//Group clusters

			//No Clusters Make New Cluster
			if(clustersForKmer.size() == 0){
				HashMap<Integer, Integer> newCluster = new HashMap<Integer, Integer>();
				for(int i = 0; i < pbIds.size(); i ++){
					newCluster.put(pbIds.get(i), 1);
				}
				clusters.add(newCluster);
			}				

			//Only one cluster with PbId
			if(clustersForKmer.size() == 1){
				int tempCluster = clustersForKmer.get(0);
				HashMap<Integer, Integer> currentCluster = clusters.get(tempCluster);
				for(int i = 0; i < pbIds.size(); i++){
					currentCluster.put(pbIds.get(i), 1);

				}
			}

			//Multiple Clusters with PbId
			if(clustersForKmer.size() > 1){
				int tempCluster = clustersForKmer.get(0);
				HashMap<Integer, Integer> currentCluster = clusters.get(tempCluster);


				//Merge clusters
				for(int j = 1; j < clustersForKmer.size(); j++){
					int clusterToMerge_index = clustersForKmer.get(j);
					HashMap<Integer, Integer> clusterToMerge = clusters.get(clusterToMerge_index);

						for(int k = 0; k < clusterToMerge.size(); k++){
							currentCluster.put(clusterToMerge.get(k), 1);
						}
				}

				//Put new cluster in there
				for(int i = 0; i < pbIds.size(); i++){
					currentCluster.put(pbIds.get(i), 1);
				}

				//Remove Merged Clusters
				int countRemoved = 0;

				Collections.sort(clustersForKmer);

				for(int j = 1; j < clustersForKmer.size(); j++){
					int clusterToMerge_index = clustersForKmer.get(j);
					clusters.remove(clusterToMerge_index - countRemoved);
					countRemoved++;
				}


			}				
			

			line = br.readLine();
			lineNum++;
			//System.out.println(lineNum);

			if(lineNum % 10000 == 0){
				System.out.println(lineNum);
			}


		}

		f.write("Num Clusters: \n");
		f.write(clusters.size() + " \n");

		for(int i = 0; i < clusters.size(); i++){
			f.write("Cluster Num: " + Integer.toString(i) + " \n");
			f.write("Cluster Size: " + Integer.toString(clusters.get(i).size()) + " \n");
			f.write("Cluster PBIds: ");

			HashMap<Integer, Integer> x = clusters.get(i);

			Iterator hmIterator = x.entrySet().iterator();

	        while (hmIterator.hasNext()) {
	            Map.Entry mapElement = (Map.Entry)hmIterator.next();
	           	int value = (int)mapElement.getValue();
	            int key = (int)mapElement.getKey();

	           	f.write(key + " ");


	        }
	        f.write("\n");

		}

		f.close();
		br.close();
		fr.close();

		}catch(IOException e){

		}
		
	}
}
