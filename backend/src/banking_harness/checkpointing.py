"""Development and production checkpoint lifecycle."""

from __future__ import annotations

import os
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver


class CheckpointRuntime:
    def __init__(self, database_url: str | None = None) -> None:
        self.database_url = database_url or os.getenv("LANGGRAPH_DATABASE_URL")
        self._connection: Any | None = None
        self._checkpointer: Any | None = None

    def get(self) -> Any:
        if self._checkpointer is not None:
            return self._checkpointer
        if not self.database_url:
            self._checkpointer = InMemorySaver()
            return self._checkpointer

        from langgraph.checkpoint.postgres import PostgresSaver
        from psycopg import Connection
        from psycopg.rows import dict_row

        self._connection = Connection.connect(self.database_url, autocommit=True, prepare_threshold=0, row_factory=dict_row)
        self._checkpointer = PostgresSaver(self._connection)
        return self._checkpointer

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
