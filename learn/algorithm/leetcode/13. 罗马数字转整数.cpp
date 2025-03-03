#include<iostream>
#include<cstring>
#include<map>
using namespace std;
class Solution {
public:
    int numm(char c){
        switch(c){
            case 'I':return 1;
            case 'V':return 5;
            case 'X':return 10;
            case 'L':return 50;
            case 'C':return 100;
            case 'D':return 500;
            case 'M':return 1000;
            default:return 0;
        }
    }
    int romanToInt(string s) {
        int ans = 0, pre_num = numm(s[0]);
        for(int i=1;i<s.length();i++){
            int now_num = numm(s[i]);
            if(now_num<=pre_num){
                ans+=pre_num;
            }else{
                ans-=pre_num;
            }
            pre_num = now_num;
        }
        ans += pre_num;
        return ans;
    }
};

int main(){
  Solution s;
  string str = "MCMXCIV";
  cout << s.romanToInt(str);
  system("pause");
  return 0;
}