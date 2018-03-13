package com.leetcode.zbf;

/**
 * Created by curry on 2018/1/1.
 */
public class IntegerToRoman {
    /**
     * 例如整数 1437 的罗马数字为 MCDXXXVII， 我们不难发现，千位，百位，十位和个位上的数分别用罗马数字表示了。 1000 - M, 400 - CD, 30 - XXX, 7 - VII。所以我们要做的就是用取商法分别提取各个位上的数字，然后分别表示出来：
     * 100 - C              1 - I               1000 - M
     * 200 - CC             2 - II              2000 - MM
     * 300 - CCC            3 - III             3000 - MM
     * 400 - CD             4 - IV
     * 500 - D              5 -  V
     * 600 - DC             6 - VI
     * 700 - DCC            7 - VII
     * 800 - DCCC           8 - VIII
     * 900 - CM             9 - IX
     * 我们可以分为四类，100到300一类，400一类，500到800一类，900最后一类。每一位上的情况都是类似的，代码如下：
     *
     * @param num
     * @return
     */
    public static String intToRoman(int num) {
        String res = "";
        char[] roman = {'M', 'D', 'C', 'L', 'X', 'V', 'I'};
        int[] value = {1000, 500, 100, 50, 10, 5, 1};
        for (int n = 0; n < roman.length; n += 2) {
            int x = num / value[n];
            if (x < 4) {
                for (int i = 0; i < x; ++i) {
                    res += roman[n];
                }
            } else if (x == 4) {
                res = res + roman[n] + roman[n - 1];
            } else if (x < 9) {
                res = res + roman[n - 1];
                for (int i = 6; i <= x; ++i) {
                    res += roman[n];
                }
            } else if (x == 9) {
                res = res + roman[n] + roman[n - 2];
            }
            num = num % value[n];
        }
        return res;
    }

    public static String intToRoman1(int num) {
        String res = "";
        int[] val = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
        String[] str = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
        for (int i = 0; i < val.length; ++i) {
            while (num >= val[i]) {
                num -= val[i];
                res += str[i];
            }
        }
        return res;
    }
}
