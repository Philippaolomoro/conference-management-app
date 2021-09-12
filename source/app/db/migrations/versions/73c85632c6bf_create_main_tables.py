"""create_main_tables

Revision ID: 73c85632c6bf
Revises:
Create Date: 2021-09-09 13:58:52.203371

"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '73c85632c6bf'
down_revision = None
branch_labels = None
depends_on = None

def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.Updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )

def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )

def create_conference_table() -> None:
    op.create_table(
        "conference",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_conference_modtime
            BEFORE UPDATE
            ON conference
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )

def create_talk_table() -> None:
    op.create_table(
        "talk",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("duration", sa.Integer, nullable=False),
        sa.Column("date_time", sa.DateTime, nullable=False),
        sa.Column("conference_id", sa.Integer, sa.ForeignKey("conference.id", ondelete="CASCADE")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_talk_modtime
            BEFORE UPDATE
            ON talk
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )

def create_speaker_table()-> None:
    op.create_table(
        "speaker",
        sa.Column("id", sa.Integer,primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("email", sa.Text, unique=True, nullable=False),
        sa.Column("talk_id", sa.Integer, sa.ForeignKey("talk.id", ondelete="CASCADE")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_speaker_modtime
            BEFORE UPDATE
            ON speaker
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )

def create_participant_table()-> None:
    op.create_table(
        "participant",
        sa.Column("id", sa.Integer,primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("email", sa.Text, unique=True, nullable=False),
        sa.Column("talk_id", sa.Integer, sa.ForeignKey("talk.id", ondelete="CASCADE")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_participant_modtime
            BEFORE UPDATE
            ON participant
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )

def upgrade() -> None:
    create_updated_at_trigger()
    create_conference_table()
    create_talk_table()
    create_speaker_table()
    create_participant_table()


def downgrade() -> None:
    op.drop_table("conference")
    op.drop_table("talk")
    op.drop_table("speaker")
    op.drop_table("participant")
    op.execute("DROP FUNCTION update_updated_at_column")
