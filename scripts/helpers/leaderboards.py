import json
import pandas as pd


class LeaderboardProcessor:
    def __init__(self, output_path):
        self.output_path = output_path

    def update_leaderboards(self, old_leaderboard_json, new_models):
        """
        Args:
            - old_leaderboard_json: json file including the previous leaderboard data
            - new_models: List[str] --> a list of strings of new models to update the leaderboard with
        """
        pass