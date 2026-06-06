# TC1-1: Branch Expansion (t1)
# Target: ±20-22 Nodes (Refactored)
# Perubahan: Ekspansi cabang pada process_data

def main():
    data = fetch_data()
    processed = process_data(data)
    save_report(processed)

def fetch_data():
    db_connect()
    return db_query()

def db_connect():
    pass 

def db_query():
    pass

def process_data(d):
    d = filter_nulls(d)
    # NEW: Cabang baru ditambahkan di sini
    run_advanced_analytics(d)
    return calculate_basic_stats(d)

# --- NEW BRANCH START (Ekspansi TC1) ---
def run_advanced_analytics(d):
    detect_anomalies(d)
    predict_future_trends(d)
    generate_meta_summary(d)

def detect_anomalies(d):
    check_outliers(d)
    log_anomaly_report()

def check_outliers(d):
    pass # leaf

def log_anomaly_report():
    pass # leaf

def predict_future_trends(d):
    apply_linear_model()

def apply_linear_model():
    pass # leaf

def generate_meta_summary(d):
    format_table_output()

def format_table_output():
    pass # leaf
# --- NEW BRANCH END ---

def filter_nulls(d):
    pass

def calculate_basic_stats(d):
    get_sum(d)
    get_avg(d)
    return d

def get_sum(d):
    pass

def get_avg(d):
    pass

def save_report(d):
    write_to_disk(d)

def write_to_disk(d):
    pass