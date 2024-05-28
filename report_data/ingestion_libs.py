
from report_data.models import InventoryBackPlane, Alarms, SlotStatus, InventoryCard, NetworkInterface, Alarms, CardStats, OltLineStatus, OnuLineStatus, GponOnuStats
from django.db.utils import IntegrityError
from datetime import datetime


def ingest_inventory_backplane_data(node, data_list):
    """
    Ingests a list of inventory backplane data dictionaries into the InventoryBackPlane table.

    Parameters:
    node (Node): The node instance associated with the inventory backplane data.
    data_list (list): A list of dictionaries containing the inventory backplane data.

    Example data_list:
    [
        {
            'EEPROM contents': 'for slot 0',
            'EEPROM_ID': '06 -- BACKPLANE',
            'Version': '01',
            'Size': '054',
            'CardType': '20701 -- BACKPLANE_MXK_1421',
            'CardVersion': '800-03406-01-A',
            'SerialNum': '12822670',
            'ShelfNumber': '00001',
            'CLEI Code': 'No CLEI',
            'Cksum': '0x221A',
            'Feature bits modification date': '0/0/2000 00:00:00'
        }
    ]

    Returns:
    None
    """
    for data in data_list:
        try:
            InventoryBackPlane.objects.create(
                node=node,
                eeprom_contents=data.get('EEPROM contents', ''),
                eeprom_id=data.get('EEPROM_ID', ''),
                version=data.get('Version', ''),
                size=int(data.get('Size', 0)),
                card_type=data.get('CardType', ''),
                card_version=data.get('CardVersion', ''),
                serial_num=data.get('SerialNum', ''),
                shelf_number=data.get('ShelfNumber', ''),
                clei_code=data.get('CLEI Code', ''),
                cksum=data.get('Cksum', ''),
                feature_bits_modification_date=data.get('Feature bits modification date', '')
            )
            print(f"Data for {data['EEPROM contents']} ingested successfully.")
        except IntegrityError:
            print(f"Data for {data['EEPROM contents']} already exists and was not ingested.")
        except Exception as e:
            print(f"Error ingesting data for {data['EEPROM contents']}: {e}")


def ingest_alarms_data(node, data_list):
    """
    Ingests a list of alarm data dictionaries into the Alarms table.

    Parameters:
    node (Node): The node instance associated with the alarms data.
    data_list (list): A list of dictionaries containing the alarms data.

    Example data_list:
    [
        {
            'ResourceId': '1-m1-1-0/eth',
            'AlarmType': 'linkDown',
            'AlarmSeverity': 'critical'
        },
        ...
    ]

    Returns:
    None
    """
    for data in data_list:
        try:
            Alarms.objects.create(
                node=node,
                resource_id=data.get('ResourceId', ''),
                alarm_type=data.get('AlarmType', ''),
                alarm_severity=data.get('AlarmSeverity', '')
            )
            print(f"Alarm for {data['ResourceId']} ingested successfully.")
        except IntegrityError:
            print(f"Alarm for {data['ResourceId']} already exists and was not ingested.")
        except Exception as e:
            print(f"Error ingesting alarm for {data['ResourceId']}: {e}")


def ingest_slot_status_data(node, data_list):
    """
    Ingests a list of slot status data dictionaries into the SlotStatus table.

    Parameters:
    node (Node): The node instance associated with the slot status data.
    data_list (list): A list of dictionaries containing the slot status data.

    Example data_list:
    [
        {
            'Component': 'Management Cards',
            'Shelf': '1',
            'Slot': 'm1',
            'Chassis Type': 'MXK 1421',
            'Type': '*MXK-MC-TOP',
            'Card Version': '800-03681-01-A',
            'Software Version': 'MXK 3.4.2.144.007.2',
            'Uptime': '149 days, 12 hours, 17 minutes',
            'Mode': 'FUNCTIONAL',
            'ROM Version': 'MXK 3.4.2.144.007',
            'Serial Number': '8676551',
            'Additional Information': 'm1',
            'State': 'RUNNING',
            'Slots Status': 'RUNNING'
        },
        ...
    ]

    Returns:
    None
    """
    for data in data_list:
        try:
            SlotStatus.objects.create(
                node=node,
                component=data.get('Component', ''),
                shelf=int(data.get('Shelf', 0)),
                slot=data.get('Slot', ''),
                chassis_type=data.get('Chassis Type', ''),
                type=data.get('Type', ''),
                card_version=data.get('Card Version', ''),
                software_version=data.get('Software Version', ''),
                uptime=data.get('Uptime', ''),
                mode=data.get('Mode', ''),
                rom_version=data.get('ROM Version', ''),
                serial_number=data.get('Serial Number', ''),
                additional_information=data.get('Additional Information', ''),
                state=data.get('State', ''),
                slots_status=data.get('Slots Status', '')
            )
            print(f"Slot status for {data['Slot']} ingested successfully.")
        except IntegrityError:
            print(f"Slot status for {data['Slot']} already exists and was not ingested.")
        except Exception as e:
            print(f"Error ingesting slot status for {data['Slot']}: {e}")


def ingest_card_stats_data(node, data_list):
    """
    Ingests a list of card stats data dictionaries into the CardStats table.

    Parameters:
    node (Node): The node instance associated with the card stats data.
    data_list (list): A list of dictionaries containing the card stats data.

    Example data_list:
    [
        {
            'Slot': '1',
            'CPU Idle (%)': 91,
            'CPU Usage (%)': 9,
            'Memory Utilization (%)': 47.14,
            'Card Memory Used (KB)': '754,780',
            'Card Memory Peak (KB)': '356,499',
            'Card Memory Available (KB)': '398,997',
            'Status': '1 - OK',
            'Uptime': '149:12:05:49',
            'Software Version': 'MXK 3.4.2.144.007.2'
        },
        ...
    ]

    Returns:
    None
    """
    for data in data_list:
        try:
            CardStats.objects.create(
                node=node,
                slot=data.get('Slot', ''),
                cpu_idle_percent=int(data.get('CPU Idle (%)', 0)),
                cpu_usage_percent=int(data.get('CPU Usage (%)', 0)),
                memory_utilization_percent=float(data.get('Memory Utilization (%)', 0)),
                card_memory_used_kb=data.get('Card Memory Used (KB)', '').replace(',', ''),
                card_memory_peak_kb=data.get('Card Memory Peak (KB)', '').replace(',', ''),
                card_memory_available_kb=data.get('Card Memory Available (KB)', '').replace(',', ''),
                status=data.get('Status', ''),
                uptime=data.get('Uptime', ''),
                software_version=data.get('Software Version', '')
            )
            print(f"Card stats for slot {data['Slot']} ingested successfully.")
        except IntegrityError:
            print(f"Card stats for slot {data['Slot']} already exists and was not ingested.")
        except Exception as e:
            print(f"Error ingesting card stats for slot {data['Slot']}: {e}")


def ingest_onu_line_status_data(node, data_list):
    """
    Ingests a list of ONU line status data dictionaries into the OnuLineStatus table.

    Parameters:
    node (Node): The node instance associated with the ONU line status data.
    data_list (list): A list of dictionaries containing the ONU line status data.

    Example data_list:
    [
        {
            'Shelf': '1',
            'Slot': '1',
            'Port': '1',
            'Channel': '0',
            'Line Type': 'ONU subport',
            '1': 'ACT',
            '2': 'ACT',
            '3': 'ACT',
            '4': 'ACT',
            '5': 'ACT',
            '6': 'ACT',
            '7': 'ACT',
            '8': 'ACT',
            '9': 'ACT',
            '10': 'ACT',
            '11': 'ACT',
            '12': 'ACT',
            '13': 'ACT',
            '14': 'OOS',
            ...
        },
        ...
    ]

    Returns:
    None
    """
    for data in data_list:
        try:
            OnuLineStatus.objects.create(
                node=node,
                shelf=int(data.get('Shelf', 0)),
                slot=int(data.get('Slot', 0)),
                port=int(data.get('Port', 0)),
                channel=int(data.get('Channel', 0)),
                line_type=data.get('Line Type', ''),
                line_1=data.get('1', ''),
                line_2=data.get('2', ''),
                line_3=data.get('3', ''),
                line_4=data.get('4', ''),
                line_5=data.get('5', ''),
                line_6=data.get('6', ''),
                line_7=data.get('7', ''),
                line_8=data.get('8', ''),
                line_9=data.get('9', ''),
                line_10=data.get('10', ''),
                line_11=data.get('11', ''),
                line_12=data.get('12', ''),
                line_13=data.get('13', ''),
                line_14=data.get('14', ''),
                line_15=data.get('15', ''),
                line_16=data.get('16', ''),
                line_17=data.get('17', ''),
                line_18=data.get('18', ''),
                line_19=data.get('19', ''),
                line_20=data.get('20', ''),
                line_21=data.get('21', ''),
                line_22=data.get('22', ''),
                line_23=data.get('23', ''),
                line_24=data.get('24', ''),
                line_25=data.get('25', ''),
                line_26=data.get('26', ''),
                line_27=data.get('27', ''),
                line_28=data.get('28', ''),
                line_29=data.get('29', ''),
                line_30=data.get('30', ''),
                line_31=data.get('31', ''),
                line_32=data.get('32', '')
            )
            print(f"ONU line status for shelf {data['Shelf']} slot {data['Slot']} port {data['Port']} ingested successfully.")
        except IntegrityError:
            print(f"ONU line status for shelf {data['Shelf']} slot {data['Slot']} port {data['Port']} already exists and was not ingested.")
        except Exception as e:
            print(f"Error ingesting ONU line status for shelf {data['Shelf']} slot {data['Slot']} port {data['Port']}: {e}")


def ingest_olt_line_status_data(node, data_list):
    """
    Ingests a list of OLT line status data dictionaries into the OltLineStatus table.

    Parameters:
    node (Node): The node instance associated with the OLT line status data.
    data_list (list): A list of dictionaries containing the OLT line status data.

    Example data_list:
    [
        {
            'Shelf': '1',
            'Slot': '1',
            'Port': '1',
            'Channel': '0',
            'Line Type': 'OLT subport',
            '1': 'ACT',
            '2': 'ACT',
            '3': 'ACT',
            '4': 'ACT',
            '5': 'ACT',
            '6': 'ACT',
            '7': 'ACT',
            '8': 'ACT',
            '9': 'ACT',
            '10': 'ACT',
            '11': 'ACT',
            '12': 'ACT',
            '13': 'ACT',
            '14': 'ACT',
            ...
        },
        ...
    ]

    Returns:
    None
    """
    for data in data_list:
        try:
            OltLineStatus.objects.create(
                node=node,
                shelf=int(data.get('Shelf', 0)),
                slot=int(data.get('Slot', 0)),
                port=int(data.get('Port', 0)),
                channel=int(data.get('Channel', 0)),
                line_type=data.get('Line Type', ''),
                line_1=data.get('1', ''),
                line_2=data.get('2', ''),
                line_3=data.get('3', ''),
                line_4=data.get('4', ''),
                line_5=data.get('5', ''),
                line_6=data.get('6', ''),
                line_7=data.get('7', ''),
                line_8=data.get('8', ''),
                line_9=data.get('9', ''),
                line_10=data.get('10', ''),
                line_11=data.get('11', ''),
                line_12=data.get('12', ''),
                line_13=data.get('13', ''),
                line_14=data.get('14', ''),
                line_15=data.get('15', ''),
                line_16=data.get('16', '')
            )
            print(f"OLT line status for shelf {data['Shelf']} slot {data['Slot']} port {data['Port']} ingested successfully.")
        except IntegrityError:
            print(f"OLT line status for shelf {data['Shelf']} slot {data['Slot']} port {data['Port']} already exists and was not ingested.")
        except Exception as e:
            print(f"Error ingesting OLT line status for shelf {data['Shelf']} slot {data['Slot']} port {data['Port']}: {e}")


def ingest_gpon_onu_stats_data(node, data_list):
    """
    Ingests a list of GPON ONU stats data dictionaries into the GponOnuStats table.

    Parameters:
    node (Node): The node instance associated with the GPON ONU stats data.
    data_list (list): A list of dictionaries containing the GPON ONU stats data.

    Example data_list:
    [
        {
            'Slot': '1-1',
            'Sub Port': 'ONU(1)',
            'Upstream Bip UNits': 184316109705504,
            'FEC Corrected Bytes': 0,
            'FEC Corrected codewords': 0,
            'FEC Uncorrected codewords': 0,
            'Total received codewords': 0,
            'received bytes': 322011187600,
            'received packets': 1449823755,
            'transmitted bytes': 3955217584194,
            'transmitted packets': 2849438534,
            'Unreceived bursts': 2,
            'BIP Error': 9,
            'Remote BIP Error': 0,
            'Drift of Window Indications': 0
        },
        ...
    ]

    Returns:
    None
    """
    for data in data_list:
        try:
            GponOnuStats.objects.create(
                node=node,
                slot=data.get('Slot', ''),
                sub_port=data.get('Sub Port', ''),
                upstream_bip_units=data.get('Upstream Bip UNits', 0),
                fec_corrected_bytes=data.get('FEC Corrected Bytes', 0),
                fec_corrected_codewords=data.get('FEC Corrected codewords', 0),
                fec_uncorrected_codewords=data.get('FEC Uncorrected codewords', 0),
                total_received_codewords=data.get('Total received codewords', 0),
                received_bytes=data.get('received bytes', 0),
                received_packets=data.get('received packets', 0),
                transmitted_bytes=data.get('transmitted bytes', 0),
                transmitted_packets=data.get('transmitted packets', 0),
                unreceived_bursts=data.get('Unreceived bursts', 0),
                bip_error=data.get('BIP Error', 0),
                remote_bip_error=data.get('Remote BIP Error', 0),
                drift_of_window_indications=data.get('Drift of Window Indications', 0)
            )
            print(f"GPON ONU stats for slot {data['Slot']} sub port {data['Sub Port']} ingested successfully.")
        except IntegrityError:
            print(f"GPON ONU stats for slot {data['Slot']} sub port {data['Sub Port']} already exists and was not ingested.")
        except Exception as e:
            print(f"Error ingesting GPON ONU stats for slot {data['Slot']} sub port {data['Sub Port']}: {e}")


def ingest_network_interface_data(node, data_list):
    """
    Ingests a list of network interface data dictionaries into the NetworkInterface table.

    Parameters:
    node (Node): The node instance associated with the network interface data.
    data_list (list): A list of dictionaries containing the network interface data.

    Example data_list:
    [
        {
            'Interface': '1-1-1-0/gponolt',
            'Vendor Name': 'Ligent',
            'Vendor OUI': '00-01-47',
            'Vendor Part Number': 'LTE3680M-BH',
            'Vendor Revision Level': '3.8',
            'Serial Number': 'LIGJ03B6004892',
            'Manufacturing Date': '2022-06-21',
            'Connector Type': 'sc (1)',
            'Transceiver Type': 'sfp (3)',
            '9/125mm Fiber Link Length (km)': '20',
            '9/125mm Fiber Link Length (100m)': '200',
            'Nominal Bit Rate (Gbps)': '25'
        },
        ...
    ]

    Returns:
    None
    """
    for data in data_list:
        try:
            NetworkInterface.objects.create(
                node=node,
                interface=data.get('Interface', ''),
                vendor_name=data.get('Vendor Name', ''),
                vendor_oui=data.get('Vendor OUI', ''),
                vendor_part_number=data.get('Vendor Part Number', ''),
                vendor_revision_level=data.get('Vendor Revision Level', ''),
                serial_number=data.get('Serial Number', ''),
                manufacturing_date=data.get('Manufacturing Date', '1900-01-01'),
                connector_type=data.get('Connector Type', ''),
                transceiver_type=data.get('Transceiver Type', ''),
                nominal_bit_rate_gbps=int(data.get('Nominal Bit Rate (Gbps)', 0)),
                fiber_link_length_km=int(data.get('9/125mm Fiber Link Length (km)', 0)),
                fiber_link_length_100m=int(data.get('9/125mm Fiber Link Length (100m)', 0))
            )
            print(f"Network interface {data['Interface']} ingested successfully.")
        except IntegrityError:
            print(f"Network interface {data['Interface']} already exists and was not ingested.")
        except Exception as e:
            print(f"Error ingesting network interface {data['Interface']}: {e}")



def ingest_inventory_card_data(node, data_list):
    """
    Ingests a list of inventory card data dictionaries into the InventoryCard table.

    Parameters:
    node (Node): The node instance associated with the inventory card data.
    data_list (list): A list of dictionaries containing the inventory card data.

    Example data_list:
    [
        {
            'Card': 'm1',
            'ROM Version': 'MXK 3.4.2.144.007',
            'Timestamp': 'Aug  5 2022, 12:30:26'
        },
        ...
    ]

    Returns:
    None
    """
    for data in data_list:
        try:
            # Parse the timestamp to the correct format
            timestamp_str = data.get('Timestamp', '1900-01-01 00:00:00')
            timestamp = datetime.strptime(timestamp_str, '%b %d %Y, %H:%M:%S')

            InventoryCard.objects.create(
                node=node,
                card=data.get('Card', ''),
                rom_version=data.get('ROM Version', ''),
                timestamp=timestamp
            )
            print(f"Inventory card {data['Card']} ingested successfully.")
        except ValueError as ve:
            print(f"Error parsing date for inventory card {data['Card']}: {ve}")
        except IntegrityError:
            print(f"Inventory card {data['Card']} already exists and was not ingested.")
        except Exception as e:
            print(f"Error ingesting inventory card {data['Card']}: {e}")
