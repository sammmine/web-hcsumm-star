# TC2-1: Deepen Call Chain (t0)
# Struktur: Linear Pendek (Baseline)

def main():
    start_process()

def start_process():
    initialize_engine()

def initialize_engine():
    load_resource()

def load_resource():
    access_disk()

def access_disk():
    read_raw_bytes()

def read_raw_bytes():
    emit_success_signal()

def emit_success_signal():
    pass # leaf