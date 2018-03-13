package com.leetcode.zbf;

/**
 * Created by curry on 2017/12/29.
 */
public class RegularExpressionMatching {
    public static int[] getNextValue(String s) {
        int[] next = new int[s.length()];
        int j = 0, k = -1;
        next[j]=k;
        while (j < s.length()-1) {
            if (k == -1 || s.charAt(j) == s.charAt(k)) {
               next[++j]=++k;
            } else {
                k = next[k];
            }
        }
        return next;
    }

    public static boolean isMatch(String s, String p) {
        if(s.equals("")){
            if(p.equals("")){
                return true;
            }
            return false;
        }
        int[] next = getNextValue(s);
        int i = 0, j = 0;
        while (i == -1 || (i < s.length() && j < p.length())) {
            if (i == -1) {
                i++;
                j++;
                continue;
            }
            char a = s.charAt(i);
            char b = p.charAt(j);
            if (b == '.') {
                ++i;
                ++j;
            } else {
                if (b == '*') {
                    if (p.charAt(j - 1) == '.') {
                        return true;
                    } else {
                        if (a != p.charAt(j - 1)) {
                            i = next[i];
                        } else {
                            while (i < s.length() && s.charAt(i) == a) {
                                i++;
                            }
                            j++;
                        }
                    }
                } else {
                    if (s.charAt(i) == p.charAt(j)) {
                        i++;
                        j++;
                    } else {
                        i = next[i];
                    }
                }
            }
        }
        if (i >= s.length()) {
            return true;
        }
        return false;
    }

    public static void main(String[] args) {
        String s = "aa";
        String p=".";
        System.out.println(isMatch(s,p));
    }

}