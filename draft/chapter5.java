import java.util.*;

public class chapter5 {
    public static void main(String[] args) {
        List<String> list = Arrays.asList("Apple", "Banana", "Orange");

        // 传统方式
        for (String fruit : list) {
            System.out.println(fruit);
        }

        // Lambda方式
        list.forEach(fruit ->System.out.println(fruit));

        // 方法引用方式
        list.forEach(System.out::println);
    }
}

interface myinf {
    void cmp();
}
