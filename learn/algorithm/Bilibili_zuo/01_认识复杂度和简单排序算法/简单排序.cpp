#include <iostream>
using namespace std;
void select_sort(int arr[], int n){
  if(arr == NULL || n <= 1)
    return;
  for (int i = 0;i<n-1;i++){
    int min_idx = i;
    for (int j = i+1;j<n;j++){
      arr[j] < arr[min_idx] ? min_idx = j : min_idx;
    }
    swap(arr[i], arr[min_idx]);
  }
}
int main(){
  int arr[10] = {5, 3, 8, 6, 2, 7, 1, 4, 9, 0};
  select_sort(arr, 10);
  for(int i = 0;i<10;i++){
    cout << arr[i] << " ";
  }
  
  cout << endl;
  system("pause");
  return 0;
}