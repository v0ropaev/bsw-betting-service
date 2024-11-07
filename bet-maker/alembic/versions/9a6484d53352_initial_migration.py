from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9a6484d53352'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('events',
    sa.Column('event_id', sa.String(), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=False),
    sa.Column('state', sa.Enum('NEW', 'FINISHED_WIN', 'FINISHED_LOSE', name='eventstate'), nullable=False),
    sa.Column('coefficient', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_index(op.f('ix_events_event_id'), 'events', ['event_id'], unique=False)
    op.create_table('bets',
    sa.Column('bet_id', sa.Uuid(), nullable=False),
    sa.Column('event_id', sa.String(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'WON', 'LOSE', name='betstatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.PrimaryKeyConstraint('bet_id')
    )
    op.create_index(op.f('ix_bets_bet_id'), 'bets', ['bet_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_bets_bet_id'), table_name='bets')
    op.drop_table('bets')
    op.drop_index(op.f('ix_events_event_id'), table_name='events')
    op.drop_table('events')
