#include<iostream>
#include<iomanip>
using namespace std;
double n;
const double eps=1e-8;//6位小数+2

int main(){
    cin>>n;
    if(n<0){
        cout<<'-';
        n=-n;
    }
    double l=0,r=1e4+10;
    while(r-l>eps){
        double mid=(l+r)/2;
        if(mid*mid*mid>=n) r=mid;
        else l=mid;
    }
    cout<<setprecision(6)<<fixed<<l;
    return 0;
}