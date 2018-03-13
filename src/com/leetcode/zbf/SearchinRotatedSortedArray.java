package com.leetcode.zbf;

/**
 * Created by curry on 2018/2/24.
 */
public class SearchinRotatedSortedArray {
    public int search(int[] nums, int target) {
        if (nums == null || nums.length == 0) {
            return -1;
        }
        if (target >= nums[0]) {
            for (int i = 0; i < nums.length; ++i) {
                if (target == nums[i]) {
                    return i;
                }
                if (nums[i] < nums[0]) {
                    return -1;
                }
            }
        } else {
            for (int i = nums.length - 1; i >= 0; --i) {
                if (target == nums[i]) {
                    return i;
                }
                if ((i<nums.length-1) && nums[i] > nums[i + 1]) {
                    return -1;
                }
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] nums = {1};
        int index = new SearchinRotatedSortedArray().search(nums, 0);
    }
}
