from http.server import BaseHTTPRequestHandler
import json
import re

REQUIRED_FIELDS = ["momo_tx_id", "sender_address", "timestamp_readable", "raw_sms_text"]


class MomoDataAPIHandler(BaseHTTPRequestHandler):
    transactions = []

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def _match(self, pattern):
        return re.match(pattern, self.path)

    def _validate(self, body):
        missing = [f for f in REQUIRED_FIELDS if f not in body]
        if missing:
            return {"error": f"Missing fields: {', '.join(missing)}"}
        return None

    #GET endpoints
    def do_GET(self):
        if self.path == "/transactions":
            return self._send_json(self.transactions)

        m = self._match(r"^/transactions/(\d+)$")
        if m:
            txn_id = int(m.group(1))
            for txn in self.transactions:
                if txn["id"] == txn_id:
                    return self._send_json(txn)
            return self._send_json({"error": "Transaction not found"}, 404)

        self._send_json({"error": "Not found"}, 404)


    #POST endpoints
    def do_POST(self):
        body = self._read_body()
        err = self._validate(body)
        if err:
            return self._send_json(err, 400)

        new_id = max((t["id"] for t in self.transactions), default=0) + 1
        new_txn = {"id": new_id, **{f: body[f] for f in REQUIRED_FIELDS}}
        self.transactions.append(new_txn)
        self.save()
        self._send_json(new_txn, 201)


    #PUT endpoints
    def do_PUT(self):
        m = self._match(r"^/transactions/(\d+)$")
        if not m:
            return self._send_json({"error": "Not found"}, 404)

        body = self._read_body()
        err = self._validate(body)
        if err:
            return self._send_json(err, 400)

        txn_id = int(m.group(1))
        for txn in self.transactions:
            if txn["id"] == txn_id:
                for f in REQUIRED_FIELDS:
                    txn[f] = body[f]
                self.save()
                return self._send_json(txn)

        self._send_json({"error": "Transaction not found"}, 404)


    #DELETE endpoints
    def do_DELETE(self):
        m = self._match(r"^/transactions/(\d+)$")
        if not m:
            return self._send_json({"error": "Not found"}, 404)

        txn_id = int(m.group(1))
        for i, txn in enumerate(self.transactions):
            if txn["id"] == txn_id:
                self.transactions.pop(i)
                self.save()
                return self._send_json({"message": "Deleted"})

        self._send_json({"error": "Transaction not found"}, 404)
