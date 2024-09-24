import csv
from collections import defaultdict

protocol_map = {
    '1': 'icmp',       # Internet Control Message Protocol
    '2': 'igmp',       # Internet Group Management Protocol
    '6': 'tcp',        # Transmission Control Protocol
    '17': 'udp',       # User Datagram Protocol
    '41': 'encap',     # Encapsulation
    '47': 'gre',       # Generic Routing Encapsulation
    '50': 'esp',       # Encrypted Security Payload
    '51': 'ah',        # Authentication Header
    '58': 'icmpv6',    # ICMP for IPv6
    '89': 'ospf',      # Open Shortest Path First
    '103': 'pim',      # Protocol Independent Multicast
    '132': 'sctp',     # Stream Control Transmission Protocol
}

def load_lookup_table(lookup_file):
    lookup = {}
    with open(lookup_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dstport = row['dstport'].strip()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()
            lookup[(dstport, protocol)] = tag
    return lookup

def parse_flow_logs(flow_log_file, lookup):
    tag_count = defaultdict(int)
    port_protocol_count = defaultdict(int)
    untagged_count = 0
    
    with open(flow_log_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            dstport = parts[5]
            protocol_num = parts[7]

            protocol = protocol_map.get(protocol_num, None)

            if protocol is None:
                untagged_count += 1
                continue
            
            # Check if there is a matching tag in the lookup table
            tag = lookup.get((dstport, protocol), 'Untagged')
            if tag == 'Untagged':
                untagged_count += 1
            else:
                tag_count[tag] += 1
            
            # Count port/protocol combinations
            port_protocol_count[(dstport, protocol)] += 1

    return tag_count, port_protocol_count, untagged_count

def write_output(tag_count, port_protocol_count, untagged_count, output_file):
    try:
        with open(output_file, 'w') as file:
            # Write Tag Counts
            file.write("Tag Counts:\nTag,Count\n")
            for tag, count in tag_count.items():
                file.write(f"{tag},{count}\n")
            file.write(f"Untagged,{untagged_count}\n\n")
            
            # Write Port/Protocol Combination Counts
            file.write("Port/Protocol Combination Counts:\nPort,Protocol,Count\n")
            for (port, protocol), count in port_protocol_count.items():
                file.write(f"{port},{protocol},{count}\n")
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")

def main():
    lookup_file = 'lookup_table.csv'  # The lookup table CSV file
    flow_log_file = 'flow_logs.txt'  # The flow log file
    output_file = 'output.txt'  # The output file

    # Step 1: Load the lookup table
    lookup = load_lookup_table(lookup_file)

    # Step 2: Parse the flow logs and count tags/port-protocol combinations
    tag_count, port_protocol_count, untagged_count = parse_flow_logs(flow_log_file, lookup)

    # Step 3: Write the output to a file
    write_output(tag_count, port_protocol_count, untagged_count, output_file)
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main()
