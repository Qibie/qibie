package com.leetcode.zbf;

import java.util.List;

/**
 * Created by curry on 2018/2/10.
 */
public class ReverseNodesinkGroup {
    public static ListNode reverseKGroup(ListNode head, int k) {
        if (head == null|| k==1) {
            return head;
        }
        int i = 0;
        ListNode end = head;
        for (i = 0; i < k-1; ++i) {
            if (end == null) {
                break;
            }
            end = end.next;
        }
        if (i < k-1 || end == null) {
            return head;
        } else {
            ListNode temp = end.next;
            reverseend(head, end);
            head.next = reverseKGroup(temp, k);
            return end;
        }
    }

    public static ListNode reverseend(ListNode head, ListNode end) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode p = head, q = head.next, k = q;
        while (!q .equals(end)) {
            q = q.next;
            k.next = p;
            p = k;
            k = q;
        }
        end.next = p;
        head.next = null;
        return end;
    }

    public static void main(String[] args) {
        ListNode listNode = ListNodeUtils.generateListNoe(2);
        ListNodeUtils.PrintListNode(listNode);
        listNode=reverseKGroup(listNode,1);
        ListNodeUtils.PrintListNode(listNode);

    }

}
