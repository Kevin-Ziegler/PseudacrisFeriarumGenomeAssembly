import java.io.*;
import java.util.*;

public class ReadByteObject{
	
	public static void main(String args[]){

	//String inputFile = "KmerCoverageMatrixObj";
	String inputFile = args[0];



	try{




		ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream(inputFile));
		byte[][] y = (byte[][])inputStream.readObject();

		
		// for(int i = 0; i < y.length; i++){
		// 	System.out.println(y[i]);
		//}

		int countPrint = 100;
		int count = 0;

		for(int i = 0; i < y.length; i++){

			for(int j = 0; j < y[i].length; j++){
				System.out.println(y[i][j]);
				count++;
				if(count > countPrint){
					break;
				}

			}

			if(count > countPrint){
				break;
			}
		}

	}catch(FileNotFoundException e){
		System.out.println(e);
	}catch(IOException e){
		System.out.println(e);
	}catch(ClassNotFoundException e){
		System.out.println(e);
	}

	}
}

