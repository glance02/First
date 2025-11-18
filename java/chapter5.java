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

        Queue<Integer> queue = new LinkedList<>();

        double d=2.5/0;

        int a[]={1,2,3};
        System.out.println(a.length);
        
    }
}

interface myinf {
    void cmp();
}
