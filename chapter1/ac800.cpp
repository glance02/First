#include<iostream>
using namespace std;
const int N=1e5+10;
int a[N],b[N];
int n,m,x,ansx,ansy;

int main(){
    cin>>n>>m>>x;
    for(int i=0;i<n;i++) cin>>a[i];
    for(int i=0;i<m;i++) cin>>b[i];

    for(int i=0,j=m-1;i<n;i++){
        while(a[i]+b[j]>x&&j>=0) j--;
        //题目有唯一解，找到答案直接输出并推出程序
        if(a[i]+b[j]==x){
            ansx=i;
            ansy=j;
            cout<<ansx<<" "<<ansy;
            return 0;
        }
    }
    return 0;
}