# TC3-1: Add New Exit Node (t1)
# Struktur: Deep Chain dengan 2 Exit Nodes (Success & Failure)
# Penambahan: ±10 Node baru di jalur exit alternatif

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
    # NEW: Percabangan di akhir alur untuk menambah Exit Node baru
    if check_write_status():
        final_success_exit()
    else:
        # Jalur menuju Exit Node Baru
        error_handling_flow()

def check_write_status():
    return True

def final_success_exit():
    print("Process Finished Successfully")
    pass # Terminal Node A

# --- NEW EXIT PATH START (TC3 Expansion) ---
def error_handling_flow():
    rollback_transaction()
    alert_administrator()
    termination_failure()

def rollback_transaction():
    undo_io_changes()
    release_locks()

def undo_io_changes(): pass
def release_locks(): pass

def alert_administrator():
    send_error_log()

def send_error_log(): pass

def termination_failure():
    print("Process Terminated: Disk Error")
    pass # Terminal Node B (New Exit Node)
# --- NEW EXIT PATH END ---