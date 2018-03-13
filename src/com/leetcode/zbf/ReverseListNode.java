package com.leetcode.zbf;

/**
 * Created by curry on 2018/2/10.
 */
public class ReverseListNode {
    //递归逆转单链表
    public static ListNode reverse(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode reversedListNode = reverse(head.next);
        head.next.next = head;
        head.next = null;
        return reversedListNode;
    }

    //非递归
    public static ListNode reverse1(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode p = head, q = head.next,k=q;
        while (q != null) {
            q=q.next;
            k.next=p;
            p=k;
            k=q;
        }
        head.next = null;
        head=p;
        return head;
    }

    //非递归
    public static ListNode reverseend(ListNode head,ListNode end) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode p = head, q = head.next,k=q;
        while (q != end) {
            q=q.next;
            k.next=p;
            p=k;
            k=q;
        }
        end.next=p;
        head.next = null;
        return end;
    }

    public static void main(String[] args) {
        ListNode head = ListNodeUtils.generateListNoe(10);
        ListNodeUtils.PrintListNode(head);
       // head=reverse(head);
        head=reverse1(head);
        ListNodeUtils.PrintListNode(head);

    }

}
