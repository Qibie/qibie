package com.leetcode.zbf;

/**
 * Created by curry on 2017/12/22.
 */
public class KmpAlgorithm {
    //获取next
    public static int[] getnextval(String s) {
        char[] chars = s.toCharArray();
        int[] next = new int[(s.length() + 1)];
        int j = 0;
        int k = -1;
        next[j] = k;
        while (j < s.length() - 1) {
            if (k == -1 || chars[j] == chars[k]) {
                //优化，去掉chars[j]==chars[next[j]]的情况
                if (chars[j++] == chars[k++]) {
                    //next[j]=next[k];
                    while (chars[j] == chars[k]) {
                        k = next[k];
                    }
                }
                next[j] = k;
            } else {
                k = next[k];
            }
        }
        return next;
    }
    //匹配
    public static int KmpMatcher(String s,String subS){
        char [] chars=s.toCharArray(),chars1=subS.toCharArray();
        int [] next=getnextval(subS);
        int i=0,j=0;
        while(j==-1||i<s.length()&&j<subS.length()){
            if(chars[i]==chars1[j]){
                i++;
                j++;
            }else {
                j=next[j];
            }
        }
        if(j>=subS.length()){
            return i-subS.length()+1;
        }else {
            return -1;
        }
    }

}
