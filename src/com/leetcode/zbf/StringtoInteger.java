package com.leetcode.zbf;

/**
 * Created by curry on 2017/12/27.
 */

/**
 * 这道题要求的 atoi 跟C++实现的不一样吧，比如我以为不符合要求的返回-1，而这道题要求返回0。

 所以，有必要解释一下题目的要求：

 1. 首先需要丢弃字符串前面的空格；

 2. 然后可能有正负号（注意只取一个，如果有多个正负号，那么说这个字符串是无法转换的，返回0。比如测试用例里就有个“+-2”）；

 3. 字符串可以包含0~9以外的字符，如果遇到非数字字符，那么只取该字符之前的部分，如“-00123a66”返回为“-123”；

 4. 如果超出int的范围，返回边界值（2147483647或-2147483648）。

 综上，要求还是有点怪的，不看要求是很难写对的，看了也不一定理解的对。
 */
public class StringtoInteger {
    public static int myAtoi(String str) {
        int result=0,flag=0,i=0;
        int INT_MAX=Integer.MAX_VALUE,INT_MIN=Integer.MIN_VALUE,cutoff=INT_MAX/10,mod=INT_MAX%10,return_temp=INT_MAX;
        //去掉空格
        str=str.trim();
        //空串
        if(str.equals("")){
            return 0;
        }
        //考虑正负号
        if(str.charAt(0)>'9'||str.charAt(0)<'0'){
            if(str.charAt(0)=='-'){
                flag=1;
            }else {
                if (str.charAt(0)!='+'){
                    return 0;
                }
            }
            ++i;
        }
        if(flag==1){
            mod++;
            return_temp=INT_MIN;
        }
        for(;i<str.length();++i){
            if(str.charAt(i)<'0'||str.charAt(i)>'9'){
               break;
            }
            if(result>cutoff){
               result=return_temp;
               break;
            }else {
                if (result == cutoff && (i < (str.length()) && (str.charAt(i) > '0' + mod))) {
                    result=return_temp;
                    break;
                }
            }
            result=result*10+(str.charAt(i)-'0');
        }

        if(flag==1){
            return result*(-1);
        }else {
            return result;
        }
    }

    public  static void main(String []args){
        String str="-2147483649";
        int result=myAtoi(str);
        System.out.println(result);

        System.out.println(Integer.MAX_VALUE);
        System.out.println(Integer.MAX_VALUE%10);
    }


}
