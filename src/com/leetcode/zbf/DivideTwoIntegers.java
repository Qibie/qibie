package com.leetcode.zbf;

import org.omg.Messaging.SYNC_WITH_TRANSPORT;

/**
 * Created by curry on 2018/2/12.
 */
public class DivideTwoIntegers {
    /**
     * o(n)
     *
     * @param dividend
     * @param divisor
     * @return
     */
    public int divide1(int dividend, int divisor) {
        if (divisor == 0) {
            return Integer.MAX_VALUE;
        }
        //判断正负
        boolean isNeg = (dividend ^ divisor) >>> 31 == 1;
        int res = 0, difference = Integer.MAX_VALUE;
        dividend = Math.abs(dividend);
        divisor = Math.abs(divisor);
        difference = dividend - divisor;
        while (difference >= 0) {
            ++res;
            difference = difference - divisor;
        }
        return isNeg == true ? -res : res;
    }


    public int divide(int dividend, int divisor) {
        if (divisor == 0) {
            return Integer.MAX_VALUE;
        }

        //判断正负
        boolean isNeg = (dividend ^ divisor) >>> 31 == 1;
        int res = 0, difference = Integer.MAX_VALUE, temp = 0, initial_divisor = Math.abs(divisor);
        if (dividend == Integer.MIN_VALUE) {
            if (divisor == -1) {
                return Integer.MAX_VALUE;
            } else {
                dividend += Math.abs(divisor);
                ++res;
            }
        }
        if (divisor == Integer.MIN_VALUE) {
            return res;
        }
        dividend = Math.abs(dividend);
        divisor = Math.abs(divisor);
        if (dividend < divisor) {
            return isNeg == true ? -res : res;
        }
        while (divisor < (dividend >> 1)) {
            ++temp;
            divisor = divisor << 1;
        }
        difference = dividend - divisor;
        res += 1 << (temp);
        while (difference >= initial_divisor) {
            while (divisor > difference) {
                --temp;
                divisor = divisor >> 1;
            }
            difference = difference - divisor;
            res += 1 << (temp);
        }
        return isNeg == true ? -res : res;
    }


    public static void main(String[] args) {
//        int divident = 10, divisor = 1;
        int divident = -2147483648, divisor = 1262480350;
        System.out.print(new DivideTwoIntegers().divide(divident, divisor));
    }
}
