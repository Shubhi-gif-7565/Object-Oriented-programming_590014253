# MediscanX (Auto Smart Version)

This folder provides a multi-language starter implementation for the MediscanX problem statement.

## Included stacks

- **Python**: backend APIs with auto medicine lookup + inventory/profit logic + hourly sync
- **HTML**: dashboard UI for scanner, inventory actions, AI query, and voice-style command input
- **Java**: domain model classes and assistant logic sample for OOP use

## Run Python backend

```bash
cd mediscanx/backend
python3 app.py
```

Backend listens on `http://localhost:8000`.

## Run HTML frontend

Open this file in browser:

`mediscanx/frontend/index.html`

(Ensure backend is running.)

## Run Java sample

```bash
cd mediscanx/java/src
javac mediscanx/*.java
java mediscanx.Main
```

## API highlights

- `GET /api/scan?barcode=...`
- `POST /api/inventory/add`
- `POST /api/inventory/sell`
- `GET /api/inventory`
- `GET /api/dashboard`
- `POST /api/ai/query`
- `GET /api/voice/command?text=...`

## Notes

- OpenFDA is used as external medicine source when available.
- Fallback seed medicines are included for offline/demo mode.
- Profit formula: `(SP - CP) * quantity sold`.
