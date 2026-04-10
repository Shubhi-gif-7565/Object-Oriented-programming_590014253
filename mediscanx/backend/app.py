#!/usr/bin/env python3
import json
import sqlite3
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_PATH = "mediscanx.db"
SYNC_INTERVAL_SECONDS = 3600  # 1 hour

FALLBACK_MEDICINES = {
    "8901234567890": {
        "barcode": "8901234567890",
        "name": "Crocin 650",
        "manufacturer": "GSK",
        "mrp": 34.0,
        "category": "Analgesic",
        "composition": "Paracetamol 650mg",
        "availability": "In Stock",
        "last_updated": "seed-data",
    },
    "8901111222333": {
        "barcode": "8901111222333",
        "name": "Azithral 500",
        "manufacturer": "Alembic",
        "mrp": 120.0,
        "category": "Antibiotic",
        "composition": "Azithromycin 500mg",
        "availability": "In Stock",
        "last_updated": "seed-data",
    },
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS medicines (
            barcode TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            manufacturer TEXT,
            mrp REAL,
            category TEXT,
            composition TEXT,
            availability TEXT,
            last_updated TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            barcode TEXT PRIMARY KEY,
            quantity INTEGER NOT NULL DEFAULT 0,
            cost_price REAL NOT NULL DEFAULT 0,
            selling_price REAL,
            updated_at TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            cost_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            profit REAL NOT NULL,
            sold_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_medicine_from_openfda(barcode: str):
    query = urllib.parse.quote(f'product_ndc:"{barcode}"')
    url = f"https://api.fda.gov/drug/ndc.json?search={query}&limit=1"
    try:
        with urllib.request.urlopen(url, timeout=6) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        result = payload.get("results", [])
        if not result:
            return None
        item = result[0]
        # MRP means Maximum Retail Price. OpenFDA NDC data does not provide price fields,
        # so price stays 0.0 here and can be overridden by local store pricing.
        mrp = 0.0
        return {
            "barcode": barcode,
            "name": item.get("brand_name") or item.get("generic_name") or "Unknown",
            "manufacturer": item.get("labeler_name") or "Unknown",
            "mrp": mrp,
            "category": item.get("dosage_form") or "General",
            "composition": item.get("active_ingredients", [{}])[0].get("name", "N/A") if item.get("active_ingredients") else "N/A",
            "availability": "Available",
            "last_updated": utc_now_iso(),
        }
    except Exception:
        return None


def upsert_medicine(medicine: dict) -> None:
    conn = db_connection()
    conn.execute(
        """
        INSERT INTO medicines (barcode, name, manufacturer, mrp, category, composition, availability, last_updated)
        VALUES (:barcode, :name, :manufacturer, :mrp, :category, :composition, :availability, :last_updated)
        ON CONFLICT(barcode) DO UPDATE SET
            name=excluded.name,
            manufacturer=excluded.manufacturer,
            mrp=excluded.mrp,
            category=excluded.category,
            composition=excluded.composition,
            availability=excluded.availability,
            last_updated=excluded.last_updated
        """,
        medicine,
    )
    conn.commit()
    conn.close()


def get_medicine(barcode: str) -> dict:
    live = fetch_medicine_from_openfda(barcode)
    if live:
        upsert_medicine(live)
        return live

    conn = db_connection()
    row = conn.execute("SELECT * FROM medicines WHERE barcode = ?", (barcode,)).fetchone()
    conn.close()
    if row:
        return dict(row)

    fallback = FALLBACK_MEDICINES.get(barcode)
    if fallback:
        upsert_medicine(fallback)
        return fallback

    unknown = {
        "barcode": barcode,
        "name": "Unknown Medicine",
        "manufacturer": "Unknown",
        "mrp": 0.0,
        "category": "Unknown",
        "composition": "Unknown",
        "availability": "Unknown",
        "last_updated": utc_now_iso(),
    }
    upsert_medicine(unknown)
    return unknown


def add_inventory(barcode: str, quantity: int, cost_price: float):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    get_medicine(barcode)
    conn = db_connection()
    row = conn.execute("SELECT quantity, cost_price, selling_price FROM inventory WHERE barcode = ?", (barcode,)).fetchone()
    now = utc_now_iso()
    if row:
        new_qty = row["quantity"] + quantity
        conn.execute(
            "UPDATE inventory SET quantity=?, cost_price=?, updated_at=? WHERE barcode=?",
            (new_qty, cost_price, now, barcode),
        )
    else:
        conn.execute(
            "INSERT INTO inventory (barcode, quantity, cost_price, selling_price, updated_at) VALUES (?, ?, ?, ?, ?)",
            (barcode, quantity, cost_price, None, now),
        )
    conn.commit()
    conn.close()


def sell_inventory(barcode: str, quantity: int, selling_price: float | None):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    conn = db_connection()
    row = conn.execute(
        """
        SELECT i.quantity, i.cost_price, i.selling_price, m.mrp AS medicine_mrp
        FROM inventory i
        JOIN medicines m ON m.barcode = i.barcode
        WHERE i.barcode = ?
        """,
        (barcode,),
    ).fetchone()
    if not row:
        conn.close()
        raise ValueError("Medicine not present in inventory")
    if row["quantity"] < quantity:
        conn.close()
        raise ValueError("Not enough stock")

    cp = float(row["cost_price"])
    if selling_price is not None:
        sp = float(selling_price)
    elif row["selling_price"] is not None:
        sp = float(row["selling_price"])
    elif row["medicine_mrp"] is not None:
        sp = float(row["medicine_mrp"])
    else:
        sp = cp
    profit = (sp - cp) * quantity
    new_qty = row["quantity"] - quantity
    now = utc_now_iso()

    conn.execute(
        "UPDATE inventory SET quantity=?, selling_price=?, updated_at=? WHERE barcode=?",
        (new_qty, sp, now, barcode),
    )
    conn.execute(
        "INSERT INTO sales (barcode, quantity, cost_price, selling_price, profit, sold_at) VALUES (?, ?, ?, ?, ?, ?)",
        (barcode, quantity, cp, sp, profit, now),
    )
    conn.commit()
    conn.close()
    return profit


def dashboard_data() -> dict:
    conn = db_connection()
    total_stock = conn.execute("SELECT COALESCE(SUM(quantity), 0) AS total FROM inventory").fetchone()["total"]
    today = datetime.now(timezone.utc).date().isoformat()
    sales_today = conn.execute(
        "SELECT COALESCE(SUM(quantity), 0) AS qty, COALESCE(SUM(profit), 0) AS profit FROM sales WHERE sold_at LIKE ?",
        (f"{today}%",),
    ).fetchone()
    low_stock_items = conn.execute(
        "SELECT m.name, i.quantity FROM inventory i JOIN medicines m ON m.barcode = i.barcode WHERE i.quantity <= 5 ORDER BY i.quantity ASC"
    ).fetchall()
    conn.close()

    alerts = [f"Low stock: {row['name']} ({row['quantity']} left)" for row in low_stock_items]
    return {
        "total_stock": total_stock,
        "today_sales": sales_today["qty"],
        "today_profit": round(float(sales_today["profit"]), 2),
        "alerts": alerts,
    }


def ai_query(query: str) -> str:
    q = query.strip().lower()
    if not q:
        return "Please ask something like 'check stock' or 'profit today'."

    conn = db_connection()
    if "profit" in q:
        result = dashboard_data()
        conn.close()
        return f"Today profit is ₹{result['today_profit']}"

    if "stock" in q:
        rows = conn.execute(
            "SELECT m.name, i.quantity FROM inventory i JOIN medicines m ON m.barcode = i.barcode ORDER BY i.quantity DESC LIMIT 5"
        ).fetchall()
        conn.close()
        if not rows:
            return "Inventory is empty."
        return "Top stock: " + ", ".join([f"{r['name']}={r['quantity']}" for r in rows])

    if "reorder" in q or "expiring" in q:
        rows = conn.execute(
            "SELECT m.name, i.quantity FROM inventory i JOIN medicines m ON m.barcode = i.barcode WHERE i.quantity <= 5 ORDER BY i.quantity ASC"
        ).fetchall()
        conn.close()
        if not rows:
            return "No urgent reorder needed right now."
        return "Reorder soon: " + ", ".join([f"{r['name']} ({r['quantity']})" for r in rows])

    if "find" in q or "search" in q:
        term = q.replace("find", "").replace("search", "").strip()
        rows = conn.execute(
            "SELECT name, barcode FROM medicines WHERE lower(name) LIKE ? LIMIT 5",
            (f"%{term}%",),
        ).fetchall()
        conn.close()
        if not rows:
            return "No matching medicine found."
        return "Matches: " + ", ".join([f"{r['name']} [{r['barcode']}]" for r in rows])

    conn.close()
    return "Try commands like: find medicine, check stock, suggest reorder, profit today."


def voice_command(text: str) -> str:
    t = text.lower()
    if "show profit" in t:
        return ai_query("profit today")
    if "check stock" in t:
        return ai_query("check stock")
    if "scan" in t:
        return "Say barcode number after 'scan'."
    return ai_query(text)


def sync_all_medicines() -> None:
    conn = db_connection()
    rows = conn.execute("SELECT barcode FROM medicines").fetchall()
    conn.close()
    for r in rows:
        live = fetch_medicine_from_openfda(r["barcode"])
        if live:
            upsert_medicine(live)


def sync_worker() -> None:
    while True:
        try:
            sync_all_medicines()
        except Exception:
            pass
        time.sleep(SYNC_INTERVAL_SECONDS)


class MediscanHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/api/scan":
            barcode = params.get("barcode", [""])[0]
            if not barcode:
                return self._send_json({"error": "barcode is required"}, 400)
            return self._send_json({"medicine": get_medicine(barcode)})

        if parsed.path == "/api/inventory":
            conn = db_connection()
            rows = conn.execute(
                "SELECT i.barcode, m.name, i.quantity, i.cost_price, COALESCE(i.selling_price, m.mrp) AS selling_price FROM inventory i JOIN medicines m ON m.barcode = i.barcode ORDER BY m.name"
            ).fetchall()
            conn.close()
            return self._send_json({"inventory": [dict(r) for r in rows]})

        if parsed.path == "/api/dashboard":
            return self._send_json({"dashboard": dashboard_data()})

        if parsed.path == "/api/voice/command":
            text = params.get("text", [""])[0]
            return self._send_json({"response": voice_command(text)})

        self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        try:
            payload = self._read_json()

            if parsed.path == "/api/inventory/add":
                barcode = str(payload.get("barcode", "")).strip()
                quantity = int(payload.get("quantity", 0))
                cost_price = float(payload.get("cost_price", 0))
                add_inventory(barcode, quantity, cost_price)
                return self._send_json({"message": "Stock updated"})

            if parsed.path == "/api/inventory/sell":
                barcode = str(payload.get("barcode", "")).strip()
                quantity = int(payload.get("quantity", 0))
                selling_price = payload.get("selling_price")
                sp = None if selling_price is None else float(selling_price)
                profit = sell_inventory(barcode, quantity, sp)
                return self._send_json({"message": "Sale recorded", "profit": round(profit, 2)})

            if parsed.path == "/api/ai/query":
                query = str(payload.get("query", ""))
                return self._send_json({"response": ai_query(query)})

            return self._send_json({"error": "Not found"}, 404)
        except ValueError as ex:
            return self._send_json({"error": str(ex)}, 400)
        except Exception as ex:
            return self._send_json({"error": f"Request failed: {ex}"}, 500)


def run_server(port: int = 8000):
    init_db()
    for med in FALLBACK_MEDICINES.values():
        upsert_medicine(med)

    thread = threading.Thread(target=sync_worker, daemon=True)
    thread.start()

    server = HTTPServer(("0.0.0.0", port), MediscanHandler)
    print(f"MediscanX backend running on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server(8000)
