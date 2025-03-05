#include<iostream>
#include<cmath>
using namespace std;
int global_n = 0;
void selectSort(int n, int arr[]){
  for (int i = 0;i<n-1;i++){
    int minIndex = i;
    for (int j = i + 1;j<n;j++){
      arr[j] < arr[minIndex] ? minIndex = j : minIndex;
    }
    swap(arr[i], arr[minIndex]);
  }
}

void bubbleSort(int n, int arr[]){
  for(int end = n-1;end>=1;end--){
    for(int j = 0;j<end;j++){
      if(arr[j]<arr[j+1]){
        swap(arr[j], arr[j + 1]);
      }
    }
  }
}

void insertSort(int n, int arr[]){
  for(int i = 0;i<n;i++){
    for(int j=i;j>=0;j--){
      if(arr[j]<arr[j-1]){
        swap(arr[j], arr[j-1]);
      }
    }
  }
}

int *randomArray(int n, int v){
  int *arr = new int[n];
  for (int i = 0;i<n;i++){
    arr[i] = (int)(rand() * v) + 1;
  }
  return arr;
}

int *copyArray(int n,int arr[]){
  int *newArr = new int[n];
  for(int i = 0;i<n;i++){
    newArr[i] = arr[i];
  }
  return newArr;
}

int sameArray(int *arr1,int *arr2){
  for(int i = 0;i<global_n;i++){
    if(arr1[i] != arr2[i]){
      return 0;
    }
  }
  return 1;
}

void Validator(){
  int N = 100;
  int V = 1000;
  int testTimes = 5000;
  cout << "start" << endl;
  for (int i = 0;i<=testTimes;i++){
    int n = (int)(rand() * N);
    int global_n = n;
    int *arr = randomArray(n, V);
    int *selectArr = copyArray(n,arr);
    int *bubbleArr = copyArray(n,arr);
    int *insertArr = copyArray(n,arr);
    selectSort(n, selectArr);
    bubbleSort(n, bubbleArr);
    insertSort(n, insertArr);
    if(!sameArray(selectArr, bubbleArr) || !sameArray(selectArr, insertArr) || !sameArray(bubbleArr, insertArr)){
      cout << "error" << endl;
    }
  }
}

int main(){
  Validator();
  system("pause");
  return 0;
}