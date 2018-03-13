package com.leetcode.zbf;

import java.util.Arrays;

/**
 * Created by curry on 2018/1/7.
 */
public class ThreeSumClosest {
    public static int threeSumClosest(int[] nums, int target) {
        int min_distance = Integer.MAX_VALUE, result = 0;
        if (nums.length < 3) {
            throw new RuntimeException("length not enough");
        }
        Arrays.sort(nums);
        for (int i = 0; i < nums.length - 2; ++i) {
            if (i > 0 && (nums[i] == nums[i - 1])) {
                continue;
            }
            int start = i + 1, end = nums.length - 1;
            while (start < end) {
                int distance = nums[start] + nums[end] + nums[i] - target;
                if (Math.abs(distance) < min_distance) {
                    min_distance = Math.abs(distance);
                    //System.out.println(min_distance);
                    result = nums[start] + nums[end] + nums[i];
                }
                if (distance == 0) {
                    break;
                } else if (distance > 0) {
                    --end;

                } else if (distance < 0) {
                    ++start;

                }


            }

        }
        return result;
    }

    public static void main(String[] args) {
        int[] S = {0, 2, 1, -3};
        System.out.print(threeSumClosest(S, 1));

    }

}
