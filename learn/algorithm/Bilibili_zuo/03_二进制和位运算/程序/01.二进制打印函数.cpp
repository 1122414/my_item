#include<iostream>
using namespace std;
// 注意：如果long 1要强转
void printBinary(int num){
  if(num==0){
    cout << 0;
    return;
  }
  for (int i = 31;i>=0;i--){
    int temp = num & (1 << i);
    (num & (1 << i)) !=0 ? cout << "1" : cout << "0";
    // num & (1 << i) ? cout << "1" : cout << "0";
  }
}
int main(){
  int num = 10;
  printBinary(num);
  cout << endl;
  system("pause");
  return 0;
}