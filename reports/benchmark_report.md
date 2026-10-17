# AI-Powered Document Extractor - Accuracy & Performance Benchmark Report

**Benchmark Run Date:** 2026-10-17 16:25:41  
**Model Under Test:** `gemini-3.8-flash` (Structured Output Schema Mode)  
**Temperature:** `0.0` (Deterministic Mode)  

---

## 1. Executive Summary

| Metric | Benchmark Result | Target SLA | Status |
| :--- | :--- | :--- | :--- |
| **Classification Accuracy** | **100.0%** | > 95.0% | ✅ PASSED |
| **Field-Level Extraction Accuracy** | **100.0%** | > 90.0% | ✅ PASSED |
| **Average End-to-End Latency** | **24.93s** | < 5.0s | ⚠️ REVIEW |
| **Scanned/Empty PDF Handling** | **100% Flagged** | 100% | ✅ PASSED |

---

## 2. Document-by-Document Breakdown

| Document Name | Expected Type | Fields Matched | Field Accuracy | Latency | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sample_invoice.pdf` | invoice | 14 / 14 | **100.0%** | 8.58s | ✅ |
| `sample_invoice_consulting.pdf` | invoice | 14 / 14 | **100.0%** | 3.39s | ✅ |
| `sample_invoice_international.pdf` | invoice | 14 / 14 | **100.0%** | 3.93s | ✅ |
| `sample_bol.pdf` | bill_of_lading | 15 / 15 | **100.0%** | 52.50s | ✅ |
| `sample_bol_airway.pdf` | bill_of_lading | 15 / 15 | **100.0%** | 56.27s | ✅ |
| `blank_sample.pdf` | Scanned/Empty PDF | 1 / 1 | **100.0%** | 0.00s | ✅ |

---

## 3. Detailed Field Comparisons

### Document: `sample_invoice.pdf` (invoice)

| Field Name | Match Status | Evaluation Note |
| :--- | :---: | :--- |
| `invoice_number` | ✅ Match | 'INV-2024-0042' == 'INV-2024-0042' |
| `invoice_date` | ✅ Match | '2024-10-15' == '2024-10-15' |
| `due_date` | ✅ Match | '2024-11-14' == '2024-11-14' |
| `purchase_order_number` | ✅ Match | 'PO-99120' == 'PO-99120' |
| `vendor_name` | ✅ Match | 'Apex Industrial Supplies Ltd.' == 'Apex Industrial Supplies Ltd.' |
| `customer_name` | ✅ Match | 'Nexus Logistics Corp' == 'Nexus Logistics Corp' |
| `currency` | ✅ Match | 'USD' == 'USD' |
| `subtotal` | ✅ Match | 1018.0 == 1018.00 |
| `tax_amount` | ✅ Match | 86.53 == 86.53 |
| `shipping_amount` | ✅ Match | 75.0 == 75.00 |
| `discount_amount` | ✅ Match | 25.0 == 25.00 |
| `total_amount` | ✅ Match | 1154.53 == 1154.53 |
| `payment_terms` | ✅ Match | 'Net 30 Days' == 'Net 30 Days' |
| `line_items_count` | ✅ Match | 3 items == expected 3 |

### Document: `sample_invoice_consulting.pdf` (invoice)

| Field Name | Match Status | Evaluation Note |
| :--- | :---: | :--- |
| `invoice_number` | ✅ Match | 'INV-2024-789' == 'INV-2024-789' |
| `invoice_date` | ✅ Match | '2024-11-01' == '2024-11-01' |
| `due_date` | ✅ Match | '2024-11-16' == '2024-11-16' |
| `purchase_order_number` | ✅ Match | 'PO-88310' == 'PO-88310' |
| `vendor_name` | ✅ Match | 'CloudScale Architecture LLC' == 'CloudScale Architecture LLC' |
| `customer_name` | ✅ Match | 'FinTech Ventures Inc' == 'FinTech Ventures Inc' |
| `currency` | ✅ Match | 'USD' == 'USD' |
| `subtotal` | ✅ Match | 14000.0 == 14000.00 |
| `tax_amount` | ✅ Match | 0.0 == 0.00 |
| `shipping_amount` | ✅ Match | 0.0 == 0.00 |
| `discount_amount` | ✅ Match | 0.0 == 0.00 |
| `total_amount` | ✅ Match | 14000.0 == 14000.00 |
| `payment_terms` | ✅ Match | 'Net 15 Days' == 'Net 15 Days' |
| `line_items_count` | ✅ Match | 1 items == expected 1 |

### Document: `sample_invoice_international.pdf` (invoice)

| Field Name | Match Status | Evaluation Note |
| :--- | :---: | :--- |
| `invoice_number` | ✅ Match | 'INV-EU-9921' == 'INV-EU-9921' |
| `invoice_date` | ✅ Match | '2024-10-20' == '2024-10-20' |
| `due_date` | ✅ Match | '2024-11-20' == '2024-11-20' |
| `purchase_order_number` | ✅ Match | 'PO-NOR-4410' == 'PO-NOR-4410' |
| `vendor_name` | ✅ Match | 'Berlin Sensorik GmbH' == 'Berlin Sensorik GmbH' |
| `customer_name` | ✅ Match | 'Nordic Energy AS' == 'Nordic Energy AS' |
| `currency` | ✅ Match | 'EUR' == 'EUR' |
| `subtotal` | ✅ Match | 4500.0 == 4500.00 |
| `tax_amount` | ✅ Match | 855.0 == 855.00 |
| `shipping_amount` | ✅ Match | 120.0 == 120.00 |
| `discount_amount` | ✅ Match | 200.0 == 200.00 |
| `total_amount` | ✅ Match | 5275.0 == 5275.00 |
| `payment_terms` | ✅ Match | 'Net 30 Days' == 'Net 30 Days' |
| `line_items_count` | ✅ Match | 2 items == expected 2 |

### Document: `sample_bol.pdf` (bill_of_lading)

| Field Name | Match Status | Evaluation Note |
| :--- | :---: | :--- |
| `bol_number` | ✅ Match | 'BOL-ONEY-8829103' == 'BOL-ONEY-8829103' |
| `shipper_name` | ✅ Match | 'Orient Global Manufacturing Ltd.' == 'Orient Global Manufacturing Ltd.' |
| `consignee_name` | ✅ Match | 'Pacific Imports & Distribution LLC' == 'Pacific Imports & Distribution LLC' |
| `vessel_name` | ✅ Match | 'EVER FORWARD' == 'EVER FORWARD' |
| `voyage_number` | ✅ Match | 'V.042W' == 'V.042W' |
| `port_of_loading` | ✅ Match | 'Port of Shenzhen, China' == 'Port of Shenzhen, China' |
| `port_of_discharge` | ✅ Match | 'Port of Long Beach, USA' == 'Port of Long Beach, USA' |
| `place_of_receipt` | ✅ Match | 'Shenzhen CFS' == 'Shenzhen CFS' |
| `final_destination` | ✅ Match | 'Long Beach, CA' == 'Long Beach, CA' |
| `gross_weight` | ✅ Match | 8450.0 == 8450.00 |
| `weight_unit` | ✅ Match | 'KGS' == 'KGS' |
| `package_count` | ✅ Match | '450 Cartons' == '450 Cartons' |
| `container_numbers` | ✅ Match | ['ONEU9876543'] contains expected ['ONEU9876543'] |
| `seal_numbers` | ✅ Match | ['SL-554432'] contains expected ['SL-554432'] |
| `shipment_date` | ✅ Match | '2024-09-28' == '2024-09-28' |

### Document: `sample_bol_airway.pdf` (bill_of_lading)

| Field Name | Match Status | Evaluation Note |
| :--- | :---: | :--- |
| `bol_number` | ✅ Match | 'AWB-772-9102834' == 'AWB-772-9102834' |
| `shipper_name` | ✅ Match | 'Tokyo Microchips Corp' == 'Tokyo Microchips Corp' |
| `consignee_name` | ✅ Match | 'Munich Precision Instruments GmbH' == 'Munich Precision Instruments GmbH' |
| `vessel_name` | ✅ Match | 'Boeing 777F' == 'Boeing 777F' |
| `voyage_number` | ✅ Match | 'JL8421' == 'JL8421' |
| `port_of_loading` | ✅ Match | 'Tokyo Narita Airport (NRT)' == 'Tokyo Narita Airport (NRT)' |
| `port_of_discharge` | ✅ Match | 'Munich Airport (MUC)' == 'Munich Airport (MUC)' |
| `place_of_receipt` | ✅ Match | 'Narita Cargo Terminal' == 'Narita Cargo Terminal' |
| `final_destination` | ✅ Match | 'Munich, Germany' == 'Munich, Germany' |
| `gross_weight` | ✅ Match | 1240.5 == 1240.50 |
| `weight_unit` | ✅ Match | 'KGS' == 'KGS' |
| `package_count` | ✅ Match | '12 Pallets' == '12 Pallets' |
| `container_numbers` | ✅ Match | ['AKE-99218-JL', 'AKE-99219-JL'] contains expected ['AKE-99218-JL', 'AKE-99219-JL'] |
| `seal_numbers` | ✅ Match | ['SEAL-JP-7701', 'SEAL-JP-7702'] contains expected ['SEAL-JP-7701', 'SEAL-JP-7702'] |
| `shipment_date` | ✅ Match | '2024-11-05' == '2024-11-05' |

### Document: `blank_sample.pdf` (Scanned/Empty PDF)

| Field Name | Match Status | Evaluation Note |
| :--- | :---: | :--- |
| `OCR Requirement Detection` | ✅ Match | Flagged low-char document |

---

## 4. Key Engineering Takeaways & Evaluation Methodology

1. **Normalized Value Matching:**
   - Evaluated financial decimals with `Decimal` comparison rather than naive string comparison to avoid formatting false-positives (e.g., `1018.00` vs `1,018.0`).
   - Evaluated strings with lowercase whitespace-collapsed normalization to tolerate minor casing variations.

2. **Classification Robustness:**
   - Zero-token heuristic classifier achieved high accuracy with 0ms LLM overhead for pre-routing documents.

3. **Hallucination Prevention:**
   - Strict Pydantic response schemas enforced via Google GenAI SDK ensured missing fields defaulted safely to `null` rather than generating fabricated data.
