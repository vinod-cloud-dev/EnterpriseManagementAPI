
"""add user information to conversations

Revision ID: 2e65bb36c37c
Revises: 04dc6ae3ed00
Create Date: 2026-08-31 18:34:38.114470
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = "2e65bb36c37c"
down_revision: Union[str, Sequence[str], None] = "04dc6ae3ed00"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add user email
    op.add_column(
        "conversations",
        sa.Column(
            "user_email",
            sa.String(length=255),
            nullable=True,
        ),
    )

    # Add last message timestamp
    op.add_column(
        "conversations",
        sa.Column(
            "last_message_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # Add archive flag.
    # Existing rows will automatically get False.
    op.add_column(
        "conversations",
        sa.Column(
            "is_archived",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    # User ID comes from the existing .NET application,
    # where User.Id is an INTEGER.
    op.alter_column(
        "conversations",
        "user_id",
        existing_type=sa.UUID(),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using="NULL::integer",
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Remove archive flag
    op.drop_column(
        "conversations",
        "is_archived",
    )

    # Remove last message timestamp
    op.drop_column(
        "conversations",
        "last_message_at",
    )

    # Remove user email
    op.drop_column(
        "conversations",
        "user_email",
    )

    # Change user_id back to UUID.
    # Existing integer values cannot safely be converted to UUID,
    # so existing values are set to NULL.
    op.alter_column(
        "conversations",
        "user_id",
        existing_type=sa.Integer(),
        type_=sa.UUID(),
        existing_nullable=True,
        postgresql_using="NULL::uuid",
    )
