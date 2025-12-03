#include<iostream>
using namespace std;
const int N=510;
int n;
int p[N];
int m[N][N],s[N][N];

void MChain(int p[],int n,int m[][N],int s[][N]){
    for(int i=1;i<=n;i++){
        m[i][i]=0;
        s[i][i]=0;
    }
    for(int len=2;len<=n;len++){
        for(int i=1;i<=n-len+1;i++){
            int j=i+len-1;
            m[i][j]=m[i][i]+m[i+1][j]+p[i-1]*p[i]*p[j];
            s[i][j]=i;

            for(int k=i+1;k<j;k++){
                int t=m[i][k]+m[k+1][j]+p[i-1]*p[k]*p[j];
                if(t<m[i][j]){
                    m[i][j]=t;
                    s[i][j]=k;
                }
            }
        }
    }   
}

void printAns(int i, int j){
    if (i == j){
        cout << "A[" << i << "]";
    }else{
        cout << "(";
        printAns(i, s[i][j]);
        printAns(s[i][j] + 1, j);
        cout << ")";
    }
}

int main(){
    cin>>n;
    for(int i=0;i<=n;i++) cin>>p[i];
    MChain(p,n,m,s);
    cout<<m[1][n]<<endl;
    printAns(1,n);
    return 0;
}