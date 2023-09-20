# Modern data warehouse modeling and ensuring data quality with dbt and OpenMetadata

This repository serves as a comprehensive guide to effective data modeling and robust data quality ensurance using popular open-source tools such as dbt, Great-Expectation and OpenMetadata. Dive into practical examples and best practices to elevate your data analytics projects.

![architecture.png](images%2Farchitecture.png)

# The contents
- [Understanding the Tools](#understanding-the-tools)
- [Understanding the Modeling techniques](#understanding-the-modeling-techniques)
- [Hybrid Data Modeling Approach: Dimensional Model + One Big Table](#hybrid-data-modeling-approach-dimensional-model--one-big-table)
- [Setting up DuckDB, dbt, OpenMetadata, and Mate with Docker Compose](#setting-up-duckdb-dbt-openmetadata-and-mate-with-docker-compose)
- [Creating the structure of the dbt project](#creating-the-structure-of-the-dbt-project)
- [Start building models](#start-building-models)
- [Ensuring data quality](#ensuring-data-quality)
- [Making data it accessible, understandable and usable for users](#making-data-it-accessible-understandable-and-usable-for-users)
- [Automate jobs with Apache Airflow](#automate-jobs-with-apache-airflow)
- [Conclusion](#conclusion)

# Understanding the Tools
In this session, we'll familiarize ourselves with the key tools that power our data modeling and data quality journey: dbt and OpenMetadata. 
## dbt
dbt, which stands for Data Build Tool, is a command-line tool that revolutionizes the way data transformations and modeling are done. Here's a deeper dive into dbt's capabilities:
- **Modular Data Transformations**: dbt uses SQL and YAML files to define data transformations and models. This modular approach allows you to break down complex transformations into smaller, more manageable pieces, enhancing mantainability and version control.
- **Data Testing**: dbt facilitates data testing by allowing you to define expectations about your data. It helps ensure data quality by automatically running tests against your transformed data.
- **Version Control**: dbt projects can be version controlled with tools like Git, enabling collaboration among data professionals while keeping a history of changes.
- **Incremental Builds**: dbt supports incremental builds, meaning it only processes data that has changed since the last run. This feature saves time and resources when working with large datasets.
- **Orchestration**: While dbt focuses on data transformations and modeling, it can be integrated with orchestration tools like Apache Airflow or dbt Cloud to create automated data pipelines.

## DuckDB
DuckDB is an in-memory, columnar analytical database that stands out for its speed, efficiency, and compatibility with SQL standard. Here is a more in-deepth look at its features:
- **High-performance Analytics**: DuckDB is optimized for analytical queries, making it an ideal choice for data warehousing and analytics workloads. It's in-memory storage and columnar data layout significantly boost query performance.
- **SQL Compatibility**: DuckDB supports SQL, making it accessible to analysts and data professionals who are ready familiar with SQL syntax. This compatibility allows you to leverage your existing SQL knowledge and tools.
- **Integration with BI Tools**: DuckDB integrates seamlessly with popular business intelligence (BI) tools like Tableau, Power BI, and Looker. This compatibility ensures that you can visualize and report on your data effectively.

## OpenMetadata
OpenMatadata is a powerful open-source metadata management platform designed to streamline metadata management processes and enhance data governance. it offers a range of key features that are essential for maintaining data quality and ensuring effective data management within your analytics projects:
- **Metadata Catalog**: OpenMetadata provides a centralized catalog for storing and managing metadata related to your data assets, including tables, databases, reports, and more. This catalog makes it easy to discover and access critical information about your data.
- **Data Linage**: Understanding data lineage is crucial for tracking the flow of data through your systems. OpenMetadata offers robust data lineage tracking, allowing you to visualize how data moves from source to destination, which is essential for ensuring data quality and accuracy.
- **Data Documentation**: Comprehensive data documentation is essential for effective data governance. OpenMetadata enables you to document your data assets. This collaborative approach enhances communication and knowledge sharing wihthin your organization. 
- **Version Control**: Version control is critical for tracking changes to metadata over time. OpenMetadata offers versioning capabilities, ensuring that you can viuew and revert to previous version of metadata when you needed.
- **API Integration**: OpenMetadata can be integrated with other tools and platforms in your data stack, enabling seamless data governance and metadata management across your entire data ecosystem.
- **Custom Metadata Types**: OpenMetadata allows you to define custom metadata types tailored to your organization's specific needs. This flexibility ensures that you can capture and manage metadata that is relevant to your unique data assets.
- **Search and Discovery**: OpenMetadata offers advanced search and discovery capabilities, making it easy to find the data assets you need quickly. Users can search based on metadata attributes, tags, and other criteria.
- **Data Quality Monitoring**: OpenMetadata can be used to track and monitor data quality by associating quality metrics and checks with data assets. This feature is vital for ensuring data accuracy and reliability.
- **Data Governance**: OpenMetadata supports data governance practices by providing access controls, audit trails, and compliance features. It helps organizations adhere to data governance policies and regulations.

These key features of OpenMetadata make it a valuable addition to your data management toolkit, particularly when combined with dbt for data modeling and transformation. Together, these tools empower data professionals to build well-structured, high-quality analytics projects while maintaining control and visibility over their data assets.

# Understanding the Modeling techniques
Data modeling is a fundamental step in the process of designing and organizing data structures to meet specific business requirements. These modeling techniques serve as blueprints for how data will be stored, organized, and accessed within a database or data warehouse. Different modeling techniques are used based on the nature of the data and the specific needs of an organization. Your downstream use cases, data warehouse, raw source data, and the skills of your data team will all help determine which data modeling approach is most appropriate for your business. Here, we explore four widely used data modeling techniques:
## Relational Model 
- The Relational Model is one of the most established and widely used data modeling techniques. It is based on the principles of tables (relations) where data is organized into rows and columns. Each table represents an entity, and relationships between entities are established through keys.
- This model is highly structured and enforces data integrity through constraints, making it suitable for transactional systems where data consistency is crucial.
- Relational databases like MySQL, PostgreSQL, and Oracle Database commonly implement this model.
#### Good fit for
- Low volume data and a small number of data sources
- Simple use cases for the data
- Low-medium concern around data warehousing costs (because relational models often need joining to be made meaningful)

## Dimensional Data Model
- The Dimensional Data Model is primarily used for data warehousing and analytics. It focuses on simplifying complex data into a structure that is optimized for querying and reporting.
- In this model, data is organized into two types of tables: dimension tables (containing descriptive attributes) and fact tables (containing numerical performance measures). These tables are connected through keys, enabling efficient multidimensional analysis.
- Dimensional modeling is ideal for business intelligence and data analytics systems and is often associated with tools like Online Analytical Processing (OLAP) cubes.

### Good fir for
- Medium-to-large number of data sources
- Centralized data teams
- End-use case for data is primarily around business intelligence and providing insights
- Teams that want to create an easily navigable and predictable data warehouse design

## Entity-Relationship Data Model (ERD)
- The Entity-Relationship Data Model is a conceptual modeling technique used to represent entities (objects or concepts) and the relationships between them.
- Entities are represented as tables, relationships as lines connecting them, and attributes as columns. It helps visualize the structure of data and how entities interact.
- ERDs are valuable in the early stages of database design for defining data requirements and understanding complex data relationships.
### Good fit for
- Low complexity data that connects neatly together
- Simple, business-focused downstream use cases for the data
- Central data teams that have deep knowledge of the facets of their data

## Data Vault Model
- The Data Vault Model is designed for building scalable and flexible data warehouses that can adapt to changing business requirements.
- It consists of three core components: **hubs** (representing business entities), **links** (representing relationships between entities), and **satellites** (containing descriptive attributes).
- Data Vault is known for its ability to handle incremental data loading and historical data, making it suitable for data integration and data warehouse architectures.
### Good fir for
- Enterprise teams where the ability to audit data is a primary concern
- Teams that need flexibility and who want to make large structural changes to their data without causing delays in reporting
- More technical data teams that can manage and govern the network-like growth of data vault models

## Wide Table or One Big Table (OBT)
OBT stands for one big table. As the name suggests, it refers to using a single table for housing all data in a single large table. This approach ensures the warehouse doesn't have to perform any joins on the fly. Due to its simplicity, OBT is good for small teams and small projects that are focused on tracking a specific item. This item is usually the one that has several attributes associated with it.

There’s no clear “right” or “wrong” data modeling technique for your data and business. However, there are ones that are probably more appropriate and aligned with the skillsets of your team.

# Hybrid Data Modeling Approach: Dimensional Model + One Big Table
In this guide, we introduce a hybrid data modeling approach that combines the strengths of two distinct data modeling techniques: the Dimensional Model and the One Big Table. This approach is designed to create a versatile and efficient data analytics ecosystem that caters to the diverse requirements of your organization's users.
## Dimensional Model for the Base Layer (Data Warehouse)
- **Target Audience**: Power users, data analysts, and data engineers who are proficient in SQL and need to perform complex analytical queries.
- **Key Characteristics**:
  - Data is organized into structured star or snowflake schemas, optimizing query performance for analytical workloads.
  - Normalization reduces data redundancy and enforces data integrity.
  Fact tables contain numerical measures, and dimension tables provide context and attributes.
  - Ideal for complex joins and aggregations required for in-depth analysis.
- **Use Case**: The Dimensional model serves as the foundation of your data warehouse (DWH) for advanced analytics. It's the go-to layer for users who are comfortable writing SQL queries and require granular data for their analyses.

## One Big Table for the Mart Layer (Business Users)
- **Target Audience**: Business users, executives, and non-technical stakeholders who need simplified access to data for reporting and dashboards.
- **Key Characteristics**:
  - Data is denormalized into a single table, simplifying data structures and queries.
  - Provides a flattened view of data, making it easy for business users to access and understand.
  - Facilitates ad-hoc reporting and self-service analytics without the need for complex joins.
  - Suitable for scenarios where query simplicity and speed are priorities.
- **Use Case**: The One Big Table approach is implemented in the Mart layer, which acts as a user-friendly data mart. It allows business users to access data quickly, create reports, and gain insights without the need for extensive SQL knowledge.

# Setting up DuckDB, dbt, OpenMetadata, and Mage with Docker Compose
## Setting up DuckDB
DuckDB will be installed as a library with dbt in the next session.

## Setting up dbt
Firstly, We need to install *dbt-core* and *dbt-duckdb* libraries, then init a dbt project.
```yaml
# create a virtual environment
cd dbt
python -m venv .env
source .env/bin/activate

# install libraries: dbt-core and dbt-duckdb
pip install -r requirements.txt

# check version
dbt --version
```
Then we initialize a dbt project with the name *stackoverflowsurvey* and create a *profiles.yml* with the following content:
```yaml
stackoverflow:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: '/data/duckdb/adventureworks_dwh.duckdb' # path to local DuckDB database file
```
Run the following commands to properly check configuration:
```bash
# install dependencies
dbt deps
# We need to point out the directory of the profiles.yml file, because we are not using the default location.
dbt debug --profiles-dir .
```
## Setting up OpenMetadata
OpenMetadata provides a default admin account to login.
You can access OpenMetadata at *http://localhost:8585*. Use the following credentials to log in to OpenMetadata.
- Username: *admin*
- Password: *admin*

Once you log in, you can goto *Settings -> Users* to add another user and make them admin as well.
![openmetadata_login.png](images%2Fopenmetadata_login.png)

## Setting up Airflow
OpenMetadata ships with an Airflow container to run the ingestion workflows that have been deployed via the UI.

In the Airflow, you will also see some sample DAGs that will ingest sample data and serve as an example.

You can access Airflow at http://localhost:8080. Use the following credentials to log in to Airflow.

- Username: `admin`
- Password: `admin`

![openmetadata_airflow.png](images%2Fopenmetadata_airflow.png)

## Setting up Slack bot and get essential credentials for alerting
You can find detailed guide to set up Slack bot in [this document](https://blog.fal.ai/how-to-dbt-slack-integration/).

# Creating the structure of the dbt project
Starting by creating a well-organized directory structure for your dbt project. The root directory might look something like this:

```bash
adventureworks_dwh/
│   dbt_project.yml
│   README.md
│
├── models/
│   ├── base/
│   ├── dimensions/
│   ├── facts/
│   ├── staging/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── macros/
│
└── analysis/
```
- **models/**: This directory is where you will define your dbt models. Create subdirectories to separate different types of models, including `dimensions/` for dimension tables and `facts/` for fact tables.
- **data/**: This directory can contain raw and processed data. Raw data might be stored in the raw/ directory, while processed data used by dbt can reside in the processed/ directory.
- **macros/**: Store custom macros and SQL functions that you use across your dbt models.
- **analysis/**: This directory can contain SQL scripts for ad-hoc analysis and queries.

# Starting to build dbt models
## Designing the Star schema

![star_schema.png](images%2Fstar_schema.png)

> **NOTE**: There are two main types of Dimensional Models that are often used today:
> **Star Schema** and **Snowflake Schema**

## Creating the dbt models

```bash
# enter dbt project directory
cd dbt/adventureworks_dwh

# load seeds
dbt seed --profiles-dir .
# run all models
dbt run --profiles-dir .
```
Get a better sense of what the records look like by executing select statements using your database's SQL editor.
For example:
```sql
SELECT * FROM marts.obt_sales LIMIT 100
```
![select_obt.png](images%2Fselect_obt.png)

## Showing data linage
```bash
# generate document
dbt docs generate --profiles-dir .
# serve document web app
dbt serve --port 8888
# Serving docs at 8888
# To access from your browser, navigate to: http://localhost:8888
```
Navigating to *http://localhost:8888* to view data lineage

![data_lineage.png](images%2Fdata_lineage.png)

# Ensuring data quality
Tests are assertions you make about your models and other resources in your dbt project (e.g. sources, seeds and snapshots). When you run **dbt test**, dbt will tell you if each test in your project passes or fails.

## Using dbt's default test capabilities
There are two ways of defining tests in dbt:
- A **singular** test is testing in its simplest form: If you can write a SQL query that returns failing rows, you can save that query in a **.sql** file within your **test** directory. It's now a test, and it will be executed by the **dbt test** command.
- A **generic** test is a parameterized query that accepts arguments. The test query is defined in a special test block (like a macro). Once defined, you can reference the generic test by name throughout your .yml files—define it on models, columns, sources, snapshots, and seeds. dbt ships with four generic tests built in.
```yaml
version: 2

models:
  - name: dim_address
    columns:
      - name: address_key
        description: The surrogate key of the addressid
        tests: # declare your generic test cases
          - not_null # the address_key column in the dim_address model should not contain null value
          - unique # the address_key column in the dim_address model should be unique
      
      - name: addressid
        description: The natural key
        tests:
          - not_null
          - unique

      - name: city_name
        description: The city name

      - name: state_name
        description: The state name

      - name: country_name
        description: The country name
```
> NOTE: You can find more information about these tests in [this document](https://docs.getdbt.com/reference/resource-properties/tests)
### Run test cases
Run following commands to trigger to generate and execute test cases
```bash
dbt test --profiles-dir . --models dim_address
```
You can find generated sql for each test case in the *target/run/..path-to-model../* directory.
Example:
```sql
select
    count(*) as failures,
    count(*) != 0 as should_warn,
    count(*) != 0 as should_error
from (
    select
    address_key as unique_field,
    count(*) as n_records
    from "adventureworks_dwh"."marts"."dim_address"
    where address_key is not null
    group by address_key
    having count(*) > 1
) dbt_internal_test
```
## Integrating with great-expectations
Integrating Great Expectations with dbt is a powerful way to expand your testing capabilities and enhance data quality assurance within your dbt projects. Great Expectations allows you to define, document, and validate expectations about your data, providing a comprehensive approach to data testing. 
Here's a step-by-step guide to integrating Great Expectations with dbt:
- Include in packages.yml
```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: ["1.0.0"]
  - package: calogica/dbt_expectations
    version: [ ">=0.9.0", "<0.10.0" ]
```
Example, If you expect the specified column to exist, you can add test case with following content:
```yaml
version: 2

models:
  - name: dim_address
    columns:
      - name: addressid
        description: The natural key
        tests:
          - not_null
          - unique
          - dbt_expectations.expect_column_to_exist # this test is powered by great-expectation library
```
> NOTE: You can find more information about these tests in [this repo](https://github.com/calogica/dbt-expectations)

## Alerting with Slack
In this guide, we will walk through a process of building a simple Slack bot that sends messages about dbt models. The bot will be written in Python and we will use fal to run the bot script inside a dbt project.

### Slack bot
The first step, we need to install *fal* library to be able to use python script in dbt models.
Add *dbt-fal==1.5.9* into the *requirements.txt* file, and run following command: 
```bash
pip install -r requiremnets.txt
```

You can find the *scripts/fal/slack_bot.py* file that will be executed via **dbt-fal run** command. 
```python
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

CHANNEL_ID = os.getenv("SLACK_BOT_CHANNEL")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")

client = WebClient(token=SLACK_TOKEN)
message_text = f"Model: {context.current_model.name}. Status: {context.current_model.status}."

try:
    response = client.chat_postMessage(
        channel=CHANNEL_ID,
        text=message_text
    )
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["error"]
```
Declare the fal script in the schema file, example:
```yaml
version: 2

models:
  - name: dim_address
    description: "The address model"
    meta:
      owner: "@Luke"
      fal:
        scripts:
          - scripts/fal/slack_bot.py
```
After running *dbt-fal run --proflile-dir . --models dim_address*, you should be received the alert message on the Slack channel, example:
![slack_alerts.png](images%2Fslack_alerts.png)

# Making data it accessible, understandable and usable for users
Next step, we'll integrate the dbt with the OpenMetadata. 
## Building a Custom DuckDB Connector for OpenMetadata
You can find more information in [this repository](https://github.com/luatnc87/openmetadata-duckdb-connector).

## Using the DuckDB Connector
### Create a Database service, Database, DatabaseSchema and Table entities 
The first step, we need to install `openmetadata-ingestion` library used to ingest metadata to OpenMeatadata server. You can run following command or use `requirments.txt` to install the library.
```bash
pip install openmetadata-ingestion==1.1.2
```
Next step, we'll install the DuckDB Connector:
```bash
# Install the duckdb library
pip install duckdb==0.8.1

# Install the DuckDB connector
cd openmetadata/duckdb-connector
pip install --no-deps .
```
Then we can run following command to ingest metadata from local DuckDB database into the OpenMetadata server.
```bash
cd openmetadata
metadata ingest -c duckdb_ingetion.yml
```
The content of the `duckdb_ingestion.yml` ingestion configuration file:
```yaml
source:
  type: customDatabase
  serviceName: duckdb_local
  serviceConnection:
    config:
      type: CustomDatabase
      sourcePythonClass: connector.duckdb_connector.DuckDBConnector
      connectionOptions:
        database_name: adventureworks_dwh
        database_schema_list: date,person,production,sales,dimensions,facts,marts
        database_file_path: /data/duckdb/adventureworks_dwh.duckdb
  sourceConfig:
    config:
      type: DatabaseMetadata
sink:
  type: metadata-rest
  config: {}
workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: openmetadata
    securityConfig:
      jwtToken: 'eyJ...fg6Q'
      # You can get this token via OpenMetadata UI, go to Settings -> Integrations -> Bots -> ingestion-bot -> OpenMetadata JWT Token
```

### Ingest dbt metadata into the OpenMetadata server from dbt assets
Next step, we'll ingest dbt metadata from local. We need to run following commands to create input files.
```bash
cd dbt/adventureworks_dwh

# generate manifest.json and run_results.json files in the `target` directory
dbt run --profiles-dir .
dbt test --profiles-dir .
# generate catalog.json
dbt docs genrate --profiles-dir .

# ingest the metadata in the `target` directory
metadata ingest -c dbt_ingestion.yml
```
The content of the `dbtb_ingestion.yml` ingestion configuration file:
```yaml
source:
  type: dbt
  serviceName: duckdb_local
  sourceConfig:
    config:
      type: DBT
      dbtConfigSource:
        dbtCatalogFilePath: /path/to/catalog.json
        dbtManifestFilePath: /path/to/manifest.json
        dbtRunResultsFilePath: /path/to/run_results.json
      databaseFilterPattern:
        includes:
          - .*adventureworks_dwh.*
      schemaFilterPattern:
        includes:
          - .*marts.*
      tableFilterPattern:
        includes:
          - .*obt_sales.*
sink:
  type: metadata-rest
  config: {}
workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: openmetadata
    securityConfig:
      jwtToken: 'eyJ...fg6Q'
```
You can check the results on OpenMetadata UI.

| ![openmetadata_duckdb_service.png](images%2Fopenmetadata_duckdb_service.png) |
|:----------------------------------------------------------------------------:|
|                             *Database metadata*                              |


| ![openmetadata_duckdb_marts_obt_sales.png](images%2Fopenmetadata_duckdb_marts_obt_sales.png) |
|:--------------------------------------------------------------------------------------------:|
|                                      *Models metadata*                                       |

| ![openmetadata_duckdb_marts_obt_sales_dbt_tab.png](images%2Fopenmetadata_duckdb_marts_obt_sales_dbt_tab.png) |
|:------------------------------------------------------------------------------------------------------------:|
|                                                *dbt SQL code*                                                |

# Automating dbt tasks with Apache Airflow
## Building the dbt DAG
When you ran dbt docs generate, dbt created manifest.json, among other things. This file is very useful, as it has the name of every model, every test, and the dependency relationships between them! Let’s build a DAG that leverages this file to automate generating all the tasks.
```python
import os
import json
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

dbt_path = os.path.join("/opt/airflow/dags", "adventureworks_dwh") # path to your dbt project
manifest_path = os.path.join(dbt_path, "target/manifest.json") # path to manifest.json

with open(manifest_path) as f: # Open manifest.json
    manifest = json.load(f) # Load its contents into a Python Dictionary
    nodes = manifest["nodes"] # Extract just the nodes

# Build an Airflow DAG
with DAG(
        dag_id="dbt_adventureworks_dwh-v1", # The name that shows up in the UI
        start_date=pendulum.today(), # Start date of the DAG
        catchup=False,
        max_active_runs=1,
) as dag:

    # Create a dict of Operators
    dbt_tasks = dict()
    for node_id, node_info in nodes.items():
      dbt_cmd = "run" if node_info["resource_type"] == "model" else node_info["resource_type"]
        dbt_tasks[node_id] = BashOperator(
            task_id=".".join(
                [
                    node_info["resource_type"],
                    node_info["package_name"],
                    node_info["name"],
                ]
            ),
            bash_command=f"cd {dbt_path}" # Go to the path containing your dbt project
                         + f" && dbt {dbt_cmd} --profiles-dir . --models {node_info['name']}", # run the model!
        )

    # Define relationships between Operators
    for node_id, node_info in nodes.items():
        upstream_nodes = node_info["depends_on"].get("nodes")
        if upstream_nodes:
            for upstream_node in upstream_nodes:
                dbt_tasks[upstream_node] >> dbt_tasks[node_id]

if __name__ == "__main__":
    dag.cli()
```
This program:
- Loads the `manifest.json` file from dbt into a Python Dictionary.
- Creates an Airflow DAG named `dbt_adventureworks_dwh-v1`.
- Creates a task for each `node` (where node is either a model/test or a seed).
- Defines the dependency relationship between nodes.

Save the file and wait about 30 seconds. Airflow will find the DAG and load it. When it’s ready, you should see it at the top of your DAG list.
> NOTE: Airflow will find and load the DAG located in this `../airflow/dags:/opt/airflow/dags` volume

Go to Airflow UI, then click on your DAG and select the graph view. Your DAG should look like this!

![airflow_dag.png](images%2Fairflow_dag.png)

Now, turn on your DAG, enable Auto-refresh, and trigger a run. All your tasks should complete successfully and turn green!

![run_dbt_airflow.png](images%2Frun_dbt_airflow.png)

# Conclusion
In this guide, we embarked on a journey to build a robust and efficient data analytics platform powered by DuckDB, dbt, OpenMetadata and Apache Airflow. Throughout this exploration, we have uncovered several essential insights and best practices that can help organizations streamline their data management and analytics workflows. Let's recap some of the key takeaways:
- **Choice of Tools**: We began by carefully selecting our tools. DuckDB served as the high-performance analytical database, dbt empowered us with data transformation capabilities and testing, and Apache Airflow facilitated job scheduling and automation.
- **Dimensional Modeling**: We discussed the importance of adopting dimensional modeling techniques, such as the Star Schema, to structure data for efficient analytics. This approach allows for optimized querying and reporting, catering to both power users and business stakeholders.
- **Data Testing**: We introduced data testing through dbt, explaining how to declare test cases to validate data quality and compliance with expectations. Integration with Great Expectations further enhances data testing capabilities.
- **Documentation and Collaboration**: We highlighted the importance of documentation at every stage of the data analytics pipeline. Documenting models, expectations, and data transformation processes fosters collaboration among data professionals and ensures transparency in data processes.
- **Data Governance**: We touched upon the concept of data governance and how it is essential for maintaining data quality, security, and compliance. Tools like dbt, OpenMetadata support data governance efforts.
- **Integration and Automation**: We integrated Apache Airflow into our data analytics platform to enable job scheduling and orchestration. Airflow allows for the automation of data workflows, ensuring data is processed and delivered at the right time.
- **Continuous Improvement**: We encouraged a culture of continuous improvement in data analytics projects. Regularly reviewing and iterating on models, tests, and workflows helps keep data assets up-to-date and aligned with business needs.

As you embark on your data analytics journey, remember that these tools and techniques are not static. The data landscape evolves, and your organization's requirements will change over time. Therefore, adaptability and a commitment to staying current with best practices are essential.

By building a data analytics platform that combines the strengths of DuckDB, dbt, and Apache Airflow and following the principles and strategies outlined in this blog post, you are well-equipped to harness the power of data for informed decision-making, drive innovation, and gain a competitive edge in your industry.

In closing, the fusion of these technologies empowers data teams to transform raw data into actionable insights, providing a solid foundation for data-driven success. We hope this blog has been a valuable resource on your data analytics journey, and we encourage you to explore, experiment, and continue building upon these foundations to unlock the full potential of your data.

Thank you for joining us on this data-driven adventure. If you have any questions or would like to explore these topics further, please feel free to reach out. Here's to a future filled with data-driven possibilities!

## Supporting Links
* <a href="https://www.getdbt.com/blog/data-modeling-techniques" target="_blank">4 data modeling techniques for modern data warehouses</a>
* <a href="https://docs.getdbt.com/blog/kimball-dimensional-model" target="_blank">Building a Kimball dimensional model with dbt</a>
* <a href="https://www.fivetran.com/blog/star-schema-vs-obt" target="_blank">Data warehouse modeling: Star schema vs OBT</a>
* <a href="https://www.getdbt.com/analytics-engineering/modular-data-modeling-technique" target="_blank">Data modeling techniques for more modularity</a>
* <a href="https://docs.getdbt.com/terms/dimensional-modeling" target="_blank">Dimensional modeling</a>
* <a href="https://docs.getdbt.com/blog/kimball-dimensional-model" target="_blank">Building a Kimball dimensional model with dbt</a>
* <a href="https://data-sleek.com/blog/modern-data-warehouse-modeling-with-dbt/" target="_blank">How To Use DBT To Bring Dimensions To Your Data</a>
* <a href="https://robinphetsavongdata.wordpress.com/2019/06/18/part-1-designing-and-building-the-data-warehous/" target="_blank">Designing and Building the Data Warehouse</a>
* <a href="https://github.com/calogica/dbt-expectations" target="_blank">Port(ish) of Great Expectations to dbt test macros</a>
* <a href="https://blog.fal.ai/how-to-dbt-slack-integration/" target="_blank">How to integrate dbt with Slack</a>
* <a href="https://docs.open-metadata.org/v1.1.0/connectors/ingestion/workflows/dbt/ingest-dbt-cli" target="_blank">OpenMetadata - Ingest dbt cli</a>
* <a href="https://github.com/open-metadata/openmetadata-demo/blob/main/custom-connector/README.md" target="_blank">Creating a Custom Connector</a>
* <a href="https://docs.open-metadata.org/v1.1.x/sdk/python/build-connector/source" target="_blank">Build OpenMetadata Source</a>
* <a href="https://atlan.com/openmetadata-dbt/?ref=/openmetadata-ingestion/" target="_blank">OpenMetadata and dbt: For an Integrated View of Data Assets</a>
* <a href="https://www.astronomer.io/blog/airflow-and-dbt/#airflow-and-dbt-core" target="_blank">Airflow and dbt, Hand in Hand</a>
* <a href="https://www.datafold.com/blog/running-dbt-with-airflow" target="_blank">Running dbt with Airflow</a>
* <a href="https://www.astronomer.io/blog/airflow-dbt-1/" target="_blank">Building a Scalable Analytics Architecture With Airflow and dbt</a>





