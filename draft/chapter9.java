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