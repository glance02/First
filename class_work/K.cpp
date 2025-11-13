#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
using namespace std;

struct Paper {
    int time;
    int value;
    double ratio;
};

bool comparePapers(const Paper& a, const Paper& b) {
    return a.ratio > b.ratio;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);

    int m, n;
    while (cin >> m >> n && (m != 0 || n != 0)) {
        vector<Paper> papers(m);
        for (int i = 0; i < m; ++i) {
            cin >> papers[i].time >> papers[i].value;
            papers[i].ratio = (double)papers[i].value / papers[i].time;
        }

        sort(papers.begin(), papers.end(), comparePapers);

        double max_value = 0.0;
        int remaining_time = n;

        for (int i = 0; i < m; ++i) {
            if (remaining_time >= papers[i].time) {
                max_value += papers[i].value;
                remaining_time -= papers[i].time;
            } else {
                max_value += remaining_time * papers[i].ratio;
                remaining_time = 0;
                break;
            }
        }

        cout << fixed << setprecision(2) << max_value << "\n";
    }

    return 0;
}