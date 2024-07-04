# Demo dbt DuckDB Excel Plugin

This repository demonstrates using the Excel plugin of the `dbt-duckdb` adapter, customized for enhanced file processing capabilities. It shows how dbt combined with DuckDB can serve as a framework for various file processing tasks while adhering to software engineering best practices.

## Key Benefits

1. Adherence to Software Engineering Best Practices: Ensures maintainability and scalability in file processing tasks.
2. Duty Segregation: Allows software engineers to manage plugin functionalities while users focus on processing files.

## Usage Examples

![Screen Recording of a dbt run demonstrating the setup](/media/example.gif)

This demo setup includes various methods to import and export data:

1. Import `raw_customers.xlsx`: Uses the excel plugin. See `models/example/staging/sources.yml` for details.
2. Import `raw_orders.xlsx`: Uses DuckDB's native feature to load data from Excel via the `st_read` function. See `models/example/staging/sources.yml` and `models/example/staging/schema.yml`.
3. Export `customers.csv`: Uses the external materialization, configured in `models/example/customers.sql`.
4. Export `orders.xlsx`: Uses the custom excel plugin defined in `plugins/excel.py`. This plugin addresses the limitation of the default extension by allowing the output file to be set at a module level instead of the target level.

### Examples using the Excel Plugin

profiles.yml

````yaml
default:
  outputs:
    dev:
      type: duckdb
      plugins:
        - module: plugins.excel
          alias: custom_excel
        - module: excel
  target: dev
````

source.yml

````yaml
version: 2

sources:
  - name: excel_source_via_plugin
    meta:
      external_location: "data/source/{name}.xlsx"
      plugin: excel
    tables:
      - name: raw_customers
````

schema.yml

````yaml
  - name: orders
    config:  
      materialized: external
      # location to which the `external` materialization writes and from where the plugin reads
      location: 'data/tmp/orders.parquet'
      plugin: custom_excel
      overrides:
        # the location to which the plugin writes
        file: 'data/destination/orders.xlsx'
````

## Setup

### Virtual Environment

Create a new virtual environment called `venv`:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the required packages:


```bash
pip install -r requirements.txt
```

### Optional: Install Spatial Extension on DuckDB

If needed, you can install the spatial extension:

```python
import duckdb
con = duckdb.connect("prod.duckdb")
con.sql("INSTALL spatial;")
```

### Ensure dbt Recognizes Custom Plugins

Make sure dbt can see the custom plugins:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

Alternatively, edit the `bin/activate` file to include this export command.

### Run 

```bash
dbt run --target dev
```
