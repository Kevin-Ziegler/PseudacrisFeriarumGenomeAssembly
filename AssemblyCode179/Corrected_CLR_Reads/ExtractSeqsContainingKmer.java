import java.io.*;

public class ExtractSeqsContainingKmer{

  public static void main(String[] args){
      try{

      	String kmer = args[0];					//CACTGCAAAAAACTG
		String inFile = args[1];				//pferWGS_4G.fastq
		String outFile = args[2];				//pferSeqsWithGA11.fasta

        BufferedWriter bw = new BufferedWriter ( new OutputStreamWriter(new FileOutputStream(   new File(outFile) ) ));

		BufferedReader br = new BufferedReader ( new InputStreamReader(new FileInputStream(   new File(inFile) ) ));
		String head=br.readLine();
		String seq;
		int pos;
		while(head!=null){
			seq=br.readLine();
			pos=seq.indexOf(kmer);
			if(pos>=5){
				bw.write(">"+inFile.split("_")[0]+"_"+head+"\n"+seq.substring(pos-4)+"\n");
			}
			head=br.readLine();		//+ or header
			if(head.equals("+")){
				head=br.readLine();	//quals
				head=br.readLine();	//header
			}

		}
		br.close();
		bw.flush();
		bw.close();

      }catch(IOException ioe){System.out.println("<<!!ERROR main()!!>> MESSAGE:"+ioe.getMessage());}
  }

}