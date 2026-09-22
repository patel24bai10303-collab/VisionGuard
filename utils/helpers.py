def vehicle_total(counts):
    return sum(counts.get(k, 0) for k in ("cars", "motorcycles", "buses", "trucks", "bicycles"))

def format_seconds(seconds):
    return f"{seconds:.2f}s"
