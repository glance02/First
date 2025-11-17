import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Random;
import java.util.LinkedList;
import java.util.ArrayList;
import java.util.List;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import javax.sound.sampled.*;
import java.net.URL;

public class SnakeGame extends JFrame {
    // 游戏常量
    private static final int WIDTH = 800;
    private static final int HEIGHT = 650;
    private static final int GAME_WIDTH = 800;
    private static final int GAME_HEIGHT = 600;
    private static final int GRID_SIZE = 25;
    private static final int CELL_SIZE = GAME_WIDTH / GRID_SIZE;
    private static final int FPS = 60;
    private static final int INITIAL_DELAY = 1000 / FPS;
    
    // 游戏模式枚举
    public enum GameMode {
        CLASSIC("经典模式"),
        LEVEL("闯关模式"),
        INFINITE("无限模式");
        
        private final String displayName;
        
        GameMode(String displayName) {
            this.displayName = displayName;
        }
        
        public String getDisplayName() {
            return displayName;
        }
    }
    
    // 游戏状态
    private GameMode currentMode = GameMode.CLASSIC;
    private Difficulty currentDifficulty = Difficulty.MEDIUM;
    private LinkedList<Point> snake;
    private Point food;
    private Point specialFood; // 特殊食物（闯关模式）
    private char direction;
    private boolean running;
    private boolean paused;
    private int score;
    private int level;
    private int highScore;
    private List<HighScoreEntry> highScores;
    
    // UI组件
    private GamePanel gamePanel;
    private JLabel scoreLabel;
    private JLabel levelLabel;
    private JLabel highScoreLabel;
    private JButton startButton;
    private JButton pauseButton;
    private JComboBox<GameMode> modeComboBox;
    private JComboBox<Difficulty> difficultyComboBox;
    private JPanel controlPanel;
    
    // 游戏循环
    private Timer gameTimer;
    private long lastUpdateTime;
    private int updateDelay;
    
    // 动画效果
    private float backgroundHue = 0;
    private float pulsePhase = 0;
    private float foodPulse = 0;
    private List<Particle> particles = new ArrayList<>();
    
    // 音效
    private Clip eatSound;
    private Clip gameOverSound;
    private Clip levelUpSound;
    private boolean soundEnabled = true;
    
    // 难度枚举
    public enum Difficulty {
        EASY("简单", 150, 1),
        MEDIUM("中等", 100, 2),
        HARD("困难", 70, 3),
        EXTREME("极限", 40, 4);
        
        private final String displayName;
        private final int speed;
        private final int multiplier;
        
        Difficulty(String displayName, int speed, int multiplier) {
            this.displayName = displayName;
            this.speed = speed;
            this.multiplier = multiplier;
        }
        
        public String getDisplayName() {
            return displayName;
        }
        
        public int getSpeed() {
            return speed;
        }
        
        public int getMultiplier() {
            return multiplier;
        }
    }
    
    // 高分记录类
    public static class HighScoreEntry implements Serializable {
        private String name;
        private int score;
        private GameMode mode;
        private Difficulty difficulty;
        private long timestamp;
        
        public HighScoreEntry(String name, int score, GameMode mode, Difficulty difficulty) {
            this.name = name;
            this.score = score;
            this.mode = mode;
            this.difficulty = difficulty;
            this.timestamp = System.currentTimeMillis();
        }
        
        public String getName() { return name; }
        public int getScore() { return score; }
        public GameMode getMode() { return mode; }
        public Difficulty getDifficulty() { return difficulty; }
        public long getTimestamp() { return timestamp; }
    }
    
    // 粒子效果类
    private static class Particle {
        float x, y;
        float vx, vy;
        float size;
        Color color;
        int life;
        
        Particle(float x, float y, Color color) {
            this.x = x;
            this.y = y;
            this.vx = (float)(Math.random() * 4 - 2);
            this.vy = (float)(Math.random() * 4 - 2);
            this.size = (float)(Math.random() * 3 + 2);
            this.color = color;
            this.life = 30;
        }
        
        void update() {
            x += vx;
            y += vy;
            vy += 0.1f; // 重力
            life--;
            size *= 0.98f;
        }
        
        void draw(Graphics g) {
            if (life <= 0) return;
            g.setColor(new Color(color.getRed(), color.getGreen(), color.getBlue(), 
                                 (int)(255 * life / 30)));
            g.fillRect((int)x, (int)y, (int)size, (int)size);
        }
    }
    
    public SnakeGame() {
        super("贪吃蛇游戏 - 增强版");
        setSize(WIDTH, HEIGHT);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);
        setLocationRelativeTo(null);
        
        // 初始化高分榜
        loadHighScores();
        
        // 初始化音效
        initSounds();
        
        // 初始化游戏
        initGame();
        
        // 设置UI
        setupUI();
        
        // 设置键盘监听
        setupKeyListeners();
        
        // 启动动画循环
        startAnimationLoop();
    }
    
    private void initGame() {
        snake = new LinkedList<>();
        snake.add(new Point(GRID_SIZE / 2, GRID_SIZE / 2));
        direction = 'R';
        running = false;
        paused = false;
        score = 0;
        level = 1;
        updateDelay = currentDifficulty.getSpeed();
        generateFood();
        specialFood = null;
        particles.clear();
    }
    
    private void setupUI() {
        setLayout(new BorderLayout());
        
        // 获取适合中文显示的字体
        Font uiFont = getCompatibleFont("SimSun", "Microsoft YaHei", "SansSerif", Font.PLAIN, 12);
        Font uiFontBold = getCompatibleFont("SimSun", "Microsoft YaHei", "SansSerif", Font.BOLD, 12);
        Font infoFont = getCompatibleFont("SimSun", "Microsoft YaHei", "SansSerif", Font.BOLD, 16);
        
        // 控制面板
        controlPanel = new JPanel(new FlowLayout());
        controlPanel.setBackground(new Color(40, 40, 50));
        controlPanel.setPreferredSize(new Dimension(WIDTH, 50));
        
        // 游戏模式选择
        modeComboBox = new JComboBox<>(GameMode.values());
        modeComboBox.setRenderer(new DefaultListCellRenderer() {
            @Override
            public Component getListCellRendererComponent(JList<?> list, Object value, int index,
                                                        boolean isSelected, boolean cellHasFocus) {
                super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);
                if (value instanceof GameMode) {
                    setText(((GameMode)value).getDisplayName());
                }
                setFont(uiFont);
                return this;
            }
        });
        modeComboBox.addActionListener(e -> {
            currentMode = (GameMode)modeComboBox.getSelectedItem();
            resetGame();
        });
        modeComboBox.setFont(uiFont);
        
        // 难度选择
        difficultyComboBox = new JComboBox<>(Difficulty.values());
        difficultyComboBox.setRenderer(new DefaultListCellRenderer() {
            @Override
            public Component getListCellRendererComponent(JList<?> list, Object value, int index,
                                                        boolean isSelected, boolean cellHasFocus) {
                super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);
                if (value instanceof Difficulty) {
                    setText(((Difficulty)value).getDisplayName());
                }
                setFont(uiFont);
                return this;
            }
        });
        difficultyComboBox.addActionListener(e -> {
            currentDifficulty = (Difficulty)difficultyComboBox.getSelectedItem();
            updateDelay = currentDifficulty.getSpeed();
        });
        difficultyComboBox.setFont(uiFont);
        
        // 按钮
        startButton = new JButton("开始游戏");
        startButton.setBackground(new Color(76, 175, 80));
        startButton.setForeground(Color.WHITE);
        startButton.setFocusPainted(false);
        startButton.setFont(uiFontBold);
        startButton.addActionListener(e -> startGame());
        
        pauseButton = new JButton("暂停");
        pauseButton.setBackground(new Color(255, 152, 0));
        pauseButton.setForeground(Color.WHITE);
        pauseButton.setFocusPainted(false);
        pauseButton.setFont(uiFontBold);
        pauseButton.addActionListener(e -> togglePause());
        pauseButton.setEnabled(false);
        
        // 音效开关
        JToggleButton soundToggle = new JToggleButton("音效开");
        soundToggle.setBackground(new Color(33, 150, 243));
        soundToggle.setForeground(Color.WHITE);
        soundToggle.setFocusPainted(false);
        soundToggle.setFont(uiFontBold);
        soundToggle.setSelected(true);
        soundToggle.addActionListener(e -> {
            soundEnabled = soundToggle.isSelected();
            soundToggle.setText(soundEnabled ? "音效开" : "音效关");
        });
        
        // 高分榜按钮
        JButton highScoreButton = new JButton("高分榜");
        highScoreButton.setBackground(new Color(156, 39, 176));
        highScoreButton.setForeground(Color.WHITE);
        highScoreButton.setFocusPainted(false);
        highScoreButton.setFont(uiFontBold);
        highScoreButton.addActionListener(e -> showHighScores());
        
        // 添加组件到控制面板
        JLabel modeLabel = new JLabel("游戏模式:");
        modeLabel.setFont(uiFont);
        controlPanel.add(modeLabel);
        controlPanel.add(modeComboBox);
        
        JLabel diffLabel = new JLabel("难度:");
        diffLabel.setFont(uiFont);
        controlPanel.add(diffLabel);
        controlPanel.add(difficultyComboBox);
        controlPanel.add(startButton);
        controlPanel.add(pauseButton);
        controlPanel.add(soundToggle);
        controlPanel.add(highScoreButton);
        
        // 信息面板
        JPanel infoPanel = new JPanel(new GridLayout(1, 3));
        infoPanel.setBackground(new Color(30, 30, 40));
        infoPanel.setPreferredSize(new Dimension(WIDTH, 30));
        
        scoreLabel = new JLabel("分数: 0", JLabel.CENTER);
        scoreLabel.setForeground(Color.WHITE);
        scoreLabel.setFont(infoFont);
        
        levelLabel = new JLabel("关卡: 1", JLabel.CENTER);
        levelLabel.setForeground(Color.WHITE);
        levelLabel.setFont(infoFont);
        
        highScoreLabel = new JLabel("最高分: " + highScore, JLabel.CENTER);
        highScoreLabel.setForeground(Color.WHITE);
        highScoreLabel.setFont(infoFont);
        
        infoPanel.add(scoreLabel);
        infoPanel.add(levelLabel);
        infoPanel.add(highScoreLabel);
        
        // 游戏面板
        gamePanel = new GamePanel();
        gamePanel.setPreferredSize(new Dimension(GAME_WIDTH, GAME_HEIGHT));
        
        // 添加组件到主窗口
        add(controlPanel, BorderLayout.NORTH);
        add(gamePanel, BorderLayout.CENTER);
        add(infoPanel, BorderLayout.SOUTH);
    }
    
    private void setupKeyListeners() {
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (!running && e.getKeyCode() == KeyEvent.VK_SPACE) {
                    startGame();
                    return;
                }
                
                if (!running || paused) return;
                
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_UP:
                    case KeyEvent.VK_W:
                        if (direction != 'D') direction = 'U';
                        break;
                    case KeyEvent.VK_DOWN:
                    case KeyEvent.VK_S:
                        if (direction != 'U') direction = 'D';
                        break;
                    case KeyEvent.VK_LEFT:
                    case KeyEvent.VK_A:
                        if (direction != 'R') direction = 'L';
                        break;
                    case KeyEvent.VK_RIGHT:
                    case KeyEvent.VK_D:
                        if (direction != 'L') direction = 'R';
                        break;
                    case KeyEvent.VK_SPACE:
                    case KeyEvent.VK_P:
                        togglePause();
                        break;
                }
            }
        });
        
        // 确保窗口可以接收键盘事件
        setFocusable(true);
        setFocusTraversalKeysEnabled(false);
        requestFocusInWindow();
        
        // 添加窗口焦点监听器，确保窗口获得焦点时能够接收键盘事件
        addWindowFocusListener(new WindowAdapter() {
            @Override
            public void windowGainedFocus(WindowEvent e) {
                requestFocusInWindow();
            }
        });
    }
    
    private void startAnimationLoop() {
        gameTimer = new Timer(INITIAL_DELAY, e -> {
            if (running && !paused) {
                long currentTime = System.currentTimeMillis();
                if (currentTime - lastUpdateTime >= updateDelay) {
                    updateGame();
                    lastUpdateTime = currentTime;
                }
            }
            
            // 更新动画效果
            updateAnimations();
            
            // 重绘游戏面板
            gamePanel.repaint();
        });
        gameTimer.start();
    }
    
    private void updateAnimations() {
        // 更新背景色相
        backgroundHue = (backgroundHue + 0.2f) % 360;
        
        // 更新脉冲相位
        pulsePhase = (pulsePhase + 0.05f) % (float)(2 * Math.PI);
        
        // 更新食物脉冲
        foodPulse = (foodPulse + 0.1f) % (float)(2 * Math.PI);
        
        // 更新粒子
        particles.removeIf(p -> {
            p.update();
            return p.life <= 0;
        });
    }
    
    private void updateGame() {
        if (!running || paused) return;
        
        moveSnake();
        
        if (checkCollision()) {
            gameOver();
            return;
        }
        
        checkFood();
        
        // 闯关模式特殊逻辑
        if (currentMode == GameMode.LEVEL) {
            checkLevelProgress();
        }
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
        
        // 如果没有吃到食物，移除尾部
        if (!newHead.equals(food) && (specialFood == null || !newHead.equals(specialFood))) {
            snake.removeLast();
        }
    }
    
    private boolean checkCollision() {
        Point head = snake.getFirst();
        
        // 检查墙壁碰撞
        if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE) {
            return true;
        }
        
        // 检查自身碰撞
        for (int i = 1; i < snake.size(); i++) {
            if (head.equals(snake.get(i))) {
                return true;
            }
        }
        
        return false;
    }
    
    private void checkFood() {
        Point head = snake.getFirst();
        
        if (head.equals(food)) {
            int points = 10 * currentDifficulty.getMultiplier();
            score += points;
            updateScore();
            
            // 创建吃食物的粒子效果
            createEatParticles(food.x * CELL_SIZE + CELL_SIZE/2, 
                              food.y * CELL_SIZE + CELL_SIZE/2);
            
            // 播放音效
            playSound(eatSound);
            
            generateFood();
            
            // 闯关模式中，每5个食物生成一个特殊食物
            if (currentMode == GameMode.LEVEL && score % 50 == 0) {
                generateSpecialFood();
            }
        }
        
        // 检查特殊食物
        if (specialFood != null && head.equals(specialFood)) {
            int points = 50 * currentDifficulty.getMultiplier();
            score += points;
            updateScore();
            
            // 创建特殊粒子效果
            createSpecialEatParticles(specialFood.x * CELL_SIZE + CELL_SIZE/2, 
                                     specialFood.y * CELL_SIZE + CELL_SIZE/2);
            
            // 播放音效
            playSound(levelUpSound);
            
            specialFood = null;
        }
    }
    
    private void checkLevelProgress() {
        // 闯关模式：每100分升一级
        int newLevel = (score / 100) + 1;
        if (newLevel > level) {
            level = newLevel;
            levelLabel.setText("关卡: " + level);
            
            // 提升游戏速度
            updateDelay = Math.max(30, currentDifficulty.getSpeed() - level * 5);
            
            // 播放升级音效
            playSound(levelUpSound);
            
            // 创建升级特效
            createLevelUpEffect();
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
    
    private void generateSpecialFood() {
        Random random = new Random();
        Point newFood;
        
        do {
            newFood = new Point(random.nextInt(GRID_SIZE), random.nextInt(GRID_SIZE));
        } while (snake.contains(newFood) || newFood.equals(food));
        
        specialFood = newFood;
    }
    
    private void createEatParticles(int x, int y) {
        Color foodColor = new Color(255, 100, 100);
        for (int i = 0; i < 10; i++) {
            particles.add(new Particle(x, y, foodColor));
        }
    }
    
    private void createSpecialEatParticles(int x, int y) {
        Color specialColor = new Color(255, 215, 0); // 金色
        for (int i = 0; i < 20; i++) {
            particles.add(new Particle(x, y, specialColor));
        }
    }
    
    private void createLevelUpEffect() {
        // 创建升级特效
        Color[] colors = {Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, new Color(128, 0, 128)};
        for (int i = 0; i < 30; i++) {
            Color color = colors[i % colors.length];
            particles.add(new Particle(GAME_WIDTH/2, GAME_HEIGHT/2, color));
        }
    }
    
    private void updateScore() {
        scoreLabel.setText("分数: " + score);
        
        if (score > highScore) {
            highScore = score;
            highScoreLabel.setText("最高分: " + highScore);
        }
    }
    
    private void startGame() {
        initGame();
        running = true;
        paused = false;
        startButton.setText("重新开始");
        pauseButton.setEnabled(true);
        lastUpdateTime = System.currentTimeMillis();
    }
    
    private void togglePause() {
        if (!running) return;
        
        paused = !paused;
        pauseButton.setText(paused ? "继续" : "暂停");
    }
    
    private void resetGame() {
        running = false;
        paused = false;
        startButton.setText("开始游戏");
        pauseButton.setText("暂停");
        pauseButton.setEnabled(false);
        initGame();
        updateScore();
        levelLabel.setText("关卡: 1");
    }
    
    private void gameOver() {
        running = false;
        pauseButton.setEnabled(false);
        
        // 播放游戏结束音效
        playSound(gameOverSound);
        
        // 保存高分
        saveHighScore();
        
        // 显示游戏结束对话框
        String message = String.format("游戏结束！\n最终分数: %d\n按空格键重新开始", score);
        JOptionPane.showMessageDialog(this, message, "游戏结束", JOptionPane.INFORMATION_MESSAGE);
        
        resetGame();
    }
    
    private void saveHighScore() {
        String name = JOptionPane.showInputDialog(this, "恭喜！请输入您的名字：", "高分记录", JOptionPane.PLAIN_MESSAGE);
        if (name != null && !name.trim().isEmpty()) {
            highScores.add(new HighScoreEntry(name.trim(), score, currentMode, currentDifficulty));
            highScores.sort((a, b) -> Integer.compare(b.getScore(), a.getScore()));
            
            // 只保留前10名
            if (highScores.size() > 10) {
                highScores = highScores.subList(0, 10);
            }
            
            saveHighScores();
        }
    }
    
    private void showHighScores() {
        StringBuilder sb = new StringBuilder("=== 高分榜 ===\n\n");
        
        if (highScores.isEmpty()) {
            sb.append("暂无记录");
        } else {
            for (int i = 0; i < highScores.size(); i++) {
                HighScoreEntry entry = highScores.get(i);
                sb.append(String.format("%d. %s - %d分 (%s - %s)\n", 
                        i + 1, entry.getName(), entry.getScore(), 
                        entry.getMode().getDisplayName(), entry.getDifficulty().getDisplayName()));
            }
        }
        
        JOptionPane.showMessageDialog(this, sb.toString(), "高分榜", JOptionPane.INFORMATION_MESSAGE);
    }
    
    @SuppressWarnings("unchecked")
    private void loadHighScores() {
        try {
            if (Files.exists(Paths.get("snake_highscores.dat"))) {
                try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("snake_highscores.dat"))) {
                    highScores = (List<HighScoreEntry>) ois.readObject();
                }
            } else {
                highScores = new ArrayList<>();
            }
        } catch (Exception e) {
            highScores = new ArrayList<>();
        }
        
        // 获取最高分
        highScore = highScores.isEmpty() ? 0 : highScores.get(0).getScore();
    }
    
    private void saveHighScores() {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("snake_highscores.dat"))) {
            oos.writeObject(highScores);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    private void initSounds() {
        try {
            // 这里应该加载实际的音频文件
            // 由于没有实际的音频文件，我们创建空的音频片段
            eatSound = createEmptyClip();
            gameOverSound = createEmptyClip();
            levelUpSound = createEmptyClip();
        } catch (Exception e) {
            e.printStackTrace();
            eatSound = null;
            gameOverSound = null;
            levelUpSound = null;
        }
    }
    
    private Clip createEmptyClip() {
        try {
            AudioFormat format = new AudioFormat(44100, 16, 1, true, false);
            DataLine.Info info = new DataLine.Info(Clip.class, format);
            Clip clip = (Clip) AudioSystem.getLine(info);
            return clip;
        } catch (Exception e) {
            return null;
        }
    }
    
    private void playSound(Clip clip) {
        if (!soundEnabled || clip == null) return;
        
        try {
            if (clip.isRunning()) {
                clip.stop();
            }
            clip.setFramePosition(0);
            clip.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    private class GamePanel extends JPanel {
        public GamePanel() {
            setPreferredSize(new Dimension(GAME_WIDTH, GAME_HEIGHT));
        }
        
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2d = (Graphics2D) g;
            
            // 启用抗锯齿
            g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            
            // 绘制渐变背景
            drawGradientBackground(g2d);
            
            // 绘制动态光效
            drawDynamicLighting(g2d);
            
            // 绘制网格
            drawGrid(g2d);
            
            // 绘制食物
            if (food != null) {
                drawFood(g2d);
            }
            
            // 绘制特殊食物
            if (specialFood != null) {
                drawSpecialFood(g2d);
            }
            
            // 绘制蛇
            drawSnake(g2d);
            
            // 绘制粒子效果
            drawParticles(g2d);
            
            // 绘制游戏状态信息
            if (!running) {
                drawStartScreen(g2d);
            } else if (paused) {
                drawPauseScreen(g2d);
            }
        }
        
        private void drawGradientBackground(Graphics2D g2d) {
            // 创建动态渐变背景
            Color color1 = Color.getHSBColor(backgroundHue / 360, 0.3f, 0.2f);
            Color color2 = Color.getHSBColor((backgroundHue + 60) / 360, 0.3f, 0.3f);
            
            GradientPaint gradient = new GradientPaint(0, 0, color1, GAME_WIDTH, GAME_HEIGHT, color2);
            g2d.setPaint(gradient);
            g2d.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);
        }
        
        private void drawDynamicLighting(Graphics2D g2d) {
            // 绘制动态光效
            float pulse = (float) Math.sin(pulsePhase) * 0.5f + 0.5f;
            
            // 创建径向渐变
            Point center = new Point(GAME_WIDTH / 2, GAME_HEIGHT / 2);
            float radius = 200 + pulse * 50;
            
            RadialGradientPaint radialGradient = new RadialGradientPaint(
                center, radius,
                new float[] {0.0f, 0.5f, 1.0f},
                new Color[] {
                    new Color(1.0f, 1.0f, 1.0f, 0.1f * pulse),
                    new Color(1.0f, 1.0f, 1.0f, 0.05f * pulse),
                    new Color(1.0f, 1.0f, 1.0f, 0.0f)
                }
            );
            
            g2d.setPaint(radialGradient);
            g2d.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);
        }
        
        private void drawGrid(Graphics2D g2d) {
            g2d.setColor(new Color(255, 255, 255, 20));
            g2d.setStroke(new BasicStroke(1));
            
            for (int i = 0; i <= GRID_SIZE; i++) {
                int x = i * CELL_SIZE;
                int y = i * CELL_SIZE;
                
                g2d.drawLine(x, 0, x, GAME_HEIGHT);
                g2d.drawLine(0, y, GAME_WIDTH, y);
            }
        }
        
        private void drawSnake(Graphics2D g2d) {
            for (int i = 0; i < snake.size(); i++) {
                Point segment = snake.get(i);
                int x = segment.x * CELL_SIZE;
                int y = segment.y * CELL_SIZE;
                
                // 计算颜色渐变
                float hue = 120 / 360.0f; // 绿色
                float saturation = 0.8f;
                float brightness = 0.9f - (i * 0.5f / snake.size()); // 从头到尾逐渐变暗
                
                Color segmentColor = Color.getHSBColor(hue, saturation, brightness);
                
                // 绘制蛇身段
                g2d.setColor(segmentColor);
                g2d.fillRoundRect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4, 8, 8);
                
                // 蛇头特殊处理
                if (i == 0) {
                    // 绘制眼睛
                    g2d.setColor(Color.WHITE);
                    int eyeSize = CELL_SIZE / 6;
                    int eyeOffset = CELL_SIZE / 3;
                    
                    switch (direction) {
                        case 'U':
                            g2d.fillOval(x + eyeOffset, y + eyeOffset, eyeSize, eyeSize);
                            g2d.fillOval(x + CELL_SIZE - eyeOffset - eyeSize, y + eyeOffset, eyeSize, eyeSize);
                            break;
                        case 'D':
                            g2d.fillOval(x + eyeOffset, y + CELL_SIZE - eyeOffset - eyeSize, eyeSize, eyeSize);
                            g2d.fillOval(x + CELL_SIZE - eyeOffset - eyeSize, y + CELL_SIZE - eyeOffset - eyeSize, eyeSize, eyeSize);
                            break;
                        case 'L':
                            g2d.fillOval(x + eyeOffset, y + eyeOffset, eyeSize, eyeSize);
                            g2d.fillOval(x + eyeOffset, y + CELL_SIZE - eyeOffset - eyeSize, eyeSize, eyeSize);
                            break;
                        case 'R':
                            g2d.fillOval(x + CELL_SIZE - eyeOffset - eyeSize, y + eyeOffset, eyeSize, eyeSize);
                            g2d.fillOval(x + CELL_SIZE - eyeOffset - eyeSize, y + CELL_SIZE - eyeOffset - eyeSize, eyeSize, eyeSize);
                            break;
                    }
                }
            }
        }
        
        private void drawFood(Graphics2D g2d) {
            int x = food.x * CELL_SIZE + CELL_SIZE / 2;
            int y = food.y * CELL_SIZE + CELL_SIZE / 2;
            
            // 食物脉冲效果
            float pulse = (float) Math.sin(foodPulse) * 0.2f + 0.8f;
            int size = (int) ((CELL_SIZE / 2 - 2) * pulse);
            
            // 绘制食物光晕
            Color glowColor = new Color(255, 100, 100, 50);
            g2d.setColor(glowColor);
            g2d.fillOval(x - size - 5, y - size - 5, (size + 5) * 2, (size + 5) * 2);
            
            // 绘制食物主体
            GradientPaint foodGradient = new GradientPaint(
                x - size, y - size, Color.RED,
                x + size, y + size, Color.PINK
            );
            g2d.setPaint(foodGradient);
            g2d.fillOval(x - size, y - size, size * 2, size * 2);
        }
        
        private void drawSpecialFood(Graphics2D g2d) {
            int x = specialFood.x * CELL_SIZE + CELL_SIZE / 2;
            int y = specialFood.y * CELL_SIZE + CELL_SIZE / 2;
            
            // 特殊食物旋转效果
            float rotation = foodPulse * 2;
            
            // 绘制特殊食物光晕
            Color glowColor = new Color(255, 215, 0, 100);
            g2d.setColor(glowColor);
            g2d.fillOval(x - 15, y - 15, 30, 30);
            
            // 绘制星形特殊食物
            g2d.setColor(Color.YELLOW);
            g2d.translate(x, y);
            g2d.rotate(rotation);
            
            int[] xPoints = {0, -8, -3, -3, 3, 3, 8};
            int[] yPoints = {-10, -3, -3, 3, 3, -3, -3};
            
            g2d.fillPolygon(xPoints, yPoints, 7);
            g2d.rotate(-rotation);
            g2d.translate(-x, -y);
        }
        
        private void drawParticles(Graphics2D g2d) {
            for (Particle particle : particles) {
                particle.draw(g2d);
            }
        }
        
        private void drawStartScreen(Graphics2D g2d) {
            // 绘制半透明背景
            g2d.setColor(new Color(0, 0, 0, 150));
            g2d.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);
            
            // 获取兼容字体
            Font titleFont = SnakeGame.this.getCompatibleFont("SimSun", "Microsoft YaHei", "SansSerif", Font.BOLD, 48);
            Font subtitleFont = SnakeGame.this.getCompatibleFont("SimSun", "Microsoft YaHei", "SansSerif", Font.PLAIN, 20);
            Font textFont = SnakeGame.this.getCompatibleFont("SimSun", "Microsoft YaHei", "SansSerif", Font.PLAIN, 16);
            Font controlFont = SnakeGame.this.getCompatibleFont("SimSun", "Microsoft YaHei", "SansSerif", Font.PLAIN, 14);
            
            // 绘制标题
            g2d.setColor(Color.WHITE);
            g2d.setFont(titleFont);
            FontMetrics fm = g2d.getFontMetrics();
            String title = "贪吃蛇游戏";
            int titleX = (GAME_WIDTH - fm.stringWidth(title)) / 2;
            int titleY = GAME_HEIGHT / 2 - 50;
            g2d.drawString(title, titleX, titleY);
            
            // 绘制副标题
            g2d.setFont(subtitleFont);
            fm = g2d.getFontMetrics();
            String subtitle = "增强版 - " + currentMode.getDisplayName();
            int subtitleX = (GAME_WIDTH - fm.stringWidth(subtitle)) / 2;
            int subtitleY = titleY + 40;
            g2d.drawString(subtitle, subtitleX, subtitleY);
            
            // 绘制开始提示
            g2d.setFont(textFont);
            fm = g2d.getFontMetrics();
            String startText = "点击'开始游戏'或按空格键开始";
            int startX = (GAME_WIDTH - fm.stringWidth(startText)) / 2;
            int startY = subtitleY + 40;
            g2d.drawString(startText, startX, startY);
            
            // 绘制控制说明
            g2d.setFont(controlFont);
            fm = g2d.getFontMetrics();
            String controls = "使用方向键或WASD控制移动，空格键暂停";
            int controlsX = (GAME_WIDTH - fm.stringWidth(controls)) / 2;
            int controlsY = startY + 30;
            g2d.drawString(controls, controlsX, controlsY);
        }
        
        private void drawPauseScreen(Graphics2D g2d) {
            // 绘制半透明背景
            g2d.setColor(new Color(0, 0, 0, 150));
            g2d.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);
            
            // 获取兼容字体
            Font pauseFont = SnakeGame.this.getCompatibleFont("SimSun", "Microsoft YaHei", "SansSerif", Font.BOLD, 48);
            Font textFont = SnakeGame.this.getCompatibleFont("SimSun", "Microsoft YaHei", "SansSerif", Font.PLAIN, 20);
            
            // 绘制暂停文字
            g2d.setColor(Color.WHITE);
            g2d.setFont(pauseFont);
            FontMetrics fm = g2d.getFontMetrics();
            String pauseText = "游戏暂停";
            int pauseX = (GAME_WIDTH - fm.stringWidth(pauseText)) / 2;
            int pauseY = GAME_HEIGHT / 2;
            g2d.drawString(pauseText, pauseX, pauseY);
            
            // 绘制继续提示
            g2d.setFont(textFont);
            fm = g2d.getFontMetrics();
            String continueText = "点击'继续'按钮或按空格键继续游戏";
            int continueX = (GAME_WIDTH - fm.stringWidth(continueText)) / 2;
            int continueY = pauseY + 40;
            g2d.drawString(continueText, continueX, continueY);
        }
    }
    
    // 获取兼容字体的辅助方法
    private Font getCompatibleFont(String primaryFont, String fallbackFont, String defaultFont, int style, int size) {
        // 尝试使用首选字体
        Font font = new Font(primaryFont, style, size);
        if (!font.getFamily().equals("Dialog")) {
            return font;
        }
        
        // 尝试使用备用字体
        font = new Font(fallbackFont, style, size);
        if (!font.getFamily().equals("Dialog")) {
            return font;
        }
        
        // 使用默认字体
        return new Font(defaultFont, style, size);
    }
    
    // 静态版本的字体获取方法，用于在静态上下文中使用
    private static Font getCompatibleFontStatic(String primaryFont, String fallbackFont, String defaultFont, int style, int size) {
        // 尝试使用首选字体
        Font font = new Font(primaryFont, style, size);
        if (!font.getFamily().equals("Dialog")) {
            return font;
        }
        
        // 尝试使用备用字体
        font = new Font(fallbackFont, style, size);
        if (!font.getFamily().equals("Dialog")) {
            return font;
        }
        
        // 使用默认字体
        return new Font(defaultFont, style, size);
    }
    
    public static void main(String[] args) {
        // 设置系统外观
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        // 在事件调度线程中创建和显示GUI
        SwingUtilities.invokeLater(() -> {
            SnakeGame game = new SnakeGame();
            game.setVisible(true);
        });
    }
}
