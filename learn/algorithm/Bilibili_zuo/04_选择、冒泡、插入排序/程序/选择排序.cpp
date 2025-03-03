#include<iostream>
using namespace std;
int n = 10, num[10] = {1, 55, 14, 66, 33, 87, 19, 56, 14, 15};
void select_sort(){
  for (int i = 0;i < n - 1;i++){
    int min_index = i;
    for (int j = i + 1;j < n;j++){
      num[min_index] > num[j] ? min_index = j : min_index;
    }
    swap(num[i], num[min_index]);
  }
}
int main(){
  select_sort();
  for (int i = 0;i < n;i++){
    cout << num[i] << ' ';
  }
  system("pause");
  return 0;
}