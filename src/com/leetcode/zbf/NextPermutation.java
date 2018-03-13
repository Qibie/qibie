package com.leetcode.zbf;

import org.omg.Messaging.SYNC_WITH_TRANSPORT;

import java.util.Arrays;

/**
 * Created by curry on 2018/2/24.
 */
public class NextPermutation {
    public void nextPermutation(int[] nums) {
        if (nums == null || nums.length == 0) {
            return;
        }
        int swap_index_previous = -1, swap_index_last = -1, TEEP = 0;
        for (int i = nums.length - 2; i >= 0; --i) {
            if (nums[i] < nums[i + 1]) {
                swap_index_previous = i;
                break;
            }
        }
        if (swap_index_previous < 0) {
            quicksort(nums, 0, nums.length - 1);
            return;
        }
        for (int i = nums.length - 1; i >= 0; --i) {
            if (nums[i] > nums[swap_index_previous]) {
                swap_index_last = i;
                break;
            }
        }
        TEEP = nums[swap_index_previous];
        nums[swap_index_previous] = nums[swap_index_last];
        nums[swap_index_last] = TEEP;

        quicksort(nums, swap_index_previous + 1, nums.length - 1);

    }

    /**
     * 以下是快速排序
     */


    public void quicksort(int[] nums, int low, int high) {
        if (low < high) {
            int partition = partition(nums, low, high);
            quicksort(nums, low, partition - 1);
            quicksort(nums, partition + 1, high);
        }
    }

    public int partition(int[] nums, int low, int high) {
        int TEMP = nums[low];
        while (low < high) {
            while (low < high && nums[high] >= TEMP) {
                --high;
            }
            nums[low] = nums[high];
            while (low < high && nums[low] < TEMP) {
                ++low;
            }
            nums[high] = nums[low];
        }
        nums[low] = TEMP;
        return low;
    }

    public static void main(String[] args) {
        int [] nums={1,1};
        NextPermutation nextPermutation=new NextPermutation();
        nextPermutation.nextPermutation(nums);
        System.out.println(Arrays.toString(nums));
    }


}
