import java.util.ArrayList;
import java.util.Iterator;
import java.util.function.Consumer;
import java.util.LinkedList;
import java.util.List;

public class chapter7 {
    public static void main(String[] args) {
        //泛型定义集合
        List<String> list=new LinkedList<>();
        //添加数据
        list.add("Hello");
        list.add("World");
        list.add("whee!");
        list.add("Hello");

        list.forEach(new Consumer<String>() {
            public void accept(String s) {
                System.out.println(s);
            }
        });
        String str="";
        list.forEach(s->{
            System.out.println(s);
        });

        list.forEach(System.out::println);
    }
}
