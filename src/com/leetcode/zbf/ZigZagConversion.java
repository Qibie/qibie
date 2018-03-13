package com.leetcode.zbf;

import sun.security.pkcs11.wrapper.CK_SSL3_KEY_MAT_OUT;

import java.util.Arrays;

/**
 * Created by curry on 2017/12/22.
 */
public class ZigZagConversion {
//    public static String convert(String s, int numRows) {
//        if(numRows==1){
//            return s;
//        }
//        char[] chars = s.toCharArray();
//        int flag = 0, x = 0, y = 0, count = chars.length / (2 * numRows - 2);
//        if (chars.length % (2 * numRows - 2) != 0) {
//            count++;
//        }
//        char[][] charses = new char[numRows][count * (numRows - 1)];
//        for (int i = 0; i <= count; ++i) {
//            for (int j = 0; j < numRows; ++j) {
//                if (flag < chars.length) {
//                    charses[x][y] = chars[flag++];
//                    x++;
//                } else {
//                    break;
//                }
//            }
//            x -= 2;
//            y++;
//            for (int j = 0; j < numRows - 2; ++j) {
//                if (flag < chars.length) {
//                    charses[x][y] = chars[flag++];
//                    x--;
//                    y++;
//                } else {
//                    break;
//                }
//            }
//        }
//        return getLineString(charses);
//    }
//    public static String getLineString(char[][] charses){
//        StringBuilder builder=new StringBuilder("");
//        for(int i=0;i<charses.length;++i){
//            for(int j=0;j<charses[i].length;++j){
//                if (charses[i][j]!=0){
//                    builder.append(charses[i][j]);
//                }
//            }
//        }
//        return builder.toString();
//    }
//

    public static String convert(String s, int numRows) {
        if (numRows==1){
            return s;
        }
        StringBuilder builder=new StringBuilder("");
        int fetchSize=numRows*2-2,distance=(numRows-2)*2;
        int i=0;
        //第一行
        while (i<s.length()){
            builder.append(s.charAt(i));
            i+=fetchSize;
        }
        //2-(numRows-1)行，也就是不算最后一行
        for(int row=1;row<numRows-1;++row){
            i=row;
            while (i<s.length()){
                builder.append(s.charAt(i));
                if(i+distance<s.length()){
                    builder.append(s.charAt(i+distance));
                }
                i+=fetchSize;
            }
            distance-=2;
        }
        //最后一行
        i=numRows-1;
        while (i<s.length()){
            builder.append(s.charAt(i));
            i+=fetchSize;
        }
        return builder.toString();
    }

    public static void main(String[] args) {
        String s = "PAYPALISHIRING";
        String result = convert(s, 3);
        System.out.print(result);
    }
}
