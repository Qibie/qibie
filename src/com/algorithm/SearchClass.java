package com.algorithm;

/**
 * Created by curry on 2018/2/25.
 */
public class SearchClass {
    /**
     * 1、 二分查找
     * <p>
     * 非递归
     *
     * @param a
     * @param value
     * @param n
     * @return
     */
    public static int BinarySearch(int a[], int value, int n) {
        int low = 0, high = n - 1, mid = 0;
        while (low <= high) {
            mid = (low + high) / 2;
            if (a[mid] == value) {
                return mid;
            }
            if (a[mid] < value) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }

    /**
     * 二分查找递归版本
     *
     * @param a
     * @param value
     * @param low
     * @param high
     * @return
     */
    public static int BinarySearch(int[] a, int value, int low, int high) {
        int mid = (low + high) / 2;
        if (a[mid] == value) {
            return mid;
        } else {
            if (a[mid] < value) {
                return BinarySearch(a, value, low, mid - 1);
            } else {
                return BinarySearch(a, value, mid + 1, high);
            }
        }
    }

    /**
     * 2、插值查找
     *
     * @param a
     * @param value
     * @param low
     * @param high
     * @return
     */
    public static int InsertionSearch(int[] a, int value, int low, int high) {
        int mid = low + (value - a[low]) / (a[high] - a[low]) * (high - low);
        if (a[mid] == value) {
            return mid;
        } else {
            if (a[mid] < value) {
                return InsertionSearch(a, value, low, mid - 1);
            } else {
                return InsertionSearch(a, value, mid + 1, high);
            }
        }
    }


    public static final int MAX_SIZE = 20;

    public static void GeneratorFibonacci(int[] F) {
        F[0] = 0;
        F[1] = 1;
        for (int i = 2; i < MAX_SIZE; ++i) {
            F[i] = F[i - 1] + F[i - 2];
        }
    }

    public static int Fibonacci(int[] a, int value) {
        int k = 0, n = a.length, temp_n;
        int[] F = new int[MAX_SIZE];
        GeneratorFibonacci(F);
        while (n > (F[k] - 1)) {
            ++k;
        }
        temp_n = F[k] - 1;
        int[] temp = new int[temp_n];
        for (int i = 0; i < n; ++i) {
            temp[i] = a[i];
        }
        for (int i = n; i < temp_n; ++i) {
            temp[i] = a[n - 1];
        }
        int low = 0, high = temp_n;
        while (low <= high) {
            int mid = low + F[k - 1] - 1;
            if (temp[mid] > value) {
                high = mid - 1;
                k -= 1;
            } else if (temp[mid] < value) {
                low = mid + 1;
                k -= 2;
            } else if (temp[mid] == value) {
                if (mid < n) {
                    return mid;
                } else {
                    return n - 1;
                }
            }
        }
        return -1;
    }


}
