#include<iostream>
using namespace std;
const int N=1e5+10;

int n,m;
int p[N];//存储父节点

int find(int x){//查找所在集合的编号，这个编号存在根节点处
    if(p[x]!=x) p[x]=find(p[x]);
    // while(p[x]!=x) x=p[x]; //如果没有优化，就是这样子，会超时
    return p[x];
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n>>m;

    //最开始每个点的父节点都是自己，即各自一个集合里面
    for(int i=0;i<n;i++) p[i]=i;

    while(m--){
        string op;cin>>op;
        int a,b;
        cin>>a>>b;
        if(op=="M") p[find(a)]=find(b);
        else{
            if(find(a)==find(b)) cout<<"Yes"<<endl;
            else cout<<"No"<<endl;
        }
    }
    return 0;
}