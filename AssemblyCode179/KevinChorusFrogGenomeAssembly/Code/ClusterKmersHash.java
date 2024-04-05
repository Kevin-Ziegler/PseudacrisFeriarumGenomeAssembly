import java.io.*;
import java.util.*;


//requires sorted pair count table, which can be obtained in R via
//R
//x=read.table("PairCounts.txt",sep="\t")
//xsorted=x[order(x[,2],decreasing=T),]
//pairs=as.vector(xsorted[,1])
//counts=as.vector(xsorted[,2])
//blah=cbind(pairs,counts)
//write(t(blah),file="PairCounts_Sorted.txt",ncol=2,sep="\t")

public class ClusterKmersHash{

	public static void main(String[] args){
		try{

			String pairCountFile=args[0];		//PairCounts_Sorted.txt
			int numberClusteringIterations=Integer.parseInt(args[1]);			//1000
			String outFile=args[2];				//ClusterIDs.txt

			//Read through the file, find the max connected kmer
			BufferedReader br = new BufferedReader(new FileReader(new File(pairCountFile)));
			String tempS=br.readLine();
			int maxKmerConnections = -1;
			int id1,id2,count;
			String tempA[];


			ArrayList<Integer> id1_Lst = new ArrayList<Integer>();
			ArrayList<Integer> id2_Lst = new ArrayList<Integer>();
			ArrayList<Integer> counts_Lst = new ArrayList<Integer>();

			while(tempS!=null){
				//parse pair
				tempA=tempS.split(" "); //e.g. 611_892\t12
				id1=Integer.parseInt(tempA[0].split("_")[0]);
				id2=Integer.parseInt(tempA[0].split("_")[1]);
				count=Integer.parseInt(tempA[1]);

				if(count>maxKmerConnections){	//find max connection
					maxKmerConnections = count;
				}

				id1_Lst.add(id1);
				id2_Lst.add(id2);
				counts_Lst.add(count);


				tempS=br.readLine();
			}

			//Step Size of Clustering iterations
			int clusterStepSize = (Integer)maxKmerConnections/numberClusteringIterations;
			ArrayList<Hashtable<Integer, Integer>> clusters = new ArrayList<Hashtable<Integer, Integer>>();
			int thresh_hold = maxKmerConnections - clusterStepSize;

			//Numer of total Kmers
			int max = Collections.max(id1_Lst);
			if(Collections.max(id2_Lst) > max){
				max = Collections.max(id2_Lst);
			}
			max = max + 1;

			//Hashtable<Integer, Integer> ht = new Hashtable<>();


			int[] allKmers = new int[max];

			System.out.println("thresh_hold");
			System.out.println(thresh_hold);

			for(int i = 0; i < numberClusteringIterations; i++){




				for(int j = 0; j < id1_Lst.size(); j++){

					//System.out.println(j);
					// if(j > 100){
					// 	break;
					// }


					//need to only do values for one cluster iteration
					if(counts_Lst.get(j) < thresh_hold || counts_Lst.get(j) > (thresh_hold + clusterStepSize)){
						continue;
					}

					int tempid1 = id1_Lst.get(j);
					int tempid2 = id2_Lst.get(j);
					allKmers[tempid1] = 1;
					allKmers[tempid2] = 1;

					// if(tempid1 == 670 || tempid2 == 670){
					// 	System.out.println("Id_670");
					// 	System.out.println(tempid1);
					// 	System.out.println(tempid2);
					// }

					// System.out.println("Id");
					// System.out.println(tempid1);
					// System.out.println(tempid2);

					int cluster1 = lookUpClusterKmer(clusters, tempid1);
					int cluster2 = lookUpClusterKmer(clusters, tempid2);

					// if(tempid1 == 670 || tempid2 == 670){
					// 	System.out.println("Id_clusters");
					// 	System.out.println(cluster1);
					// 	System.out.println(cluster2);
					// }

					// System.out.println("Id_clusters");
					// System.out.println(cluster1);
					// System.out.println(cluster2);

					//if both unknow create new cluster
					if(cluster1 == -1 && cluster2 == -1){
						Hashtable<Integer, Integer> temp = new Hashtable<>();
						temp.put(tempid1, 1);
						temp.put(tempid2, 1);
						// temp[tempid1] = 1;
						// temp[tempid2] = 1;
						clusters.add(temp);
					}


					//if one unknown connect it to the other cluster
					if(cluster1 == -1 && cluster2 != -1){
						Hashtable<Integer, Integer> temp = clusters.get(cluster2);
						temp.put(tempid1, 1);
					}

					if(cluster2 == -1 && cluster1 != -1){
						Hashtable<Integer, Integer> temp = clusters.get(cluster1);
						temp.put(tempid2, 1);
					}

					//if both known connect clusters
					if(cluster1 != -1 &&  cluster2 != -1){

						//if same cluster skip

						if(cluster1 == cluster2){
							continue;
						}

						Hashtable<Integer, Integer> temp = clusters.get(cluster1);
						Hashtable<Integer, Integer> replace = clusters.get(cluster2);

						// System.out.println("Connecting Clusters Size is:");
						// System.out.println(temp.size());
						// System.out.println(replace.size());


						for (Map.Entry<Integer, Integer> e : replace.entrySet()){
				            int tempKey = e.getKey();
				            //System.out.println(tempKey);
				            int tempVal = e.getValue();
				            temp.put(tempKey, tempVal);
						}




						// for(int k = 0; k < replace.length; k++){
						// 	int newKmerToMergeIntoCluster = replace[k];
						// 	//System.out.println(newKmerToMergeIntoCluster);
						// 	if(newKmerToMergeIntoCluster == 1){
						// 		temp[k] = newKmerToMergeIntoCluster;
						// 	}

						// }
						// System.out.println(temp.size());
						// System.out.println(clusters.get(cluster1).size());
						clusters.remove(replace);
						//System.out.println("Updated");

					}

					// if(j == 70){
					// 	break;
					// }


					// System.out.println("Current Clusters");
					// for(int l =0; l < clusters.size(); l++){
					// 	//System.out.println(clusters.get(l).size());
					// 	int tempp = nonZero(clusters.get(l));
					// 	System.out.println(tempp);
					// 	//sum = sum + tempp;

					// 	//if(l == (clusters.size()-1)){
					// 	if(l == l){

					// 		Hashtable<Integer, Integer> x = clusters.get(l);
					// 		for (Map.Entry<Integer, Integer> e : x.entrySet()){
					//             int tempKey = e.getKey();
					//             System.out.println(tempKey);
					// 		}
					// 	}
					// }


				}

				thresh_hold = thresh_hold - clusterStepSize;


				// for(int j = 0; j < 10; j++){
				// 	ArrayList<ArrayList> temp = clusters.get(j);
				// 	System.out.println(temp.size());
				// }
			System.out.println("Results for iteration:");
			System.out.println(i);
			System.out.println("Total Clusters:");
			System.out.println(clusters.size());
			int sum = 0;

			for(int l =0; l < clusters.size(); l++){
				//System.out.println(clusters.get(l).size());
				int tempp = nonZero(clusters.get(l));
				System.out.println("Cluster num:");
				System.out.println(l);
				System.out.println("Cluster size:");
				System.out.println(tempp);
				System.out.println("PB Ids for Cluster:");

				//for (Map.Entry<Integer, Integer> e : clusters.get(l).entrySet()){
		            //int tempKey = e.getKey();
		            //int tempVal = e.getValue();
		            //System.out.println(tempKey);
				//}

				sum = sum + tempp;

				//if(l == (clusters.size()-1)){
				// if(l == l){

				// 	int temp[] = clusters.get(l);
				// 	for(int ll = 0; ll < temp.length; ll++){

				// 		if(temp[ll] != 0){
				// 			System.out.println(ll);
				// 		}
				// 	}
				// }
			}

			System.out.println("sum:");
			System.out.println(sum);

			int counter = 0;
			for(int k =0; k < allKmers.length; k++){
				if(allKmers[k] == 1){
					counter++;
				}
			}
			System.out.println("Num Kmers");
			System.out.println(counter);

			}




			// //write the result
			// BufferedWriter bw = new BufferedWriter(new FileWriter(new File(outFile)));
			// for(int i=0; i<nPBReads; i++){
			// 	Node node=nodes[i];
			// 	bw.write(""+node.score);
			// 	while(node.up!=null){
			// 		node=node.up;
			// 	}
			// 	bw.write("\t"+(i+1)+"\t"+node.id+"\n");
			// }
			// bw.flush();
			// bw.close();


		}catch(IOException ioe){System.out.println(ioe.getMessage());}
	}

	public static int lookUpClusterKmer(ArrayList<Hashtable<Integer, Integer>> arr, int kmer){

		for(int i = 0; i < arr.size(); i++){

		    Hashtable<Integer, Integer> temp = arr.get(i);

		    boolean result = temp.containsKey(kmer);

		    if(result == true){
		    	return i;
		    }

		}

		return -1;

	}

	public static int binarySearch(ArrayList<Integer> arr, int l, int r, int x)
	{
	    if (r >= l) {
	        int mid = l + (r - l) / 2;
	 
	        // If the element is present at the middle
	        // itself
	        if (arr.get(mid) == x)
	            return mid;
	 
	        // If element is smaller than mid, then
	        // it can only be present in left subarray
	        if (arr.get(mid) > x)
	            return binarySearch(arr, l, mid - 1, x);
	 
	        // Else the element can only be present
	        // in right subarray
	        return binarySearch(arr, mid + 1, r, x);
	    }
	 
	    // We reach here when element is not
	    // present in array
	    return -1;
	}

	public static int nonZero(Hashtable<Integer, Integer> x){

		int count = 0;
		for (Map.Entry<Integer, Integer> e : x.entrySet()){
            int tempKey = e.getKey();
            int tempVal = e.getValue();
            count++;
		}
		return count;

	}

}

class Node{
	int id=-1;
	int score=0;
	Node up=null;
}
