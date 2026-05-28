
import xml.etree.ElementTree as ET
import re
import os
import json
from pathlib import Path


def parse_momo_xml(xml_file_path):
    """
    Parse MTN MoMo XML SMS backup file
    and convert messages into Python dictionaries.
    """

    # Check if file exists
    if not os.path.exists(xml_file_path):
        raise FileNotFoundError(
            f"Could not find XML file: {xml_file_path}"
        )

    # ==========================
    # CLEAN AND PARSE XML
    # ==========================

    print("Reading XML file...")

    # Read XML manually
    with open(xml_file_path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    print("Cleaning malformed XML characters...")

    # Fix invalid ampersands
    xml_content = re.sub(
        r'&(?!amp;|lt;|gt;|apos;|quot;)',
        '&amp;',
        xml_content
    )

    # Escape problematic symbols
    xml_content = xml_content.replace(
        '<#>',
        '&lt;#&gt;'
    )

    # Remove invalid control characters
    xml_content = re.sub(
        r'[\x00-\x08\x0B\x0C\x0E-\x1F]',
        '',
        xml_content
    )

    print("Parsing cleaned XML data...")

    # Parse cleaned XML
    root = ET.fromstring(xml_content)

    # ==========================
    # PROCESS SMS RECORDS
    # ==========================

    sms_records = []
    current_id = 1

    print("Processing SMS records...")

    # Loop through SMS messages
    for sms in root.findall("sms"):

        raw_body = sms.get("body", "")
        readable_date = sms.get("readable_date", "")
        address = sms.get("address", "")

        # Extract Transaction ID
        tx_id_match = re.search(
            r"(?:TxId:|Transaction Id:)\s*([0-9]+)",
            raw_body
        )

        extracted_tx_id = (
            tx_id_match.group(1)
            if tx_id_match
            else "N/A"
        )

        # Create record dictionary
        sms_record = {
            "id": current_id,
            "momo_tx_id": extracted_tx_id,
            "sender_address": address,
            "timestamp_readable": readable_date,
            "raw_sms_text": raw_body
        }

        # Add record to list
        sms_records.append(sms_record)

        # Increment ID
        current_id += 1

    return sms_records


def save_to_json(data, output_path):
    """
    Save parsed SMS records into JSON file.
    """

    # Create parent folders if they don't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save JSON file
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(
            data,
            json_file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nJSON file saved successfully at:")
    print(output_path)


# ==========================
# MAIN PROGRAM
# ==========================

if __name__ == "__main__":

    # Base project directory
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Input XML file path
    XML_PATH = (
        BASE_DIR
        / "data"
        / "raw"
        / "momo.xml"
    )

    # Output JSON file path
    JSON_OUTPUT_PATH = (
        BASE_DIR
        / "data"
        / "processed"
        / "dashboard.json"
    )

    try:

        # Parse XML data
        parsed_data = parse_momo_xml(XML_PATH)

        print("\nSuccessfully parsed XML file.")
        print(f"Total SMS records: {len(parsed_data)}")

        # Save parsed data into JSON
        save_to_json(
            parsed_data,
            JSON_OUTPUT_PATH
        )

        # Preview first 3 records
        print("\nPreview of first 3 records:\n")

        for record in parsed_data[:3]:
            print(record)

    except Exception as e:
        print(f"\nAn error occurred: {e}")
