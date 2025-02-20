import datetime

def generate_invoice_prefix():
    return f"INV-{datetime.datetime.now().strftime('%Y%m%d')}-"