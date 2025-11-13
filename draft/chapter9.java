import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;

public class chapter9 {
    public static void main(String[] args) {
        //创建线程对象
        MyThread t1 = new MyThread();
        //启动线程
        t1.start(); 

        new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                System.out.println("Anonymous Runnable running: " + i);
            }
        }).start();

        Callable<String> c1=new MyCallable(100);
        FutureTask<String> f1=new FutureTask<>(c1);
        //启动线程
        new Thread(f1).start();

        try {
            System.out.println("Callable result: " + f1.get());
        } catch (Exception e) {
            e.printStackTrace();
        } 
    }
}

class MyCallable implements Callable<String>{
    private int n;
    public MyCallable(int n){
        this.n = n;
    }
    public String call(){
        int sum = 0;
        for (int i = 0; i <= n; i++) {
            sum += i;
        }
        return String.valueOf(sum);
    }
}

//定义一个线程任务类
class MyRunnable implements Runnable {
    @Override
    public void run() {
        //线程要执行的代码
        for (int i = 0; i < 10; i++) {
            System.out.println("Runnable running: " + i);
        }
    }
}

class MyThread extends Thread{
    //重写run方法
    @Override
    public void run() {
        //线程要执行的代码
        for (int i = 0; i < 10; i++) {
            System.out.println("Thread running: " + i);
        }
    }
}