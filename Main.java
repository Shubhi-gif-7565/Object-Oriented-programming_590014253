class Subject {
    int sum(int a, int b) {
        return a + b;
    }
}

class Main {
    public static void main(String[] args) {
        Subject d = new Subject();
        System.out.println(d.sum(1, 3));  // Pass values directly in order
    }
}
