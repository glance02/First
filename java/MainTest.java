public class MainTest {
   public static void main(String[] args) {
        A a1 = new A();
        A a2 = new B();
        B b = new B();
        C c = new C();
        D d = new D();
        B e=new C();

        System.out.println(a1.Show(e));
        System.out.println(e instanceof C);
   }
}


class A {
    public String Show(D obj) {
        return "A and D";
    }

    public String Show(A obj) {
        return "A and A";
    }

    public String Show(B obj) {
        return "A and B";
    }

    public String Show(C obj) {
        return "A and C";
    }
}

class B extends A {
    public String Show(B obj) {
        return "B and B";
    }

    public String Show(A obj) {
        return "B and A";
    }
}

class C extends B {
    public String Show(C obj) {
        return "C and C";
    }

    public String Show(B obj) {
        return "C and B";
    }
}

class D extends B {
    public String Show(D obj) {
        return "D and D";
    }

    public String Show(B obj) {
        return "D and B";
    }
}