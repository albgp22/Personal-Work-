//UVA Online Judge. Problem 544

#include <string.h>
#include <iostream>
#include <limits.h>
#define INF INT_MAX
using namespace std;

int max(int i, int j){
	return (i>j ? i : j);
}

int min(int i, int j){
	return (i<j ? i : j);
}

int index(char** array, int length, char* str){
	for (int i=0; i<length; i++){
		if (strlen(array[i]) == 0) return -1;
		if (strcmp(array[i], str)==0){ 
			return i;
		}
	}
	return -1;

}

void bfs(int initial, int dst, bool* seen, int** loads, int minimum, int* maximumMinimum, int n){
	if (initial==dst) maximumMinimum[0]=max(maximumMinimum[0], minimum);

	else{
		for(int i=0; i<n; i++){
			if (loads[initial][i]!=-1 && !seen[i]){
				seen[i]=true;
				bfs(i, dst, seen, loads, min(minimum, loads[initial][i]), maximumMinimum,n);
				seen[i]=false;
			}
		}
	}
	seen[initial]=true;
}

int findMaxLoad(int** loads, int src, int dst, int n){
	bool* seen = new bool[n]();
	seen[src]=true;
	int* max= new int[1];
	bfs(src, dst, seen, loads, INF, max, n);
	delete seen;
	return max[0];
}

int main(void){
	/* Reading the graph */

	int n, r;
	cin >> n >> r;
	int counter=0;

	while(n!=0 && r!=0){
		counter++;

		int cities=0;

		char** names = new char*[n];
		for (int i=0; i<n; i++) names[i]=new char[32]();

		int** loads = new int*[n];
		for (int i=0; i<n; i++){
			loads[i]=new int[n];
			for (int j=0; j<n; j++) loads[i][j]=-1;
		}

		for (int i=0; i<r; i++){
			char* str1 = new char[32]();
			char* str2 = new char[32]();
			int dist;

			cin >> str1 >> str2 >> dist;

			int city1, city2;
			city1=index(names, n, str1);
			city2=index(names, n, str2);

			if (city1==-1){
				names[cities]= str1;
				city1=cities;
				cities++;
			}
			if (city2==-1){
				names[cities]= str2;
				city2=cities;
				cities++;
			}

			loads[city1][city2]=dist;
			loads[city2][city1]=dist;
		}

		char* srcstr = new char[32];
		char* dststr = new char[32];
		int src, dst;

		cin >> srcstr >> dststr;
		src=index(names, n, srcstr);
		dst=index(names, n, dststr);


		cout << findMaxLoad(loads, src, dst,n) << endl;


		for (int i=0; i<n; i++){
			delete names[i];
			delete loads[i];
		}
		delete names; delete loads;

		cin >> n >> r;

	}
}
