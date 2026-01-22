import java.util.Scanner;
        class Car {
            int model_year;
            int mileage;
        public static void main(String[] args){
            Car C1=new Car();
            C1.model_year=2020;
            C1.mileage=15000;
            System.out.println("Model Year: " + C1.model_year);
            System.out.println("Mileage: " + C1.mileage);
            
            Car C2=new Car();
            C2.model_year=2021;
            C2.mileage=10000;
            System.out.println("Model Year: " + C2.model_year);
            System.out.println("Mileage: " + C2.mileage);

            }
    
}