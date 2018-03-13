package com.leetcode.zbf;

import org.omg.Messaging.SYNC_WITH_TRANSPORT;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Created by curry on 2018/2/10.
 */
public class ListNodeUtils {
    /**
     * 产生长度为k的listnode
     *
     * @param k
     * @return
     */
    public static ListNode generateListNoe(int k) {
        List<Integer> integers = new ArrayList<>();
        for (int i = 0; i < k; ++i) {
            integers.add(i);
        }
        Collections.shuffle(integers);
        ListNode head = new ListNode(Integer.MIN_VALUE);
        head.next = null;
        for (int i = 0; i < k; ++i) {
            ListNode node = new ListNode(integers.get(i));
            node.next = head.next;
            head.next = node;
        }
        return head.next;
    }

    /**
     * 打印listnode
     *
     * @param head
     */
    public static void PrintListNode(ListNode head) {
        ListNode temp = head;
        StringBuilder stringBuilder = new StringBuilder("[");
        while (temp != null) {
            stringBuilder.append(temp.val + ",");
            temp = temp.next;
        }
        stringBuilder.setCharAt(stringBuilder.length() - 1, ']');
        System.out.println(stringBuilder.toString());
    }
}
