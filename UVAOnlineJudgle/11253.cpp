#include <iostream>
using namespace std;


int main(){
	int a;
	while (true){
		cin >> a;
		if (a==-1) break;
		int x, y;
		x=0; y=0;
		int face = 1; //1 east, 2 north, 3 west, 4 south
		for (unsigned int n=0; n<a; n++){
			bool turn = (((n & -n) << 1 ) & n) !=0; //true left, false right 
			if (turn){
				switch (face){
					case 1:
						y++;
						face++;
						break;
					case 2:
						x--;
						face++;
						break;
					case 3:
						y--;
						face++;
						break;
					case 4:
						x++;
						face=1;
						break;
				}
			}
			else{
				switch(face){
					case 1:
						y--;
						face=4;
						break;
					case 2:
						x++;
						face--;
						break;
					case 3:
						y++;
						face--;
						break;
					case 4:
						x--;
						face--;
						break;
				}
			}

		}
		cout << -y << " " << -x << endl;
	}
	return 0;
}