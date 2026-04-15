import java.util.*;

public class JavaSortMethods {
    public static void main(String[] args) {
        System.out.println("Java中重写排序规则的几种方法\n");

        // 创建测试数据
        List<Person> people = Arrays.asList(
                new Person("张三", 25),
                new Person("李四", 20),
                new Person("王五", 30),
                new Person("赵六", 25));

        System.out.println("原始数据:");
        people.forEach(System.out::println);

        Collections.sort(people, (p1, p2) -> {
            return p2.getAge() - p1.getAge();
        });
        System.out.println("---------------");
        for (Person p : people) {
            System.out.println(p);
        }
        System.out.println(Collections.binarySearch(people, new Person("赵六", 25)));
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

    @Override
    public int compareTo(Person other) {
        // 先按年龄比较
        int ageCompare = Integer.compare(this.age, other.age);
        if (ageCompare != 0) {
            return ageCompare;
        }
        // 年龄相同再按姓名比较
        return this.name.compareTo(other.name);
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