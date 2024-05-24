
from report_data.models import InventoryBackPlane
from django.db.utils import IntegrityError


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

