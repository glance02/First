#include<iostream>
using namespace std;
const int N=1e5+10;
int n,m;
int h[N],cnt;

void down(int x){
    //t用来存x的左右两个儿子中最小的数的下标
    int t=x;

    if(x*2<=cnt&&h[x*2]<h[t]) t=x*2;
    if(x*2+1<=cnt&&h[x*2+1]<h[t]) t=x*2+1;

    if(t!=x){
        //如果下标改变了，说明要更换两个数的位置
        swap(h[x],h[t]);
        //此时x已经换到t处，然后要对t再进行递归更换
        down(t);
    }
}

void up(int x){
    while(x/2>0&&h[x/2]>h[x]){
        swap(h[x/2],h[x]);
        x/=2;
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n>>m;
    for(int i=1;i<=n;i++) cin>>h[i];
    cnt=n;

    //初始化堆，最下面那一层其实已经可以看成是一个合理的小根堆了
    for(int i=n/2;i;i--){
        down(i);
    }

    while(m--){
        cout<<h[1]<<" ";
        //pop
        h[1]=h[cnt--];
        down(1);
    }
    return 0;
}