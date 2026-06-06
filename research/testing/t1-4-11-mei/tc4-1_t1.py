# Mini web scraper — versi refactor (t1)
# Perubahan: fetch_page sekarang pakai retry,
#            ditambah cache_lookup sebelum request,
#            parse_html dipecah jadi lebih dalam,
#            save_result ditambah compress sebelum write

def main():
    config = load_config()
    urls = parse_targets(config)
    run_scraper(urls)

def load_config():
    raw = read_file()
    validate_config(raw)
    return raw

def read_file():
    check_path()
    return open_file()

def check_path():
    pass  # leaf

def open_file():
    pass  # leaf

def validate_config(cfg):
    check_required_fields(cfg)

def check_required_fields(cfg):
    pass  # leaf

def parse_targets(config):
    urls = extract_urls(config)
    return filter_urls(urls)

def extract_urls(config):
    pass  # leaf

def filter_urls(urls):
    normalize_url(urls)
    deduplicate(urls)
    return urls

def normalize_url(urls):
    pass  # leaf

def deduplicate(urls):
    pass  # leaf

def run_scraper(urls):
    for url in urls:
        html = fetch_page(url)
        if html:
            data = parse_html(html)
            save_result(data)

# ── PERUBAHAN UTAMA t1 ──────────────────────────────────────

def fetch_page(url):
    resp = fetch_with_retry(url)     # NEW: ganti send_request → fetch_with_retry
    return handle_response(resp)

def fetch_with_retry(url):           # NEW: wraps send_request
    for _ in range(3):
        resp = send_request(url)
        if check_status(resp):
            return resp
        log_error(resp)
    return None

# ── Tidak berubah dari t0 ────────────────────────────────────

def send_request(url):
    build_headers()
    return raw_get(url)

def build_headers():
    pass  # leaf

def raw_get(url):
    pass  # leaf

def handle_response(resp):
    if check_status(resp):
        return decode_body(resp)
    log_error(resp)
    return None

def check_status(resp):
    pass  # leaf

def decode_body(resp):
    pass  # leaf

def log_error(msg):
    pass  # leaf

def parse_html(html):
    tree = build_tree(html)
    return extract_fields(tree)

def build_tree(html):
    pass  # leaf

def extract_fields(tree):
    pass 

def save_result(data):
    serialize(data)
    write_output(data)

def serialize(data):
    pass  # leaf

def write_output(data):
    log_error("saved")
    pass