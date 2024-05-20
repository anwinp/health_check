# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class InventoryBp(models.Model):
    node_ip_address = models.CharField(primary_key=True, max_length=255)  # The composite primary key (node_ip_address, serial_num) found, that is not supported. The first column is selected.
    eeprom_contents = models.CharField(max_length=255)
    eeprom_id = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    size = models.IntegerField()
    card_type = models.CharField(max_length=255)
    card_version = models.CharField(max_length=255)
    serial_num = models.CharField(max_length=255)
    shelf_number = models.CharField(max_length=255)
    clei_code = models.CharField(max_length=255)
    cksum = models.CharField(max_length=255)
    feature_bits_modification_date = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'inventory_bp'
        unique_together = (('node_ip_address', 'serial_num'),)


class InventoryCard(models.Model):
    card = models.CharField(primary_key=True, max_length=10)
    rom_version = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    node_ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory_card'


class NetworkInterface(models.Model):
    node_ip = models.CharField(primary_key=True, max_length=15)  # The composite primary key (node_ip, interface) found, that is not supported. The first column is selected.
    interface = models.CharField(max_length=50)
    vendor_name = models.CharField(max_length=100)
    vendor_oui = models.CharField(max_length=10)
    vendor_part_number = models.CharField(max_length=50)
    vendor_revision_level = models.CharField(max_length=10)
    serial_number = models.CharField(max_length=50)
    manufacturing_date = models.DateField()
    connector_type = models.CharField(max_length=50)
    transceiver_type = models.CharField(max_length=50)
    fiber_link_length_km = models.IntegerField()
    fiber_link_length_100m = models.IntegerField()
    nominal_bit_rate_gbps = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'network_interface'
        unique_together = (('node_ip', 'interface'),)


class NodeAlarms(models.Model):
    node_ip = models.CharField(max_length=15)
    resource_id = models.CharField(max_length=50)
    alarm_type = models.CharField(max_length=50)
    alarm_severity = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'node_alarms'


class NodeCardStats(models.Model):
    node_ip = models.CharField(max_length=15)
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
        managed = False
        db_table = 'node_card_stats'


class NodeGponOnuStats(models.Model):
    node_ip = models.CharField(max_length=15)
    slot = models.CharField(max_length=5)
    sub_port = models.CharField(max_length=10)
    upstream_bip_units = models.DecimalField(max_digits=65535, decimal_places=65535)
    fec_corrected_bytes = models.DecimalField(max_digits=65535, decimal_places=65535)
    fec_corrected_codewords = models.DecimalField(max_digits=65535, decimal_places=65535)
    fec_uncorrected_codewords = models.DecimalField(max_digits=65535, decimal_places=65535)
    total_received_codewords = models.DecimalField(max_digits=65535, decimal_places=65535)
    received_bytes = models.DecimalField(max_digits=65535, decimal_places=65535)
    received_packets = models.DecimalField(max_digits=65535, decimal_places=65535)
    transmitted_bytes = models.DecimalField(max_digits=65535, decimal_places=65535)
    transmitted_packets = models.DecimalField(max_digits=65535, decimal_places=65535)
    unreceived_bursts = models.DecimalField(max_digits=65535, decimal_places=65535)
    bip_error = models.DecimalField(max_digits=65535, decimal_places=65535)
    remote_bip_error = models.DecimalField(max_digits=65535, decimal_places=65535)
    drift_of_window_indications = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'node_gpon_onu_stats'


class NodeInfo(models.Model):
    node_ip = models.CharField(primary_key=True, max_length=15)
    node_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'node_info'


class NodeOltLineStatus(models.Model):
    node_ip = models.CharField(max_length=15)
    shelf = models.IntegerField()
    slot = models.IntegerField()
    port = models.IntegerField()
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
        managed = False
        db_table = 'node_olt_line_status'


class NodeOnuLineStatus(models.Model):
    node_ip = models.CharField(max_length=15)
    shelf = models.IntegerField()
    slot = models.IntegerField()
    port = models.IntegerField()
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
        managed = False
        db_table = 'node_onu_line_status'


class NodeSlotStatus(models.Model):
    node_ip = models.CharField(max_length=15)
    component = models.CharField(max_length=100)
    shelf = models.IntegerField()
    slot = models.CharField(max_length=10)
    type = models.CharField(max_length=100)
    card_version = models.CharField(max_length=50)
    software_version = models.CharField(max_length=50)
    uptime = models.DurationField()
    mode = models.CharField(max_length=50)
    rom_version = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    additional_information = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=20)
    slots_status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'node_slot_status'
