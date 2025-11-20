
public class Test {
    public static void main(String arg[]) {
        Rdemo rd = new Rdemo();
        Thread t1 = new Tdemo();
        Thread t2 = new Thread(rd);
        t1.start();
        t2.start();
    }
}

class Tdemo extends Thread {
    private int stack = 5;

    public void run() {
        for (int i = 0; i < 10; i++)
            System.out.println("the value of stack is: " + (--stack));
    }
}

class Rdemo implements Runnable {
    private int stack = 5;

    public void run() {
        for (int i = 0; i < 10; i++)
            System.out.println("the value of stack is: " + (--stack));
    }
}