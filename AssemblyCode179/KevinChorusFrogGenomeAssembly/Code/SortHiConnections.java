import java.io.*;
import java.util.*;


public class SortHiConnections{
	
	public static void main(String args[]){

		String inputFile = args[0];
		String outputFile = args[1];

		try{
			FileReader fr = new FileReader(inputFile);
			BufferedReader br = new BufferedReader(fr);

			FileWriter f = new FileWriter(outputFile);

			HashMap<String, Integer> map = new HashMap<String, Integer>();

			String line = br.readLine();

			while(line!= null){
				String[] sline = line.split("_");

				int id1 = Integer.parseInt(sline[0]);
				String[] templ = sline[1].split(" ");

				int id2 = Integer.parseInt(templ[0]);

				if(id1 > id2){
					int temp = id1;
					id1 = id2;
					id2 = temp;

				}

				String id1s = Integer.toString(id1);
				String id2s = Integer.toString(id2);

				String key = id1s + "_" + id2s;


				if(map.containsKey(key)){
					int temp = map.get(key);
					temp = temp + 1;
					map.put(key, temp);
				}else{
					map.put(key, 1);
				}			
				line = br.readLine();


			}
			Iterator hmIterator = map.entrySet().iterator();

	        while (hmIterator.hasNext()) {
	            Map.Entry mapElement = (Map.Entry)hmIterator.next();
	           	int value = (int)mapElement.getValue();
	            String pbConnection = (String)mapElement.getKey();

	           	f.write(pbConnection + " " + Integer.toString(value) + " \n");


	        }

		f.close();			
		br.close();
		fr.close();

		}catch(IOException e){
			System.out.println(e);
		}

	}
}
