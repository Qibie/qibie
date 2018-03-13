package com.leetcode.zbf;

/**
 * Created by curry on 2018/1/1.
 */
public class LongestCommonPrefix {
    public static String longestCommonPrefix(String[] strs) {
        if(strs.length==0){
            return "";
        }
        String res="";
        int i=0;
        boolean flag=true;
        //获取最小的长度
        int min=Integer.MAX_VALUE;
        for(int j=0;j<strs.length;++j){
            if(min>strs[j].length()){
                min =strs[j].length();
            }
        }
        while (flag&&i<min){
            char a=strs[0].charAt(i);
            for(int j=1;j<strs.length;++j){
                if (strs[j].charAt(i)!=a){
                    flag=false;
                    break;
                }
            }
            if(flag) {
                res += a;
            }
            ++i;
        }
        return res;
    }

    public static void main(String [] args){
        String [] strings={"a"};
        System.out.println(longestCommonPrefix(strings));
    }
}
