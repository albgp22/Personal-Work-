#include <iostream>
#include <math.h>
#include <iomanip>


double round3(double val){
	return roundf(val * 1000) / 1000;
}

int main(){
	double mu=0.02169426125474089; //integrate from 0 to 1/2 of 1-sqrt(1-u^2)
	double PI=3.141592653589793;
	double a;
	while(std::cin>>a){
		double T=a*a*mu; //half of curved triangle between the wall and the figure
		double C=8*T; //Area of all enclosed areas
		double A=4*(a*a*((4-PI)/4)-4*T); //Area of pointed curved triangles
		double B=a*a-A-C; //Remaining area (stripped area)
		//A=round3(A);
		//B=round3(B);
		//C=round3(C);
		std::cout << std::fixed << std::setprecision(3) << B << " " << A << " " << C << std::endl;
	}
}