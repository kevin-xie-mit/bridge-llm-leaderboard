import warnings
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union, Literal
import pandas as pd
from pandas.io.formats.style import Styler
import semantic_version
from gradio.data_classes import GradioModel

class DataframeData(GradioModel):
    headers: List[str]
    data: Union[List[List[Any]], List[Tuple[Any, ...]]]
    metadata: Optional[Dict[str, Optional[List[Any]]]] = None

def postprocess(self, value: pd.DataFrame) -> DataframeData:
    """Custom postprocess function that sorts by Average Performance"""
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