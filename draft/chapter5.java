import java.util.*;

public class chapter5 {
    public static void main(String[] args) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("Hello from a thread!");
            }
        }).start();

        new myinf() {
            @Override
            public void cmp() {
                System.out.println("Anonymous class implementing myinf");
            }
        }.cmp();
    }
}

interface myinf{
    void cmp();
}

