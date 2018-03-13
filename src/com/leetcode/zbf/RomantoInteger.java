package com.leetcode.zbf;

/**
 * Created by curry on 2018/1/1.
 */
public class RomantoInteger {
    /**
     * 例如整数 1437 的罗马数字为 MCDXXXVII， 我们不难发现，千位，百位，十位和个位上的数分别用罗马数字表示了。 1000 - M, 400 - CD, 30 - XXX, 7 - VII。所以我们要做的就是用取商法分别提取各个位上的数字，然后分别表示出来：
     * 100 - C      10 - X              1 - I               1000 - M
     * 200 - CC     20 - XX             2 - II              2000 - MM
     * 300 - CCC    30 - XXX            3 - III             3000 - MM
     * 400 - CD     40 - XL             4 - IV
     * 500 - D      50 - L              5 -  V
     * 600 - DC     60 - LX             6 - VI
     * 700 - DCC    70 - LXX            7 - VII
     * 800 - DCCC   80 - LXXX           8 - VIII
     * 900 - CM     90 - XC             9 - IX
     * 我们可以分为四类，100到300一类，400一类，500到800一类，900最后一类。每一位上的情况都是类似的，代码如下：
     *
     * @param s
     * @return
     */
    public static int romanToInt(String s) {
        int result = 0, i = 0;
        //千
        while (i < s.length() && s.charAt(i) == 'M') {
            ++i;
            result += 1000;
        }
        char[] roman = {'M', 'D', 'C', 'L', 'X', 'V', 'I'};
        int[] value = {1000, 500, 100, 50, 10, 5, 1};

        for (int n = 2; n < roman.length; n += 2) {
            //说明1-4之间,或者9
            if (i < s.length() && s.charAt(i) == roman[n]) {
                if (i < s.length() - 1 && s.charAt(i + 1) == roman[n - 2]) {
                    //9
                    result += (value[n - 2] - value[n]);
                    i += 2;
                } else if (i < s.length() - 1 && s.charAt(i + 1) == roman[n - 1]) {
                    //4
                    result += (value[n - 1] - value[n]);
                    i += 2;
                } else {
                    while (i < s.length() && s.charAt(i) == roman[n]) {
                        result += value[n];
                        ++i;
                    }
                }
            } else if (i < s.length() && s.charAt(i) == roman[n - 1]) {
                //5-8之间
                result += value[n - 1];
                ++i;
                while (i < s.length() && s.charAt(i) == roman[n]) {
                    result += value[n];
                    ++i;
                }
            }
        }
        return result;
    }



/*
    Symbol	I	V	X	L	C	D	M
    Value	1	5	10	50	100	500	1,000

    1 to 10
    I, II, III, IV, V, VI, VII, VIII, IX, X

    10 to 100
    X, XX, XXX, XL, L, LX, LXX, LXXX, XC, C.

    100 to 1000
    C, CC, CCC, CD, D, DC, DCC, DCCC, CM, M.
 */


    public static int romanToInt1(String s) {
        int result = 0;
        for (int i = s.length() - 1; i >= 0; i--) {
            switch (s.charAt(i)) {
                case 'I':
                    result += (result >= 5) ? -1 : 1;
                    break;
                case 'V':
                    result += 5;
                    break;
                case 'X':
                    result += (result >= 50) ? -10 : 10;
                    break;
                case 'L':
                    result += 50;
                    break;
                case 'C':
                    result += (result >= 500) ? -100 : 100;
                    break;
                case 'D':
                    result += 500;
                    break;
                case 'M':
                    result += (result >= 5000) ? -1000 : 1000;
                    break;
                default:

            }
        }
        return result;
    }


    public static void main(String[] args) {
        String roman = "CM";
        System.out.println(romanToInt1(roman));
    }

}
