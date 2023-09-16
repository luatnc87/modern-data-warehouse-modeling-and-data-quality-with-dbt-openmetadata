#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
Custom Database Service Extracting metadata from a DuckDB database
"""
import duckdb
from pydantic import BaseModel, ValidationError, validator
from pathlib import Path
from typing import Iterable, Optional, List, Dict, Any

from metadata.ingestion.api.common import Entity
from metadata.ingestion.api.source import Source, SourceStatus, InvalidSourceException
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.entity.services.connections.database.customDatabaseConnection import (
    CustomDatabaseConnection,
)
from metadata.generated.schema.entity.data.database import Database
from metadata.generated.schema.entity.data.databaseSchema import DatabaseSchema
from metadata.generated.schema.api.data.createDatabaseSchema import (
    CreateDatabaseSchemaRequest,
)
from metadata.generated.schema.api.data.createDatabase import CreateDatabaseRequest
from metadata.generated.schema.entity.services.databaseService import (
    DatabaseService,
)
from metadata.generated.schema.entity.data.table import (
    Column,
)
from metadata.generated.schema.metadataIngestion.workflow import (
    Source as WorkflowSource,
)
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.generated.schema.api.data.createTable import CreateTableRequest
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.utils.logger import ingestion_logger

logger = ingestion_logger()


class InvalidDuckDBConnectorException(Exception):
    """
    Sample data is not valid to be ingested
    """


class DuckDBModel(BaseModel):
    database_name: Optional[str]
    database_schema_name: Optional[str]
    table_name: Optional[str]
    column_names: Optional[List[str]]
    column_types: Optional[List[str]]


class DuckDBConnector(Source):
    """
    Custom connector to ingest Database metadata.

    We'll suppose that we can read metadata from a DuckDB database
    with a custom database name from a business_unit connection option.
    """

    def __init__(self, config: WorkflowSource, metadata_config: OpenMetadataConnection):
        self.config = config
        self.service_connection = config.serviceConnection.__root__.config
        self.metadata_config = metadata_config

        self.metadata = OpenMetadata(self.metadata_config)
        self.status = SourceStatus()

        # Connection params
        self.database_name: str = (
            self.service_connection.connectionOptions.__root__.get("database_name")
        )
        if not self.database_name:
            raise InvalidDuckDBConnectorException(
                "Missing database_name connection option"
            )

        self.database_schema_list: [str] = (
            self.service_connection.connectionOptions.__root__.get("database_schema_list")
            .replace(" ", "").split(",")
        )
        if not self.database_schema_list:
            raise InvalidDuckDBConnectorException(
                "Missing database_schema_list connection option"
            )

        self.database_file_path: str = (
            self.service_connection.connectionOptions.__root__.get("database_file_path")
        )
        if not self.database_file_path:
            raise InvalidDuckDBConnectorException(
                "Missing database_file_path connection option"
            )

        self.data: Optional[List[{str, List[DuckDBModel]}]] = []

    @classmethod
    def create(
            cls, config_dict: dict, metadata_config: OpenMetadataConnection
    ) -> "DuckDBConnector":
        config: WorkflowSource = WorkflowSource.parse_obj(config_dict)
        connection: CustomDatabaseConnection = config.serviceConnection.__root__.config
        if not isinstance(connection, CustomDatabaseConnection):
            raise InvalidSourceException(
                f"Expected CustomDatabaseConnection, but got {connection}"
            )
        return cls(config, metadata_config)

    def prepare(self):
        # Validate that the db file exists
        source_database_file_path = Path(self.database_file_path)
        if not source_database_file_path.exists():
            raise InvalidDuckDBConnectorException("Source Database file path does not exist")

        # to use a database file (shared between processes)
        conn = duckdb.connect(database=self.database_file_path, read_only=True)
        try:
            #sql_get_schemas = f"SELECT DISTINCT schema_name FROM duckdb_schemas() WHERE schema_name like '{self.database_schema_name}'"
            #schema_list = conn.sql(sql_get_schemas).fetchall()
            for schema in self.database_schema_list:
                self.crawl_schema_table_metadata(conn= conn, database_name=self.database_name, database_schema_name=schema)

            conn.close()
        except Exception as exc:
            logger.error("Unknown error reading the source file")
            conn.close()
            raise exc

    def crawl_schema_table_metadata(self, conn, database_name, database_schema_name):
        logger.debug(f"Start crawling the schemas: {database_name}.{database_schema_name}")
        sql_get_tables = f"SELECT DISTINCT table_name FROM duckdb_tables() WHERE database_name = '{database_name}' and schema_name like '{database_schema_name}'"
        table_list = conn.sql(sql_get_tables).fetchall()

        table_models = []
        for table in table_list:
            sql_get_columns = f"SELECT DISTINCT column_name, data_type FROM duckdb_columns() WHERE schema_name = '{database_schema_name}' and table_name = '{table[0]}'"
            column_list = conn.sql(sql_get_columns).fetchall()

            table_model = DuckDBModel(database_name=database_name
                                        , database_schema_name=database_schema_name
                                        , table_name=table[0]
                                        , column_names=[column[0] for column in column_list]
                                        , column_types=[self.convert_data_type(column[1]) for column in column_list]
                                      )
            table_models.append(table_model)
        self.data.append({"database_schema_name": database_schema_name, "tables": table_models})

    def convert_data_type(self, input_data_type):
        output_data_type = input_data_type

        if input_data_type == "INTEGER":
            output_data_type = "INT"
        elif input_data_type.startswith("DECIMAL"):
            output_data_type = "DECIMAL"
        elif input_data_type.startswith("TIMESTAMP"):
            output_data_type = "TIMESTAMP"

        return output_data_type

    def yield_create_request_database_service(self):
        yield self.metadata.get_create_service_from_source(
            entity=DatabaseService, config=self.config
        )

    def yield_create_request_database(self):
        # Pick up the service we just created (if not UI)
        service_entity: DatabaseService = self.metadata.get_by_name(
            entity=DatabaseService, fqn=self.config.serviceName
        )

        yield CreateDatabaseRequest(
            name=self.database_name,
            service=service_entity.fullyQualifiedName,
        )

    def yield_create_request_schema(self):
        # Pick up the service we just created (if not UI)
        database_entity: Database = self.metadata.get_by_name(
            entity=Database, fqn=f"{self.config.serviceName}.{self.database_name}"
        )

        for schema_name in self.database_schema_list:
            yield CreateDatabaseSchemaRequest(
                name=schema_name,
                database=database_entity.fullyQualifiedName,
            )

    def yield_data(self):
        """
        Iterate over the data list to create tables
        """
        for row in self.data:
            database_schema: DatabaseSchema = self.metadata.get_by_name(
                entity=DatabaseSchema,
                fqn=f"{self.config.serviceName}.{self.database_name}.{row['database_schema_name']}",
            )

            for table_row in row["tables"]:
                yield CreateTableRequest(
                    name=table_row.table_name,
                    databaseSchema=database_schema.fullyQualifiedName,
                    columns=[
                        Column(
                            name=model_col[0],
                            dataType=model_col[1],
                            dataLength=-1
                            # character_maximum_length: Always NULL.
                            # DuckDB text types do not enforce a value length restriction based on a length type parameter.
                        )
                        for model_col in zip(table_row.column_names, table_row.column_types)
                    ],
                )

    def next_record(self) -> Iterable[Entity]:
        yield from self.yield_create_request_database_service()
        yield from self.yield_create_request_database()
        yield from self.yield_create_request_schema()
        yield from self.yield_data()

    def get_status(self) -> SourceStatus:
        return self.status

    def test_connection(self) -> None:
        pass

    def close(self):
        pass