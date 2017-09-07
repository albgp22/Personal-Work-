#include <iostream>
#include <list>

using namespace std;


int main(){

	long powers[30]={3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535, 131071, 262143, 524287, 1048575, 2097151, 4194303, 8388607, 16777215, 33554431, 67108863, 134217727, 268435455, 536870911, 1073741823, 2147483647};

	string line;
	while(true){
		getline(cin, line);
		if (line=="0") break;
		long sum=0;
		for (int i=line.length()-1; i>=0; i--){
			int j=line.length()-i-2;
			if(j==-1){
				sum+=((int)(line[i]-'0'));
			}
			else if (j>=0){
				sum+=((int)(line[i]-'0'))*powers[j];
			}
		}
		cout << sum << endl;
	}
	return 0;

}