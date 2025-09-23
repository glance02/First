#include<iostream>
using namespace std;
const int N=1e5+10;
int a[N],s[N];
int n,ans;

int main(){
    cin>>n;
    for(int i=0;i<n;i++) cin>>a[i];

    for(int i=0,j=0;i<n;i++){
        s[a[i]]++;//记录已经有一个a[i]
        //1 2 2 3 4
        //查看[i,j]这个窗口内的数据是否合理，不合理就向右移动j，缩小窗口
        while(s[a[i]]>1&&j<i) s[a[j++]]--;
        ans=max(ans,i-j+1);
    }

    cout<<ans;

    return 0;
}