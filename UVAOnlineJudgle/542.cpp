//UVA Online Judge. Problem 542

#include <iostream> 
#include <stdlib.h>
#include <iomanip>
using namespace std;

bool isRival(int i, int j,int phase){
	if (phase==2){
		if (abs(i/2-j/2)==1 && i/4==j/4){
			return true;
		}
	}
	else if (phase==3){
		if (abs(i/4-j/4)==1 && i/8==j/8){
			return true;
		}
	}
	else if (phase==4){
		if (abs(i/8-j/8)==1){
			return true;
		}
	}
	return false;
}

int main(void){
	char** names = new char*[16];

	int** probabilities = new int*[16];
	for (int i=0; i<16; i++) probabilities[i]=new int[16]; //Create a matrix of probabilities

	for (int i=0; i<16; i++){
		names[i]=new char[32];
		cin >> names[i];
	}

	for (int i=0; i<16; i++) for (int j=0; j<16; j++) cin >> probabilities[i][j];

	double* _1step=new double[16];
	double* _2step=new double[16];
	double* _3step=new double[16];
	double* _4step=new double[16];

	for(int i=0; i<16; i=i+2){
		_1step[i]=probabilities[i][i+1]/100.;
		_1step[i+1]=1-_1step[i];
	}

	for (int i=0; i<16; i++){
		double sum=0;
		for (int j=0; j<16; j++){
			if (isRival(i,j,2)){
				sum+=probabilities[i][j]*_1step[j]/100.;
			}
		}
		_2step[i]=_1step[i]*sum;
	}

	for (int i=0; i<16; i++){
		double sum=0;
		for (int j=0; j<16; j++){
			if (isRival(i,j,3)){
				sum+=probabilities[i][j]*_2step[j]/100.;
			}
		}
		_3step[i]=_2step[i]*sum;
	}

	for (int i=0; i<16; i++){
		double sum=0;
		for (int j=0; j<16; j++){
			if (isRival(i,j,4)){
				sum+=probabilities[i][j]*_3step[j]/100.;
			}
		}
		_4step[i]=_3step[i]*sum;
	}

	for (int i=0; i<16; i++){
		cout << setw(11) << left << names[i] << fixed << setprecision( 2 ) << "p=" << _4step[i]*100 <<  "\%" << endl;
	}






	return 0;


}
