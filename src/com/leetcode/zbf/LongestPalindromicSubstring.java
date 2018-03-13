package com.leetcode.zbf;

/**
 * Created by curry on 2017/12/21.
 */
public class LongestPalindromicSubstring {
    //长度递减
//    public String longestPalindrome(String s) {
//        int size=s.length();
//        int low=0;
//        int high=low+size-1;
//        for(;size>0;size--) {
//            for (low = 0, high = low+size-1; high < s.length(); low++, high++) {
//                if (shrinkCheckPalindrome(s, low, high)) {
//                    return s.substring(low, high + 1);
//                }
//            }
//        }
//
//        return "";
//    }
//
//    /**
//     * 判断是否是回味
//     * @param s
//     * @return
//     */
//    public boolean shrinkCheckPalindrome(String s,int low,int high){
//        while (low <high){
//            if(s.charAt(low)!=s.charAt(high)){
//                return false;
//            }
//            low++;
//            high--;
//        }
//        return true;
//    }

    //中心扩展
    int maxSize=0;
    String res="";
    public String longestPalindrome(String s) {
        if(s.length()==1){
            return s;
        }
        for(int i=0;i<s.length()-1;i++){
            checkPalindromeExpand(s,i,i);
            checkPalindromeExpand(s,i,i+1);
        }
        return res;
    }
    public void checkPalindromeExpand(String s,int low,int high){
        while((low>=0)&&(high<=s.length()-1)){
            if(s.charAt(low)==s.charAt(high)){
                if((high-low+1)>maxSize){
                    maxSize=high-low+1;
                    res=s.substring(low,high+1);
                }
                low--;
                high++;
            }else {
                return;
            }
        }
    }


    public static void main(String []args){
        String  s="abb";
        LongestPalindromicSubstring longestPalindromicSubstring=new LongestPalindromicSubstring();
        String result=longestPalindromicSubstring.longestPalindrome(s);
        System.out.print(result);
    }
}
