from report_data.ingestion_libs import ingest_inventory_backplane_data, \
        ingest_inventory_card_data, ingest_network_interface_data, \
        ingest_alarms_data, ingest_gpon_onu_stats_data, \
        ingest_olt_line_status_data, ingest_onu_line_status_data, \
        ingest_slot_status_data, ingest_card_stats_data


class IngestionRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, command, ingestion_function):
        self.registry[command] = ingestion_function

    def get_ingestion_method(self, command):
        return self.registry.get(command,  None)

ingestion_registry = IngestionRegistry()

print('Registering HW Inventory Backplane ingestion method...')
ingestion_registry.register('HW Inventory Backplane', ingest_inventory_backplane_data)
print('HW Inventory Backplane ingestion method registered successfully.', ingestion_registry.registry) 
 
ingestion_registry.register('HW Inventory - Sfp', ingest_network_interface_data)
ingestion_registry.register('Alarms', ingest_alarms_data)
ingestion_registry.register('ONU-Line-Stats', ingest_onu_line_status_data)
ingestion_registry.register('OLT-Line-Stats', ingest_olt_line_status_data)
ingestion_registry.register('HW Inventory - Card ROM Version', ingest_inventory_card_data)
ingestion_registry.register('GPON-ONU-Stats', ingest_gpon_onu_stats_data)
ingestion_registry.register('Card Status', ingest_card_stats_data)
ingestion_registry.register('Slot Status', ingest_slot_status_data)