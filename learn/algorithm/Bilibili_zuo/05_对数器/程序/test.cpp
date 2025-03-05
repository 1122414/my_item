#include<iostream>
#include <ctime>
using namespace std;
int *randomArray(int n, int v){
  int *arr = new int[n];
  srand( (unsigned)time( NULL ) );
  for (int i = 0;i<n;i++){
    arr[i] = (int)(rand() * v) + 1;
    cout << arr[i] << " ";
  }
  cout << endl;
  return arr;
}

int main(){
  int *arr = randomArray(10, 100);
  // 对指针不起作用  sizeof(arr)返回的是指针大小
  int n = sizeof(arr) / sizeof(arr[0]);

  // int arr[10] = {1, 2, 3, 4, 5, 6, 7, 7, 8, 8};
  // end(arr)-begin(arr)也只能给普通数组使用
  // int n = end(arr)-begin(arr);

  for (int i = 0;i<n;i++){
    cout<<arr[i]<<' ';
  }
    
  cout << n;
  system("pause");
  return 0;
}