package mediscanx;

public class Main {
    public static void main(String[] args) {
        InventoryManager manager = new InventoryManager();
        Medicine crocin = new Medicine("8901234567890", "Crocin 650", "GSK", 34.0, "Paracetamol 650mg");
        manager.addMedicine(crocin, 20, 28.0);

        double profit = manager.sellMedicine("8901234567890", 2, null);
        AIAssistant assistant = new AIAssistant(manager);

        System.out.println("Sale profit: ₹" + profit);
        System.out.println(assistant.answer("profit today"));
        System.out.println(assistant.answer("suggest reorder"));
    }
}
