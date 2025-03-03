#include<iostream>
using namespace std;
int n = 10, num[10] = {1, 55, 14, 66, 33, 87, 19, 56, 14, 15};
void bubble_sort(){
  // 最大的往右冒泡
  // for (int i = 0;i < n;i++){
  //   for (int j = i + 1;j < n;j++){
  //     if(num[i]>num[j]){
  //       swap(num[i], num[j]);
  //     }
  //   }
  // }
  for(int end = n - 1; end > 0; end--){
    for(int i = 0; i < end; i++){
      if(num[i] > num[i+1]){
        swap(num[i], num[i+1]);
      }
    }
  }
}
int main(){
  bubble_sort();
  for (int i = 0;i < n;i++){
    cout << num[i] << ' ';
  }
  system("pause");
  return 0;
}