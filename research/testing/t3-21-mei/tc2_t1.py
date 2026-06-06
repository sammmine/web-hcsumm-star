# TC2-1: Deepen Call Chain (t1)
# Struktur: Linear Panjang (Refactored)
# Perubahan: Penambahan rantai delegasi/wrapper

def main():
    proxy_entry()

# --- NEW CHAIN START ---
def proxy_entry():
    security_filter()

def security_filter():
    logging_wrapper()

def logging_wrapper():
    start_process()
# --- NEW CHAIN END ---

def start_process():
    engine_delegator()

# --- NEW CHAIN START ---
def engine_delegator():
    initialize_engine()
# --- NEW CHAIN END ---

def initialize_engine():
    resource_manager()

# --- NEW CHAIN START ---
def resource_manager():
    load_resource()
# --- NEW CHAIN END ---

def load_resource():
    disk_controller()

# --- NEW CHAIN START ---
def disk_controller():
    io_scheduler()

def io_scheduler():
    access_disk()
# --- NEW CHAIN END ---

def access_disk():
    low_level_reader()

# --- NEW CHAIN START ---
def low_level_reader():
    read_raw_bytes()
# --- NEW CHAIN END ---

def read_raw_bytes():
    signal_handler()

# --- NEW CHAIN START ---
def signal_handler():
    emit_success_signal()
# --- NEW CHAIN END ---

def emit_success_signal():
    pass # leaf