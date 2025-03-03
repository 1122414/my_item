#define ll long long int
#include<vector>
#include<iostream>
#include<unordered_map>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
      unordered_map<int,int>mp;
      for(int i=0;i<nums.size();i++){
        int aim = target - nums[i];
        if(mp.find(aim)!=mp.end()){
          return {mp[aim],i};
        }
        mp[nums[i]] = i;
      }
      return {};
    }
};
int main(){
  Solution so;
  vector<int> nums = {3,3};
  int target = 6;
  vector<int> res = so.twoSum(nums, target);
  for(int i=0;i<res.size();i++){
    cout<<res[i]<<" ";
  }
  cout<<endl;
  system("pause");
}


// // 哈希解法
// #include<iostream>
// #include<unordered_map>
// #define ll long long int
// using namespace std;
// ll n, nums[10005], target;
// unordered_map<ll, ll> mp;
// int main(){
//   cin >> n;
//   for (int i = 0;i<n;i++){
//     cin >> nums[i];
//   }
//   cin >> target;
//   for (int i = 0;i<n;i++){
//     int aim = target - nums[i];
//     if(mp.find(aim)!= mp.end()){
//       cout <<mp[aim]<< " " << i << endl;
//     }
//     mp[nums[i]] = i;
//   }
//   cout << endl;
//   system("pause");
//   return 0;
// }

// 10
// -2 -3 -4 -7 10 11 12 15 17 20
// 3

