#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
int n;
typedef pair<int,int>PII;
vector<PII> segs;//存放所有的区间

void merge(){//进行合并算法
    vector<PII> tmp;
    sort(segs.begin(),segs.end());//先排序

    int st=-2e9,end=-2e9;
    for(auto seg:segs){
        if(end<seg.first){
            if(st!=-2e9) tmp.push_back({st,end});
            st=seg.first;end=seg.second;
        }else{
            end=max(end,seg.second);
        }
    }

    //如果输入的都是一个区间，那st则不会改变值，也就是说不会有区间进入tmp数组，在这边需要将这个区间加入tmp
    if(st!=-2e9) tmp.push_back({st,end});

    segs=tmp;
}

int main(){
    cin>>n;
    for(int i=0;i<n;i++){
        int l,r;
        cin>>l>>r;
        segs.push_back({l,r});
    }

    merge();

    cout<<segs.size();
    return 0;
}