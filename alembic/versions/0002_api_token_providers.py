"""api_token_providers in ai schema.

Revision ID: 0002
Revises: 0001
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "ai"


def upgrade() -> None:
    op.create_table(
        "api_token_providers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="inactive", nullable=False),
        sa.Column("api_key_cipher", sa.Text(), server_default="", nullable=False),
        sa.Column("base_url", sa.String(length=512), server_default="", nullable=False),
        sa.Column("is_default", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        schema=SCHEMA,
    )
    op.create_index("ix_ai_api_token_providers_provider", "api_token_providers", ["provider"], schema=SCHEMA)


def downgrade() -> None:
    op.drop_table("api_token_providers", schema=SCHEMA)