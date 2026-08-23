from core.routing import GeoPoint, nearest_neighbor_order


class TestNearestNeighborOrder:
    def test_returns_empty_for_no_stops(self):
        assert nearest_neighbor_order((0.0, 0.0), []) == []

    def test_returns_single_stop_unchanged(self):
        stops = [GeoPoint(stop_id=7, lat=1.0, lng=1.0)]

        assert nearest_neighbor_order((0.0, 0.0), stops) == [7]

    def test_visits_greedy_nearest_first(self):
        far = GeoPoint(stop_id=3, lat=0.0, lng=3.0)
        near = GeoPoint(stop_id=1, lat=0.0, lng=1.0)
        mid = GeoPoint(stop_id=2, lat=0.0, lng=2.0)

        assert nearest_neighbor_order((0.0, 0.0), [far, near, mid]) == [1, 2, 3]

    def test_reanchors_at_each_visited_stop(self):
        a = GeoPoint(stop_id=1, lat=0.0, lng=2.0)
        b = GeoPoint(stop_id=2, lat=0.0, lng=1.0)
        c = GeoPoint(stop_id=3, lat=0.0, lng=4.0)
        d = GeoPoint(stop_id=4, lat=0.0, lng=3.5)

        assert nearest_neighbor_order((0.0, 0.0), [a, b, c, d]) == [2, 1, 4, 3]

    def test_equidistant_tie_breaks_on_input_order(self):
        north = GeoPoint(stop_id=1, lat=1.0, lng=0.0)
        east = GeoPoint(stop_id=2, lat=0.0, lng=1.0)

        assert nearest_neighbor_order((0.0, 0.0), [east, north]) == [2, 1]
