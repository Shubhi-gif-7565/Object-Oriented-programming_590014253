class T1 extends Thread {
    public void run() {
        for (int i = 1; i <= 5; i++) {
            System.out.println("T1: " + i);
        }
    }
}

class T2 extends Thread {
    public void run() {
        for (int i = 6; i <= 10; i++) {
            System.out.println("T2: " + i);
        }
    }
}

public class Thread1 {
    public static void main(String[] args) {
        T1 t1 = new T1();
        T2 t2 = new T2();

        t1.start();

        try {
            t1.join(); 
        } catch (InterruptedException e) {
            System.out.println(e);
        }

        t2.start();
    }
}