import gradio as gr
from gradio_leaderboard import Leaderboard, SelectColumns, SearchColumns
import config
from pathlib import Path
import pandas as pd
import json

import warnings
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union, Literal
import pandas as pd
from pandas.io.formats.style import Styler

import semantic_version
from dataclasses import dataclass, field

from gradio.components import Component
from gradio.data_classes import GradioModel
from gradio.events import Events

@dataclass
class SelectColumns:
    default_selection: Optional[list[str]] = field(default_factory=list)
    cant_deselect: Optional[list[str]] = field(default_factory=list)
    allow: bool = True
    label: Optional[str] = None
    show_label: bool = True
    info: Optional[str] = None

@dataclass
class ColumnFilter:
    column: str
    type: Literal["slider", "dropdown", "checkboxgroup", "boolean"] = None
    default: Optional[Union[int, float, List[Tuple[str, str]]]] = None
    choices: Optional[Union[int, float, List[Tuple[str, str]]]] = None
    label: Optional[str] = None
    info: Optional[str] = None
    show_label: bool = True
    min: Optional[Union[int, float]] = None
    max: Optional[Union[int, float]] = None
    
class DataframeData(GradioModel):
    headers: List[str]
    data: Union[List[List[Any]], List[Tuple[Any, ...]]]
    metadata: Optional[Dict[str, Optional[List[Any]]]] = None


abs_path = Path(__file__).parent

# Load the leaderboard data for 
zero_shot_df = pd.read_json("leaderboards/Zero-Shot_leaderboard_data.json", precise_float=True)
five_shot_df = pd.read_json("leaderboards/Few-Shot_leaderboard_data.json", precise_float=True)
cot_df = pd.read_json("leaderboards/CoT_leaderboard_data.json", precise_float=True)

# Original Average Performances
original_zero_shot_avg_perf = zero_shot_df["Average Performance"]
original_five_shot_avg_perf = five_shot_df["Average Performance"]
original_cot_avg_perf = cot_df["Average Performance"]

# Load the task information json data
with open("task_information.json", 'r') as file:
    task_information_json = json.load(file)

cot_currently_selected_filters = {
    "Language": [],
    "Task Type": [],
    "Clinical Context": [],
    "Data Access": [],
    "Applications": [],
    "Clinical Stage": []
}

five_shot_currently_selected_filters = {
    "Language": [],
    "Task Type": [],
    "Clinical Context": [],
    "Data Access": [],
    "Applications": [],
    "Clinical Stage": []
}

zero_shot_currently_selected_filters = {
    "Language": [],
    "Task Type": [],
    "Clinical Context": [],
    "Data Access": [],
    "Applications": [],
    "Clinical Stage": []
}

# with open("/Users/kevinxie/Desktop/Clinical NLP/Clinical-Text-Leaderboard/leaderboard_data.json", 'r') as file:
with open("leaderboards/Few-Shot_leaderboard_data.json", 'r') as file:
    five_shot_leaderboard_json = json.load(file)

with open("leaderboards/CoT_leaderboard_data.json", 'r') as file:
    CoT_leaderboard_json = json.load(file)

with open("leaderboards/Zero-Shot_leaderboard_data.json", 'r') as file:
    zero_shot_leaderboard_json = json.load(file)

valid_tasks = {'NUBES', 'NorSynthClinical-NER', 'MEDIQA 2023-sum-A', 'Medication extraction', 
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
               'n2c2 2014-CAD'}

n_models = int(list(zero_shot_leaderboard_json["Model"].keys())[-1]) + 1

def get_filtered_columns(filter_selections):
    """
    Given an array of selected filters, this function will return a list of all
    the columns that match the criteria.

    Input:
        filter_selections: dictionary of all task type filter selections

    Output:
        Returns a list of all valid tasks to display (by task name)
    """
    # Need to add a flag to this filter so that it only displays those that match all attributes
    valid_columns = []
    for task in task_information_json:
        task_info = task_information_json[task]
        
        # Flag to keep track of whether this task is valid
        isValid = True

        # Iterate through each attribute of the task
        for attribute in task_info:
            # If the filter is empty
            if not filter_selections[attribute]:
                continue

            value = task_info[attribute]

            # print(filter_selections[attribute])

            # Handle edge case for multiple categories
            if "," in value:
                all_categories = value.split(", ")

                flag = False
                for category in all_categories:
                    if category in filter_selections[attribute]:
                        flag = True
                        break

                if flag:  # one category matches
                    isValid = True

                else: # none of the categories matched
                    isValid  = False

            # Handle Brazilian Edge Case
            elif (value == 'Portuguese\n(Brazilian)') and ('Portuguese' in filter_selections[attribute]):
                isValid = True
                break
        
            elif value not in filter_selections[attribute]:
            # if filter_selections[attribute] not in task_info[attribute]:
                isValid = False
                # break

        if task in valid_tasks and isValid:
            valid_columns.append(task)

    return valid_columns

def isEmpty(currently_selected_filters):
    """
    Checks if there are no selected filters
    """
    flag = True
    for key, value in currently_selected_filters.items():
        if not value:
            continue
        else:
            return False
        
    return True


####################################################################################################
####### CoT Filters
####################################################################################################


def cot_filter_language(language_choice):
    # Update the Global store for the currently selected filters
    cot_currently_selected_filters["Language"] = language_choice

    if isEmpty(cot_currently_selected_filters):
        cot_df["Average Performance"] = original_cot_avg_perf
        return cot_df

    filtered_cols = get_filtered_columns(cot_currently_selected_filters)

    updated_performance = cot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    cot_df["Average Performance"] = cot_df.index.map(updated_performance_int)
    
    return cot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Size (B)', 'Average Performance'] + filtered_cols]
  
def cot_filter_task_type(task_type_choice):
    # Update the Global store for the currently selected filters
    cot_currently_selected_filters["Task Type"] = task_type_choice

    if isEmpty(cot_currently_selected_filters):
        cot_df["Average Performance"] = original_cot_avg_perf
        return cot_df

    filtered_cols = get_filtered_columns(cot_currently_selected_filters)

    updated_performance = cot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    cot_df["Average Performance"] = cot_df.index.map(updated_performance_int)

    return cot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]
    
def cot_filter_clinical_context(clinical_context_choice):
    # Update the Global store for the currently selected filters
    cot_currently_selected_filters["Clinical Context"] = clinical_context_choice

    if isEmpty(cot_currently_selected_filters):
        cot_df["Average Performance"] = original_cot_avg_perf
        return cot_df

    filtered_cols = get_filtered_columns(cot_currently_selected_filters)

    updated_performance = cot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    cot_df["Average Performance"] = cot_df.index.map(updated_performance_int)

    return cot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def cot_filter_applications(applications_choice):
    # Update the Global store for the currently selected filters
    cot_currently_selected_filters["Applications"] = applications_choice

    if isEmpty(cot_currently_selected_filters):
        cot_df["Average Performance"] = original_cot_avg_perf
        return cot_df

    filtered_cols = get_filtered_columns(cot_currently_selected_filters)

    updated_performance = cot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    cot_df["Average Performance"] = cot_df.index.map(updated_performance_int)

    return cot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def cot_filter_stage_options(stage_choice):
    # Update the Global store for the currently selected filters
    cot_currently_selected_filters["Clinical Stage"] = stage_choice

    if isEmpty(cot_currently_selected_filters):
        cot_df["Average Performance"] = original_cot_avg_perf
        return cot_df

    filtered_cols = get_filtered_columns(cot_currently_selected_filters)

    updated_performance = cot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    cot_df["Average Performance"] = cot_df.index.map(updated_performance_int)

    return cot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def cot_filter_data_access(data_access_choice):
    # Update the Global store for the currently selected filters
    cot_currently_selected_filters["Data Access"] = data_access_choice

    if isEmpty(cot_currently_selected_filters):
        cot_df["Average Performance"] = original_cot_avg_perf
        return cot_df

    filtered_cols = get_filtered_columns(cot_currently_selected_filters)

    updated_performance = cot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    cot_df["Average Performance"] = cot_df.index.map(updated_performance_int)

    return cot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def cot_update_average_performance(selected_columns):
    """
    When a user clicks filters to filter certain tasks, the average performance
    of the model should update. This function takes uses the updated filtered columns
    and calculates the average performances of only those columns. It then updates
    the leaderboard accordingly.
    """
    updated_average_performance = {}
    
    for i in range(n_models):
        performance = 0

        num_tasks = 0
        for task in selected_columns:
            num_tasks += 1
            performance += float(CoT_leaderboard_json[task][str(i)])

        if num_tasks == 0:
            num_tasks = 1
        
        updated_average_performance[f"{i}"] = float(round(performance / num_tasks, 2))

    return updated_average_performance


####################################################################################################
####### Few Shot Filters
####################################################################################################

def five_shot_filter_language(language_choice):
    # Update the Global store for the currently selected filters
    five_shot_currently_selected_filters["Language"] = language_choice

    if isEmpty(five_shot_currently_selected_filters):
        five_shot_df["Average Performance"] = original_five_shot_avg_perf
        return five_shot_df

    filtered_cols = get_filtered_columns(five_shot_currently_selected_filters)

    updated_performance = five_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    five_shot_df["Average Performance"] = five_shot_df.index.map(updated_performance_int)
    
    return five_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]
  
def five_shot_filter_task_type(task_type_choice):
    # Update the Global store for the currently selected filters
    five_shot_currently_selected_filters["Task Type"] = task_type_choice

    if isEmpty(five_shot_currently_selected_filters):
        five_shot_df["Average Performance"] = original_five_shot_avg_perf
        return five_shot_df

    filtered_cols = get_filtered_columns(five_shot_currently_selected_filters)

    updated_performance = five_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    five_shot_df["Average Performance"] = five_shot_df.index.map(updated_performance_int)

    return five_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def five_shot_filter_clinical_context(clinical_context_choice):
    # Update the Global store for the currently selected filters
    five_shot_currently_selected_filters["Clinical Context"] = clinical_context_choice

    if isEmpty(five_shot_currently_selected_filters):
        five_shot_df["Average Performance"] = original_five_shot_avg_perf
        return five_shot_df

    filtered_cols = get_filtered_columns(five_shot_currently_selected_filters)

    updated_performance = five_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    five_shot_df["Average Performance"] = five_shot_df.index.map(updated_performance_int)

    return five_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def five_shot_filter_applications(applications_choice):
    # Update the Global store for the currently selected filters
    five_shot_currently_selected_filters["Applications"] = applications_choice

    if isEmpty(five_shot_currently_selected_filters):
        five_shot_df["Average Performance"] = original_five_shot_avg_perf
        return five_shot_df

    filtered_cols = get_filtered_columns(five_shot_currently_selected_filters)

    updated_performance = five_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    five_shot_df["Average Performance"] = five_shot_df.index.map(updated_performance_int)

    return five_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def five_shot_filter_stage_options(stage_choice):
    # Update the Global store for the currently selected filters
    five_shot_currently_selected_filters["Clinical Stage"] = stage_choice

    if isEmpty(five_shot_currently_selected_filters):
        five_shot_df["Average Performance"] = original_five_shot_avg_perf
        return five_shot_df

    filtered_cols = get_filtered_columns(five_shot_currently_selected_filters)

    updated_performance = five_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    five_shot_df["Average Performance"] = five_shot_df.index.map(updated_performance_int)

    return five_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def five_shot_filter_data_access(data_access_choice):
    # Update the Global store for the currently selected filters
    five_shot_currently_selected_filters["Data Access"] = data_access_choice

    if isEmpty(five_shot_currently_selected_filters):
        five_shot_df["Average Performance"] = original_five_shot_avg_perf
        return five_shot_df

    filtered_cols = get_filtered_columns(five_shot_currently_selected_filters)

    updated_performance = five_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    five_shot_df["Average Performance"] = five_shot_df.index.map(updated_performance_int)

    return five_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]


def five_shot_update_average_performance(selected_columns):
    """
    When a user clicks filters to filter certain tasks, the average performance
    of the model should update. This function takes uses the updated filtered columns
    and calculates the average performances of only those columns. It then updates
    the leaderboard accordingly.
    """
    updated_average_performance = {}
    
    for i in range(n_models):
        performance = 0

        num_tasks = 0
        for task in selected_columns:
            num_tasks += 1
            performance += float(five_shot_leaderboard_json[task][str(i)])

        if num_tasks == 0:
            num_tasks = 1
        
        updated_average_performance[f"{i}"] = float(round(performance / num_tasks, 2))

    return updated_average_performance


####################################################################################################
###### Zero Shot Filters
####################################################################################################


def zero_shot_filter_language(language_choice):
    # Update the Global store for the currently selected filters
    zero_shot_currently_selected_filters["Language"] = language_choice

    if isEmpty(zero_shot_currently_selected_filters):
        zero_shot_df["Average Performance"] = original_zero_shot_avg_perf
        return zero_shot_df

    filtered_cols = get_filtered_columns(zero_shot_currently_selected_filters)

    updated_performance = zero_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    zero_shot_df["Average Performance"] = zero_shot_df.index.map(updated_performance_int)
    
    return zero_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]
  
def zero_shot_filter_task_type(task_type_choice):
    # Update the Global store for the currently selected filters
    zero_shot_currently_selected_filters["Task Type"] = task_type_choice

    if isEmpty(zero_shot_currently_selected_filters):
        zero_shot_df["Average Performance"] = original_zero_shot_avg_perf
        return zero_shot_df

    filtered_cols = get_filtered_columns(zero_shot_currently_selected_filters)

    updated_performance = zero_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    zero_shot_df["Average Performance"] = zero_shot_df.index.map(updated_performance_int)

    return zero_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]
    
def zero_shot_filter_clinical_context(clinical_context_choice):
    # Update the Global store for the currently selected filters
    zero_shot_currently_selected_filters["Clinical Context"] = clinical_context_choice

    if isEmpty(zero_shot_currently_selected_filters):
        zero_shot_df["Average Performance"] = original_zero_shot_avg_perf
        return zero_shot_df

    filtered_cols = get_filtered_columns(zero_shot_currently_selected_filters)

    updated_performance = zero_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    zero_shot_df["Average Performance"] = zero_shot_df.index.map(updated_performance_int)

    return zero_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def zero_shot_filter_applications(applications_choice):
    # Update the Global store for the currently selected filters
    zero_shot_currently_selected_filters["Applications"] = applications_choice

    if isEmpty(zero_shot_currently_selected_filters):
        zero_shot_df["Average Performance"] = original_zero_shot_avg_perf
        return zero_shot_df

    filtered_cols = get_filtered_columns(zero_shot_currently_selected_filters)

    updated_performance = zero_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    zero_shot_df["Average Performance"] = zero_shot_df.index.map(updated_performance_int)

    return zero_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def zero_shot_filter_stage_options(stage_choice):
    # Update the Global store for the currently selected filters
    zero_shot_currently_selected_filters["Clinical Stage"] = stage_choice

    if isEmpty(zero_shot_currently_selected_filters):
        zero_shot_df["Average Performance"] = original_zero_shot_avg_perf
        return zero_shot_df

    filtered_cols = get_filtered_columns(zero_shot_currently_selected_filters)

    updated_performance = zero_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    zero_shot_df["Average Performance"] = zero_shot_df.index.map(updated_performance_int)

    return zero_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def zero_shot_filter_data_access(data_access_choice):
    # Update the Global store for the currently selected filters
    zero_shot_currently_selected_filters["Data Access"] = data_access_choice

    if isEmpty(zero_shot_currently_selected_filters):
        zero_shot_df["Average Performance"] = original_zero_shot_avg_perf
        return zero_shot_df

    filtered_cols = get_filtered_columns(zero_shot_currently_selected_filters)

    updated_performance = zero_shot_update_average_performance(filtered_cols)

    # Convert dictionary keys to integers to match the DataFrame index
    updated_performance_int = {int(k): v for k, v in updated_performance.items()}

    # Map the values to the 'Average Performance' column based on index
    zero_shot_df["Average Performance"] = zero_shot_df.index.map(updated_performance_int)

    return zero_shot_df[['T', 'Model', 'Model: Domain', 'Model: Accessibility', 'Model: Size Range', 'Size (B)', 'Average Performance'] + filtered_cols]

def zero_shot_update_average_performance(selected_columns):
    """
    When a user clicks filters to filter certain tasks, the average performance
    of the model should update. This function takes uses the updated filtered columns
    and calculates the average performances of only those columns. It then updates
    the leaderboard accordingly.
    """
    updated_average_performance = {}
    
    for i in range(n_models):
        performance = 0

        num_tasks = 0
        for task in selected_columns:
            num_tasks += 1
            performance += float(zero_shot_leaderboard_json[task][str(i)])

        if num_tasks == 0:
            num_tasks = 1
        
        updated_average_performance[f"{i}"] = float(round(performance / num_tasks, 2))

    return updated_average_performance


def postprocess(self, value: pd.DataFrame) -> DataframeData:
        # Ensure that the "Average Performance" column exists
        if "Average Performance" in value.columns:
            # Sort the DataFrame by the "average performance" column in descending order
            value = value.sort_values(by="Average Performance", ascending=False)
        
            return DataframeData(
                headers=list(value.columns),  # type: ignore
                data=value.to_dict(orient="split")["data"],  # type: ignore
            )

        if value is None:
            return self.postprocess(pd.DataFrame({"column 1": []}))
        if isinstance(value, (str, pd.DataFrame)):
            if isinstance(value, str):
                value = pd.read_csv(value)  # type: ignore
            if len(value) == 0:
                return DataframeData(
                    headers=list(value.columns),  # type: ignore
                    data=[[]],  # type: ignore
                )
            return DataframeData(
                headers=list(value.columns),  # type: ignore
                data=value.to_dict(orient="split")["data"],  # type: ignore
            )
        elif isinstance(value, Styler):
            if semantic_version.Version(pd.__version__) < semantic_version.Version(
                "1.5.0"
            ):
                raise ValueError(
                    "Styler objects are only supported in pandas version 1.5.0 or higher. Please try: `pip install --upgrade pandas` to use this feature."
                )
            if self.interactive:
                warnings.warn(
                    "Cannot display Styler object in interactive mode. Will display as a regular pandas dataframe instead."
                )
            df: pd.DataFrame = value.data  # type: ignore
            if len(df) == 0:
                return DataframeData(
                    headers=list(df.columns),
                    data=[[]],
                    metadata=self.__extract_metadata(value),  # type: ignore
                )
            return DataframeData(
                headers=list(df.columns),
                data=df.to_dict(orient="split")["data"],  # type: ignore
                metadata=self.__extract_metadata(value),  # type: ignore
            )

# Models are sorted in order of decreasing average performance (best performance at the top!)
Leaderboard.postprocess = postprocess


####################################################################################################
###### Leaderboard
####################################################################################################

with gr.Blocks() as app:
    gr.Markdown("# BRIDGE (Benchmarking Large Language Models for Understanding Real-world Clinical Practice Text)")

    with gr.Tabs():
        with gr.Tab("README"):
            # gr.Markdown((Path(__file__).parent / "docs.md").read_text())
            html_content = (Path(__file__).parent / "docs.md").read_text()
            gr.HTML(html_content)

        with gr.Tab("Zero-Shot"):
            leaderboard = Leaderboard(
                value=zero_shot_df,
                select_columns = None,
                search_columns=SearchColumns(primary_column = "Model", secondary_columns = "",
                                     placeholder="Search by Model Name",
                                     label="Model Search"),
                hide_columns=["Model: Size Range", "Model: Accessibility"],
                filter_columns=["Model: Domain", "Model: Size Range", "Model: Accessibility"],
                datatype=config.TYPES,
            )

            # Language Filter
            all_languages = ['English', 'Spanish', 
                             'Chinese', 'Norwegian', 
                             'Russian', 'Portuguese', 
                             'German', 'Japanese', 'French']
            
            language_options = gr.CheckboxGroup(all_languages, label="Filter Task: Language")

            # Task Type Filter
            all_task_types = ['Question Answering', 'Text Classification', 'Named Entity Recognition', 
                              'Normalization and Coding', 'Natural Language Inference', 'Summarization', 
                              'Event Extraction', 'Semantic Similarity']


            task_type_options = gr.CheckboxGroup(all_task_types, label="Filter Task: Task Type")
            
            all_clinical_contexts = ['Neurology',  'Oncology',  'Radiology',  'Pulmonology',  
                                     'Cardiology',  'Dermatology',  'Critical Care',  'Nephrology',  
                                     'General',  'Endocrinology',  'Pediatrics',  'Pharmacology',  
                                     'Gastroenterology',  'Psychology']
            
            cc_options = gr.CheckboxGroup(all_clinical_contexts, label="Filter Task: Clinical Context")

            # Applications Filter
            all_applications = ['Procudure information', 'Concept standarization', 
                                'Specialist recommendation', 'Negation identification', 
                                'Clinical trial matching', 'Consultation summarization', 
                                'Semantic relation', 'Post-discharge patient management', 
                                'De-identification', 'Billing & Coding', 'Phenotyping', 
                                'Data organization', 'Temporal & Causality relation', 
                                'Summarization', 'Screen & Consultation', 'Diagnosis', 
                                'ADE & Incidents', 'Risk factor extraction', 'Prognosis', 
                                'Medication information']


            application_options = gr.CheckboxGroup(all_applications, label="Filter Task: Clinical Application")

            # Clinical Stage Filter
            all_stages = ['Treatment and Intervention', 'Triage and Referral', 
                          'Initial Assessment', 'Discharge and Administration', 
                          'Research', 'Diagnosis and Prognosis']
            
            stage_options = gr.CheckboxGroup(all_stages, label="Filter Task: Clinical Stage")

            # Data Access Filter
            all_data_access = ['Open Access', 'Regulated']
            
            da_options = gr.CheckboxGroup(all_data_access, label="Filter Task: Data Access")


            language_options.change(fn=zero_shot_filter_language, inputs=language_options, outputs=leaderboard)
            task_type_options.change(fn=zero_shot_filter_task_type, inputs=task_type_options, outputs=leaderboard)
            cc_options.change(fn=zero_shot_filter_clinical_context, inputs=cc_options, outputs=leaderboard)
            application_options.change(fn=zero_shot_filter_applications, inputs=application_options, outputs=leaderboard)
            da_options.change(fn=zero_shot_filter_data_access, inputs=da_options, outputs=leaderboard)
            stage_options.change(fn=zero_shot_filter_stage_options, inputs=stage_options, outputs=leaderboard)


        with gr.Tab("Few-Shot"):
            leaderboard = Leaderboard(
                value=five_shot_df,
                select_columns = None,
                search_columns=SearchColumns(primary_column = "Model", secondary_columns = "",
                                     placeholder="Search by Model Name",
                                     label="Model Search"),
                hide_columns=["Model: Size Range", "Model: Accessibility"],
                filter_columns=["Model: Domain", "Model: Size Range", "Model: Accessibility"],
                datatype=config.TYPES,
            )

            # Language Filter
            all_languages = ['English', 'Spanish', 
                             'Chinese', 'Norwegian', 
                             'Russian', 'Portuguese', 
                             'German', 'Japanese', 'French']
            
            language_options = gr.CheckboxGroup(all_languages, label="Filter Task: Language")

            # Task Type Filter
            all_task_types = ['Question Answering', 'Text Classification', 'Named Entity Recognition', 
                              'Normalization and Coding', 'Natural Language Inference', 'Summarization', 
                              'Event Extraction', 'Semantic Similarity']

            task_type_options = gr.CheckboxGroup(all_task_types, label="Filter Task: Task Type")


            # Clinical Context Filter
            all_clinical_contexts = ['Neurology',  'Oncology',  'Radiology',  'Pulmonology',  
                                     'Cardiology',  'Dermatology',  'Critical Care',  'Nephrology',  
                                     'General',  'Endocrinology',  'Pediatrics',  'Pharmacology',  
                                     'Gastroenterology',  'Psychology']
            
            cc_options = gr.CheckboxGroup(all_clinical_contexts, label="Filter Task: Clinical Context")

            # Applications Filter
            all_applications = ['Procudure information', 'Concept standarization', 
                                'Specialist recommendation', 'Negation identification', 
                                'Clinical trial matching', 'Consultation summarization', 
                                'Semantic relation', 'Post-discharge patient management', 
                                'De-identification', 'Billing & Coding', 'Phenotyping', 
                                'Data organization', 'Temporal & Causality relation', 
                                'Summarization', 'Screen & Consultation', 'Diagnosis', 
                                'ADE & Incidents', 'Risk factor extraction', 'Prognosis', 
                                'Medication information']

            application_options = gr.CheckboxGroup(all_applications, label="Filter Task: Clinical Application")

            # Clinical Stage Filter
            all_stages = ['Treatment and Intervention', 'Triage and Referral', 
                          'Initial Assessment', 'Discharge and Administration', 
                          'Research', 'Diagnosis and Prognosis']
            
            stage_options = gr.CheckboxGroup(all_stages, label="Filter Task: Clinical Stage")

            # Data Access Filter
            all_data_access = ['Open Access', 'Regulated']
            
            da_options = gr.CheckboxGroup(all_data_access, label="Filter Task: Data Access")

            language_options.change(fn=five_shot_filter_language, inputs=language_options, outputs=leaderboard)
            task_type_options.change(fn=five_shot_filter_task_type, inputs=task_type_options, outputs=leaderboard)
            cc_options.change(fn=five_shot_filter_clinical_context, inputs=cc_options, outputs=leaderboard)
            application_options.change(fn=five_shot_filter_applications, inputs=application_options, outputs=leaderboard)
            da_options.change(fn=five_shot_filter_data_access, inputs=da_options, outputs=leaderboard)
            stage_options.change(fn=five_shot_filter_stage_options, inputs=stage_options, outputs=leaderboard)


        with gr.Tab("CoT"):
            leaderboard = Leaderboard(
                value=cot_df,
                select_columns = None,
                search_columns=SearchColumns(primary_column = "Model", secondary_columns = "",
                                     placeholder="Search by Model Name",
                                     label="Model Search"),
                hide_columns=["Model: Size Range", "Model: Accessibility"],
                filter_columns=["Model: Domain", "Model: Size Range", "Model: Accessibility"],
                datatype=config.TYPES,
            )

            # Language Filter
            all_languages = ['English', 'Spanish', 
                             'Chinese', 'Norwegian', 
                             'Russian', 'Portuguese', 
                             'German', 'Japanese', 'French']
            
            language_options = gr.CheckboxGroup(all_languages, label="Filter Task: Language")

            # Task Type Filter
            all_task_types = ['Question Answering', 'Text Classification', 'Named Entity Recognition', 
                              'Normalization and Coding', 'Natural Language Inference', 'Summarization', 
                              'Event Extraction', 'Semantic Similarity']

            task_type_options = gr.CheckboxGroup(all_task_types, label="Filter Task: Task Type")

            # Clinical Context Filter
            all_clinical_contexts = ['Neurology',  'Oncology',  'Radiology',  'Pulmonology',  
                                     'Cardiology',  'Dermatology',  'Critical Care',  'Nephrology',  
                                     'General',  'Endocrinology',  'Pediatrics',  'Pharmacology',  
                                     'Gastroenterology',  'Psychology']
            
            cc_options = gr.CheckboxGroup(all_clinical_contexts, label="Filter Task: Clinical Context")

            # Applications Filter
            all_applications = ['Procudure information', 'Concept standarization', 
                                'Specialist recommendation', 'Negation identification', 
                                'Clinical trial matching', 'Consultation summarization', 
                                'Semantic relation', 'Post-discharge patient management', 
                                'De-identification', 'Billing & Coding', 'Phenotyping', 
                                'Data organization', 'Temporal & Causality relation', 
                                'Summarization', 'Screen & Consultation', 'Diagnosis', 
                                'ADE & Incidents', 'Risk factor extraction', 'Prognosis', 
                                'Medication information']

            application_options = gr.CheckboxGroup(all_applications, label="Filter Task: Clinical Application")

            # Clinical Stage Filter
            all_stages = ['Treatment and Intervention', 'Triage and Referral', 
                          'Initial Assessment', 'Discharge and Administration', 
                          'Research', 'Diagnosis and Prognosis']
            
            stage_options = gr.CheckboxGroup(all_stages, label="Filter Task: Clinical Stage")
            

            # Data Access Filter
            all_data_access = ['Open Access', 'Regulated']
            
            da_options = gr.CheckboxGroup(all_data_access, label="Filter Task: Data Access")


            language_options.change(fn=cot_filter_language, inputs=language_options, outputs=leaderboard)
            task_type_options.change(fn=cot_filter_task_type, inputs=task_type_options, outputs=leaderboard)
            cc_options.change(fn=cot_filter_clinical_context, inputs=cc_options, outputs=leaderboard)
            application_options.change(fn=cot_filter_applications, inputs=application_options, outputs=leaderboard)
            da_options.change(fn=cot_filter_data_access, inputs=da_options, outputs=leaderboard)

            stage_options.change(fn=cot_filter_stage_options, inputs=stage_options, outputs=leaderboard)

        
if __name__ == "__main__":
    app.launch()

