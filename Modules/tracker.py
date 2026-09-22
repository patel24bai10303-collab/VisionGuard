import math

class CentroidTracker:
    """Simple centroid tracker suitable for an academic demonstration."""

    def __init__(self, max_distance=80, max_missing=15):
        self.next_id = 1
        self.tracks = {}
        self.missing = {}
        self.max_distance = max_distance
        self.max_missing = max_missing

    @staticmethod
    def centroid(bbox):
        x1, y1, x2, y2 = bbox
        return ((x1+x2)//2, (y1+y2)//2)

    def update(self, detections):
        new_tracks = {}
        unmatched = set(range(len(detections)))

        # Greedy nearest-neighbour matching, restricted to same class.
        for tid, old in self.tracks.items():
            best_i, best_dist = None, float("inf")
            for i in list(unmatched):
                d = detections[i]
                if d["label"] != old["label"]:
                    continue
                c = self.centroid(d["bbox"])
                dist = math.dist(c, old["centroid"])
                if dist < best_dist:
                    best_i, best_dist = i, dist
            if best_i is not None and best_dist <= self.max_distance:
                d = detections[best_i]
                new_tracks[tid] = {**d, "id": tid, "centroid": self.centroid(d["bbox"])}
                unmatched.remove(best_i)
                self.missing[tid] = 0
            else:
                self.missing[tid] = self.missing.get(tid, 0) + 1

        for i in unmatched:
            d = detections[i]
            tid = self.next_id
            self.next_id += 1
            new_tracks[tid] = {**d, "id": tid, "centroid": self.centroid(d["bbox"])}
            self.missing[tid] = 0

        self.tracks = {
            tid: track for tid, track in new_tracks.items()
            if self.missing.get(tid, 0) <= self.max_missing
        }
        return list(self.tracks.values())

    @property
    def active_tracks(self):
        return list(self.tracks.values())
