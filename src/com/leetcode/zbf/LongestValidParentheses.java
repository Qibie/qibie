package com.leetcode.zbf;

import org.omg.PortableInterceptor.INACTIVE;

import java.util.LinkedList;

/**
 * Created by curry on 2018/2/24.
 */
public class LongestValidParentheses {
    public int longestValidParentheses(String s) {
        int N = s.length();
        if (N % 2 != 0) {
            N = N - 1;
        }
        while (N >= 0) {
            for (int i = 0; i <= s.length() - N; ) {
                if (IsValid(s.substring(i, i + N))) {
                    return N;
                } else {
                    ++i;
                    while ((i <= (s.length() - N)) && (s.charAt(i) != '(' || s.charAt(i + N - 1) != ')')) {
                        ++i;
                    }
                }
            }
            N -= 2;
        }
        return 0;
    }

    /**
     * 判断是否匹配合格
     *
     * @param s
     * @return
     */
    public static boolean IsValid(String s) {
        LinkedList<Character> parentheses = new LinkedList<>();
        if (s == null || s.equals("")) {
            return true;
        }
        if (s.charAt(0) == ')') {
            return false;
        }
        for (char c : s.toCharArray()) {
            if (c == '(') {
                parentheses.addLast(c);
            } else if (c == ')' && parentheses.size() > 0) {
                parentheses.removeLast();
            } else {
                return false;
            }
        }
        if (parentheses.size() == 0) {
            return true;
        } else {
            return false;
        }
    }

    public int longestValidParentheses1(String s) {
        int res = 0, start = 0;
        LinkedList<Integer> linkedList = new LinkedList<>();
        for (int i = 0; i < s.length(); ++i) {
            if (s.charAt(i) == '(') {
                linkedList.addLast(i);
            } else if (s.charAt(i) == ')') {
                if (linkedList.isEmpty()) {
                    start = i + 1;
                } else {
                    linkedList.removeLast();
                    res = linkedList.isEmpty() ? Math.max(res, i - start + 1) : Math.max(res, i - linkedList.getLast());
                }
            }
        }
        return res;
    }


    public static void main(String[] args) {
        String s="))))((()((";
        System.out.println(new LongestValidParentheses().longestValidParentheses1(s));
    }
}
