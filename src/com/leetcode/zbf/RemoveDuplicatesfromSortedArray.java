package com.leetcode.zbf;

/**
 * Created by curry on 2018/2/11.
 */
public class RemoveDuplicatesfromSortedArray {
    public int removeDuplicates(int[] nums) {
        int temp_position = 0;
        for (int i = 1; i < nums.length; ++i) {
            if (nums[i] != nums[temp_position]) {
                nums[++temp_position]=nums[i];
            }
        }
        return temp_position+1;
    }
}
