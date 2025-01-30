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
10. [Author's Explanation](#authors-explanation)  
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

Flow logs file (flow_logs.txt) – Contains VPC flow logs in default version 2 format.
Lookup CSV file (lookup.csv) – Defines (dstport, protocol) → tag mappings.

### Step 2: Run the Script

Run the parser with: python FlowLogsParser.py <flow_logs_file> <lookup_csv_file> <output_file>

Where:
- flow_logs_file: Path to the VPC flow logs text file.
- lookup_csv_file: Path to your CSV file mapping.
- output_file: Results are written to this file.

Example: python3 FlowLogsParser.py /Users/basanthyajman/Downloads/flow_logs.txt /Users/basanthyajman/Downloads/lookup.csv /Users/basanthyajman/Downloads/results.txt

Expected Console Output:

- Will write results to: /Users/basanthyajman/Downloads/results.txt
- Writing results to: /Users/basanthyajman/Downloads/results.txt
- Output successfully written.

### Step 3: View Results
Open output_report.txt, which contains:

- Tag Counts –> Number of logs assigned to each tag.
- Port/Protocol Combination Counts –> Frequency of each (dstport, protocol) pair.

## Lookup CSV Format

Each row in lookup.csv must have three columns:

Which are : dstport,protocol,tag

- dstport: An integer (80, 443).
- protocol: Case-insensitive string (tcp, udp).
- tag: The label to apply (web, secure, email).

### Example CSV

#### Comment lines (ignored by parser)

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

Port,Protocol,Count
443,tcp,15
80,tcp,20
25,tcp,10

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

## Author's Explanation

Here, I describe my thought process, design decisions, and the rationale behind certain implementation details.

### 1. Understanding the AWS VPC Flow Logs (Version 2) Format
A typical version 2 AWS VPC Flow Log record looks like this (fields are space-delimited):

version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status

For example (one line from the sample logs):

2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK

Breaking this down by column:

| Field         | Value         |
|---------------|---------------|
| version       | 2             |
| account-id    | 123456789012  |
| interface-id  | eni-0a1b2c3d  |
| srcaddr       | 10.0.1.201    |
| dstaddr       | 198.51.100.2  |
| srcport       | 443           |
| dstport       | 49153         |
| protocol      | 6             |
| packets       | 25            |
| bytes         | 20000         |
| start         | 1620140761    |
| end           | 1620140821    |
| action        | ACCEPT        |
| log-status    | OK            |

#### Important Fields for Tagging

dstport is at position 7
protocol is at position 8
Note: AWS Flow Logs store the protocol as a numeric (IANA protocol number). For example:

- 6 = TCP
- 17 = UDP
- 1 = ICMP (and so on).

### 2. Understanding the Lookup Table
A CSV file with three columns:

dstport,protocol,tag

For example:


| dstport | protocol | tag    |
|---------|----------|--------|
| 25      | tcp      | sv_P1  |
| 68      | udp      | sv_P2  |
| 23      | tcp      | sv_P1  |
| 31      | udp      | SV_P3  |
| 443     | tcp      | sv_P2  |
| 22      | tcp      | sv_P4  |
| 3389    | tcp      | sv_P5  |
| 0       | icmp     | sv_P5  |
| 110     | tcp      | email  |
| 993     | tcp      | email  |
| 143     | tcp      | email  |

- dstport: The numeric port to match on.
- protocol: A textual representation (tcp, udp, icmp, etc.).
- tag: The label to apply if a flow record matches this (dstport, protocol) pair.
  
##### Case Insensitivity
The matching should be case-insensitive:

The protocol in the CSV might appear as tcp, Tcp, TCP, etc., and it should be treated the same.
The protocol from the flow log is numeric, so it's better to convert numeric to a lower-case text form (6 -> tcp, 17 -> udp, 1 -> icmp, etc.) before lookup.

### 3. What the program does

Read/Parse the flow log file line by line.
For each line (flow record), extract the dstport and the protocol.

Convert the protocol number from the flow record to a textual protocol:

Example mapping:
6 -> tcp
17 -> udp
1 -> icmp

This mapping can be expanded as needed if other protocol numbers appear.

Read/Parse the lookup CSV file into an in-memory structure (e.g., a dictionary) for quick lookups:

Key: (dstport, protocol) pair (both as strings or integers, consistently).
Value: tag
Convert protocol to lowercase for case-insensitive matching.

Perform the lookup for each flow record:
Form the (dstport, protocol) pair. (Convert protocol to text, e.g., 6 -> "tcp")
Check if that pair is in the lookup dictionary.
- If yes, get the corresponding tag.
- If not, the tag is "Untagged".

Maintain two sets of counts:

Tag Counts: how many flow records ended up in a given tag.
Example: {"sv_P1": 2, "sv_P2": 1, "email": 3, "Untagged": 9, ...}

Port/Protocol Combination Counts: how many times a (dstport, protocol-text) combination appears regardless of the tag.
Example: {"(23, tcp)": 1, "(25, tcp)": 1, "(443, tcp)": 1, ...}

At the end, output two reports (in plain text:
Tag Counts (the summary of how many records got each tag).
Port/Protocol Combination Counts (the summary of how many times each unique (dstport, protocol-text) pair occurred).

### 4. Sample Output Explanation
From the sample logs, you might see an output like this (just an example):

Tag Counts:

Tag,Count
sv_P2,1
sv_P1,2
sv_P4,1
email,3
Untagged,9

Port/Protocol Combination Counts:

Port,Protocol,Count
22,tcp,1
23,tcp,1
25,tcp,1
110,tcp,1
143,tcp,1
443,tcp,1
993,tcp,1
1024,tcp,1
49158,tcp,1
80,tcp,1

Explanation:

Tag Counts shows that:

sv_P2 was matched once (likely for a (443, tcp) record).
sv_P1 was matched twice (maybe for (25, tcp) and (23, tcp), etc.).
sv_P4 matched once (perhaps (22, tcp)).
email matched 3 times (for (110, tcp), (993, tcp), (143, tcp)).
Untagged matched 9 times (flows whose (dstport,protocol) did not appear in the CSV lookup).
Port/Protocol Combination Counts simply lists every unique (dstport, protocol) that appeared in the flow logs and how many times it appeared. This count is independent of whether or not that combination had a matching tag.

### 5. Handling Edge Cases and Assumptions

We need to maintain a small mapping, for example:
6 -> tcp
17 -> udp
1 -> icmp
etc.

If the log file has protocol numbers that are not recognized, you can either:
Tag them as "Untagged", or
Log a warning and skip them, or
(Depending on your design) treat them as a literal numeric protocol.

## References & Further Reading

- 📖 [AWS VPC Flow Logs Documentation][https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html].
- 📖 [IANA Protocol Numbers][https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml].
- 📖 [Python Official Docs][https://docs.python.org/3/].
