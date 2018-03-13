package com.leetcode.zbf;

/**
 * Created by curry on 2018/2/12.
 */
public class ImplementStrStr {
    /**
     * using kmp algorithm
     */
    public int strStr(String haystack, String needle) {
        if (needle.equals("")) {
            return 0;
        }
        int i = 0, j = 0;
        int[] next = new int[needle.length()];
        getNext(needle, next);//get the next index
        while (i < haystack.length() && j < needle.length()) {
            if (j == -1 || haystack.charAt(i) == needle.charAt(j)) {
                ++i;
                ++j;
            } else {
                j = next[j];
            }
        }
        if (j == needle.length()) {
            return i - j;
        } else {
            return -1;
        }
    }

    public void getNext(String needle, int[] next) {
        next[0] = -1;
        int i = 0, j = -1;
        while (i < needle.length() - 1) {
            if (j == -1 || needle.charAt(i) == needle.charAt(j)) {
                ++i;
                ++j;
                next[i] = j;
            } else {
                j = next[j];
            }
        }
    }

    public static void main(String[] args) {
        String hastack="mississippi",needle="issip";
        System.out.println(new ImplementStrStr().strStr(hastack,needle));
    }


}
