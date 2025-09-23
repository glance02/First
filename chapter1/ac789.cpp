#include<iostream>
using namespace std;
const int N=1e5+10;
int n,k,q[N];

void bsearch(int a,int b,int x){
    //找左边的x
    int l=a,r=b;
    while(l<r){
        int mid=l+r>>1;
        if(q[mid]>=x) r=mid;
        else l=mid+1;//这边必须要有，不然无法跳出循环，因为循环条件是l<r，所以每次两者之间的距离要缩短一点
    }

    if(q[l]!=x){
        cout<<-1<<" "<<-1<<endl;
        return;
    }else{
        cout<<l<<" ";
        //找右边的x
        l=a,r=b;
        while(l<r){
            int mid=(l+r+1)>>1;
            if(q[mid]<=x) l=mid;
            else r=mid-1;
        }
        cout<<l<<endl;
    }
}
int main(){
    cin>>n>>k;
    for(int i=0;i<n;i++) cin>>q[i];

    while(k--){
        int x;cin>>x;
        bsearch(0,n-1,x);
    }
    return 0;
}