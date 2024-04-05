
//Try to ge coverage level for repeat canu contigs

// Location of Contig Repeat Names: /pool2/PseudacrisFeriarumGenomeAssemblyKevin/ChorusFrog_Canu_CLR_2/Canu_Filtered_Repeats_Headers.txt
// Location BWA Illumnia Reads Mapped to Canu Contigs: /pool2/PseudacrisFeriarumGenomeAssemblyKevin/PurgeHaplotigs/MapIlluminaToCanu/BWAPE1_Correct.sam

#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>

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


int * countReadsPerContig(string * nameRepeats, int * countReads){
	string line;
	ifstream myfile("/pool2/PseudacrisFeriarumGenomeAssemblyKevin/PurgeHaplotigs/MapIlluminaToCanu/BWAPE1_Correct.sam");
	//ifstream myfile("test");
	if(myfile.is_open()){
		int lineNum = 0;
		while(getline(myfile, line)){
			string temp;
			int countSpace = 0;
			//cout << line;
			for(int i = 0; i < line.length(); i++){
				char c = line[i];
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
			for(int i = 0; i < 74504; i++){
				if(nameRepeats[i] == temp){
					countReads[i] = countReads[i] + 1;
					//cout << i << endl;
					break;
				}
			}
			lineNum++;
			//if(lineNum > 100000){
			//	break;
			//}

		}
	myfile.close();
	}else{
		cout << "Unable to open file";
	}

	return countReads;


}



int main(){
	int numRepeats = 74504;
	string nameRepeats[numRepeats] = {};
	int lengthRepeats[numRepeats] = {};
	struct returnPointers p = readInRepeats(nameRepeats, lengthRepeats);
	cout << "after function" << endl;
	string * x = p.nameRepeats;
	int * y = p.lengthRepeats;
	cout << x[1] << endl;
	cout << y[1] << endl;

	cout << "Count Reads" << endl;
	int readsPerContig[numRepeats] = {};
	int *z = countReadsPerContig(x, readsPerContig);

	cout << z[0] << endl;
	float coveragePerContig[numRepeats] = {};


	for(int i = 0; i < numRepeats; i++){
		coveragePerContig[i] = static_cast<float>(z[i])/ static_cast<float>(y[i]);
		cout << x[i] << " " << z[i] << " " << y[i] << " " << coveragePerContig[i] << endl;
	}




	return 0;
}


