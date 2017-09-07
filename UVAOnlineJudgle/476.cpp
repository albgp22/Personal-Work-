#include <iostream>
#include <stdlib.h>
#include <list>
using namespace std;

typedef struct Rectanglee{
	double* a;
	double* b;
	double* c;
	double* d;
} Rectangle;

typedef Rectangle* Rpt;

Rpt createRectangle(double px, double py, double qx, double qy){
	Rpt R = (Rpt) malloc(sizeof(Rectangle));
	R->a=new double[2];
	R->b=new double[2];
	R->c=new double[2];
	R->d=new double[2];
	R->a[0]=px; R->a[1]=py;
	R->c[0]=qx; R->c[1]=qy;

	R->d[0]=px;
	R->d[1]=qy;
	R->b[0]=qx;
	R->b[1]=py;

	return R;
}

double scalar(double x1, double y1, double x2, double y2){
	return x1*x2+y1*y2;
}

bool inside(double x, double y, Rpt R){
	double* AM = new double[2];
	double* AD = new double[2];
	double* AB = new double[2];

	AM[0]=x-R->a[0];
	AM[1]=y-R->a[1];

	AD[0]=R->d[0]-R->a[0];
	AD[1]=R->d[0]-R->a[1];

	AB[0]=R->b[0]-R->a[0];
	AB[1]=R->b[0]-R->a[1];

	double AMAB=scalar(AM[0], AM[1], AB[0], AB[1]);
	double AMAD=scalar(AM[0], AM[1], AD[0], AD[1]);
	double ABAB=scalar(AB[0], AB[1], AB[0], AB[1]);
	double ADAD=scalar(AD[0], AD[1], AD[0], AD[1]);

	delete AM; delete AD; delete AB;

	bool ret = (0 < AMAB && AMAB < ABAB && 0 < AMAD && AMAD < ADAD );
	return ret;

}

void freeRectangles(list<Rpt> rectangles){
	for (list<Rpt>::iterator it=rectangles.begin(); it != rectangles.end(); ++it){
		Rpt R=*it;
		delete R->a;
		delete R->b;
		delete R->c;
		delete R->d;
		free(R);
	}
}



int main(){
	list<Rpt> rectangles;
	char a;
	cin >> a;
	while(a=='r'){
		double px, py, qx, qy;
		cin >> px >> py >> qx >> qy;
		rectangles.insert(rectangles.end(), createRectangle(px, py, qx, qy));
		cin >> a;
	}
	double x,y;
	cin >> x >> y ;
	int point=1;
	while (x!=9999.9 || y!=9999.9){
		int counter=1;
		bool contained=false;
		for (list<Rpt>::iterator it=rectangles.begin(); it != rectangles.end(); ++it){
			if (inside(x,y,*it)){
				cout << "Point " << point << " is contained in figure " << counter << endl;
				contained = true;
			}
			counter++;
		}
		if (!contained) cout << "Point " << point << " is not contained in any figure" << endl;
		point++;
		cin >> x >> y;
	}
	freeRectangles(rectangles);
	return 0;
}
