# Modern data warehouse modeling and ensuring data quality with dbt and OpenMetadata

This repository serves as a comprehensive guide to effective data modeling and robust data quality assurance using popular open-source tools such as dbt and OpenMetadata. Dive into practical examples and best practices to elevate your data analytics projects.

![architecture.png](images%2Farchitecture.png)

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

# Setting up DuckDB, dbt, OpenMetadata, and Mate with Docker Compose
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
# We need to point out the directory of the profiles.yml file, because we are not using the default location.
dbt debug --profiles-dir .
```
## Setting up OpenMetadata
OpenMetadata provides a default admin account to login.
You can access OpenMetadata at *http://localhost:8585*. Use the following credentials to log in to OpenMetadata.
- Username: *admin*
- Password: *admin*

Once you log in, you can goto *Settings -> Users* to add another user and make them admin as well.

## Setting up Mage

## Setting up Slack bot for alerts


# How to structure dbt project
Start by creating a well-organized directory structure for your dbt project. The root directory might look something like this:

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
- **models/**: This directory is where you will define your dbt models. Create subdirectories to separate different types of models, including **dimensions/** for dimension tables and **facts/** for fact tables.
- **data/**: This directory can contain raw and processed data. Raw data might be stored in the raw/ directory, while processed data used by dbt can reside in the processed/ directory.
- **macros/**: Store custom macros and SQL functions that you use across your dbt models.
- **analysis/**: This directory can contain SQL scripts for ad-hoc analysis and queries.

# Start building models
## Design Star schema

![star_schema.png](images%2Fstar_schema.png)

> **NOTE**: There are two main types of Dimensional Models that are often used today:
> **Star Schema** and **Snowflake Schema**

## Create models

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

## Show data linage
```bash
# generate document
dbt docs generate --profiles-dir .
# serve document web app
dbt serve --port 8888
# Serving docs at 8888
# To access from your browser, navigate to: http://localhost:8888
```

![data_lineage.png](images%2Fdata_lineage.png)

# Ensuring data quality
## Using dbt's default test capabilities

## Integrating with great-expectation

## Alerting with Slack

# Making data it accessible,understandable and usable for users

# Conclusion

## Supporting Links
* <a href="https://www.getdbt.com/blog/data-modeling-techniques" target="_blank">4 data modeling techniques for modern data warehouses</a>
* <a href="https://docs.getdbt.com/blog/kimball-dimensional-model" target="_blank">Building a Kimball dimensional model with dbt</a>
* <a href="https://www.fivetran.com/blog/star-schema-vs-obt" target="_blank">Data warehouse modeling: Star schema vs OBT</a>
* <a href="https://www.getdbt.com/analytics-engineering/modular-data-modeling-technique" target="_blank">Data modeling techniques for more modularity</a>
* <a href="https://docs.getdbt.com/terms/dimensional-modeling" target="_blank">Dimensional modeling</a>
* <a href="https://docs.getdbt.com/blog/kimball-dimensional-model" target="_blank">Building a Kimball dimensional model with dbt</a>
* <a href="https://data-sleek.com/blog/modern-data-warehouse-modeling-with-dbt/" target="_blank">How To Use DBT To Bring Dimensions To Your Data</a>
* <a href="https://robinphetsavongdata.wordpress.com/2019/06/18/part-1-designing-and-building-the-data-warehous/" target="_blank">Designing and Building the Data Warehouse</a>




