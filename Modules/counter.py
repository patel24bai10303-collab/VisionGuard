from collections import Counter

class VehicleCounter:
    def __init__(self):
        self.seen_ids = set()
        self.latest_counts = Counter()

    def update(self, tracks):
        for track in tracks:
            self.seen_ids.add(track["id"])
        self.latest_counts = Counter(t["category"] for t in tracks)

    def count_by_class(self, tracks):
        counts = Counter(t["category"] for t in tracks)
        keys = ["cars", "motorcycles", "buses", "trucks", "bicycles", "pedestrians"]
        return {k: int(counts.get(k, 0)) for k in keys}
