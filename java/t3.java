import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class t3 {
    public static void main(String[] args) {
        //显示界面在线程中启动
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                setBasicGui();
            }
        });
    }

    public static void setBasicGui() {
        JFrame jf = new JFrame("求一元二次方程根");
        jf.setSize(350, 200);
        jf.setLocationRelativeTo(null);
        jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // 设置布局管理器为 BorderLayout
        jf.setLayout(new BorderLayout());

        // 添加标题标签并居中
        JLabel titleLabel = new JLabel("求一元二次方程根", JLabel.CENTER);
        titleLabel.setFont(new Font("Simsun", Font.BOLD, 16));
        jf.add(titleLabel, BorderLayout.NORTH);

        JPanel inputPanel = new JPanel(new GridLayout(3, 2, 5, 5));
        JPanel buttonPanel = new JPanel(new FlowLayout());

        // 创建输入框和标签
        JTextField textA = new JTextField(10);
        JTextField textB = new JTextField(10);
        JTextField textC = new JTextField(10);

        //使用匿名内部类来简化代码
        inputPanel.add(new JLabel("请输入系数a:"));
        inputPanel.add(textA);
        inputPanel.add(new JLabel("请输入系数b:"));
        inputPanel.add(textB);
        inputPanel.add(new JLabel("请输入系数c:"));
        inputPanel.add(textC);

        // 创建按钮
        JButton solveButton = new JButton("求根");
        JButton clearButton = new JButton("清空");

        //与事件源合二为一
        ExitButton exitButton = new ExitButton("退出");

        // 添加按钮到按钮面板
        buttonPanel.add(solveButton);
        buttonPanel.add(clearButton);
        buttonPanel.add(exitButton);

        // 添加组件到窗口
        jf.add(inputPanel, BorderLayout.CENTER);
        jf.add(buttonPanel, BorderLayout.SOUTH);

        // 按钮事件处理，使用匿名内部类
        solveButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    double a = Double.parseDouble(textA.getText());
                    double b = Double.parseDouble(textB.getText());
                    double c = Double.parseDouble(textC.getText());
                    f equation = new f(a, b, c);
                    String result = equation.cal();
                    JOptionPane.showMessageDialog(jf, result, "求解结果", JOptionPane.INFORMATION_MESSAGE);
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(jf, "请输入有效的数字", "输入错误", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

        // 使用 Lambda 表达式
        clearButton.addActionListener(e -> {
            textA.setText("");
            textB.setText("");
            textC.setText("");
        });
        
        jf.setVisible(true);
    }
}

class f {
    private double a, b, c;

    public f(double a, double b, double c) {
        this.a = a;
        this.b = b;
        this.c = c;
    }

    public String cal() {
        if (a == 0) {
            return "系数不能为0";
        }
        double deta = b * b - 4 * a * c;
        if (deta > 0) {
            double root1 = (-b + Math.sqrt(deta)) / (2 * a);
            double root2 = (-b - Math.sqrt(deta)) / (2 * a);
            return " x1 = " + root1 + ", x2 = " + root2;
        } else if (deta == 0) {
            double root = -b / (2 * a);
            return " x = " + root;
        } else {
            return "方程无实根";
        }
    }
}

class ExitButton extends JButton {
    public ExitButton(String text) {
        super(text);
    }
    
    @Override
    protected void fireActionPerformed(ActionEvent event) {
        System.exit(0);
    }
}
