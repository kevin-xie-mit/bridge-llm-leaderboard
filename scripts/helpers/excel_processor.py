import pandas as pd
import json
from .CONSTANTS import *

class ExcelProcessor:
    def __init__(self, excel_path, invalid_models=None):
        """Initialize the ExcelProcessor with an Excel file.
        
        Args:
            excel_path (str): Path to the Excel file containing model and task data.
        """
        # excel_path = path to excel file
        self.sheet_path = excel_path 
        self.excel_data = self.load_excel()
        self.model_sheet = self.load_sheet("Models (Simplified)")
        self.invalid_models = invalid_models

        print("You have excluded the following models: ", self.invalid_models)

        # Get all of the valid models (exclude invalid models)
        self.valid_models = self.get_valid_models(self.invalid_models)

        # print("VALID MODELS: ", self.valid_models)


    def load_excel(self):
        """Load the Excel file into a pandas ExcelFile object.
        
        Returns:
            pd.ExcelFile: The loaded Excel file object.
        """
        return pd.ExcelFile(self.sheet_path)

    def load_sheet(self, sheet_name):
        """Load a specific sheet from the Excel file.
        
        Args:
            sheet_name (str): Name of the sheet to load.
            
        Returns:
            pd.DataFrame: The loaded sheet as a pandas DataFrame.
        """
        return self.excel_data.parse(sheet_name)
    
    def get_valid_models(self, invalid_models=None):
        """Get all valid models from the Models sheet, excluding invalid ones.
        
        Returns:
            list: List of valid model names that should be included in evaluation.
        """
        valid_models = []

        for idx, model_name in enumerate(self.model_sheet["Name"]):
            if model_name not in invalid_models:
                valid_models.append(model_name)

        return valid_models

    def get_valid_columns(self, sheet_name):
        """Get all non-empty columns from a specified sheet.
        
        Args:
            sheet_name (str): Name of the sheet to analyze.
            
        Returns:
            list: List of valid column names (excluding unnamed columns).
        """
        valid_columns = []

        for column in self.load_sheet(sheet_name).columns:
            if column.split(' ')[0] != "Unnamed:":
                valid_columns.append(column.strip())

        return valid_columns

    def get_model_information(self,
                            sheet_name = "Models (Simplified)", 
                            name_column = "Name", 
                            domain_column = "Domain",
                            license_column = "License",
                            size_column = "Size (B)",
                          ):
        """Extract model information from the Models sheet.
        
        Args:
            sheet_name (str, optional): Name of the sheet containing model info. 
                Defaults to "Models (Simplified)".
            name_column (str, optional): Column name containing model names. 
                Defaults to "Name".
            domain_column (str, optional): Column name containing model domains. 
                Defaults to "Domain".
            license_column (str, optional): Column name containing license info. 
                Defaults to "License".
            size_column (str, optional): Column name containing model sizes. 
                Defaults to "Size (B)".
        
        Returns:
            tuple: A tuple containing 7 dictionaries:
                - model_name_info: Model names indexed by position
                - domain_info: Model domains mapped using DOMAIN_MAPPING
                - license_info: License information (abbreviated if needed)
                - accessibility_info: Accessibility mapped using LICENSE_MAPPING
                - displayed_size_info: Raw size values for display
                - hidden_size_info: Size ranges for filtering
                - T_info: Position markers for the leaderboard
        """
        # Load the model sheet
        model_sheet = self.load_sheet(sheet_name)

        # Everything to be returned.
        T_info = {}
        model_name_info = {}
        domain_info = {}
        license_info = {}
        accessibility_info = {}
        displayed_size_info = {} # shown on leaderboard
        hidden_size_info = {} # hidden column

        def map_size(param_size):
            """Map parameter size to predefined ranges.
            
            Args:
                param_size: The parameter size value.
                
            Returns:
                str: Size range category.
            """
            if param_size == "/":
                return "None"
            if param_size == "Unknown":
                return "Unknown"
            size = int(param_size)
            if size < 5:
                return "0-5"
            elif size < 10:
                return "5-10"
            elif size < 40:
                return "10-40"
            elif size < 80:
                return "40-80"  
            else:
                return ">80"
        
        i = 0
        for name, domain, license, size in zip(model_sheet[name_column], 
                                                    model_sheet[domain_column],
                                                    model_sheet[license_column],
                                                    model_sheet[size_column]):
            
            # If it is a valid model (used in evaluation)
            if name in self.valid_models:
                T_info[f"{i}"] = "\ud83d\udd36"
                model_name_info[f"{i}"] = name
                
                domain_info[f"{i}"] = DOMAIN_MAPPING[domain]

                if license == "PhysioNet Credentialed Health Data License 1.5.0":
                    license_info[f"{i}"] = "PhysioNet 1.5.0"   # Abbreviate license name to fit on leaderboard
                else:
                    license_info[f"{i}"] = license

                accessibility_info[f"{i}"] = LICENSE_MAPPING[license]
                displayed_size_info[f"{i}"] = size
                hidden_size_info[f"{i}"] = map_size(size)

                i += 1

            else:
                print("Invalid model: ", name)

        return model_name_info, domain_info, license_info, accessibility_info, displayed_size_info, hidden_size_info, T_info

    def get_sheet_information(self, sheets_list, task_names_list, task_types_list):
        """Extract task performance information from specified sheets.
        
        Args:
            sheets_list (list): List of sheet names to process.
            task_names_list (list): List of task names corresponding to each sheet.
            task_types_list (list): List of task types ('ext', 'gen', etc.) for each sheet.
            
        Returns:
            dict: Dictionary mapping task names to model performance data.
                Format: {task_name: {model_index: performance_score}}
        """
        task_info = {}

        # Iterate through each row
        for idx, sheet in enumerate(sheets_list):
            # Get the task type (tt)
            tt = task_types_list[idx]

            # Load the sheet
            model_sheet = self.load_sheet(sheet)

            # Name of the task (i.e. 1.1-ADE Identification)
            task_name = task_names_list[idx]

            # Get all columns in the sheet
            for i, t in enumerate(model_sheet['Task Type']):
                if i == 0:
                    continue

                # Break out of loop when it reaches the end of the sheet
                if t == "-":
                    break
                
                row = i
                task_counter = 0

                for model in self.valid_models:
                    column_name = model.strip()

                    if column_name == "gpt-35-turbo-0125":
                        column_name = "gpt-35-turbo"
                    elif column_name == "gpt-4o-0806":
                        column_name = "gpt-4o"
                    elif column_name == "gemini-2.0-flash-001":
                        column_name = "gemini-2.0-flash"
                    elif column_name == "gemini-1.5-pro-002":
                        column_name = "gemini-1.5-pro"

                    if column_name == "gpt-oss-20b":
                        column_name = "gpt-oss-20b-high"
                    elif column_name == "gpt-oss-120b":
                        column_name = "gpt-oss-120b-high"

                    if tt == 'ext':
                        column_name = column_name + '.1'

                    elif tt == 'gen':
                        column_name = column_name + '.1'

                    # Name of the task (i.e 1.1-ADE Identification)
                    task = model_sheet[task_name][row]

                    # Update task name to more simple version
                    task = TASK_MAPPING[task]
                                                                    
                    if task == "Average score":
                        break
                                    
                    # Update the information for each task
                    if task not in task_info:
                        task_info[task] = {}

                    task_info[task][f"{task_counter}"] = round(float(model_sheet[column_name.strip()][row].split(" ")[0]), 2)
                    task_counter += 1

        return task_info
    
    def add_average_performance(self, task_info):
        """Calculate average performance across all tasks for each model.
        
        Args:
            task_info (dict): Dictionary containing task performance data.
                Format: {task_name: {model_index: performance_score}}
                
        Returns:
            dict: Dictionary mapping model indices to average performance scores.
                Format: {model_index: average_score}
        """
        for task in task_info:
            n = len(task_info[task])
            break

        average_performance_info = {}
        for i in range(n):
            perf = 0
            num_tasks = 0
            for task in task_info:
                perf += float(task_info[task][str(i)])
                num_tasks += 1

            average_performance_info[f"{i}"] = str(round(perf / num_tasks, 2))

        return average_performance_info

    def create_leaderboards(
            self, 
            sheet_names_list=None, 
            task_names_list=["Task-Classification", "Task-Extraction", "Task-Generation"], 
            task_types_list=["cls", "ext", "gen"], 
            output_path=None):
        """Create a leaderboard JSON file from Excel data.
        
        Args:
            sheet_names_list (list, optional): List of sheet names to process.
            task_names_list (list, optional): List of task names corresponding to sheets.
            task_types_list (list, optional): List of task types for each sheet.
            leaderboard_name (str, optional): Name of the leaderboard being created.
            output_path (str, optional): Path where the JSON file should be saved.
            
        Note:
            Creates one leaderboard per call (CoT, Direct, or Few-Shot).
            The output JSON contains model information, task performance, and metadata.
        """
        data = {}

        model_info, domain_info, license_info, accessibility_info, displayed_size_info, hidden_size_info, T_info = self.get_model_information()

        task_info = self.get_sheet_information(sheet_names_list, task_names_list, task_types_list)
        average_performance_info = self.add_average_performance(task_info)

        data["T"] = T_info
        data["Model"] = model_info
        data["Model: Domain"] = domain_info
        data["Model: License"] = license_info
        data["Model: Accessibility"] = accessibility_info
        data["Size (B)"] = displayed_size_info
        data["Model: Size Range"] = hidden_size_info
        data["Average Performance"] = average_performance_info

        for task in task_info:
            data[task] = task_info[task]

        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)

    def create_task_information(self, output_path: str):
        """Create a JSON file containing detailed task information.
        
        Args:
            output_path (str): Path where the task information JSON should be saved.
            
        Note:
            Extracts task metadata from the "Task-all" sheet including language,
            task type, clinical context, data access requirements, applications,
            and clinical stage information.
        """
        task_sheet = self.load_sheet("Task-all")

        # Initialize a map to store the json information
        info = {}

        # Iterate through the "Task-Original" column, which contains all of the task names
        for idx, task in enumerate(task_sheet["Task name"]):
            # Add the task to the final json

            if task not in info:
                info[task] = {}

            # Add all of the attributes to the task
            language = task_sheet["Language"][idx]
            task_type = task_sheet["Task Type - fine grained"][idx]
            clinical_context = task_sheet["Clinical context"][idx]
            data_access = task_sheet["Data Access\nOpen Access (OA) / \nRegulated (R) / \nPhysionet (P) / \nn2c2 (N)"][idx]
            application = task_sheet['Clinical Application'][idx]
            clinical_stage = task_sheet['Clinical Stage'][idx]

            info[task]["Language"] = language.strip()
            info[task]["Task Type"] = task_type.strip()
            info[task]["Clinical Context"] = clinical_context.strip()
            info[task]["Data Access"] = DATA_ACCESS_MAP[data_access.strip()]
            info[task]['Applications'] = application.strip()
            info[task]['Clinical Stage'] = clinical_stage.strip()

        with open(output_path, 'w') as file:
            json.dump(info, file, indent=4)