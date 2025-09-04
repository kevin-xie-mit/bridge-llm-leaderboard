from typing import Dict, List, Any
import pandas as pd

class FilterManager:
    """Manages filtering logic for all leaderboard types"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.valid_tasks = {
            'NUBES', 'NorSynthClinical-NER', 'MEDIQA 2023-sum-A', 'Medication extraction', 
            'IMCS-V2-DAC', 'Cantemist-Coding', 'IFMIR-NER', 'EHRQA-QA', 'Ex4CDS', 'MedDG', 
            'MTS-Temporal', 'CHIP-MDCFNPC', 'n2c2 2014-Diabetes', 'MIMIC-III Outcome.LoS', 
            'n2c2 2014-Hypertension', 'RuCCoN', 'CARES-ICD10 Chapter', 'RuDReC-NER', 'MIMIC-IV DiReCT.Dis', 
            'n2c2 2014-Medication', 'iCorpus', 'Brateca-Hospitalization', 'n2c2 2010-Assertion', 
            'NorSynthClinical-PHI', 'IFMIR - NER&factuality', 'JP-STS', 'NorSynthClinical-RE', 
            'n2c2 2010-Concept', 'BARR2', 'IMCS-V2-NER', 'IMCS-V2-MRG', 'cMedQA', 'MedSTS', 
            'BRONCO150-NER&Status', 'n2c2 2018-ADE&medication', 'CLISTER', 'ClinicalNotes-UPMC', 
            'PPTS', 'CLIP', 'IMCS-V2-SR', 'EHRQA-Sub department', 'BrainMRI-AIS', 'Brateca-Mortality', 
            'meddocan', 'CHIP-CDEE', 'CAS-evidence', 'MEDIQA 2019-RQE', 'Cantemis-Norm', 'MEDIQA 2023-sum-B', 
            'CHIP-CTC', 'C-EMRS', 'CARES ICD10 Block', 'Cantemis-NER', 'CLINpt-NER', 'MEDIQA 2023-chat-A', 
            'n2c2 2014-De-identification', 'n2c2 2014-Hyperlipidemia', 'EHRQA-Primary department', 
            'ADE-Drug dosage', 'IFMIR-Incident type', 'MIMIC-III Outcome.Mortality', 'n2c2 2006-De-identification', 
            'CAS-label', 'MIMIC-IV CDM', 'CodiEsp-ICD-10-CM', 'n2c2 2010-Relation', 'CARES-ICD10 Subblock', 
            'MIE', 'HealthCareMagic-100k', 'ADE-Identification', 'MIMIC-IV DiReCT.PDD', 'ADE-Extraction', 
            'DialMed', 'GOUT-CC-Consensus', 'GraSSCo PHI', 'RuMedNLI', 'RuMedDaNet', 'CBLUE-CDN', 'icliniq-10k', 
            'CARDIO-DE', 'CARES-Area', 'DiSMed-NER', 'CodiEsp-ICD-10-PCS', 'MedNLI', 'MTS', 'MIMIC-IV BHC', 
            'n2c2 2014-CAD'
        }
        
        # Initialize filter states for each leaderboard type
        self.filter_states = {
            'zero_shot': self._create_empty_filter_state(),
            'few_shot': self._create_empty_filter_state(),
            'cot': self._create_empty_filter_state()
        }
    
    def _create_empty_filter_state(self) -> Dict[str, List]:
        """Create an empty filter state"""
        return {
            "Language": [],
            "Task Type": [],
            "Clinical Context": [],
            "Data Access": [],
            "Applications": [],
            "Clinical Stage": []
        }
    
    def get_filtered_columns(self, filter_selections: Dict[str, List]) -> List[str]:
        """
        Given an array of selected filters, return a list of all
        the columns that match the criteria.
        """
        valid_columns = []
        for task in self.data_loader.task_information:
            task_info = self.data_loader.task_information[task]
            
            # Flag to keep track of whether this task is valid
            is_valid = True

            # Iterate through each attribute of the task
            for attribute in task_info:
                # If the filter is empty
                if not filter_selections[attribute]:
                    continue

                value = task_info[attribute]

                # Handle edge case for multiple categories
                if "," in value:
                    all_categories = value.split(", ")
                    flag = False
                    for category in all_categories:
                        if category in filter_selections[attribute]:
                            flag = True
                            break
                    
                    if flag:  # one category matches
                        is_valid = True
                    else:  # none of the categories matched
                        is_valid = False

                # Handle Brazilian Edge Case
                elif (value == 'Portuguese\n(Brazilian)') and ('Portuguese' in filter_selections[attribute]):
                    is_valid = True
                    break
            
                elif value not in filter_selections[attribute]:
                    is_valid = False

            if task in self.valid_tasks and is_valid:
                valid_columns.append(task)

        return valid_columns

    def is_empty(self, filter_selections: Dict[str, List]) -> bool:
        """Check if there are no selected filters"""
        return all(not value for value in filter_selections.values())

    def update_average_performance(self, leaderboard_type: str, selected_columns: List[str]) -> Dict[str, float]:
        """
        Calculate updated average performance based on selected columns
        """
        updated_average_performance = {}
        leaderboard_json = self.data_loader.get_leaderboard_json(leaderboard_type)
        
        for i in range(self.data_loader.n_models):
            performance = 0
            num_tasks = 0
            
            for task in selected_columns:
                if task in leaderboard_json:
                    num_tasks += 1
                    performance += float(leaderboard_json[task][str(i)])

            if num_tasks == 0:
                num_tasks = 1
            
            updated_average_performance[f"{i}"] = float(round(performance / num_tasks, 2))

        return updated_average_performance

    def apply_filter(self, leaderboard_type: str, filter_type: str, filter_values: List[str]) -> pd.DataFrame:
        """
        Apply a filter to a specific leaderboard type and return updated dataframe
        """
        # Update the filter state
        self.filter_states[leaderboard_type][filter_type] = filter_values
        
        # Get the dataframe
        df = self.data_loader.get_dataframe(leaderboard_type).copy()
        
        # If no filters are applied, reset to original performance
        if self.is_empty(self.filter_states[leaderboard_type]):
            df["Average Performance"] = self.data_loader.get_original_performance(leaderboard_type)
            # Reset T column to original values when no filters are applied
            return df

        # Get filtered columns
        filtered_cols = self.get_filtered_columns(self.filter_states[leaderboard_type])
        
        # Update average performance
        updated_performance = self.update_average_performance(leaderboard_type, filtered_cols)
        
        # Convert dictionary keys to integers to match the DataFrame index
        updated_performance_int = {int(k): v for k, v in updated_performance.items()}
        
        # Map the values to the 'Average Performance' column based on index
        df["Average Performance"] = df.index.map(updated_performance_int)
        
        # Update T column to reflect new ranking based on filtered average performance
        # Sort by Average Performance in descending order and assign ranks 1, 2, 3, etc.
        df_sorted = df.sort_values(by="Average Performance", ascending=False, na_position='last')
        rank_mapping = {}
        for rank, idx in enumerate(df_sorted.index):
            rank_mapping[idx] = rank + 1
        
        # Apply the new ranking to the T column
        df["T"] = df.index.map(rank_mapping)
        
        # Return dataframe with filtered columns
        base_columns = ['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance']
        return df[base_columns + filtered_cols] 