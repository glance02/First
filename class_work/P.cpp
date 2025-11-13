#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);

    int n;
    string s;
    while (cin >> n >> s) {
        int left = 0, right = n - 1;
        string t;

        while (left <= right) {
            bool takeLeft = false;
            // 比较左侧和右侧的字典序
            for (int i = 0; left + i <= right; ++i) {
                if (s[left + i] < s[right - i]) { takeLeft = true; break; }
                else if (s[left + i] > s[right - i]) { takeLeft = false; break; }
            }
            if (takeLeft) t += s[left++];
            else t += s[right--];
        }

        cout << t << "\n";
    }
    return 0;
}
