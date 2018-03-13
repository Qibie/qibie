package com.leetcode.zbf;

import org.omg.PortableInterceptor.INACTIVE;

/**
 * Created by curry on 2017/12/23.
 */
public class ReverseInteger {
    public static int reverse(int x) {
        if (x == -x)
        {
            return 0;
        }
        if(x<0){return -reverse(Math.abs(x));}
        int cutoff=Integer.MAX_VALUE/10;
        int result=0;
        while (x!=0){
            result=result*10+x%10;
            x=x/10;
            if(result>cutoff&&x!=0){
                return 0;
            }
        }
        return result;
    }

    public static int myAtoi(String str) {
        if(str.equals("")){
            return 0;
        }
        return Integer.parseInt(str);
    }

    public static void main(String []args){
        int num=-2147483648;
        int result=reverse(num);
        System.out.println(result);

    }
}
