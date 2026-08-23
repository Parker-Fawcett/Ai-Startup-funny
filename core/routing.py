"""Pure route-ordering math: greedy nearest-neighbor over haversine distance."""

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

EARTH_RADIUS_MILES: Final[float] = 3958.8

type LatLng = tuple[float, float]


@dataclass(frozen=True, slots=True)
class GeoPoint:
    """A routable stop carrying a stable domain identifier."""

    stop_id: int
    lat: float
    lng: float

    @property
    def coords(self) -> LatLng:
        """Return the point as a plain ``(lat, lng)`` pair."""
        return (self.lat, self.lng)


def haversine_miles(a: LatLng, b: LatLng) -> float:
    """Return the great-circle distance in miles between two ``(lat, lng)`` pairs."""
    lat_a, lon_a = math.radians(a[0]), math.radians(a[1])
    lat_b, lon_b = math.radians(b[0]), math.radians(b[1])
    d_lat = lat_b - lat_a
    d_lon = lon_b - lon_a
    half_chord = (
        math.sin(d_lat / 2) ** 2 + math.cos(lat_a) * math.cos(lat_b) * math.sin(d_lon / 2) ** 2
    )
    return 2 * EARTH_RADIUS_MILES * math.asin(math.sqrt(half_chord))


def nearest_neighbor_order(start: LatLng, stops: Sequence[GeoPoint]) -> list[int]:
    """Greedily order ``stops`` by proximity, re-anchoring at each visited stop.

    Ties break toward earlier input order. The input sequence is not mutated.
    """
    remaining: list[GeoPoint] = list(stops)
    ordered_ids: list[int] = []
    cursor: LatLng = start
    while remaining:
        nearest_index = min(
            range(len(remaining)),
            key=lambda i, c=cursor: (haversine_miles(c, remaining[i].coords), i),
        )
        nearest = remaining.pop(nearest_index)
        ordered_ids.append(nearest.stop_id)
        cursor = nearest.coords
    return ordered_ids
