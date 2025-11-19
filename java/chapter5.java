import java.util.*;

public class chapter5 {
    public static void main(String[] args) {
        List<Point> list = Arrays.asList(new Point(1,2), new Point(3,4), new Point(5,6), new Point(7,8));

        // Iterator<Point> it = list.iterator();
        // while(it.hasNext()){
        //     System.out.println(it.next().getX() + "," + it.next().getY());
        // }

        list.sort(new Comparator<Point>() {
            @Override
            public int compare(Point p1, Point p2) {
                return p1.getX() - p2.getX();
            }
        });

        for(Point p : list){
            System.out.println(p.getX() + "," + p.getY());
        }
    }
}

interface myinf {
    void cmp();
}

class Point {
    private int x, y;
    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
    int getX() {return x;}
    int getY() {return y;}
 }
