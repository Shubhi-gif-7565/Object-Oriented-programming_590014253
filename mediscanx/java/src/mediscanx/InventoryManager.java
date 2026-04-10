package mediscanx;

import java.util.HashMap;
import java.util.Map;

public class InventoryManager {
    private final Map<String, Medicine> medicineByBarcode = new HashMap<>();
    private final Map<String, Integer> quantityByBarcode = new HashMap<>();
    private final Map<String, Double> costByBarcode = new HashMap<>();
    private double totalProfit = 0.0;

    public void addMedicine(Medicine medicine, int quantity, double costPrice) {
        medicineByBarcode.put(medicine.getBarcode(), medicine);
        quantityByBarcode.put(medicine.getBarcode(), quantityByBarcode.getOrDefault(medicine.getBarcode(), 0) + quantity);
        costByBarcode.put(medicine.getBarcode(), costPrice);
    }

    public double sellMedicine(String barcode, int quantity, Double sellingPriceOverride) {
        int current = quantityByBarcode.getOrDefault(barcode, 0);
        if (quantity <= 0 || current < quantity) {
            throw new IllegalArgumentException("Invalid quantity for sale");
        }
        Medicine med = medicineByBarcode.get(barcode);
        if (med == null) {
            throw new IllegalArgumentException("Medicine not found");
        }

        Double cpValue = costByBarcode.get(barcode);
        if (cpValue == null) {
            throw new IllegalStateException("Cost price missing for barcode: " + barcode);
        }
        double cp = cpValue;
        double sp = sellingPriceOverride != null ? sellingPriceOverride : med.getMrp();
        double profit = (sp - cp) * quantity;

        quantityByBarcode.put(barcode, current - quantity);
        totalProfit += profit;
        return profit;
    }

    public int getStock(String barcode) {
        return quantityByBarcode.getOrDefault(barcode, 0);
    }

    public double getTotalProfit() {
        return totalProfit;
    }

    public Map<String, Integer> lowStock(int threshold) {
        Map<String, Integer> low = new HashMap<>();
        for (Map.Entry<String, Integer> e : quantityByBarcode.entrySet()) {
            if (e.getValue() <= threshold) {
                low.put(e.getKey(), e.getValue());
            }
        }
        return low;
    }
}
