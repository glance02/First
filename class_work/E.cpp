#include<iostream>
#include<algorithm>
using namespace std;
const int N=1e6+10;
int n,k;
int num[N];

void quick_sort(int l,int r){
    //递归函数首先考虑的都是退出条件
    if(l>=r) return;

    //定义需要的变量
    int i=l-1,j=r+1,x=num[l+r>>1];
    while(i<j){
        //左边的都小于x，右边的都大于x
        while(num[i]<x) ++i;
        while(num[j]>x) ++j;
        if(i<j) swap(num[i],num[j]);
    }
    //递归再找一遍
    quick_sort(l,j);
    quick_sort(j+1,r);
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n>>k;
    for(int i=1;i<=n;i++) cin>>num[i];
    sort(num+1,num+1+n);
    // quick_sort(1,n);
    cout<<num[k];
    return 0;
}