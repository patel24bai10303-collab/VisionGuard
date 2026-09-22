from modules.preprocessing import validate_media
from modules.density import DensityAnalyzer
from modules.counter import VehicleCounter

def test_validate_media():
    assert validate_media("road.jpg")[2] == "image"
    assert validate_media("traffic.mp4")[2] == "video"
    assert validate_media("file.exe")[0] is False

def test_density():
    analyzer = DensityAnalyzer()
    assert analyzer.classify(0, 1000, 1000) == "LOW"

def test_counter():
    counter = VehicleCounter()
    tracks = [
        {"id": 1, "category": "cars"},
        {"id": 2, "category": "cars"},
        {"id": 3, "category": "pedestrians"},
    ]
    counter.update(tracks)
    assert counter.count_by_class(tracks)["cars"] == 2
    assert counter.count_by_class(tracks)["pedestrians"] == 1
