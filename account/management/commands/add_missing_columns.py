from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Adds missing columns to the account_transaction table'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        
        # Check if directories exist, create if they don't
        try:
            # Add transaction_ref column
            self.stdout.write('Adding transaction_ref column...')
            cursor.execute("""
                ALTER TABLE account_transaction 
                ADD COLUMN IF NOT EXISTS transaction_ref UUID DEFAULT gen_random_uuid()
            """)
            
            # Add transaction_status column
            self.stdout.write('Adding transaction_status column...')
            cursor.execute("""
                ALTER TABLE account_transaction 
                ADD COLUMN IF NOT EXISTS transaction_status VARCHAR(300) DEFAULT 'pending'
            """)
            
            # Add transaction_type column
            self.stdout.write('Adding transaction_type column...')
            cursor.execute("""
                ALTER TABLE account_transaction 
                ADD COLUMN IF NOT EXISTS transaction_type VARCHAR(300) NULL
            """)
            
            # Add other missing columns
            self.stdout.write('Adding other missing columns...')
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS disbursement_source VARCHAR(300) NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS beneficiary_account_number VARCHAR(300) NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS beneficiary_bank_code VARCHAR(300) NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS beneficiary_bank_name VARCHAR(300) NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS beneficiary_account_name VARCHAR(300) NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS balance_before FLOAT NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS balance_after FLOAT NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS source_account_name VARCHAR(300) NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS source_account_number VARCHAR(300) NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS source_bank_code VARCHAR(300) NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS narration VARCHAR(500) NULL")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS attempt_payout BOOLEAN DEFAULT FALSE")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS is_disbursed BOOLEAN DEFAULT FALSE")
            cursor.execute("ALTER TABLE account_transaction ADD COLUMN IF NOT EXISTS escrow_id VARCHAR(300) NULL")
            
            self.stdout.write(self.style.SUCCESS('Successfully added all missing columns to account_transaction table'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))