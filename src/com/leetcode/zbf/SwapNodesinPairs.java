package com.leetcode.zbf;

import org.omg.Messaging.SYNC_WITH_TRANSPORT;

import javax.print.attribute.standard.RequestingUserName;
import java.util.*;

/**
 * Created by curry on 2018/2/10.
 */
public class SwapNodesinPairs {
    public ListNode swapPairs(ListNode head) {
        if (head == null) {
            return head;
        }
        //temp head
        ListNode temp_head = new ListNode(0);
        temp_head.next = head;
        ListNode temp_node = temp_head;
        while (temp_node.next != null && temp_node.next.next != null) {
            ListNode temp = temp_node.next;
            temp_node.next = temp.next;
            temp.next = temp_node.next.next;
            temp_node.next.next = temp;
            temp_node = temp_head.next.next;
        }
        return temp_head.next;
    }


    public ListNode swapPairs1(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode nextNode = head.next;
        head.next = swapPairs(nextNode.next);
        nextNode.next = head;
        return nextNode;
    }





}
