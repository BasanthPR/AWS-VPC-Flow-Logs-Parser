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
12. [License](#license)  

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

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
