from helpers.excel_processor import ExcelProcessor
from helpers.reorganize_indices import reorganize_indices
import json

def update_ranks():
    final_leaderboard_paths = [
        "/Users/kevinxie/Desktop/projects/BRIDGE-Medical-Leaderboard/leaderboards/CoT_leaderboard.json",
        "/Users/kevinxie/Desktop/projects/BRIDGE-Medical-Leaderboard/leaderboards/Few-Shot_leaderboard.json",
        "/Users/kevinxie/Desktop/projects/BRIDGE-Medical-Leaderboard/leaderboards/Zero-Shot_leaderboard.json"
    ]

    for leaderboard_path in final_leaderboard_paths:
        with open(leaderboard_path, 'r') as f:
            data = json.load(f)
        
        avg_performance_dict = data['Average Performance']

        # Tuples of the original index (key) and the performance score
        tps = []
        for idx, value in avg_performance_dict.items():
            tps.append((idx, value))
        
        # Sort the tuples by the performance score in descending order
        tps.sort(key=lambda x: float(x[1]), reverse=True)

        for rank, tp in enumerate(tps):
            original_idx = tp[0]

            data['T'][original_idx] = rank + 1  # Rank starts from 1

        with open(leaderboard_path, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        

def create_leaderboards(
        excel_path: str, 
        output_path: str, 
        sheet_names_list: list, 
        invalid_models=None
        ):
    
    """
    Function that updates a singular leaderboard (JSON).
    
    Args:
        excel_path: Path to the excel file
        output_path: Path to the output file
        sheet_names_list: List of sheet names to create leaderboards from
        invalid_models: List of models to exclude from the leaderboards
    """
    excel_processor = ExcelProcessor(excel_path, invalid_models)

    # Create leaderboards (JSON)
    excel_processor.create_leaderboards(sheet_names_list=sheet_names_list, output_path=output_path)

    # Reorganize the leaderboard inices
    reorganize_indices(output_path)

    # Create task information JSON
    excel_processor.create_task_information('task_information.json')


def create_all_leaderboards(
        excel_path: str, 
        leaderboard_configs: list, 
        invalid_models=None
        ):
    
    """
    Loops through each leaderboard's configs to update all leaderboards 
    (calls the above function multiple times)

    Args:
        excel_path: Path to the excel file
        leaderboard_configs: List of leaderboard configs
        invalid_models: List of models to exclude from the leaderboards
    """

    for config in leaderboard_configs:
        print(f"Creating {config['name']} leaderboard...")
        create_leaderboards(
            excel_path, 
            config['output_path'],
            config['sheet_names'], 
            invalid_models=invalid_models
            )

        print(f"{config['name']} leaderboard created successfully!")


if __name__ == "__main__":
    print("***" * 50)
    print("Starting script...")

    # # ######################################################### #
    # # ######################################################### #

    #  HOW TO UPDATE LEADERBOARDS
    # 1. Download the new excel sheet and/or update the path to the excel sheet
    # 2. Specify which models to exclude from the leaderboard in "invalid_models" list
    # 3. Run scripts/main.py
    # 4. Done! All leaderboards and task information have been updated.
    # 5. Push to GitHub and deploy to Hugging Face Spaces.

    # # ######################################################### #
    # # ######################################################### #

    # excel_path --> path to the Google Sheet version you want to use (Clinical Benchmark and LLM)
    excel_path = "/Users/kevinxie/Desktop/projects/BRIDGE-Leaderboard-INTERNAL/Clinical Benchmark and LLM.xlsx"
    
    # Configuration for all leaderboards
    leaderboard_configs = [
        {
            'name': 'Zero-Shot',
            'output_path': 'leaderboards/Zero-Shot_leaderboard.json',
            'sheet_names': ["B-CLF", "B-EXT", "B-GEN"]
        },
        {
            'name': 'Few-Shot',
            'output_path': 'leaderboards/Few-Shot_leaderboard.json',
            'sheet_names': ["B-CLF-5shot", "B-EXT-5shot", "B-GEN-5shot"]
        },
        {
            'name': 'CoT',
            'output_path': 'leaderboards/CoT_leaderboard.json',
            'sheet_names': ["B-CLF-CoT", "B-EXT-CoT", "B-GEN-CoT"]
        }
    ]

    invalid_models = [
            "gemma-3-27b-pt",
            "gemma-3-12b-pt",
            "gemma-3-12b-pt-ylab-4-1-1",
            "gemma-3-12b-pt-ylab-8-1-1",
            "gemma-3-12b-pt-ylab-16-1-1"  
        ]
    
    # Create all leaderboards with a single function call
    create_all_leaderboards(excel_path, leaderboard_configs, invalid_models)

    print("***" * 50)
    print("Leaderboards created successfully!")

    # Update the ranks of the leaderboards (leftmost column)
    update_ranks()

    print("***" * 50)
    print("Ranks updated successfully!")
    print("***" * 50)
    print("Complete!")

