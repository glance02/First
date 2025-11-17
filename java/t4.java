public class t4 {
    public static void main(String[] args) {
        // 创建银行账户，初始余额为 1000 元
        BankAccount account = new BankAccount(1000);

        System.out.println("初始账户余额：" + account.getBalance() + " 元\n");

        // 创建存钱线程和取钱线程
        Thread giveMoneyMan = new DepositThread("存钱者", account, 500);
        Thread takeMoneyMan = new WithdrawThread("取钱者", account, 300);

        // 启动两个线程
        giveMoneyMan.start();
        takeMoneyMan.start();

        // 等待两个线程完成
        try {
            giveMoneyMan.join();
            takeMoneyMan.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("\n最终账户余额：" + account.getBalance() + " 元");
    }
}
// 银行账户类
class BankAccount {
    private double balance;
    public BankAccount(double initialBalance) {
        this.balance = initialBalance;
    }
    
    // 存钱方法
    public synchronized void deposit(double amount) {
        System.out.println(Thread.currentThread().getName() + " 开始存钱 " + amount + " 元");
        try {
            Thread.sleep(1000); // 模拟操作时间
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        balance += amount;
        System.out.println(Thread.currentThread().getName() + " 存钱完成，当前余额：" + balance + " 元");
    }

    // 取钱方法
    public synchronized void withdraw(double amount) {
        System.out.println(Thread.currentThread().getName() + " 开始取钱 " + amount + " 元");
        try {
            Thread.sleep(1000); // 模拟操作时间
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        if (balance >= amount) {
            balance -= amount;
            System.out.println(Thread.currentThread().getName() + " 取钱完成，当前余额：" + balance + " 元");
        } else {
            System.out.println(Thread.currentThread().getName() + " 余额不足，取钱失败！当前余额：" + balance + " 元");
        }
    }

    // 获取余额
    public synchronized double getBalance() {
        return balance;
    }
}

// 存钱线程
class DepositThread extends Thread {
    private BankAccount account;
    private double amount;

    public DepositThread(String name, BankAccount account, double amount) {
        super(name);
        this.account = account;
        this.amount = amount;
    }

    @Override
    public void run() {
        for (int i = 0; i < 3; i++) {
            account.deposit(amount);
            try {
                Thread.sleep(500); // 线程间隔时间
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

// 取钱线程
class WithdrawThread extends Thread {
    private BankAccount account;
    private double amount;

    public WithdrawThread(String name, BankAccount account, double amount) {
        super(name);
        this.account = account;
        this.amount = amount;
    }

    @Override
    public void run() {
        for (int i = 0; i < 3; i++) {
            account.withdraw(amount);
            try {
                Thread.sleep(500); // 线程间隔时间
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
