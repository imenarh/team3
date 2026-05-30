import xml.etree.ElementTree as ET
import re
import os
import json
import time
from pathlib import Path


def parse_momo_xml(xml_file_path):
    if not os.path.exists(xml_file_path):
        raise FileNotFoundError(f"Could not find XML file: {xml_file_path}")

    with open(xml_file_path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    xml_content = re.sub(r'&(?!amp;|lt;|gt;|apos;|quot;)', '&amp;', xml_content)
    xml_content = xml_content.replace('<#>', '&lt;#&gt;')
    xml_content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', xml_content)

    root = ET.fromstring(xml_content)

    sms_records = []
    current_id = 1

    for sms in root.findall("sms"):
        raw_body = sms.get("body", "")

        tx_id_match = re.search(r"(?:TxId:|Transaction Id:)\s*([0-9]+)", raw_body)
        reference_id = tx_id_match.group(1) if tx_id_match else "N/A"

        amount_match = re.search(r"([\d,]+)\s*RWF", raw_body)
        amount = int(amount_match.group(1).replace(",", "")) if amount_match else 0

        fee_match = re.search(r"[Ff]ee\s*(?:was:?\s*)([\d,]+)\s*RWF", raw_body)
        fee = int(fee_match.group(1).replace(",", "")) if fee_match else 0

        ts_match = re.search(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", raw_body)
        timestamp = ts_match.group(1).replace(" ", "T") if ts_match else ""

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
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    
# Task 5: Data Structures & Algorithms (DSA Integration)

def linear_search(transactions_list, target_id):
    """
    Scans through the list array one-by-one to locate a matching transaction ID.
    Time Complexity: O(N)
    """
    for transaction in transactions_list:
        if transaction['id'] == target_id:
            return transaction
    return None


def dictionary_lookup(transactions_dict, target_id):
    """
    Direct hashmap lookup searching by dictionary key.
    Time Complexity: O(1)
    """
    return transactions_dict.get(target_id, None)


def run_dsa_benchmark(transactions_list):
    """
    Measures and compares the efficiency of Linear Search vs Dictionary Lookup
    for at least 20 records as specified by the assignment requirements.
    """
    transactions_dict = {txn['id']: txn for txn in transactions_list}

    total_records = len(transactions_list)
    step = max(1, total_records // 20)
    target_ids = [i for i in range(1, min(total_records, step * 22), step)][:22]

    print("\nDATA STRUCTURES & ALGORITHMS BENCHMARK\n")
    print(f"Dataset Size: {total_records} loaded records")
    print(f"Benchmarking lookups for {len(target_ids)} records...")

    loops = 5000

    start_linear = time.perf_counter()
    for _ in range(loops):
        for tid in target_ids:
            linear_search(transactions_list, tid)
    end_linear = time.perf_counter()
    linear_duration = end_linear - start_linear

    start_dict = time.perf_counter()
    for _ in range(loops):
        for tid in target_ids:
            dictionary_lookup(transactions_dict, tid)
    end_dict = time.perf_counter()
    dict_duration = end_dict - start_dict

    print(f"Linear Search Performance:     {linear_duration:.6f} seconds")
    print(f"Dictionary Lookup Performance: {dict_duration:.6f} seconds")

    speed_factor = linear_duration / dict_duration if dict_duration > 0 else 1
    print(f"\nResult: Dictionary Lookup is roughly {speed_factor:.1f}x FASTER than Linear Search.")


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

        if len(parsed_data) >= 20:
            run_dsa_benchmark(parsed_data)
        else:
            print("\n[Warning] Dataset too small to reliably benchmark 20+ keys.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
