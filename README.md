# AWS VPC Flow Logs Parser


---

## Table of Contents

1. [Overview](#overview)  
2. [Key Features](#key-features)  
3. [System Requirements](#system-requirements)  
4. [Installation](#installation)  
5. [Compiling & Running the Program](#compiling--running-the-program)  
6. [Lookup CSV Format](#lookup-csv-format)  
7. [Example Inputs/Outputs](#example-inputsoutputs)  
8. [Testing & Validation](#testing--validation)  
9. [Assumptions & Limitations](#assumptions--limitations)  
10. [Known Issues](#known-issues)  
11. [References & Further Reading](#references--further-reading) 

---

## Overview

This repository contains a **Python** script that parses **AWS VPC Flow Logs (version 2)** and maps them to **tags** based on a user-provided **lookup CSV**. It outputs two reports:

1. **Tag Counts** – Number of flow records assigned to each tag.  
2. **Port/Protocol Combination Counts** – Frequency of each `(dstport, protocol)` pair.

AWS VPC Flow Logs record network traffic at the **Elastic Network Interface (ENI)** level. This script **automates analysis** by mapping flows to human-readable categories such as `web`, `secure`, `email`, etc.

---

## Key Features

✅ **Supports AWS VPC Flow Log Version 2** (14 default fields).  
✅ **Flexible Lookup-Based Tagging** using a CSV file.  
✅ **Case-Insensitive Protocol Matching** (e.g., `TCP`, `tcp`).  
✅ **Handles Unknown Protocols Gracefully** (falls back to numeric values).  
✅ **Error Handling**:  
   - Detects empty/missing lookup CSV.  
   - Validates flow log format and version.  
✅ **Lightweight & No External Dependencies** – Uses **only Python standard library**.

---

## System Requirements

- **Python**: 3.6+ recommended (compatible with all Python 3 versions).  
- **Operating System**: Linux, macOS, or Windows.  
- **Storage**: Minimal disk space required (typically <10 MB).  

---

## Installation

### Step 1: Clone or Download the Repository


git clone https://github.com/BasanthPR/AWS-VPC-Flow-Logs-Parser.git
cd AWS-VPC-Flow-Logs-Parser

### Step 2: (Optional) Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


### Step 3: Verify Python Version

python --version

## Compiling & Running the Program:

### Step 1: Ensure you have the following files:

Flow logs file (flow_logs.txt) – Contains AWS flow logs in default version 2 format.
Lookup CSV file (lookup.csv) – Defines (dstport, protocol) → tag mappings.

### Step 2: Run the Script

Run the parser with: python parse_flow_logs.py <flow_logs_file> <lookup_csv_file> <output_file>

Where:
- flow_logs_file: Path to the AWS flow logs text file.
- lookup_csv_file: Path to your CSV file mapping (dstport, protocol) → tag.
- output_file: Results are written to this file.

Example: python3 FlowLogsParser.py /Users/basanthyajman/Downloads/flow_logs.txt /Users/basanthyajman/Downloads/lookup.csv /Users/basanthyajman/Downloads/results.txt

Expected Console Output:
Will write results to: /Users/basanthyajman/Downloads/results.txt
Writing results to: /Users/basanthyajman/Downloads/results.txt
Output successfully written.

### Step 3: View Results
Open output_report.txt, which contains:

Tag Counts – Number of logs assigned to each tag.
Port/Protocol Combination Counts – Frequency of each (dstport, protocol) pair.

## Lookup CSV Format

Each row in lookup.csv must have three columns:

Which are : dstport,protocol,tag

- dstport: An integer (80, 443).
- protocol: Case-insensitive string (tcp, udp).
- tag: The label to apply (web, secure, email).

### Example CSV

# Comment lines (ignored by parser)
25,tcp,email
443,tcp,secure
80,tcp,web
23,tcp,legacy

### Example Inputs/Outputs
### Example Flow Log Line

2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK

### Parsed Data
- dstport = 49153
- protocol = 6 → Converted to "tcp"
If (49153, "tcp") is not in the CSV, it is labeled "Untagged".

### Example Output

Tag Counts:
Tag,Count
secure,15
web,20
email,10
Untagged,5

Port/Protocol Combination Counts:

(Port,Protocol,Count)
(443,tcp,15)
(80,tcp,20)
(25,tcp,10)

## Testing & Validation

## Test Cases
- ✅ Validates CSV parsing (including duplicate rules).
- ✅ Ensures case-insensitivity (tcp vs. TCP).
- ✅ Checks unknown protocols default to numeric representation.
- ✅ Handles missing/invalid flow log fields gracefully.

## Assumptions & Limitations

1. Only Supports AWS Flow Log Version 2 (14 default fields).
2. Unsupported Protocols: Unrecognized numbers (e.g., 999) remain numeric.
3. Duplicate CSV Entries: The last occurrence of (dstport, protocol) in lookup.csv overrides earlier ones.

## References & Further Reading

- 📖 [AWS VPC Flow Logs Documentation][https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html].
- 📖 [IANA Protocol Numbers][https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml].
- 📖 [Python Official Docs][https://docs.python.org/3/].
