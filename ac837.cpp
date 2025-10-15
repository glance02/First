#include<iostream>
using namespace std;
const int N=1e5+10;
int n,m;
int p[N],cnt[N];//cnt存储根节点所在的这个集合的数量

//找到x的根节点，并且优化路径
int find(int x){
    if(p[x]!=x) p[x]=find(p[x]);
    return p[x];
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    int n,m;cin>>n>>m;

    for(int i=1;i<=n;i++){
        p[i]=i;
        cnt[i]=1;
    }

    while(m--){
        string str;cin>>str;

        if(str=="C"){
            //合并ab两个集合
            int a,b;
            cin>>a>>b;
            //如果a和b在同一个集合，就没必要合并了
            if(find(a)==find(b)) continue;

            cnt[find(b)]+=cnt[find(a)];
            p[find(a)]=find(b);
        }else if(str=="Q1"){
            int a,b;cin>>a>>b;
            if(find(a)==find(b)) cout<<"Yes"<<endl;
            else cout<<"No"<<endl;
        }else{
            int a;cin>>a;
            cout<<cnt[find(a)]<<endl;
        }
    }

    return 0;
}