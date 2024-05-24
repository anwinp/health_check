from report_data.ingestion_libs import ingest_inventory_backplane_data

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
 