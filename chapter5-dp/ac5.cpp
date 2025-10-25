#include<iostream>
using namespace std;
const int N=12000,M=2010;
int n,m;//n表示数量，m表示容积，这题容积并不变
int v[N],w[N];
int f[M];//如果不优化空间的话，就会超时

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n>>m;
    int cnt=0;
    for(int i=1;i<=n;i++){
        int a,b,s;
        cin>>a>>b>>s;
        //把s个物品拆成多个物品,每个物品的编号是当前的cnt值
        int k=1;
        while(k<=s){
            cnt++;
            v[cnt]=k*a;
            w[cnt]=k*b;
            s-=k;
            k*=2;
        }
        if(s>0){
            cnt++;
            v[cnt]=s*a;
            w[cnt]=s*b;
        }

    }
    //重新分配完之后再对n值进行修正
    n=cnt;//1000*11=11000
    for(int i=1;i<=n;i++){
        for(int j=m;j>=v[i];j--){//倒着来算
            f[j]=max(f[j],f[j-v[i]]+w[i]);
        }
    }
    cout<<f[m]<<endl;
    return 0;
}