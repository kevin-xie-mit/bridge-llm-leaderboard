import gradio as gr
from gradio_leaderboard import Leaderboard
from typing import List, Tuple, Callable

class UIComponents:
    """Handles creation of UI components for the leaderboard"""
    
    @staticmethod
    def create_filter_components() -> Tuple[List[gr.CheckboxGroup], List[str]]:
        """Create all filter components and return them with their labels"""
        
        # Language Filter
        all_languages = ['English', 'Spanish', 'Chinese', 'Norwegian', 
                        'Russian', 'Portuguese', 'German', 'Japanese', 'French']
        language_options = gr.CheckboxGroup(all_languages, label="Filter Task: Language")

        # Task Type Filter
        all_task_types = ['Question Answering', 'Text Classification', 'Named Entity Recognition', 
                         'Normalization and Coding', 'Natural Language Inference', 'Summarization', 
                         'Event Extraction', 'Semantic Similarity']
        task_type_options = gr.CheckboxGroup(all_task_types, label="Filter Task: Task Type")
        
        # Clinical Context Filter
        all_clinical_contexts = ['Neurology', 'Oncology', 'Radiology', 'Pulmonology', 
                               'Cardiology', 'Dermatology', 'Critical Care', 'Nephrology', 
                               'General', 'Endocrinology', 'Pediatrics', 'Pharmacology', 
                               'Gastroenterology', 'Psychology']
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

        components = [language_options, task_type_options, cc_options, 
                     application_options, stage_options, da_options]
        
        filter_types = ["Language", "Task Type", "Clinical Context", 
                       "Applications", "Clinical Stage", "Data Access"]
        
        return components, filter_types
    
    @staticmethod
    def setup_filter_events(components: List[gr.CheckboxGroup], 
                          filter_types: List[str], 
                          leaderboard: Leaderboard,
                          filter_manager,
                          leaderboard_type: str):
        """Setup event handlers for filter components"""
        
        def create_filter_function(filter_type: str, lb_type: str):
            """Create a filter function with proper closure"""
            return lambda values: filter_manager.apply_filter(lb_type, filter_type, values)
        
        for component, filter_type in zip(components, filter_types):
            filter_fn = create_filter_function(filter_type, leaderboard_type)
            component.change(
                fn=filter_fn,
                inputs=component,
                outputs=leaderboard
            ) 