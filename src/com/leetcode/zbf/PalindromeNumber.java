package com.leetcode.zbf;

import java.util.Map;

/**
 * Created by curry on 2017/12/29.
 */
public class PalindromeNumber {
    public static boolean isPalindrome(int x) {
        if (x < 0) {
            return false;
        }
        if (x < 10) {
            return true;
        }
        //首先找最高位的整数
        int level=10,top=0,right=0;
        while (true) {
            if ((x/level)<1 ) {
                level=level/10;
                break;
            }
            level*=10;
            if(level==1000000000){
                break;
            }
        }


        while (x!=0){
            top=x/level;
            right=x%10;
            if(top!=right){
                return false;
            }
            x=x%level;
            x=x/10;
            level=level/100;
        }
        return true;
    }

    public static void main(String args[]) {
        int i = 11;
        System.out.println(isPalindrome(i));
    }

}
