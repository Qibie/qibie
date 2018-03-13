package com.leetcode.zbf;

/**
 * Created by curry on 2018/1/24.
 */
public class MergekSortedLists {
    public ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) {
            return null;
        }
        return helper(lists, 0, lists.length - 1);
    }

    public ListNode helper(ListNode[] listNodes, int start, int end) {
        if (start < end) {
            int m=(start+end)/2;
            return mergeTwoListNode(helper(listNodes,start,m),helper(listNodes,m+1,end));
        }else {
            return listNodes[start];
        }

    }


    public ListNode mergeTwoListNode(ListNode listNode1, ListNode listNode2) {
        ListNode head, temp;
        if (listNode1 == null) {
            return listNode2;
        }
        if (listNode2 == null) {
            return listNode1;
        }
        if (listNode1.val < listNode2.val) {
            head = listNode1;
            listNode1 = listNode1.next;
        } else {
            head = listNode2;
            listNode2 = listNode2.next;
        }
        temp = head;
        while (listNode1 != null && listNode2 != null) {
            if (listNode1.val < listNode2.val) {
                temp.next = listNode1;
                listNode1 = listNode1.next;
            } else {
                temp.next = listNode2;
                listNode2 = listNode2.next;
            }
            temp = temp.next;
        }
        while (listNode1 != null) {
            temp.next = listNode1;
            listNode1 = listNode1.next;
            temp = temp.next;
        }
        while (listNode2 != null) {
            temp.next = listNode2;
            listNode2 = listNode2.next;
            temp = temp.next;
        }
        return head;
    }

    public static void main(String[] args) {
        ListNode [] listNodes=new ListNode[2];
        listNodes[0]=new ListNode(1);
        listNodes[1]=new ListNode(0);
        MergekSortedLists mergekSortedLists=new MergekSortedLists();
        ListNode result=mergekSortedLists.mergeKLists(listNodes);
        System.out.print(result.val);
    }
}
