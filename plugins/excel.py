from typing import Any
from typing import Dict

import pandas as pd
from pandas.io.formats import excel

from dbt.adapters.duckdb.plugins.excel import Plugin as ExcelPlugin
from dbt.adapters.duckdb.plugins import pd_utils
from dbt.adapters.duckdb.utils import SourceConfig
from dbt.adapters.duckdb.utils import TargetConfig
from dbt.logger import GLOBAL_LOGGER as logger


class Plugin(ExcelPlugin):
    def initialize(self, plugin_config: Dict[str, Any]):
        super().initialize(plugin_config)

    def load(self, source_config: SourceConfig):
        return super().load(source_config)

    def store(self, target_config: TargetConfig):
        plugin_output_config = {}
        if "output" in self._config:
            plugin_output_config = self._config["output"]
        
        target_output_config = {
            **plugin_output_config,
            **target_config.config.get("overrides", {}),
        }

        # Instead of creating the writer as attribute we keep it as local object.
        excel_writer = pd.ExcelWriter(
            target_output_config["file"],
            mode=target_output_config.get("mode", "w"),
            engine=target_output_config.get("engine", "xlsxwriter"),
            engine_kwargs=target_output_config.get("engine_kwargs", {}),
            date_format=target_output_config.get("date_format"),
            datetime_format=target_output_config.get("datetime_format"),
        )

        if not target_output_config.get("header_styling", True):
            excel.ExcelFormatter.header_style = None

        if "sheet_name" not in target_output_config:
            # Excel sheet name is limited to 31 characters
            sheet_name = (target_config.relation.identifier or "Sheet1")[0:31]
            target_output_config["sheet_name"] = sheet_name

        # could be changed to directly read from duckdb, but this plugin 
        # is always writing to external first, can swap if performance issues arise
        # relation = target_config.relation
        # with duckdb.connect(f"{relation.database}.duckdb") as con:
        #     con.execute(f"SET search_path TO {relation.schema}")
        #     df = con.table(relation.identifier).to_df()

        df = pd_utils.target_to_df(target_config)
        if target_output_config.get("skip_empty_sheet", False) and df.shape[0] == 0:
            return
        try:
            df.to_excel(
                excel_writer,
                sheet_name=target_output_config["sheet_name"],
                na_rep=target_output_config.get("na_rep", ""),
                float_format=target_output_config.get("float_format", None),
                header=target_output_config.get("header", True),
                index=target_output_config.get("index", True),
                merge_cells=target_output_config.get("merge_cells", True),
                inf_rep=target_output_config.get("inf_rep", "inf"),
            )
            excel_writer.close()
        except ValueError as ve:
            # Catches errors resembling the below & logs an appropriate message
            # ValueError('This sheet is too large! Your sheet size is: 1100000, 1 Max sheet size is: 1048576, 16384')
            if (
                str(ve).startswith("This sheet is too large")
                and target_output_config["ignore_sheet_too_large"]
            ):
                pd.DataFrame(
                    [{"Error": target_output_config.get("ignore_sheet_too_large_error", str(ve))}]
                ).to_excel(
                    self._excel_writer, sheet_name=target_output_config["sheet_name"], index=False
                )
            else:
                raise ve
