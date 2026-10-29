from pandas import DataFrame

from trackpy import filter_stubs

import pytest

class TestFilterStubs:
    @pytest.mark.parametrize("frame_threshold,expected", [
        (1, [0, 1, 2, 3, 4, 5, 6]),
        (2, [0, 1, 2, 3, 4, 5, 6]),
        (3, [1, 2, 3, 4, 5, 6]),
        (5, [1, 2, 4, 5, 6]),
        (10, [4, 5, 6]),
        (50, [5, 6])])
    def test_removes_tracks_shorter_than_threshold(self, frame_threshold:int, expected:list[int]):
        track_lengths = [2, 9, 5, 4, 49, 50, 51]
        test_data = []
        for particle in range(7): 
            for frame in range(track_lengths[particle]):
                test_data.append({
                    'frame':frame,
                    'particle':particle
                })
        tracks = DataFrame.from_records(test_data)

        filtered_tracks: DataFrame = filter_stubs(tracks, frame_threshold)

        remaining_particles:list[int] = [int(particle) 
                                         for particle in filtered_tracks['particle'].unique()]
        assert remaining_particles == expected