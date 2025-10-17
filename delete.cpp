#include <iostream>
#include <set>

int main() {
    std::set<int> s = {9, 1, 7, 3, 5};  // 乱序插入
    
    // 遍历时会按顺序输出
    for ( auto i=s.begin();i!=s.end();i++) {
        std::cout << *i << " ";  // 输出: 1 3 5 7 9
    }
    
    return 0;
}