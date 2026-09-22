class DensityAnalyzer:
    """Density heuristic based on object count and image area."""

    def __init__(self, low=0.000010, medium=0.000025):
        self.low = low
        self.medium = medium

    def classify(self, object_count, width, height):
        area = max(width * height, 1)
        density = object_count / area
        if density < self.low:
            return "LOW"
        if density < self.medium:
            return "MEDIUM"
        return "HIGH"

    def score(self, object_count, width, height):
        area = max(width * height, 1)
        return object_count / area
