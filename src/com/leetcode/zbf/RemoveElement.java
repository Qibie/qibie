package com.leetcode.zbf;

/**
 * Created by curry on 2018/2/11.
 */
public class RemoveElement {
    public int removeElement(int[] nums, int val) {
        int current_position = 0;
        for (int i = 0; i < nums.length; ++i) {
            if (nums[i] != val) {
                nums[current_position] = nums[i];
                current_position++;
            }
        }
        return current_position;
    }
}
