import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Random;
import java.util.LinkedList;

public class SnakeGame extends JFrame {
    private static final int WIDTH = 600;
    private static final int HEIGHT = 600;
    private static final int GRID_SIZE = 20;
    private static final int CELL_SIZE = WIDTH / GRID_SIZE;
    
    private LinkedList<Point> snake;
    private Point food;
    private char direction;
    private boolean running;
    private int score;
    
    private GamePanel gamePanel;
    private JLabel scoreLabel;
    
    public SnakeGame() {
        setTitle("贪吃蛇游戏");
        setSize(WIDTH, HEIGHT + 50);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);
        setLocationRelativeTo(null);
        
        initGame();
        setupUI();
        
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                // 空格键用于重新开始游戏，无论游戏是否运行都应该响应
                if (e.getKeyCode() == KeyEvent.VK_SPACE) {
                    if (!running) {
                        initGame();
                        running = true;
                        scoreLabel.setText("分数: " + score);
                        gamePanel.repaint();
                    }
                    return;
                }
                
                // 其他按键只在游戏运行时响应
                if (!running) return;
                
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_UP:
                        if (direction != 'D') direction = 'U';
                        break;
                    case KeyEvent.VK_DOWN:
                        if (direction != 'U') direction = 'D';
                        break;
                    case KeyEvent.VK_LEFT:
                        if (direction != 'R') direction = 'L';
                        break;
                    case KeyEvent.VK_RIGHT:
                        if (direction != 'L') direction = 'R';
                        break;
                }
            }
        });
        
        Timer timer = new Timer(150, e -> {
            if (running) {
                moveSnake();
                checkCollision();
                checkFood();
                gamePanel.repaint();
            }
        });
        timer.start();
    }
    
    private void initGame() {
        snake = new LinkedList<>();
        snake.add(new Point(GRID_SIZE / 2, GRID_SIZE / 2));
        direction = 'R';
        running = true;
        score = 0;
        generateFood();
    }
    
    private void setupUI() {
        setLayout(new BorderLayout());
        
        scoreLabel = new JLabel("分数: " + score, JLabel.CENTER);
        scoreLabel.setFont(new Font("Arial", Font.BOLD, 20));
        add(scoreLabel, BorderLayout.NORTH);
        
        gamePanel = new GamePanel();
        add(gamePanel, BorderLayout.CENTER);
    }
    
    private void moveSnake() {
        Point head = snake.getFirst();
        Point newHead = new Point(head);
        
        switch (direction) {
            case 'U':
                newHead.y--;
                break;
            case 'D':
                newHead.y++;
                break;
            case 'L':
                newHead.x--;
                break;
            case 'R':
                newHead.x++;
                break;
        }
        
        snake.addFirst(newHead);
        snake.removeLast();
    }
    
    private void checkCollision() {
        Point head = snake.getFirst();
        
        // 检查墙壁碰撞
        if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE) {
            gameOver();
            return;
        }
        
        // 检查自身碰撞
        for (int i = 1; i < snake.size(); i++) {
            if (head.equals(snake.get(i))) {
                gameOver();
                return;
            }
        }
    }
    
    private void checkFood() {
        Point head = snake.getFirst();
        
        if (head.equals(food)) {
            score += 10;
            scoreLabel.setText("分数: " + score);
            
            // 增加蛇的长度
            Point tail = snake.getLast();
            snake.addLast(new Point(tail));
            
            generateFood();
        }
    }
    
    private void generateFood() {
        Random random = new Random();
        Point newFood;
        
        do {
            newFood = new Point(random.nextInt(GRID_SIZE), random.nextInt(GRID_SIZE));
        } while (snake.contains(newFood));
        
        food = newFood;
    }
    
    private void gameOver() {
        running = false;
        JOptionPane.showMessageDialog(this, "游戏结束！\n最终分数: " + score + "\n按空格键重新开始", 
                                    "游戏结束", JOptionPane.INFORMATION_MESSAGE);
    }
    
    private class GamePanel extends JPanel {
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            
            // 设置背景
            g.setColor(Color.BLACK);
            g.fillRect(0, 0, WIDTH, HEIGHT);
            
            // 绘制网格线
            g.setColor(Color.DARK_GRAY);
            for (int i = 0; i <= GRID_SIZE; i++) {
                g.drawLine(i * CELL_SIZE, 0, i * CELL_SIZE, HEIGHT);
                g.drawLine(0, i * CELL_SIZE, WIDTH, i * CELL_SIZE);
            }
            
            // 绘制蛇
            g.setColor(Color.GREEN);
            for (int i = 0; i < snake.size(); i++) {
                Point segment = snake.get(i);
                if (i == 0) {
                    // 蛇头用更亮的颜色
                    g.setColor(new Color(0, 255, 0));
                } else {
                    g.setColor(new Color(0, 200, 0));
                }
                g.fillRect(segment.x * CELL_SIZE + 1, segment.y * CELL_SIZE + 1, 
                           CELL_SIZE - 2, CELL_SIZE - 2);
            }
            
            // 绘制食物
            g.setColor(Color.RED);
            g.fillOval(food.x * CELL_SIZE + 2, food.y * CELL_SIZE + 2, 
                      CELL_SIZE - 4, CELL_SIZE - 4);
            
            // 如果游戏结束，显示游戏结束文字
            if (!running) {
                g.setColor(Color.WHITE);
                g.setFont(new Font("Arial", Font.BOLD, 40));
                FontMetrics fm = g.getFontMetrics();
                String text = "游戏结束";
                int x = (WIDTH - fm.stringWidth(text)) / 2;
                int y = HEIGHT / 2;
                g.drawString(text, x, y);
                
                g.setFont(new Font("Arial", Font.PLAIN, 20));
                fm = g.getFontMetrics();
                text = "按空格键重新开始";
                x = (WIDTH - fm.stringWidth(text)) / 2;
                y = HEIGHT / 2 + 40;
                g.drawString(text, x, y);
            }
        }
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            SnakeGame game = new SnakeGame();
            game.setVisible(true);
        });
    }
}
