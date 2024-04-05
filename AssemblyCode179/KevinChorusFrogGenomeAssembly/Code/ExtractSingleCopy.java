import java.util.*;
import java.io.*;

public class ExtractSingleCopy{

	public static void main(String args[]){
		
		// String inputFile_Coverage = "SingleCopy.txt";
		// //String inputFile_CoverageLevel = "SingleCopy2.txt";

		// String inputFile_Fasta = "ccs1_4Mb.fasta";
		// String outputFile_SingleCopyKmers = "output.txt";


		String inputFile_Coverage = args[0];
		//String inputFile_CoverageLevel = "SingleCopy2.txt";

		String inputFile_Fastas = args[1];
		String outputFile_SingleCopyKmers = args[2];
		

		int numLinesToProcess = 999999999;
		if(args.length >= 4){
			String numLinesToProcess_S = args[3];
			numLinesToProcess = Integer.parseInt(numLinesToProcess_S);
		}

		int lengthKmer = 19;

		try{
			String[] files = inputFile_Fastas.split("__");

			FileReader covF = new FileReader(inputFile_Coverage);
			BufferedReader covbr = new BufferedReader(covF);

			// FileReader covLF = new FileReader(inputFile_CoverageLevel);
			// BufferedReader covLbr = new BufferedReader(covLF);



			FileWriter fw = new FileWriter(outputFile_SingleCopyKmers);

			String line = covbr.readLine();
			// String line_covL = covLbr.readLine();

			//String line_pb = pbbr.readLine();
			//line_pb = pbbr.readLine();



			int numLines = 0;

			

			for(int f =0; f < files.length; f++){
			String inputFile_Fasta = files[f];
			System.out.println(inputFile_Fasta);
			
                        FileReader pbF = new FileReader(inputFile_Fasta);
                        BufferedReader pbbr = new BufferedReader(pbF);


                        String line_pb = pbbr.readLine();
                        line_pb = pbbr.readLine();

			while(line_pb != null && line != null){
				
				//if( numLines < 427550){
                                //	numLines++;
                                //	line = covbr.readLine();
                                //	// line_covL = covLbr.readLine();
                                //	line_pb = pbbr.readLine();
                                //	line_pb = pbbr.readLine();
				//	continue;
				//}

				//if(numLines > 427570){
				//	break;
				//}


				//System.out.println(line);
				String[] sline = line.split("\t");
				// String[] sline_covL = line_covL.split("\t");
				// System.out.println(line);

				// System.out.println(sline.length);
				for(int i = 0; i < sline.length; i++){
					if(sline[i].equals("")){
						break;
					}


					int temp = Integer.parseInt(sline[i]);
					
					System.out.println(numLines);
					System.out.println(temp);
					System.out.println(line_pb.length());
					System.out.println(line);
					
					String tempS = line_pb.substring(temp, temp+lengthKmer);
					//System.out.println(numLines);
					fw.write(tempS +  " " + Integer.toString(numLines) + " \n");


				}







				numLines++;



				line = covbr.readLine();
				// line_covL = covLbr.readLine();
				line_pb = pbbr.readLine();
				line_pb = pbbr.readLine();

				if(numLines >= numLinesToProcess){
					break;
				}


			}
			
			pbF.close();
			pbbr.close();
			}
			fw.close();


			System.out.println(numLines);
		}catch(IOException e){
			System.out.println(e);
		}

	}
}
