#include<iostream>
#include<cstring>
using namespace std;
const int N=2e3+10;
char a[N],b[N];
int f[N][N];

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    
    cin>>a+1>>b+1;
    int la=strlen(a+1),lb=strlen(b+1);

    for(int i=1;i<=la;i++){
        for(int j=1;j<=lb;j++){
            f[i][j]=max(f[i-1][j],f[i][j-1]);
            if(a[i]==b[j]) f[i][j]=max(f[i][j],f[i-1][j-1]+1);
        }
    }

    cout<<f[la][lb];
    return 0;
}