import java.util.*;
import java.math.BigInteger;

public class t1 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();

        int ans = gcd(a, b);
        System.out.println("自行实现的辗转相除的结果：" + ans);

        int ans2 = BigInteger.valueOf(a).gcd(BigInteger.valueOf(b)).intValue();
        System.out.println("BigInteger调用的结果：" + ans2);

        if (ans == ans2)
            System.out.println("两种方法结果一致");
        else
            System.out.println("两种方法结果不一致");

        sc.close();
    }

    // 利用熟悉的递归来实现辗转相除法
    public static int gcd(int a, int b) {
        if (b == 0) {
            return a;
        }
        return gcd(b, a % b);// 实现辗转相除
    }
}