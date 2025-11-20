import javax.swing.*;
import java.awt.*;

public class Main extends JFrame {
	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			public void run() {
				new Main().setVisible(true);
			}
		});
	}

	public Main() {
		setTitle("电话簿");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setSize(300, 300);
		// 初始化组件
		JTextField name = new JTextField();
		JTextField company = new JTextField();
		JTextField position = new JTextField();
		JTextField show = new JTextField();
		JPanel jp1 = new JPanel(new GridLayout(3, 2));
		jp1.add(new JLabel("姓名"));
		jp1.add(name);
		jp1.add(new JLabel("公司"));
		jp1.add(company);
		jp1.add(new JLabel("地址"));
		jp1.add(position);

		JPanel jp2 = new JPanel(new GridLayout(1, 2));
		JButton submit = new JButton("提交");
		JButton clearbtn = new JButton("清空");
		jp2.add(submit);
		jp2.add(clearbtn);

		add(jp1, BorderLayout.NORTH);
		add(show, BorderLayout.CENTER);
		add(jp2, BorderLayout.SOUTH);

		// 加入按键绑定
		submit.addActionListener(e -> {
			String uname = name.getText();
			String ucompany = company.getText();
			String uposition = position.getText();

			String totInfo = "姓名：" + uname + "\n公司：" + ucompany + "\n地址" + uposition;
			show.setText(totInfo);
		});

		clearbtn.addActionListener(e -> {
			name.setText("");
			company.setText("");
			position.setText("");
			show.setText("");
		});
	}
}