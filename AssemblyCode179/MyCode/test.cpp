#include <string>
#include <stdio.h>
#include <iostream>

using namespace::std;

int main(){

string myArray[5] = {};

myArray[0] = "apple";

string *pointerArray[5] = {};


string y = "pine";
string z = "two";

pointerArray[0] = &y;
pointerArray[4] = &z;

for(int i = 0; i < 5; i++){
	if(pointerArray[i] != NULL){
		cout << *pointerArray[i];
	}
}

//cout << *pointerArray[0];

return 0;
}
