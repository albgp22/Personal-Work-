#include <iostream>
#include <stdlib.h>
#include <list>
using namespace std;

typedef struct tree_node{
	int val;
	bool extreme;
	int where1, where2;
	list<tree_node*> *descendants;
} Node;

typedef tree_node* Tree;

int value(int** b){
	int win1=0;
	int win0=0;
	for (int i=0; i<3; i++){
		if (b[i][0]==b[i][1] && b[i][2]==b[i][1]){
			if (b[i][0]==1) win1++;
			else win0++;
		}
		if (b[0][i]==b[1][i] && b[2][i]==b[1][i]){
			if (b[0][i]==1) win1++;
			else win0++;
		}
	}
	if (b[0][0]==b[1][1] && b[1][1]==b[2][2]){
		if (b[0][0]==1) win1++;
		else win0++;	
	}
	if (b[0][2]==b[1][1] && b[1][1]==b[2][0]){
		if (b[1][1]==1) win1++;
		else win0++;	
	}
	if (win1>0 && win0>0) return 0;
	else if (win1>0) return -10;
	else if (win0>0) return 10;
	return 0;
}

tree_node* generateTree(int** board, int visited){	
	Tree T = (Tree) malloc(sizeof(Node));

	//T->descendants.insert(T->descendants.end(), (tree_node*)NULL);
	T->extreme=false;
	T->descendants = new list<tree_node*>[1];
	if (visited==9){
		T->extreme=true;
		T->val=value(board);
		return T;
	}
	int min=1000000;
	int max=-1000000;
	for (int i=0; i<3; i++){
		for (int j=0; j<3; j++){
			if (board[i][j]==-1){
				board[i][j]=1;
				tree_node* AuxT1=generateTree(board, visited+1);
				min= (min < AuxT1->val ? min : AuxT1->val);
				if (max<AuxT1->val){
					max=AuxT1->val;
					T->where1=i;
					T->where2=j;
				}
				T->descendants[0].push_back(AuxT1);
				board[i][j]=0;
				tree_node* AuxT2=generateTree(board, visited+1);
				min= (min < AuxT2->val ? min : AuxT2->val);
				if (max<AuxT2->val){
					max=AuxT2->val;
					T->where1=i;
					T->where2=j;
				}
					T->descendants[0].push_back(AuxT2);
				
				board[i][j]=-1;
			}
		}
	}
	if (visited%2==1) T->val=max;
	else T->val=min;
	return T;


}

void freeTree(Tree T){
	NULL;
}



int main(){
	//Let's create the game board
	int** board = new int*[3];
	for (int i=0; i<3; i++) board[i]=new int[3];

	for (int i=0; i<3; i++){
		for (int j=0; j<3; j++){
			board[i][j]=-1;
		}
	}

	int a,b;
	bool finished=false;
	int visited=0;
	while (visited<9){
		cin >> a >> b;
		if (board[a][b]==-1) board[a][b]=1;
		else {
			cout << "This cell is not unused";
			continue;
		}
		visited+=1;
		tree_node* T=generateTree(board, visited);
		int next1; int next2;
		next1=T->where1;
		next2=T->where2;
		board[next1][next2]=0;
		cout << next1 << " " << next2 << endl;

		freeTree(T);
		visited+=1;

	}



	//Free the board
	for(int i=0; i<3; i++) delete board[i];
	delete board;

}
