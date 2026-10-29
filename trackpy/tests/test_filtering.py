from pandas import DataFrame

from trackpy import filter_stubs, filter_clusters

import pytest

class TestFilterStubs:
    def test_cannot_filter_stubs_with_only_particle_col(self):
        tracks = DataFrame({'particle':[]})

        with pytest.raises(ValueError) as e:
            filter_stubs(tracks)

    def test_cannot_filter_stubs_with_only_frame_col(self):
        tracks = DataFrame({'frame':[]})

        with pytest.raises(ValueError) as e:
            filter_stubs(tracks)


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

class TestFilterClusters:
    def test_cannot_filter_clusters_if_frame_col_is_missing(self):
        tracks = DataFrame({'size': [], 'particle':[]})

        with pytest.raises(ValueError) as e:
            filter_clusters(tracks)

    def test_cannot_filter_clusters_if_size_col_is_missing(self):
        tracks = DataFrame({'particle': [], 'frame':[]})

        with pytest.raises(ValueError) as e:
            filter_clusters(tracks)

    def test_cannot_filter_clusters_if_particle_col_is_missing(self):
        tracks = DataFrame({'size': [], 'frame':[]})

        with pytest.raises(ValueError) as e:
            filter_clusters(tracks)

    def test_removes_particles_with_size_in_66th_percentile(self):
        tracks = DataFrame.from_records([{'particle':particle, 'size':particle, 'frame':0}
                                         for particle in range(1, 11)])

        filtered_tracks:DataFrame = filter_clusters(tracks, 0.66)

        remaining_particles:list[int] = [int(particle)
                                         for particle in filtered_tracks['particle'].unique()]
        assert remaining_particles == [1, 2, 3, 4, 5, 6]