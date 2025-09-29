#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

//除法多一个余数r，r可以使用引用，这样可以直接对本体的r进行修改
vector<int> div(vector<int> &A,int b,int &r){
    vector<int>C;
    r=0;//最开始余数为0

    //除法一般从高位算起
    for(int i=A.size()-1;i>=0;i--){
        r=r*10+A[i];
        C.push_back(r%b);//上位
        r%=b;//相减得到下一次的余数
    }

    //此时的C是高位在前，需要反转
    reverse(C.begin(),C.end());

    //去除前导零
    while(C.size()>1&&C.back()==0) C.pop_back();

    return C;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    vector<int>A;
    string a;int b,r;
    cin>>a>>b;

    for(int i=a.size()-1;i>=0;i--) A.push_back(a[i]-'0');

    vector<int>C=div(A,b,r);

    for(int i=C.size()-1;i>=0;i--) cout<<C[i];
    
    return 0;
}