import os
import json
import re
from collections import OrderedDict
from typing import Dict, List, Tuple, Optional

def extract_model_size(model_name: str) -> float:
    """
    Extract the size (in billions of parameters) from a model name.
    Returns a large number for models without explicit size (like DeepSeek-R1).
    """
    # Look for patterns like "1.5B", "7B", "70B", "32B", etc.
    size_match = re.search(r'(\d+(?:\.\d+)?)[Bb]', model_name)
    if size_match:
        return float(size_match.group(1))
    
    # Special handling for models without explicit size
    if 'DeepSeek-R1' in model_name and 'Distill' not in model_name:
        return 999.0  # Treat as very large model
    
    # Default fallback - treat as medium size
    return 50.0

def get_size_based_order(models: Dict[str, str]) -> List[Tuple[str, str, float]]:
    """
    Get models sorted by size with their original indices.
    Returns list of (original_index, model_name, size) tuples sorted by size.
    """
    model_data = []
    for idx, model_name in models.items():
        size = extract_model_size(model_name)
        model_data.append((idx, model_name, size))
    
    # Sort by size (ascending), then by name for ties
    return sorted(model_data, key=lambda x: (x[2], x[1]))

def create_size_based_mapping(leaderboard_json_path: str) -> Dict[str, str]:
    """
    Create a mapping from current indices to size-based indices for a specific leaderboard.
    """
    try:
        with open(leaderboard_json_path, 'r') as f:
            data = json.load(f)
        
        if 'Model' not in data:
            raise ValueError(f"No 'Model' section found in {leaderboard_json_path}")
        
        models = data['Model']
        
        # Get the first 8 models (the main ones we want to reorder)
        first_8_models = {k: v for k, v in list(models.items())[:8]}
        
        # Get size-based ordering
        sorted_models = get_size_based_order(first_8_models)
        
        # Create mapping from old index to new index
        mapping = {}
        for new_idx, (old_idx, model_name, size) in enumerate(sorted_models):
            mapping[old_idx] = str(new_idx)
            print(f"  {model_name} ({size}B): {old_idx} → {new_idx}")
        
        # For indices 8 and beyond, they stay the same
        # Now properly handle all models (up to 99 instead of hard-coded 73)
        max_index = max(int(k) for k in models.keys())
        print(f"  Total models: {len(models)}, max index: {max_index}")
        for i in range(8, max_index + 1):
            mapping[str(i)] = str(i)
        
        return mapping
        
    except Exception as e:
        print(f"Error creating mapping for {leaderboard_json_path}: {e}")
        raise

def reorganize_indices(leaderboard_json_path: str, custom_mapping: Optional[Dict[str, str]] = None):
    """
    Reorganize the indices of a leaderboard JSON file based on model size.
    
    Args:
        leaderboard_json_path: Path to the leaderboard JSON file
        custom_mapping: Optional custom mapping dict. If None, will auto-generate based on model sizes.
    """
    try:
        print(f"\nProcessing {leaderboard_json_path}...")
        
        # Create mapping based on model sizes if not provided
        if custom_mapping is None:
            print("  Creating size-based mapping...")
            mapping = create_size_based_mapping(leaderboard_json_path)
        else:
            mapping = custom_mapping
            print("  Using provided custom mapping...")

        # Load the data
        with open(leaderboard_json_path, 'r') as f:
            data = json.load(f)
        
        # Create new data structure with proper ordering
        new_data = OrderedDict()
        
        # Process each section
        for section_name, section_data in data.items():
            new_section = OrderedDict()
            
            # First, collect all the remapped data with their new indices
            temp_dict = {}
            for old_idx, value in section_data.items():
                new_idx = mapping.get(old_idx, old_idx)
                temp_dict[int(new_idx)] = value
            
            # Sort by new index and add to ordered dict - this ensures physical ordering
            for key in sorted(temp_dict.keys()):
                new_section[str(key)] = temp_dict[key]
            
            new_data[section_name] = new_section
        
        # Write the reorganized data with proper physical ordering
        with open(leaderboard_json_path, 'w') as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)
        
        print(f"  ✅ Successfully reorganized indices and physical ordering in {leaderboard_json_path}")

        # Print the new order for verification
        with open(leaderboard_json_path, 'r') as f:
            example_data = json.load(f)
        
        print(f'\n  New model order (first 8) from {leaderboard_json_path}:')
        model_section = example_data['Model']
        model_keys = list(model_section.keys())[:8]
        for i, key in enumerate(model_keys):
            model_name = model_section[key]
            size = extract_model_size(model_name)
            print(f'    Position {i} (Index {key}): {model_name} ({size}B)')
            
    except Exception as e:
        print(f"  ❌ Error processing {leaderboard_json_path}: {e}")
        raise

def reorganize_all_leaderboards(leaderboard_dir: str = "leaderboards"):
    """
    Reorganize all leaderboard files in the specified directory.
    """
    leaderboard_files = [
        f"{leaderboard_dir}/CoT_leaderboard.json",
        f"{leaderboard_dir}/Zero-Shot_leaderboard.json", 
        f"{leaderboard_dir}/Few-Shot_leaderboard.json"
    ]
    
    print("🔄 Starting reorganization of all leaderboards based on model size...")
    
    for file_path in leaderboard_files:
        if os.path.exists(file_path):
            reorganize_indices(file_path)
        else:
            print(f"  ⚠️  Warning: {file_path} not found, skipping...")
    
    print("\n✅ All leaderboards have been reorganized!")

# Legacy function for backward compatibility (but with dynamic range)
def reorganize_indices_legacy(leaderboard_json_path: str):
    """
    Legacy function that uses the old hard-coded mapping style but with dynamic range.
    This is kept for backward compatibility but now properly handles all 99 models.
    """
    # Create the mapping from old indices to new indices (ordered by model size)
    mapping = {
        '0': '7',   # DeepSeek-R1-Distill-Llama-70B (70B) goes to 7 (end)
        '1': '0',   # DeepSeek-R1-Distill-Qwen-1.5B (1.5B) goes to 0 (start)
        '2': '6',   # DeepSeek-R1 (large model) goes to 6
        '3': '1',   # DeepSeek-R1-Distill-Qwen-7B (7B) goes to 1
        '4': '3',   # DeepSeek-R1-Distill-Qwen-14B (14B) goes to 3
        '5': '2',   # DeepSeek-R1-Distill-Llama-8B (8B) goes to 2
        '6': '5',   # Baichuan-M2-32B (32B) goes to 5
        '7': '4',   # Baichuan-M1-14B-Instruct (14B) goes to 4
    }

    # Dynamically determine the range based on actual data
    with open(leaderboard_json_path, 'r') as f:
        data = json.load(f)
    
    if 'Model' in data:
        max_index = max(int(k) for k in data['Model'].keys())
        print(f"  Found {len(data['Model'])} models (indices 0-{max_index})")
        
        # For indices 8 and beyond, they stay the same
        for i in range(8, max_index + 1):
            mapping[str(i)] = str(i)
    else:
        print("  Warning: No 'Model' section found, using default range")
        # Fallback to 99 models (0-98)
        for i in range(8, 99):
            mapping[str(i)] = str(i)

    # Process each JSON file
    print(f"\nProcessing {leaderboard_json_path}...")

    with open(leaderboard_json_path, 'r') as f:
        data = json.load(f)
        
        # Create new data structure with proper ordering
        new_data = OrderedDict()
        
        # Process each section
        for section_name, section_data in data.items():
            new_section = OrderedDict()
            
            # First, collect all the remapped data with their new indices
            temp_dict = {}
            for old_idx, value in section_data.items():
                new_idx = mapping.get(old_idx, old_idx)
                temp_dict[int(new_idx)] = value
            
            # Sort by new index and add to ordered dict - this ensures physical ordering
            for key in sorted(temp_dict.keys()):
                new_section[str(key)] = temp_dict[key]
            
            new_data[section_name] = new_section
        
        # Write the reorganized data with proper physical ordering
        with open(leaderboard_json_path, 'w') as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)
        
    print(f"  Successfully reorganized indices and physical ordering in {leaderboard_json_path}")

    # Print the new order for verification    
    with open(leaderboard_json_path, 'r') as f:
        example_data = json.load(f)
        
    print(f'\nNew model order (first 8) from {leaderboard_json_path}:')
    model_section = example_data['Model']
    # Since we're using OrderedDict and sorted insertion, the first 8 entries should be indices 0-7
    model_keys = list(model_section.keys())[:8]
    for i, key in enumerate(model_keys):
        print(f'  Position {i} (Index {key}): {model_section[key]}')