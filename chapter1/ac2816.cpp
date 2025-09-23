#include<iostream>
using namespace std;
const int N=1e5+10;
int a[N],b[N];
int n,m;

int main(){
    cin>>n>>m;
    for(int i=0;i<n;i++) cin>>a[i];
    for(int i=0;i<m;i++) cin>>b[i];
    
    //i指向a数组，j指向b数组
    int i=0;
    for(int j=0;j<m;j++){
        if(a[i]==b[j]&&i<n) i++;
    }
    if(i==n) cout<<"Yes";
    else cout<<"No";
    return 0;
}