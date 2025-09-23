#include<iostream>
using namespace std;
const int N=1e6+10;
int a[N],q[N];

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    int n,k;cin>>n>>k;
    for(int i=0;i<n;i++) cin>>a[i];

    int hh=0,tt=-1;
    for(int i=0;i<n;i++){
        //判断队头是否已经滑出窗口
        if(hh<=tt&&q[hh]<i-k+1) hh++;
        //维护单调队列
        while(hh<=tt&&a[q[tt]]>=a[i]) tt--;

        q[++tt]=i;//淡掉队列中存放的是下标，而不是数
        if(i-k+1>=0) cout<<a[q[hh]]<<" ";
    }
    cout<<endl;

    hh=0,tt=-1;
    for(int i=0;i<n;i++){
        //判断队头是否已经滑出窗口
        if(hh<=tt&&q[hh]<i-k+1) hh++;
        //维护单调队列
        while(hh<=tt&&a[q[tt]]<=a[i]) tt--;

        q[++tt]=i;//淡掉队列中存放的是下标，而不是数
        if(i-k+1>=0) cout<<a[q[hh]]<<" ";
    }
    return 0;
}