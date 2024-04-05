import java.io.*;
import java.util.*;

public class CreateHiCMatrix{
	
	public static void main(String args[]){

		String inputFile_HiC_Connections = "outputHiC_Connections_Spaced.txt";
		String outputFile_HiC_Matrix = "outputHiC_Connections_Spaced_Matrix.txt";


		try{

			FileReader f = new FileReader(inputFile_HiC_Connections);
			BufferedReader br = new BufferedReader(f);

			String line = br.readLine();

			ArrayList<Integer> allPacBioIds = new ArrayList<Integer>();
			ArrayList<Integer> index1Lst = new ArrayList<Integer>();
			ArrayList<Integer> index2Lst = new ArrayList<Integer>();


			while(line != null){

				String[] sline = line.split("_");

				if(sline.equals("")){
					break;
				}

				String temp = sline[1].split(" ")[0];

				int pb1 = Integer.parseInt(sline[0]);
				int pb2 = Integer.parseInt(temp);


				int index1 = -1;
				int index2 = -1;

				if(allPacBioIds.contains(pb1) == false){
					allPacBioIds.add(pb1);
				}
				index1 = allPacBioIds.indexOf(pb1);

				if(allPacBioIds.contains(pb2) == false){
					allPacBioIds.add(pb2);
				}
				index2 = allPacBioIds.indexOf(pb2);

				index1Lst.add(index1);
				index2Lst.add(index2);

				line = br.readLine();
			}


			System.out.println(allPacBioIds.size());


			int[][] matrix = new int[allPacBioIds.size()][allPacBioIds.size()];

			for(int i = 0; i < index1Lst.size(); i++){
				matrix[index1Lst.get(i)][index2Lst.get(i)]++;
			}


			FileWriter fw = new FileWriter(outputFile_HiC_Matrix);

			for(int i = 0; i < allPacBioIds.size(); i++){
				fw.write(Integer.toString(allPacBioIds.get(i)) + ",");
			}

			fw.write("\n");


			for(int i = 0; i < matrix.length; i++){

				for(int j = 0; j < matrix[0].length; j++){

					fw.write(Integer.toString(matrix[i][j]));
					if(j < (matrix[0].length -1)){
						fw.write(",");
					}

				}

				fw.write("\n");

			}

			fw.close();




		}catch(IOException e){
			System.out.println(e);
		}


	}
}
