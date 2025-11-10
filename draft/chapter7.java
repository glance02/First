import java.util.ArrayList;
import java.util.Iterator;
import java.util.function.Consumer;

public class chapter7 {
    public static void main(String[] args) {
        //泛型定义集合
        ArrayList<String> list=new ArrayList<>();
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
