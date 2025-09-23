#include<iostream>
using namespace std;
const int N=1e5+10;
int e[N],l[N],r[N],idx;

void init(){
    //0表示左端点，1表示右端点
    r[0]=1,l[1]=0;
    idx=2;
}

//在下标是k的右边插入一个值为x的点
void insert(int k,int x){
    e[idx]=x;
    r[idx]=r[k],l[idx]=k;
    l[r[k]]=idx,r[k]=idx++;
}

//删除第k个点
void remove(int k){
    r[l[k]]=r[k];
    l[r[k]]=l[k];
}

int main(){
    ios::sync_with_stdio(false);
    int n;cin>>n;

    init();
    while(n--){
        string str;
        cin>>str;
        int k,x;
        if(str=="L"){
            cin>>x;
            insert(0,x);
        }else if(str=="R"){
            cin>>x;
            insert(l[1],x);
        }else if(str=="D"){
            cin>>k;
            remove(k+1);//k=idx-1+2,因为idx是从2开始的
        }else if(str=="IL"){
            cin>>k>>x;
            insert(l[k+1],x);
        }else{
            cin>>k>>x;
            insert(k+1,x);
        }
    }

    for(int i=r[0];i!=1;i=r[i]) cout<<e[i]<<" ";
    return 0;
}