class Car1 {
    int speed = 500;   
}

class BMW extends Car1 {
    void showSpeed() {
        int s = super.speed;   
            System.out.println("Speed: " + s);
    }

    public static void main(String[] args) {
        BMW obj = new BMW();
        obj.showSpeed();
    }
}