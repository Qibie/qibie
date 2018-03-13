package com.leetcode.zbf;

/**
 * Created by curry on 2017/12/31.
 */
public class ContainerWithMostWater {
    public int maxArea(int[] height) {
        int i = 0, j = height.length - 1, max_size = Math.min(height[i], height[j]) * (j - i);
        while (i < j) {
            int temp_size = Math.min(height[i], height[j]) * (j - i);
            if (temp_size > max_size) {
                max_size = temp_size;
            }
            if (height[i] < height[j]) {
                ++i;
            } else {
                --j;
            }
        }
        return max_size;
    }


    public static void main(String[] args) {

    }

}
