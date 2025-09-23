#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
const int N=3e5+10;
int n,m,a[N],s[N];
typedef pair<int,int>PII;
vector<int>alls;//映射数组
vector<PII>add,query;

//查找在映射的数组中这个数的坐标
int find(int x){
    int l=0,r=alls.size()-1;
    while(l<r){
        int mid=l+r>>1;
        if(alls[mid]>=x) r=mid;
        else l=mid+1;
    }
    return l+1;
}

int main(){
    cin>>n>>m;
    for(int i=0;i<n;i++){
        int x,c;cin>>x>>c;
        add.push_back({x,c});//相加的数据

        alls.push_back(x);//把需要寻找的数放进映射数组中
    }
    for(int i=0;i<m;i++){
        int l,r;cin>>l>>r;
        query.push_back({l,r});
        
        alls.push_back(l);
        alls.push_back(r);
    }

    //去重
    //先排序再去重
    sort(alls.begin(),alls.end());
    alls.erase(unique(alls.begin(),alls.end()),alls.end());

    //处理插入相加
    for(auto item:add){
        int x=find(item.first);
        a[x]+=item.second;
    }

    //前缀和
    for(int i=1;i<=alls.size();i++) s[i]=s[i-1]+a[i];

    //处理查询
    for(auto item:query){
        int l=find(item.first),r=find(item.second);
        int ans=s[r]-s[l-1];
        cout<<ans<<endl;
    }

    return 0;
}