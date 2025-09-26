#include<iostream>
using namespace std;
const int N=1e5+10;
string str;
int son[N][26],cnt[N],idx;

void insert(){
    int p=0;//从根节点开始
    for(char s:str){
        int u=s-'a';//得到对应字母的数值
        if(!son[p][u]) son[p][u]=++idx;
        p=son[p][u];//去到下一个结点，没有就创建这个结点
    }
    cnt[p]++;//表示以第p个结点结束的字符串加一个
}

int query(){
    int p=0;
    for(auto s:str){
        int u=s-'a';
        if(!son[p][u]) return 0;
        p=son[p][u];
    }
    return cnt[p];
}

int main(){
    int n;cin>>n;
    while(n--){
        char q;cin>>q;
        if(q=='I'){
            cin>>str;
            insert();
        }
        if(q=='Q'){
            cin>>str;
            cout<<query()<<endl;
        }
    }
    return 0;
}