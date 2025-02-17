import mysql.connector
import xml.etree.ElementTree as ET
from datetime import datetime
import re
import logging



class SmsProcessor:
  """This class is for parsing, cleaning and storing
  data in the db, it contains a method for creating a db connection
  """

  DEFAULT_CONFIG = {
    'host': 'localhost',
    'user': 'remote',
    'password': 'RutaGandA95',
    'database': 'momo_sms',
    'auth_plugin': 'mysql_native_password'
  }
  DEFAULT_XML = "modified_sms_v2.xml"

  def __init__(self, xml_file=DEFAULT_XML, db_config=DEFAULT_CONFIG, log_file="unprocessed_sms.log"):
    """
    Initialize the SMSProcessor with an XML file, database configuration, and a log file.

    Args:
        xml_file (str): Path to the XML file.
        db_config (dict): Database configuration with keys 'host', 'user', 'password', 'database'.
        log_file (str): Path to the log file for unprocessed SMS messages.
    """

    self.xml_file = xml_file
    self.db_config = db_config
    self.log_file = log_file
    self.conn = None
    self.cursor = None

    # Configure logging
    logging.basicConfig(
      filename=self.log_file,
      level=logging.WARNING,
      format="%(asctime)s - %(levelname)s - %(message)s"
    )

  def connect_to_database(self):
    """Connect to the MySQL database."""
    try:
      self.conn = mysql.connector.connect(
        host = self.db_config['host'],
        user = self.db_config['user'],
        password =self.db_config['password'],
        database = self.db_config['database'],
        auth_plugin = self.db_config['auth_plugin']
      )
      self.cursor = self.conn.cursor()
      print('Database connection established.')
    except mysql.connector.error as e:
      logging.error(f"Database connection failed: {e}")
      raise

  def create_table(self):
    """Create the database table if it doesn't exist."""
    try:
      self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS sms_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        address VARCHAR(200),
        date_sent DATETIME NOT NULL,
        message TEXT,
        service_center VARCHAR(255),
        amount DECIMAL(10, 2),
        message_type VARCHAR(100),
        category VARCHAR(50),
        date DATETIME NOT NULL
      )
      """)
      self.conn.commit()
      print("Table created or already exists.")
    except mysql.connector.Error as e:
      logging.error(f"Failed to create table: {e}")
      raise

  def parse_message(self, message):
    """
    Parse the message to extract amount, message_type, and category.

    Args:
        message (str): The SMS message content.

    Returns:
        tuple: Extracted (amount, message_type, category). Returns (None, None, None) if parsing fails.
    """
    amount = None
    message_type_ = None
    category = None

    try:
      # Extract amount associated with each transaction
      amount_search = re.search(r"(\d+(?:,\d{3})*)\s*RWF", message)

      if amount_search:

        amount = float(amount_search.group(1).replace(',', ''))
      else:
        amount = None

      # Determine type and category based on keywords
      # Incoming Money 
      if "received" in message.lower():
        category = "Coming"
        message_type_ = "Incoming Money"

      # Transfers To Mobile Numbers 
      elif "transferred" in message.lower():
        category = "Going"
        message_type_ = "Transfers To Mobile Numbers"
        
      # Payments to Code Holders
      elif "payment" in message.lower():
        category = "Going"
        message_type_ = "Payments to Code Holders"
        
      # Bank Deposits
      elif "bank deposit" in message.lower():
        category = "Coming"
        message_type_ = "Bank Deposits"
        
      # Airtime Bill Payments
      elif "to Airtime" in message.lower():
        category = "Going"
        message_type_ = "Airtime Bill Payments"
        
      # Cash Power Bill Payments
      elif "Cash Power" in message.lower():
        category = "Going"
        message_type_ = "Cash Power Bill Payments"
        
      # Transactions Initiated by Third Parties
      elif "a transaction of" in message.lower():
        category = "Going"
        message_type_ = "Transactions Initiated by Third Parties"
        
      # Withdrawals from Agents
      elif "agent" in message.lower():
        category = "Going"
        message_type_ = "Withdrawals from Agents"
        
      # Internet and Voice Bundle Purchases
      elif "kugura" in message.lower():
        category = "Going"
        message_type_ = "Internet and Voice Bundle Purchases"
      
      elif "failed" in message.lower():
        category = "No change"
        message_type_ = "Failed Transactions"

      elif "reversed" in message.lower() or "reversal" in message.lower():
        category = "both ways"
        message_type_ = "Reversed Transactions"

      else:
        category = "Unknown"
        message_type_ = "Unknown"
    except Exception as e:
      logging.warning(f"Error parsing message: {message}. Error: {e}")    
    return amount, message_type_, category

  def is_duplicates(self, message, date, date_sent):
    """Check if the SMS already exists in the database to avoid duplicates."""
    query = """
    SELECT COUNT(*) FROM sms_data
    WHERE message = %s AND date = %s AND date_sent = %s
    """
    self.cursor.execute(query, (message, date, date_sent))
    count = self.cursor.fetchone()[0]
    return count > 0
  
  def process_and_store_sms(self):
    """Parse the XML file and store SMS data into the database."""
    try:
      tree = ET.parse(self.xml_file)
      root = tree.getroot()
      for sms in root.findall("sms"):
        try:
          address = sms.attrib.get('address', '')
          message = sms.attrib.get('body', '')
          service_center = sms.attrib.get('service_center', '')
          date = datetime.fromtimestamp(int(sms.attrib['date'])/1000).strftime('%Y-%m-%d %H:%M:%S')
          date_sent = datetime.fromtimestamp(int(sms.attrib['date_sent'])/1000).strftime('%Y-%m-%d %H:%M:%S')
          # Parse message to extract additional fields
          amount, message_type_, category = self.parse_message(message)
          if message_type_ == 'Unknown':
            # Log unprocessed messages
            logging.warning(f"Unprocessed message: {message}")
            with open(self.log_file, 'a') as log:
              log.write(f"{sms.attrib}\n")
            continue

          if self.is_duplicates(message, date, date_sent):
            logging.warning(f"Duplicate SMS detected and skipped: {message}")
            continue
        
          # Insert into the database
          self.cursor.execute("""
          INSERT INTO sms_data (address, date_sent, message, service_center, amount, message_type, category, date)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
          """, (address, date_sent, message, service_center, amount, message_type_, category, date))

        except Exception as e:
          logging.error(f"Failed to process SMS: {sms.attrib}. Error: {e}")

      self.conn.commit()
      print("Data has been processed and stored.")
      
    except Exception as e:
      logging.error(f"Failed to process XML file: {e}")
      raise
  
  def data(self):
    self.cursor.execute("SELECT * FROM sms_data LIMIT 1")
    results = self.cursor.fetchall()  # Add this line to fetch results
    self.conn.commit()
    return results



  def close_connection(self):
    """Close the database connection."""
    if self.cursor:
        self.cursor.close()
    if self.conn:
        self.conn.close()
    print("Database connection closed.")





        
if __name__ == "__main__":
  xml_file = "modified_sms_v2.xml"
  sms_processor = SmsProcessor()
  try:
    sms_processor.connect_to_database()
    sms_processor.create_table()
    sms_processor.process_and_store_sms()
  finally:
    sms_processor.close_connection()
