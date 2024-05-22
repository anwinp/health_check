from django.db import models

class Node(models.Model):
    ip_address = models.GenericIPAddressField(primary_key=True)
    name = models.CharField(max_length=255)
    
class InventoryBackPlane(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    eeprom_contents = models.CharField(max_length=50)
    eeprom_id = models.CharField(max_length=20)
    version = models.CharField(max_length=10)
    size = models.IntegerField()
    card_type = models.CharField(max_length=30)
    card_version = models.CharField(max_length=20)
    serial_num = models.CharField(max_length=20)
    shelf_number = models.CharField(max_length=10)
    clei_code = models.CharField(max_length=10)
    cksum = models.CharField(max_length=10)
    feature_bits_modification_date = models.CharField(max_length=25)

    class Meta:
        db_table = 'inventory_backplane'
        unique_together = (('node', 'serial_num'),)


class InventoryCard(models.Model):
    card = models.CharField(primary_key=True, max_length=10)
    rom_version = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    node = models.ForeignKey(Node, on_delete=models.CASCADE)

    class Meta:
        db_table = 'inventory_card'


class NetworkInterface(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    interface = models.CharField(max_length=50)
    vendor_name = models.CharField(max_length=100)
    vendor_oui = models.CharField(max_length=10)
    vendor_part_number = models.CharField(max_length=50)
    vendor_revision_level = models.CharField(max_length=10)
    serial_number = models.CharField(max_length=50)
    manufacturing_date = models.DateField()
    connector_type = models.CharField(max_length=50)
    transceiver_type = models.CharField(max_length=50)
    nominal_bit_rate_gbps = models.IntegerField()
    fiber_link_length_km = models.IntegerField()
    fiber_link_length_100m = models.IntegerField()

    class Meta:
        db_table = 'network_interface'
        unique_together = (('node', 'interface'),)


class Alarms(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    resource_id = models.CharField(max_length=50)
    alarm_type = models.CharField(max_length=50)
    alarm_severity = models.CharField(max_length=20)

    class Meta:
        db_table = 'alarms'


class CardStats(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    slot = models.CharField(max_length=10)
    cpu_idle_percent = models.IntegerField()
    cpu_usage_percent = models.IntegerField()
    memory_utilization_percent = models.DecimalField(max_digits=5, decimal_places=2)
    card_memory_used_kb = models.CharField(max_length=20)
    card_memory_peak_kb = models.CharField(max_length=20)
    card_memory_available_kb = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    uptime = models.CharField(max_length=20)
    software_version = models.CharField(max_length=50)

    class Meta:
        db_table = 'card_stats'


class GponOnuStats(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    slot = models.CharField(max_length=5)
    sub_port = models.CharField(max_length=10)
    upstream_bip_units = models.DecimalField(max_digits=20, decimal_places=2)
    fec_corrected_bytes = models.BigIntegerField()
    fec_corrected_codewords = models.BigIntegerField()
    fec_uncorrected_codewords = models.BigIntegerField()
    total_received_codewords = models.BigIntegerField()
    received_bytes = models.BigIntegerField()
    received_packets = models.BigIntegerField()
    transmitted_bytes = models.BigIntegerField()
    transmitted_packets = models.BigIntegerField()
    unreceived_bursts = models.BigIntegerField()
    bip_error = models.BigIntegerField()
    remote_bip_error = models.BigIntegerField()
    drift_of_window_indications = models.IntegerField()

    class Meta:
        db_table = 'gpon_onu_stats'


class OltLineStatus(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    shelf = models.IntegerField()
    slot = models.IntegerField()
    port = models.IntegerField()
    channel = models.IntegerField()
    line_type = models.CharField(max_length=20)
    line_1 = models.CharField(max_length=10)
    line_2 = models.CharField(max_length=10)
    line_3 = models.CharField(max_length=10)
    line_4 = models.CharField(max_length=10)
    line_5 = models.CharField(max_length=10)
    line_6 = models.CharField(max_length=10)
    line_7 = models.CharField(max_length=10)
    line_8 = models.CharField(max_length=10)
    line_9 = models.CharField(max_length=10)
    line_10 = models.CharField(max_length=10)
    line_11 = models.CharField(max_length=10)
    line_12 = models.CharField(max_length=10)
    line_13 = models.CharField(max_length=10)
    line_14 = models.CharField(max_length=10)
    line_15 = models.CharField(max_length=10)
    line_16 = models.CharField(max_length=10)

    class Meta:
        db_table = 'olt_line_status'


class OnuLineStatus(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    shelf = models.IntegerField()
    slot = models.IntegerField()
    port = models.IntegerField()
    channel = models.IntegerField()
    line_type = models.CharField(max_length=20)
    line_1 = models.CharField(max_length=10)
    line_2 = models.CharField(max_length=10)
    line_3 = models.CharField(max_length=10)
    line_4 = models.CharField(max_length=10)
    line_5 = models.CharField(max_length=10)
    line_6 = models.CharField(max_length=10)
    line_7 = models.CharField(max_length=10)
    line_8 = models.CharField(max_length=10)
    line_9 = models.CharField(max_length=10)
    line_10 = models.CharField(max_length=10)
    line_11 = models.CharField(max_length=10)
    line_12 = models.CharField(max_length=10)
    line_13 = models.CharField(max_length=10)
    line_14 = models.CharField(max_length=10)
    line_15 = models.CharField(max_length=10)
    line_16 = models.CharField(max_length=10)
    line_17 = models.CharField(max_length=10)
    line_18 = models.CharField(max_length=10)
    line_19 = models.CharField(max_length=10)
    line_20 = models.CharField(max_length=10)
    line_21 = models.CharField(max_length=10)
    line_22 = models.CharField(max_length=10)
    line_23 = models.CharField(max_length=10)
    line_24 = models.CharField(max_length=10)
    line_25 = models.CharField(max_length=10)
    line_26 = models.CharField(max_length=10)
    line_27 = models.CharField(max_length=10)
    line_28 = models.CharField(max_length=10)
    line_29 = models.CharField(max_length=10)
    line_30 = models.CharField(max_length=10)
    line_31 = models.CharField(max_length=10)
    line_32 = models.CharField(max_length=10)

    class Meta:
        db_table = 'onu_line_status'


class SlotStatus(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    component = models.CharField(max_length=50)
    shelf = models.IntegerField()
    slot = models.CharField(max_length=5)
    type = models.CharField(max_length=50)
    card_version = models.CharField(max_length=20)
    software_version = models.CharField(max_length=20)
    uptime = models.CharField(max_length=50)
    mode = models.CharField(max_length=20)
    rom_version = models.CharField(max_length=20)
    serial_number = models.CharField(max_length=20)
    additional_information = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=20)
    slots_status = models.CharField(max_length=20)

    class Meta:
        db_table = 'slot_status'
