import java.util.*;

public class JavaSortMethods {
    public static void main(String[] args) {
        System.out.println("Java中重写排序规则的几种方法\n");
        
        // 创建测试数据
        List<Person> people = Arrays.asList(
            new Person("张三", 25),
            new Person("李四", 20),
            new Person("王五", 30),
            new Person("赵六", 25)
        );
        
        System.out.println("原始数据:");
        people.forEach(System.out::println);
        
        // 方法1: 使用Comparable接口
        System.out.println("\n方法1: 使用Comparable接口(按年龄升序)");
        List<Person> list1 = new ArrayList<>(people);
        list1.sort(null);//如果传入null，则使用元素的自然排序
        // Collections.sort(list1);
        list1.forEach(System.out::println);
        
        // 方法2: 使用匿名内部类实现Comparator
        System.out.println("\n方法2: 使用匿名内部类实现Comparator(按姓名排序)");
        List<Person> list2 = new ArrayList<>(people);
        Collections.sort(list2, new Comparator<Person>() {
            @Override
            public int compare(Person p1, Person p2) {
                return p1.getName().compareTo(p2.getName());
            }
        });
        list2.forEach(System.out::println);
        
        // 方法3: 使用Lambda表达式
        System.out.println("\n方法3: 使用Lambda表达式(按年龄降序)");
        List<Person> list3 = new ArrayList<>(people);
        Collections.sort(list3, (p1, p2) -> p2.getAge() - p1.getAge());
        list3.forEach(System.out::println);
        
        // 方法4: 使用Comparator.comparing方法
        System.out.println("\n方法4: 使用Comparator.comparing(按年龄升序)");
        List<Person> list4 = new ArrayList<>(people);
        list4.sort(Comparator.comparing(Person::getAge));
        list4.forEach(System.out::println);
        
        // 方法5: 多条件排序
        System.out.println("\n方法5: 多条件排序(先按年龄升序，年龄相同按姓名升序)");
        List<Person> list5 = new ArrayList<>(people);
        list5.sort(Comparator.comparing(Person::getAge)
                             .thenComparing(Person::getName));
        list5.forEach(System.out::println);
        
        // 方法6: 自定义比较器类
        System.out.println("\n方法6: 自定义比较器类(按姓名长度排序)");
        List<Person> list6 = new ArrayList<>(people);
        Collections.sort(list6, new NameLengthComparator());
        list6.forEach(System.out::println);
    }
}

// 1. 实现Comparable接口，让类自身具备比较能力
class Person implements Comparable<Person> {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String getName() {
        return name;
    }
    
    public int getAge() {
        return age;
    }
    
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
    
    // 重写compareTo方法，定义自然排序规则
    @Override
    public int compareTo(Person other) {
        // 按年龄升序排序
        return this.age - other.age;
    }
}

// 6. 自定义比较器类
class NameLengthComparator implements Comparator<Person> {
    @Override
    public int compare(Person p1, Person p2) {
        // 按姓名长度排序
        return p1.getName().length() - p2.getName().length();
    }
}