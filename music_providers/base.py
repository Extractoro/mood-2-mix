from abc import ABC, abstractmethod


class MusicProvider(ABC):
    @abstractmethod
    def recommend_tracks(
            self,
            mood: str,
            genres: list[str],
            valence: float,
            energy: float,
            limit: int = 10
    ):
        pass

    @abstractmethod
    def create_playlist_with_tracks(
            self,
            name: str,
            description: str
    ) -> str:
        pass
