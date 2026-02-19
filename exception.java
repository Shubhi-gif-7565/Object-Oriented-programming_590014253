import java.util.Scanner;

// Custom Exception (no super used)
class InvalidDataException extends java.lang.Exception {
    String message;

    public InvalidDataException(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}

// Employee class
class Employee {
    private String name;
    private int age;
    private float salary;

    public Employee(String name, int age, float salary) throws InvalidDataException {

        if (name.length() > 20) {
            throw new InvalidDataException("Name must be maximum 20 characters.");
        }

        if (age <= 5) {
            throw new InvalidDataException("Age must be greater than 5.");
        }

        if (salary <= 12) {
            throw new InvalidDataException("Salary must be greater than 12 LPA.");
        }

        this.name = name;
        this.age = age;
        this.salary = salary;
    }

    public void display() {
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("Salary: " + salary + " LPA");
    }
}

// Public class (file name: Exception.java)
public class Exception {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        try {
            System.out.print("Enter Name: ");
            String name = sc.nextLine();

            System.out.print("Enter Age: ");
            int age = sc.nextInt();

            System.out.print("Enter Salary (LPA): ");
            float salary = sc.nextFloat();

            Employee emp = new Employee(name, age, salary);
            emp.display();

            System.out.println("data inserted successful");
        } 
        catch (InvalidDataException e) {
            System.out.println("Exception: " + e.getMessage());
        } 
        catch (java.lang.Exception e) {
            System.out.println("Invalid input.");
        } 
        finally {
            sc.close();
        }
    }
}
