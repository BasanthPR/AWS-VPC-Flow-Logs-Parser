import sys
import os

def main():
    """
    Usage:
        python parse_flow_logs.py <flow_logs_file> <lookup_csv_file> <output_file>

    This script:
      1. Reads a flow logs file (version 2 default format).
      2. Reads a lookup CSV file (dstport,protocol,tag).
      3. Generates two reports:
         a) Tag Counts
         b) Port/Protocol Combination Counts
      4. Writes the reports into <output_file>.

    Additional Requirements:
      - Throw error if lookup table is empty.
      - Throw errors for invalid log file formatting (wrong # fields, version != 2).
    """

    # 1) Parsing command line arguments
    if len(sys.argv) < 4:
        print("Error: Missing arguments.")
        print("Usage: python parse_flow_logs.py <flow_logs_file> <lookup_csv_file> <output_file>")
        sys.exit(1)
    
    flow_logs_file = sys.argv[1] # Path to the VPC flow logs file
    lookup_csv_file = sys.argv[2] # Path to the CSV file that maps (dstport, protocol) to a tag
    output_file = sys.argv[3] # Path to the file where results will be written

    # 2) Printing debugging info
    outputPath = os.path.abspath(output_file)
    print(f"Will write results to: {outputPath}")

    # 3) Reading the lookup CSV into a dictionary
    #    Key:   (dstport_int, protocol_lowercase)
    #    Value: tag (string)
    lookupDict = {}
    try:
        with open(lookup_csv_file, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                # Skipping blank lines or commented lines
                if not line or line.startswith("#"):
                    continue
                parts = line.split(",")
                if len(parts) < 3:
                    continue

                dstportStr = parts[0].strip()
                protocolStr   = parts[1].strip().lower()
                tag         = parts[2].strip()

                try:
                    dstportInt = int(dstportStr)
                except ValueError:
                    continue

                lookupDict[(dstportInt, protocolStr)] = tag
    except FileNotFoundError:
        print(f"Error: Lookup file '{lookup_csv_file}' not found.")
        sys.exit(1)

    # 4) Throws error if lookup table is empty
    if not lookupDict:
        print("Error: The lookup table is empty. Please provide a valid lookup CSV.")
        sys.exit(1)

    # 5) Prepare counters
    #    - Tag counts: how many flows ended up with each tag
    #    - Port/Protocol counts: how many flows seen for each (dstport, protocol) pair
    tagCount = {}              # { tag: count }
    portProtocolCount = {}        # { (port, protocol): count }

    # 6) Protocol number -> text mapping
    #    VPC Flow Logs store protocol as a numeric field:
    #        6 => TCP, 17 => UDP, 1 => ICMP, etc.
    #    If we do not find it in this map, we just use the numeric string.
    protocolMap = {
        1:  "icmp",
        6:  "tcp",
        17: "udp",
        # Can add more if needed
    }

    # 7) Reading flow logs and populating counters
    lineNumber = 0
    try:
        with open(flow_logs_file, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                lineNumber += 1
                line = line.strip()
                
                # skip blank lines
                if not line:
                    continue

                fields = line.split()
                # Check for minimal fields (version 2 must have at least 14)
                if len(fields) < 14:
                    raise ValueError(
                        f"Error (line {lineNumber}): "
                        f"Wrong formatting in flow log. Only {len(fields)} fields found."
                    )

                # Checking version
                if fields[0] != "2":
                    raise ValueError(
                        f"Error (line {lineNumber}): "
                        f"Unsupported version '{fields[0]}'. Only version 2 is allowed."
                    )

                # field[6] = dstport, field[7] = protocol
                try:
                    dstportNum = int(fields[6])
                    protocolNum   = int(fields[7])
                except ValueError:
                    raise ValueError(
                        f"Error (line {lineNumber}): Cannot parse dstport/protocol as integers."
                    )

                # Convert protocol number to string
                if protocolNum in protocolMap:
                    protocolText = protocolMap[protocolNum].lower()
                else:
                    protocolText = str(protocolNum)  # fallback if unrecognized

                # Lookup the tag
                if (dstportNum, protocolText) in lookupDict:
                    tag = lookupDict[(dstportNum, protocolText)]
                else:
                    tag = "Untagged"

                # Update counters
                tagCount[tag] = tagCount.get(tag, 0) + 1
                pp_key = (dstportNum, protocolText)
                portProtocolCount[pp_key] = portProtocolCount.get(pp_key, 0) + 1

    except FileNotFoundError:
        print(f"Error: Flow logs file '{flow_logs_file}' not found.")
        sys.exit(1)
    except ValueError as e:
        # For formatting errors, print the message and exit
        print(str(e))
        sys.exit(1)

    # 8) Write results to output file
    print(f"Writing results to: {outputPath}")
    try:
        with open(output_file, "w", encoding="utf-8") as out:
            # a) Tag Counts
            out.write("Tag Counts:\n")
            out.write("Tag,Count\n")
            for t, cnt in tagCount.items():
                out.write(f"{t},{cnt}\n")
            out.write("\n")

            # b) Port/Protocol Combination Counts
            out.write("Port/Protocol Combination Counts:\n")
            out.write("Port,Protocol,Count\n")
            for (port, proto), count in portProtocolCount.items():
                out.write(f"{port},{proto},{count}\n")

        print("Output successfully written.")
    except Exception as e:
        print(f"Error writing to output file '{output_file}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()