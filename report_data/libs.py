from .models import SlotStatus, NetworkInterface
from django.db.models import Count, Q
from collections import defaultdict


def fetch_olt_info_report_data():
    # Fetch data from SlotStatus and NetworkInterface
    slot_status_data = SlotStatus.objects.all()
    network_interface_data = NetworkInterface.objects.all()

    # Group data by node
    slot_status_by_node = defaultdict(list)
    for slot in slot_status_data:
        slot_status_by_node[slot.node.name].append(slot)

    network_interface_by_node = defaultdict(list)
    for iface in network_interface_data:
        network_interface_by_node[iface.node.name].append(iface)

    # Prepare data for each node
    report_data_by_node = {}
    for node in slot_status_by_node.keys() | network_interface_by_node.keys():
        slot_status = slot_status_by_node[node]
        network_interface = network_interface_by_node[node]

        chassis_types = {slot.chassis_type for slot in slot_status}
        software_versions = {slot.software_version for slot in slot_status}
        rom_versions = {slot.rom_version for slot in slot_status}
        active_cards = defaultdict(int)
        for slot in slot_status:
            active_cards[slot.type] += 1
        offline_cards = sum(1 for slot in slot_status if slot.mode == 'non-functional')
        
        # Count SFP Types by Vendor Name
        sfp_type_counts = defaultdict(int)
        for iface in network_interface:
            sfp_type_counts[iface.vendor_name] += 1
        sfp_types = [f"{vendor} X {count}" for vendor, count in sfp_type_counts.items()]

        report_data = [
            {"Info Type": "Chassis Type", "Data": ', '.join(chassis_types)},
            {"Info Type": "Software Version", "Data": ', '.join(software_versions)},
            {"Info Type": "ROM Version", "Data": ', '.join(rom_versions)},
            {"Info Type": "# Active Cards", "Data": ', '.join(f"{card_type} ({count})" for card_type, count in active_cards.items())},
            {"Info Type": "# Offline Cards", "Data": str(offline_cards)},
            {"Info Type": "PON Ports Active", "Data": ''},
            {"Info Type": "PON Ports Offline", "Data": ''},
            {"Info Type": "# ONTs", "Data": ''},
            {"Info Type": "SFP Types", "Data": ', '.join(sfp_types)},
            {"Info Type": "System Uptime", "Data": ''},  # System Uptime column added and left empty
        ]

        report_data_by_node[node] = report_data

    return report_data_by_node
