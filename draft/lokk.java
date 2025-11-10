import javax.swing.*;
import java.awt.*;

public class lokk {
    public static void main(String[] args) {
        // 需要导入 javax.swing.*
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 100; i++) {
                showAutoCloseDialog("哈基涂哈基涂");
            }
        });

        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 100; i++) {
                showAutoCloseDialog("我会永远看着你!!");
            }
        });

        Thread t3 = new Thread(() -> {
            for (int i = 0; i < 100; i++) {
                showAutoCloseDialog("你永远别想逃出我的眼睛!!");
            }
        });

        t1.start();
        t2.start();
        t3.start();
    }

    // 弹出自动关闭的提示框
    public static void showAutoCloseDialog(String message) {
        JOptionPane pane = new JOptionPane(message, javax.swing.JOptionPane.INFORMATION_MESSAGE);
        JDialog dialog = pane.createDialog(null, "视奸");
        dialog.setModal(false);
        // 随机位置
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        int width = dialog.getWidth();
        int height = dialog.getHeight();
        int x = (int) (Math.random() * (screenSize.width - width));
        int y = (int) (Math.random() * (screenSize.height - height));
        dialog.setLocation(x, y);
        dialog.setVisible(true);
        new Thread(() -> {
            try {
                Thread.sleep(2000); // 2秒后关闭
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            dialog.setVisible(false);
            dialog.dispose();
        }).start();
    }
    
}
