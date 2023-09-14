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
    name: str
    column_names: List[str]
    column_types: List[str]

    @validator("column_names", "column_types", pre=True)
    def str_to_list(cls, value):
        """
        Suppose that the internal split is in ;
        """
        return value.split(";")


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
        if not self.database_file_path:
            raise InvalidDuckDBConnectorException(
                "Missing database_name connection option"
            )

        self.database_file_path: str = (
            self.service_connection.connectionOptions.__root__.get("database_file_path")
        )
        if not self.database_file_path:
            raise InvalidDuckDBConnectorException(
                "Missing database_file_path connection option"
            )

        self.business_unit: str = (
            self.service_connection.connectionOptions.__root__.get("business_unit")
        )
        if not self.business_unit:
            raise InvalidDuckDBConnectorException(
                "Missing business_unit connection option"
            )

        self.data: Optional[List[DuckDBModel]] = None

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

    @staticmethod
    def read_row_safe(row: Dict[str, Any]):
        try:
            return DuckDBModel.parse_obj(row)
        except ValidationError:
            logger.warning(f"Error parsing row {row}. Skipping it.")

    def prepare(self):
        # Validate that the db file exists
        source_database_file_path = Path(self.database_file_path)
        if not source_database_file_path.exists():
            raise InvalidDuckDBConnectorException("Source Database file path does not exist")

        try:

            with open(source_data, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.data = [self.read_row_safe(row) for row in reader]
        except Exception as exc:
            logger.error("Unknown error reading the source file")
            raise exc

    def yield_create_request_database_service(self):
        yield self.metadata.get_create_service_from_source(
            entity=DatabaseService, config=self.config
        )

    def yield_business_unit_db(self):
        # Pick up the service we just created (if not UI)
        service_entity: DatabaseService = self.metadata.get_by_name(
            entity=DatabaseService, fqn=self.config.serviceName
        )

        yield CreateDatabaseRequest(
            name=self.business_unit,
            service=service_entity.fullyQualifiedName,
        )

    def yield_default_schema(self):
        # Pick up the service we just created (if not UI)
        database_entity: Database = self.metadata.get_by_name(
            entity=Database, fqn=f"{self.config.serviceName}.{self.business_unit}"
        )

        yield CreateDatabaseSchemaRequest(
            name="default",
            database=database_entity.fullyQualifiedName,
        )

    def yield_data(self):
        """
        Iterate over the data list to create tables
        """
        database_schema: DatabaseSchema = self.metadata.get_by_name(
            entity=DatabaseSchema,
            fqn=f"{self.config.serviceName}.{self.business_unit}.default",
        )

        for row in self.data:
            yield CreateTableRequest(
                name=row.name,
                databaseSchema=database_schema.fullyQualifiedName,
                columns=[
                    Column(
                        name=model_col[0],
                        dataType=model_col[1],
                    )
                    for model_col in zip(row.column_names, row.column_types)
                ],
            )

    def next_record(self) -> Iterable[Entity]:
        yield from self.yield_create_request_database_service()
        yield from self.yield_business_unit_db()
        yield from self.yield_default_schema()
        yield from self.yield_data()

    def get_status(self) -> SourceStatus:
        return self.status

    def test_connection(self) -> None:
        pass

    def close(self):
        pass