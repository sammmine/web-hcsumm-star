# TC3-1: Add New Exit Node (t0)
# Struktur: Deep Linear Chain dengan 1 Exit Node

def main():
    system_entry()

def system_entry():
    gatekeeper_proxy()

def gatekeeper_proxy():
    secure_session_init()

def secure_session_init():
    business_orchestrator()

def business_orchestrator():
    data_transformer()

def data_transformer():
    schema_validator()

def schema_validator():
    persistence_layer()

def persistence_layer():
    io_writer()

def io_writer():
    disk_sync()

def disk_sync():
    # Hanya ada satu jalan keluar (Success)
    final_success_exit()

def final_success_exit():
    print("Process Finished Successfully")
    pass # Terminal Node A