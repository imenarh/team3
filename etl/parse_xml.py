import xml.etree.ElementTree as ET
import re
import os
import json
from pathlib import Path


def parse_momo_xml(xml_file_path):
    # Parse MTN MoMo XML SMS backup and extract structured transaction data

    if not os.path.exists(xml_file_path):
        raise FileNotFoundError(f"Could not find XML file: {xml_file_path}")

    # Read and clean XML
    print("Reading XML file...")
    with open(xml_file_path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    print("Cleaning malformed XML characters...")
    xml_content = re.sub(r'&(?!amp;|lt;|gt;|apos;|quot;)', '&amp;', xml_content)
    xml_content = xml_content.replace('<#>', '&lt;#&gt;')
    xml_content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', xml_content)

    # Parse XML
    print("Parsing cleaned XML data...")
    root = ET.fromstring(xml_content)

    # Process SMS records
    sms_records = []
    current_id = 1
    print("Processing SMS records...")

    for sms in root.findall("sms"):
        raw_body = sms.get("body", "")

        # Extract reference ID
        tx_id_match = re.search(r"(?:TxId:|Transaction Id:)\s*([0-9]+)", raw_body)
        reference_id = tx_id_match.group(1) if tx_id_match else "N/A"

        # Extract amount
        amount_match = re.search(r"([\d,]+)\s*RWF", raw_body)
        amount = int(amount_match.group(1).replace(",", "")) if amount_match else 0

        # Extract fee
        fee_match = re.search(r"[Ff]ee\s*(?:was:?\s*)([\d,]+)\s*RWF", raw_body)
        fee = int(fee_match.group(1).replace(",", "")) if fee_match else 0

        # Extract timestamp
        ts_match = re.search(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", raw_body)
        timestamp = ts_match.group(1).replace(" ", "T") if ts_match else ""

        # Categorize by SMS pattern
        if "You have received" in raw_body:
            category = "INCOMING_MONEY"
        elif "Your payment of" in raw_body and "has been completed" in raw_body:
            category = "PAYMENT"
        elif "RWF transferred to" in raw_body:
            category = "TRANSFER_OUT"
        elif "bank deposit" in raw_body:
            category = "BANK_DEPOSIT"
        elif "withdrawn" in raw_body:
            category = "WITHDRAWAL"
        elif "Airtime" in raw_body:
            category = "AIRTIME"
        elif "reversal" in raw_body.lower():
            category = "REVERSAL"
        elif "A transaction of" in raw_body or "DIRECT PAYMENT" in raw_body:
            category = "MERCHANT_PAYMENT"
        else:
            category = "OTHER"

        sms_records.append({
            "id": current_id,
            "reference_id": reference_id,
            "amount": amount,
            "fee": fee,
            "status": "SUCCESS",
            "category": category,
            "timestamp": timestamp,
            "raw_sms_text": raw_body
        })
        current_id += 1

    return sms_records


def save_to_json(data, output_path):
    # Save parsed SMS records to JSON file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"\nJSON file saved successfully at:\n{output_path}")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    XML_PATH = BASE_DIR / "data" / "raw" / "momo.xml"
    JSON_OUTPUT_PATH = BASE_DIR / "data" / "processed" / "dashboard.json"

    try:
        parsed_data = parse_momo_xml(XML_PATH)
        print(f"\nSuccessfully parsed XML file.")
        print(f"Total SMS records: {len(parsed_data)}")

        save_to_json(parsed_data, JSON_OUTPUT_PATH)

        print("\nPreview of first 3 records:\n")
        for record in parsed_data[:3]:
            print(record)

    except Exception as e:
        print(f"\nAn error occurred: {e}")