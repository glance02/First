#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
vector<int>alls;//存储所有离散化的值，类似于一个映射表，把所有需要的值存进数组当中


//利用二分查找，在离散数组当中查找对应的下标
int find(int x){
    int l=0,r=alls.size()-1;//左右两边正好是两个端点
    while(l<r){
        int mid=l+r>>1;
        if(alls[mid]>=x) r=mid;//这里为什么又是等于
        else l=mid+1;
    }

    return l+1;//返回从1开始的下标。
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    string s1="admin";
    string s2;cin>>s2;
    if(s1==s2) cout<<"yes";
    return 0;
}