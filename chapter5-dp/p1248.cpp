#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
const int N=1010;
int n;

struct node{
    int time1,time2,idx;
};
node m[N];

bool cmp1(node a,node b){
    return a.time1<=b.time1;
}
bool cmp2(node a,node b){
    return a.time2>=b.time2;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    //初始化数据
    cin>>n;
    for(int i=1;i<=n;i++){
        cin>>m[i].time1;
        m[i].idx=i;
    }
    for(int i=1;i<=n;i++){
        cin>>m[i].time2;
    }

    vector<node> n1,n2;
    for(int i=1;i<=n;i++){
        if(m[i].time1<m[i].time2) 
            n1.push_back(m[i]);
        else n2.push_back(m[i]);
    }
    
    sort(n1.begin(),n1.end(),cmp1);
    sort(n2.begin(),n2.end(),cmp2);

    vector<node> ans;
    for(auto it:n1) ans.push_back(it);
    for(auto it:n2) ans.push_back(it);
    
    int t1=0,t2=0;
    for(auto it:ans){
        t1+=it.time1;
        t2=max(t1,t2)+it.time2;
    }

    cout<<t2<<endl;
    for(auto it:ans) cout<<it.idx<<" ";
    return 0;
}

//这个题目是洛谷上老师讲的题目，我知道该怎么写，不过原理还是不太懂。书上把这道题划为动态规划，我感觉挺像贪心的