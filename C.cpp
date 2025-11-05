#include<iostream>
#include<cstring>
#include<map>
using namespace std;
typedef pair<int,int>Dem;
const int N=105;
int f[N][N];//存储Ai-Aj所需的最小连乘次数
Dem dem[200];
char cal[N];
int n,m;
map<char,int>m;

bool checkyn(){
    for(int i=1;i<strlen(cal+1);i++){
        if(dem[cal[i]-64].second!=dem[cal[i+1]-64].first)
            return false;
    }   
    return true;
}

int f(){
    for(int i=1;i<=n;i++){

    }
    return 0;
}
int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n>>m;
    for(int i=1;i<=n;i++){
        char c;cin>>c;
        cin>>dem[c-64].first>>dem[c-64].second;
    }
    // for(int i=1;i<=n;i++) cout<<dem[i].first<<" "<<dem[i].second<<endl;
    while(m--){
        cin>>cal+1;
        //判断能不能乘，复杂度为O(m)
        if(!checkyn){
            cout<<"MengMengDa"<<endl;
            continue;
        }
        //计算最小连乘次数
        cout<<f()<<endl;
    }
    return 0;
}