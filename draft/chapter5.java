import java.util.*;

public class chapter5 {
    public static void main(String[] args) {
        List<String> list = Arrays.asList("zoe","Apple", "Banana", "Orange");

        Iterator<String> it = list.iterator();
        while(it.hasNext()){
            System.out.println(it.next());
        }

        list.sort(null);

        list.forEach(System.out::println);
    }
}

interface myinf {
    void cmp();
}
