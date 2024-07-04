# Demo dbt DuckDB Excel Plugin

This repo is a small experiment to for data ingestion and transformation via DuckDB and dbt with arbitrary destinations using the Plugin System.

The really neat thing about this setup is that, it offers a segregation of concerns especially when using the plugin.
It is easy to overwrite the plugin with a custom plugin that can execute all kinds of custom hooks, before data is loaded.

## Development Setup

Create a new virtual environment named 'venv' in your project directory

```bash
python3 -m venv venv
```

Activate the virtual environment

```bash
source venv/bin/activate
```

Install requirements


```bash
pip install -r requirements.txt
```

You might need to install spatial on DuckDB, but for me this was not needed.

```python
import duckdb
con = duckdb.connect("prod.duckdb")
con.sql("INSTALL spatial;")
```
