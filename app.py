import gradio as gr
from gradio_leaderboard import Leaderboard, SearchColumns
import config
from pathlib import Path

# Import our new modular components
from utils import LeaderboardDataLoader, FilterManager, UIComponents, postprocess

def create_leaderboard_tab(leaderboard_type: str, data_loader: LeaderboardDataLoader, 
                          filter_manager: FilterManager) -> None:
    """Create a leaderboard tab with filters"""
    
    # Create the leaderboard component
    leaderboard = Leaderboard(
        value=data_loader.get_dataframe(leaderboard_type),
        select_columns=None,
        search_columns=SearchColumns(
            primary_column="Model", 
            secondary_columns="",
            placeholder="Search by Model Name",
            label="Model Search"
        ),
        hide_columns=["Model: Size Range", "Model: Accessibility"],
        filter_columns=["Model: Domain", "Model: Size Range", "Model: Accessibility"],
        datatype=config.TYPES,
    )
    
    # Create filter components
    filter_components, filter_types = UIComponents.create_filter_components()
    
    # Setup event handlers for filters
    UIComponents.setup_filter_events(
        filter_components, filter_types, leaderboard, filter_manager, leaderboard_type
    )

def main():
    """Main application function"""
    
    # Initialize data loader and filter manager
    data_loader = LeaderboardDataLoader()
    filter_manager = FilterManager(data_loader)
    
    # Apply custom postprocessing to Leaderboard class
    # Models are sorted in order of decreasing average performance (best performance at the top!)
    Leaderboard.postprocess = postprocess
    
    # Create the Gradio app
    with gr.Blocks() as app:
        gr.Markdown("# BRIDGE (Benchmarking Large Language Models for Understanding Real-world Clinical Practice Text)")

        with gr.Tabs():
            with gr.Tab("README"):
                html_content = (Path(__file__).parent / "docs.md").read_text()
                gr.HTML(html_content)

            with gr.Tab("Zero-Shot"):
                create_leaderboard_tab("zero_shot", data_loader, filter_manager)

            with gr.Tab("Few-Shot"):
                create_leaderboard_tab("few_shot", data_loader, filter_manager)

            with gr.Tab("CoT"):
                create_leaderboard_tab("cot", data_loader, filter_manager)
    
    return app

if __name__ == "__main__":
    app = main()
    app.launch()

