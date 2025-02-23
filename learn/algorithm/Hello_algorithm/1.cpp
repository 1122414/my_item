#include <iostream>
#include <windows.h>  // 新增头文件

using namespace std;

int main() {
    // SetConsoleOutputCP(65001);  // 设置控制台为UTF-8
    cout << u8"测试外部控制台" << endl;  // 注意u8前缀
    system("pause");
    return 0;
}