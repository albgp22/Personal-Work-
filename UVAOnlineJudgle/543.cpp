#include <iostream>
using namespace std;


void criba(bool* m, int tam){
    m[0] = false;
    m[1] = false;
    for(int i = 2; i <= tam; ++i) 
        m[i] = true;

    for(int i = 2; i*i <= tam; ++i) {
        if(m[i]) {
            for(int h = 2; i*h <= tam; ++h)
                m[i*h] = false;
        }
    }
}

int main(){
    int size=1000000;
    bool* cr = new bool[size];
    criba(cr, size);

    int n;
    cin >> n;
    while(n!=0){
        for (int i=0; i<size; i++){
            if (cr[i] && cr[n-i]){
                cout << n << " = " << i << " + " << n-i << endl;
                break;
            }
        }
        cin>>n;
    }
}