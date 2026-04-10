package mediscanx;

import java.util.Map;

public class AIAssistant {
    private final InventoryManager inventoryManager;

    public AIAssistant(InventoryManager inventoryManager) {
        this.inventoryManager = inventoryManager;
    }

    public String answer(String query) {
        String q = query.toLowerCase();
        if (q.contains("profit")) {
            return "Total profit: ₹" + inventoryManager.getTotalProfit();
        }
        if (q.contains("reorder") || q.contains("expiring")) {
            Map<String, Integer> low = inventoryManager.lowStock(5);
            return low.isEmpty() ? "No reorder needed" : "Reorder these barcodes: " + low;
        }
        if (q.contains("stock")) {
            return "Ask with barcode in app to get exact stock.";
        }
        return "Try queries: profit, suggest reorder, check stock";
    }
}
