class Subject {
    int sum(int a, int b) {
        return a + b;
    }
}

class BMW extends Subject {
    @Override
    int sum(int a, int b) {
        return a - b;
    }
    int display(){
        int v = super.sum(3,1);
        return v;
    }
}

class Main1 {
    public static void main(String[] args) {
        Subject d = new Subject();
        BMW e = new BMW(); 
        System.out.println(e.sum(8, 3));
        System.out.println(e.display());
    }
}

