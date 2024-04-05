import java.io.*;
import java.util.Arrays;
import java.util.HashMap;
import java.util.*;

//VERSION 3 DOES NOT ASSUME A FOLDER STRUCTURE AN INSTEAD JUST ASKES FOR THE FILENAME.

//VERSION 2 DOES ALL LOCI IN SEQUENCE...MULTIPLE INPUT MAP FILES ARE ALLOWED...all results go into single .seed file

//////////////////////////////////////////////////////////////////////////////
//THIS PROGRAM PERFORMS A SIMPLE ALIGNMENT OF THE MAPPED READS ASUMING NO GAPS
//THIS IS ALAN'S ADJUSTMENT OF TIMS "AlignMappedReads.java"
//THIS VERSION IMPLEMENTS THE NEW SCREEN FOR CONTAMINATION AND PARALOGS
//25 June 2012  

public class FindMaskPointsVia15merProfile{							//THIS VERSION DOES NOT WORRY ITSELF WITH THE REFERENCE (IGNORES REFERENCE MAPPED SINCE ONLY ONE REFERENCE IS TYPICALLY USED)
	public static void main(String[] args){
	  try {		
		
		String infile = args[0];
		int nLoci = Integer.parseInt(args[1]);
		String outfileStem = args[2];
		double minLogScore=Double.parseDouble(args[3]);					//e.g. 3 (log10(1000))

		int hardcodekmerlength = 21;

		//int threshold1 = Integer.parseInt(args[3]);	//e.g. 3000 <<-15mer score above which a site is considered bad
		//int threshold2 = Integer.parseInt(args[4]);	//e.g. 30	<<-maximum consecuative bad sites allowed
		
		BufferedReader br = new BufferedReader (new InputStreamReader (	new FileInputStream (new File(infile))));		
		BufferedWriter bwA = new BufferedWriter (new OutputStreamWriter(new FileOutputStream(new File(outfileStem+"_MaskCoords.txt"))));
		BufferedWriter bwB = new BufferedWriter (new OutputStreamWriter(new FileOutputStream(new File(outfileStem+"_VerifyInR.r")))); //width of region x average log10(15mer score)

		String blah[]=outfileStem.split("/");
		
		//get the number of sites
		int nSites = 0;
		int tempInt=0;
		String tempS;
		for(int loc=1; loc<nLoci; loc++){
			//tempInt=br.readLine().split("\t").length;
			tempInt=br.readLine().split(" ").length;
			//System.out.println(tempInt);
			if(tempInt>nSites){nSites=tempInt;}			
		}
		br.close();
		
		//now determine which regions to mask due to repetitive elements
		br = new BufferedReader (new InputStreamReader (	new FileInputStream (new File(infile))));
	System.out.println(blah[blah.length-1]);
		bwB.write("pdf(\""+blah[blah.length-1]+"_repeatMap.pdf\")\n");
		bwB.write("plot(-9999,-9999,xlim=c(0,"+nSites+"),ylim=c(0,"+nLoci+"),main=\""+infile+"\",xlab=\"Site\",ylab=\"Locus\")\n");
		bwB.write("rect(0,-15,"+nSites+","+nLoci+",col=\"black\")\n");
		bwB.write("text("+(1*nSites/5.0)+",-4,\"1,000 copies\",col=rainbow(40)["+(int)(10*(8-3)-19)+"],cex=0.5)\n");
		bwB.write("text("+(2*nSites/5.0)+",-4,\"10,000 copies\",col=rainbow(40)["+(int)(10*(8-4)-19)+"],cex=0.5)\n");
		bwB.write("text("+(3*nSites/5.0)+",-4,\"100,000 copies\",col=rainbow(40)["+(int)(10*(8-5)-19)+"],cex=0.5)\n");
		bwB.write("text("+(4*nSites/5.0)+",-4,\"1,000,000 copies\",col=rainbow(40)["+(int)(10*(8-6)-19)+"],cex=0.5)\n");		
		bwB.write("text("+(1*nSites/5.0)+",-12,\">50bp\",col=rainbow(40)["+(int)(10*(8-3)-19)+"],cex=0.5)\n");
		bwB.write("text("+(2*nSites/5.0)+",-12,\">40bp\",col=rainbow(40)["+(int)(10*(8-4)-19)+"],cex=0.5)\n");
		bwB.write("text("+(3*nSites/5.0)+",-12,\">30bp\",col=rainbow(40)["+(int)(10*(8-5)-19)+"],cex=0.5)\n");
		bwB.write("text("+(4*nSites/5.0)+",-12,\">20bp\",col=rainbow(40)["+(int)(10*(8-6)-19)+"],cex=0.5)\n");		


	 	double scores15mer[];
		boolean mask[];
		for(int i=0; i<nLoci; i++){
			tempS=br.readLine();
			//String tempS2[]=tempS.split("\t");
			String tempS2[] = tempS.split(" ");
			scores15mer = new double[nSites];
			mask = new boolean[nSites+hardcodekmerlength];
			for(int j=0; j<nSites; j++){
				scores15mer[j]=Math.min(6.0,Math.log10(Double.parseDouble(tempS2[j])/100.0));	//treat over 10^6.5 million as 10^6.5 million
			}

			//use different threshold x length combinations
			for(double threshold=3; threshold<=6; threshold+=0.1){
				if(threshold<minLogScore){continue;}
				int begBadRegion=0;
				boolean inBadRegion=false;
				for(int j=0; j<nSites; j++){
				
					//System.out.print((i+1)+"\t"+j+"\t"+threshold+"vs"+scores15mer[j]);
					
					if(!inBadRegion && scores15mer[j]>=threshold){	//moving into bad region
						inBadRegion=true;
						begBadRegion=j;
					}else if(inBadRegion && (scores15mer[j]<threshold || j==nSites-1)){	//moving into good region or end of sequence
						inBadRegion=false;
						//check length of bad region
						if(hardcodekmerlength+j-begBadRegion>10*(8-threshold)){	//longer regions tollerated when score threshold is lower
							for(int x=begBadRegion; x<j+hardcodekmerlength-1; x++){
								mask[x]=true;
							}
							bwB.write("lines(x=c("+begBadRegion+","+(j+hardcodekmerlength-1)+"),y=c("+(i+1)+","+(i+1)+"),col=rainbow(40)["+(int)(10*(8-threshold)-19)+"],lwd=1)\n");
						}
					}else{
						//not transitioning
					}

				}				
			}
			
			//Now write mask coords base on boolean vector

			bwA.write(""+(i+1));			
			for(int j=0; j<nSites; j++){
				//System.out.println("print stuff?");
				if(mask[j] && (j==0 || !mask[j-1])){	//entering into masked region start 
					bwA.write("\t"+(j));
					System.out.println("Entering Mask Region");
				}else if( (!mask[j] && j>0 && mask[j-1]) || (mask[j] && j==nSites-1)){ //leaving masked region
					bwA.write("\t"+(j-1));
					System.out.println("Leaving Mask Region");
				}
			}
			bwA.write("\n");
		}
		br.close();
		bwB.write("dev.off()\n");
		bwB.flush();
		bwB.close();
		bwA.flush();
		bwA.close();

/*


			for(int j=0; j<length-30; j++){
				for(int k=0; k<30; k++){
					if(scores15mer[j+k]<score30merMin){
						score30merMin=scores15mer[j+k];
					}
					score30merAvg+=scores15mer[j+k];
					if(scores15mer[j+k]>0){
						scoreLOG30merAvg+=Math.log10(scores15mer[j+k]);
					}
					
				}
				
				score30merAvg/=30.0;
				scoreLOG30merAvg/=30.0;
				
				if(scoreLOG30merAvg>Math.log10(threshold1)){
					if(inBadRegion && j==length-30-1){
						if(j-begBadRegion>threshold2){	//allow bad regions below 60bp
							bw3.write(begBadRegion+"\t"+((j-1)+30)+"\t");
							bw4.write("points(c("+begBadRegion+","+(j-1)+"),c("+(i+1)+","+(i+1)+"),cex=0.5,pch=19,col=\"blue\")"+"\n");
						}						
					}else if(inBadRegion){
						//do nothing	
					}else{	//we are moving into a bad region
						inBadRegion=true;
						begBadRegion=j;
					}
				}else{
					if(inBadRegion){	//we are moving out of a bad region
						inBadRegion=false;
						if(j-begBadRegion>threshold2){	//allow bad regions below 60bp
							bw3.write(begBadRegion+"\t"+((j-1)+30)+"\t");
							bw4.write("points(c("+begBadRegion+","+(j-1)+"),c("+(i+1)+","+(i+1)+"),cex=0.5,pch=19,col=\"blue\")"+"\n");
						}
					}
				}
				bw.write(scoreLOG30merAvg+"\t");
				bw2.write(score30merMin+"\t");
			}

			bw.write("\n");
			bw2.write("\n");
			bw3.write("\n");
		}
		br.close();
		bw.flush();
		bw.close();
		bw2.flush();
		bw2.close();
		bw3.flush();
		bw3.close();
		bw4.flush();
		bw4.close();
*/
	} catch(IOException ioe){System.out.println("\n\n<<!!ERROR main()!!>>"+ioe.getMessage());}			
  }	//close main()
}
