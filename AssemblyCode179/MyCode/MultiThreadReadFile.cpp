#include <stdio.h>
#include <omp.h>
#include <vector>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <map>

using namespace std;

struct returnPointers {
	string * nameRepeats;
	int * lengthRepeats;
};


struct returnPointers readInRepeats(string * nameRepeats, int * lengthRepeats) {
    //cout << "Hello World";
	string line;
	int counter = 0;
	ifstream myfile("/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ChorusFrog_Canu_CLR_2/Canu_Contig_Headers.txt");
	if (myfile.is_open()){
		while(getline(myfile, line)){
			//cout << line << '\n';

			int lengthLine = line.length();
			string temp = "";
			string lengthR = "";

			int countSpaces = 0;
			int countSkip = 0;

			for(int i = 0; i < lengthLine; i++){
				char c = line[i];
				if(c != ' ' && countSpaces == 0){
					if(i != 0){
						temp = temp + c;
					}
				}else if(c != ' ' && countSpaces == 1){
					if(countSkip >  3){
						lengthR = lengthR + c;
					}
					countSkip++;
				}else{
					countSpaces++;
				} 
				//cout << line[i] << " ";
			}
			//cout << temp << endl;
			nameRepeats[counter] = temp;
			lengthRepeats[counter] = stoi(lengthR);
			counter++;
			//break;

			//if(counter > 11){
			//	break;
			//}
		}

	myfile.close();
	} else{
		cout << "Unable to open File";
	}

	//cout << nameRepeats[1] << endl;
	//cout << lengthRepeats[1] << endl;
	//cout << nameRepeats[6] << endl;
	struct returnPointers p;
	p.lengthRepeats = lengthRepeats;
	p.nameRepeats = nameRepeats;


	return p;
}



string segment_read(char *buff, const int len, const int count) {
	//cout << "In segment Read" << endl;
			string temp;
			int countSpace = 0;
			
			for(int i = 0; i < len; i++){
				char c = buff[i];
				if(c != '\t'){
					if(countSpace == 2){
						temp = temp + c;
					}

					if(countSpace == 3){
						break;
					}
				}else{
					//cout << "space" << endl;
					countSpace++;
				}

				//if(c == '\t'){
				//	cout << "tab" << endl;
				//}
			}

			//cout << temp << endl;
			//break;

			//if (temp.length() > 5){
			//	cout << temp << endl;
			//}

			//cout << nameRepeats[0] << endl;
			
			//if(countReads.find(temp) != countReads.end()){
			//	countReads[temp] = countReads[temp] + 1;
			//}


  return temp;  
}

std::map<string, int> foo(char* buffer, size_t size, string * nameRepeats, std::map<string, int> &countReads) {
    int count_of_reads = 0;
    int count = 1;
    std::vector<int> *posa;
    int nthreads;

	//omp_set_num_threads(50);

    #pragma omp parallel 
    {
        nthreads = omp_get_num_threads();
	//omp_set_num_threads(1);
	//nthreads = 1;
	//cout << "Number threads " << nthreads << endl;
        const int ithread = omp_get_thread_num();
        #pragma omp single 
        {
		//cout << "single" << endl;
            posa = new vector<int>[nthreads];
            posa[0].push_back(0);
        }

        //get the number of lines and end of line position
	int independentCount = 0;
        #pragma omp for reduction(+: count)
        for(int i=0; i<size; i++) {
            if(buffer[i] == '\n') { //should add EOF as well to be safe
                count++;
		independentCount++;
                posa[ithread].push_back(i);
            }
        }

	//cout << "Real Count n " << count << endl;
	//cout << "Thread Number " << ithread << "Vector size " << posa[ithread].size() << " Number Lines" << independentCount << endl;
	
        //#pragma omp for     
        for(int i=1; i<independentCount ;i++) {    
		//cout << "Thread " << ithread << "Start " << posa[ithread][i] << "end " << posa[ithread][i-1] << endl;

            const int len = posa[ithread][i] - posa[ithread][i-1];
            char* buff = &buffer[posa[ithread][i-1]];
            string contig = segment_read(buff,len,i);
            
		#pragma omp atomic
		countReads[contig] = countReads[contig] + 1;
	
                #pragma omp atomic
                count_of_reads++;
                //printf("\n Total No. of reads: %d \n",count_of_reads);
            //if(count_of_reads % 100000 == 0){
		//cout << count_of_reads << endl;
	    //}

        }
    }

	//cout << "Total Number Lines " << count_of_reads << endl;
    delete[] posa;
	return countReads;
}

int main () {
  FILE * pFile;
  long lSize;
  char * buffer;
  size_t result;


	int numRepeats = 74504;
	string nameRepeats[numRepeats] = {};
	int lengthRepeats[numRepeats] = {};
	struct returnPointers p = readInRepeats(nameRepeats, lengthRepeats);
	cout << "after function" << endl;
	string * x = p.nameRepeats;
	int * y = p.lengthRepeats;
	cout << x[1] << endl;
	cout << y[1] << endl;


	std::map<string, int> hashmap;
	for(int i = 0; i < numRepeats; i++){
		hashmap[x[i]] = 0;
	}

  pFile = fopen ( "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/PurgeHaplotigs/MapIlluminaToCanu/BWAPE1_Correct.sam" , "rb" );
  if (pFile==NULL) {fputs ("File error",stderr); exit (1);}


for(int s = 0; s < 850; s++){

cout << s << endl;
//cout << "before file open" << endl;

	//TestSam.sam
  //pFile = fopen ( "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/PurgeHaplotigs/MapIlluminaToCanu/BWAPE1_Correct.sam" , "rb" );
  //if (pFile==NULL) {fputs ("File error",stderr); exit (1);}

//cout << "after opening file" << endl;

  // obtain file size:
  //fseek (pFile , 0 , SEEK_END);
  //lSize = ftell (pFile);
  //rewind (pFile);

	lSize = 1000000000;

//cout << lSize << endl;
//cout << "before allocate memory" << endl;

  // allocate memory to contain the whole file:
  buffer = (char*) malloc (sizeof(char)*lSize);
  if (buffer == NULL) {fputs ("Memory error",stderr); exit (2);}

//cout << "before copy" << endl;

  // copy the file into the buffer:
  result = fread (buffer, 1,lSize, pFile);
  if (result != lSize) {fputs ("Reading error",stderr); exit (3);}

//cout << "before foo" << endl;
  /* the whole file is now loaded in the memory buffer. */
	//int readsPerContig[numRepeats] = {};
  std::map<string, int>  countReads = foo(buffer, result, x, hashmap);
  // terminate

        cout << hashmap[x[0]] << endl;
        cout << hashmap[x[1]] << endl;
        cout << hashmap[x[2]] << endl;

  //fclose (pFile);
  free (buffer);

}

fclose(pFile);

cout << "after foo" << endl;

	//cout << countReads[x[0]] << endl;
	//cout << countReads[x[1]] << endl;
	//cout << countReads[x[2]] << endl;

	//for(int i = 0; i < numRepeats; i++){
	//	cout << x[i] << " " << countReads[i] << endl;
	//}

  ofstream myfile;
  myfile.open ("ReadsMappedToContigs.txt");
	for(int i = 0; i < numRepeats; i++){
  		myfile << x[i] << " " << hashmap[x[i]]  << "\n";
	}  
myfile.close();

  return 0;
}
