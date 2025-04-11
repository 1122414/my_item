#include<iostream>
#include<algorithm>
#include<cstdlib>
#include<time.h>
#define N 10

using namespace std;
int arr[N];

void make_arr(){
  srand(time(NULL));
  for (int i=0;i<N;i++){
    arr[i] = rand()%100+1;
  }
  sort(arr,arr+N);
}

int true_search(int num){
  for (int i = 0;i<N;i++){
    if (arr[i] == num) return i;
  }
  return -1;
}

int dichotomia(int num){
  int l = 0, r = N - 1;
  while(l<=r){
    int m = (l+r)/2;
    if (arr[m] == num) return m;
    else if(arr[m]>num) r = m - 1;
    else l = m + 1;
  }
  return 0;
}

void is_true(){
  int test_time = 10;
  while(test_time--){
    make_arr();
    int i = rand() % N;
    int true_i = true_search(arr[i]);
    int dichotomia_i = dichotomia(arr[i]);
    if(true_i != dichotomia_i){
      cout << true_i << ' ' << dichotomia_i;
    }
  }
  cout << "true" <<endl;
}

int main(){
  ios::sync_with_stdio(false);
  cin.tie(0);
  cout.tie(0);
  is_true();
  system("pause");
  return 0;
}