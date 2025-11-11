import java.util.*;
public class chapter7 {
    public static void main(String[] args) {
        Set<Student> set = new HashSet<>();
        set.add(new Student("Apple", 20));
        set.add(new Student("Banana", 22));
        set.add(new Student("Orange", 21));
        set.add(new Student("Apple", 20));
        set.add(new Student("Cheeze", 23));
        System.out.println(set);
    }
}

class Student {
    String name;
    int age;

    public Student(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public String toString() {
        return "Student{" +
                "name='" + name + '\'' +
                ", age=" + age +
                '}'+'\n';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Student student = (Student) o;
        return age == student.age && Objects.equals(name, student.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}
