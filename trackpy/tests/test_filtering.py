from pandas import DataFrame

from trackpy import filter_stubs
from trackpy.tests.common import StrictTestCase

class TestFilterStubs(StrictTestCase): 
    def test_tracks_shorter_than_5_frames_removed(self):
        track_lengths = [2, 9, 5, 4]
        test_data = []
        for particle in range(4): 
            for frame in range(track_lengths[particle]):
                test_data.append({
                    'frame':frame,
                    'particle':particle
                })
        tracks = DataFrame.from_records(test_data)

        filtered_tracks: DataFrame = filter_stubs(tracks, 5)

        remaining_particles: list[int] = list(filtered_tracks['particle'].unique())
        assert remaining_particles == [1, 2]
