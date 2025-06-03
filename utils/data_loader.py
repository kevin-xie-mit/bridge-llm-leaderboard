import pandas as pd
import json
from pathlib import Path
from typing import Dict, List

class LeaderboardDataLoader:
    """Handles loading and managing leaderboard data"""
    
    def __init__(self):
        self.abs_path = Path(__file__).parent.parent
        self.task_information = self._load_task_information()
        self.leaderboard_data = self._load_leaderboard_data()
        self.dataframes = self._create_dataframes()
        self.original_avg_performances = self._store_original_performances()
        self.n_models = self._calculate_n_models()
        
    def _load_task_information(self) -> Dict:
        """Load task information from JSON"""
        with open(self.abs_path / "task_information.json", 'r') as file:
            return json.load(file)
    
    def _load_leaderboard_data(self) -> Dict[str, Dict]:
        """Load all leaderboard JSON data"""
        leaderboard_files = {
            'zero_shot': 'leaderboards/Zero-Shot_leaderboard_data.json',
            'few_shot': 'leaderboards/Few-Shot_leaderboard_data.json',
            'cot': 'leaderboards/CoT_leaderboard_data.json'
        }
        
        data = {}
        for key, filepath in leaderboard_files.items():
            with open(self.abs_path / filepath, 'r') as file:
                data[key] = json.load(file)
        
        return data
    
    def _create_dataframes(self) -> Dict[str, pd.DataFrame]:
        """Create pandas DataFrames from JSON data"""
        dataframes = {}
        for key in ['zero_shot', 'few_shot', 'cot']:
            json_file = f"leaderboards/{key.replace('_', '-').title()}_leaderboard_data.json"
            if key == 'few_shot':
                json_file = "leaderboards/Few-Shot_leaderboard_data.json"
            elif key == 'cot':
                json_file = "leaderboards/CoT_leaderboard_data.json"
            else:
                json_file = "leaderboards/Zero-Shot_leaderboard_data.json"
                
            dataframes[key] = pd.read_json(self.abs_path / json_file, precise_float=True)
        
        return dataframes
    
    def _store_original_performances(self) -> Dict[str, pd.Series]:
        """Store original average performances for reset functionality"""
        return {
            key: df["Average Performance"].copy() 
            for key, df in self.dataframes.items()
        }
    
    def _calculate_n_models(self) -> int:
        """Calculate number of models from the data"""
        return int(list(self.leaderboard_data['zero_shot']["Model"].keys())[-1]) + 1
    
    def get_dataframe(self, leaderboard_type: str) -> pd.DataFrame:
        """Get dataframe for specific leaderboard type"""
        return self.dataframes[leaderboard_type]
    
    def get_leaderboard_json(self, leaderboard_type: str) -> Dict:
        """Get JSON data for specific leaderboard type"""
        return self.leaderboard_data[leaderboard_type]
    
    def get_original_performance(self, leaderboard_type: str) -> pd.Series:
        """Get original average performance for specific leaderboard type"""
        return self.original_avg_performances[leaderboard_type] 