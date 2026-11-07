"""Create ai schema tables: index_jobs, decode_jobs.

Revision ID: 0001
Revises:
Create Date: 2026-03-28

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "ai"


def upgrade() -> None:
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")

    op.create_table(
        "index_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("index_run_id", sa.String(length=120), nullable=False),
        sa.Column("client_user_id", sa.String(length=36), nullable=False),
        sa.Column("backend_id", sa.String(length=80), nullable=False),
        sa.Column("repository", sa.Text(), nullable=False),
        sa.Column("branch", sa.String(length=120), server_default="main", nullable=False),
        sa.Column("commit_sha", sa.String(length=64), server_default="", nullable=False),
        sa.Column("status", sa.String(length=20), server_default="pending", nullable=False),
        sa.Column("node_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("edge_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("error_message", sa.Text(), server_default="", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        schema=SCHEMA,
    )
    op.create_index("ix_ai_index_jobs_index_run_id", "index_jobs", ["index_run_id"], schema=SCHEMA)
    op.create_index("ix_ai_index_jobs_client_user_id", "index_jobs", ["client_user_id"], schema=SCHEMA)
    op.create_index("ix_ai_index_jobs_backend_id", "index_jobs", ["backend_id"], schema=SCHEMA)

    op.create_table(
        "decode_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("index_run_id", sa.String(length=120), nullable=False),
        sa.Column("client_user_id", sa.String(length=36), nullable=False),
        sa.Column("backend_id", sa.String(length=80), nullable=False),
        sa.Column("provider", sa.String(length=20), server_default="openai", nullable=False),
        sa.Column("status", sa.String(length=20), server_default="pending", nullable=False),
        sa.Column("prompt_tokens", sa.Integer(), server_default="0", nullable=False),
        sa.Column("completion_tokens", sa.Integer(), server_default="0", nullable=False),
        sa.Column("error_message", sa.Text(), server_default="", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        schema=SCHEMA,
    )
    op.create_index("ix_ai_decode_jobs_index_run_id", "decode_jobs", ["index_run_id"], schema=SCHEMA)
    op.create_index("ix_ai_decode_jobs_client_user_id", "decode_jobs", ["client_user_id"], schema=SCHEMA)
    op.create_index("ix_ai_decode_jobs_backend_id", "decode_jobs", ["backend_id"], schema=SCHEMA)


def downgrade() -> None:
    op.drop_table("decode_jobs", schema=SCHEMA)
    op.drop_table("index_jobs", schema=SCHEMA)
