import xml.etree.ElementTree as ET

def parse_nmap_xml(xml_output: str) -> list[dict]:
    root = ET.fromstring(xml_output)

    records = []

    for host in root.findall("host"):
        address_element = host.find("address")

        if address_element is None:
            continue

        host_address = address_element.get("addr", "Unknown")

        hostname = ""

        hostname_element = host.find("./hostnames/hostname")

        if hostname_element is not None:
            hostname = hostname_element.get("name", "")

        for port_element in host.findall("./ports/port"):
            state_element = port_element.find("state")
            service_element = port_element.find("service")

            record = {
                "host": host_address,
                "hostname": hostname,
                "port": int(port_element.get("portid", 0)),
                "protocol": port_element.get("protocol", ""),
                "state": (
                    state_element.get("state", "")
                    if state_element is not None
                    else ""
                ),
                "service": (
                    service_element.get("name", "")
                    if service_element is not None
                    else ""
                ),
                "product": (
                    service_element.get("product", "")
                    if service_element is not None
                    else ""
                ),
                "version": (
                    service_element.get("version", "")
                    if service_element is not None
                    else ""
                )
            }

            records.append(record)

    return records