"""fix candidate status enum

Revision ID: 6a7dd1e21d28
Revises: 1810e68748f3
Create Date: 2025-08-01 14:25:40.885864

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6a7dd1e21d28'
down_revision = '1810e68748f3'
branch_labels = None
depends_on = None

def upgrade():
    # 注意：MySQL ENUM 需要用原生SQL
    op.execute(
        """
        ALTER TABLE candidates 
        MODIFY COLUMN status ENUM('待审核','已审核','已拒绝','活跃','非活跃') 
        NOT NULL DEFAULT '待审核'
        """
    )

def downgrade():
    # 回退为varchar(20)，如有需要
    op.execute(
        """
        ALTER TABLE candidates 
        MODIFY COLUMN status VARCHAR(20) NOT NULL DEFAULT '待审核'
        """
    )
