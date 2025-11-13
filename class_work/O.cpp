#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Worker {
    int start, end;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);

    int N;
    cin >> N;
    vector<Worker> v(N);
    for (int i = 0; i < N; ++i) {
        cin >> v[i].start >> v[i].end;
    }

    sort(v.begin(), v.end(), [](const Worker &a, const Worker &b) {
        return a.start < b.start;
    });

    int current_start = v[0].start;
    int current_end = v[0].end;
    int max_work = current_end - current_start;
    int max_idle = 0;

    for (int i = 1; i < N; ++i) {
        if (v[i].start <= current_end) {
            // overlap, merge intervals
            current_end = max(current_end, v[i].end);
        } else {
            // gap detected
            max_idle = max(max_idle, v[i].start - current_end);
            max_work = max(max_work, current_end - current_start);
            current_start = v[i].start;
            current_end = v[i].end;
        }
    }

    max_work = max(max_work, current_end - current_start);

    cout << max_work << " " << max_idle << "\n";
    return 0;
}
