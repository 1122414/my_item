#include<iostream>
using namespace std;
int n = 10, num[10] = {1, 55, 14, 66, 33, 87, 19, 56, 14, 15};
void insert_sort(){
  for (int i = 0;i < n;i++){
    for (int j = i;j >= 0;j--){
      if(num[j]<num[j-1]){
        swap(num[j], num[j-1]);
      }else{
        break;
      }
    }
  }
}
int main(){
  insert_sort();
  for (int i = 0;i < n;i++){
    cout << num[i] << ' ';
  }
  cout << endl;
  system("pause");
  return 0;
}