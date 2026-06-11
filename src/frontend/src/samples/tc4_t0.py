# Mini web scraper — versi awal (t0)
# ~24 fungsi, tidak simetris

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

def fetch_page(url):
    resp = send_request(url)
    return handle_response(resp)

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
    pass  # leaf (dipanggil dari banyak tempat)

def parse_html(html):
    tree = build_tree(html)
    return extract_fields(tree)

def build_tree(html):
    pass  # leaf

def extract_fields(tree):
    return tree

def save_result(data):
    serialize(data)
    write_output(data)

def serialize(data):
    pass  # leaf

def write_output(data):
    log_error("saved")  # reuse log_error
    pass