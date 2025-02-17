from db_formation import SmsProcessor


class get_data(SmsProcessor):
    """This class is used to get data from the database and use.
    Use db_formation to get the db connection
    """

    def __init__(self):
        super().__init__()
        self.connect_to_database()  # Add this line to initialize connection

    def all_data(self):
        """This function is used to"""
        self.cursor.execute("""SELECT * FROM sms_data""")
        results = self.cursor.fetchall()  # Add this line to fetch results
        self.conn.commit()
        return results

    def filter_by_mean(self, value):
        """This method is used to filtered data from the database by type or category"""
        # filter by type, category, date
        # filter by mean, sum, min, max
        self.cursor.execute(
            """
    SELECT message_type, AVG(amount)
    FROM sms_data
    WHERE message_type = %s
    GROUP BY message_type
    """,
            (value,),
        )
        results = self.cursor.fetchall()
        self.conn.commit()
        return results


if __name__ == "__main__":
    model = get_data()
    all_data = model.all_data()
    # filtered_data = model.filter_by_mean('Payments to Code Holders')
    # count = 0
    print(type(all_data[0][0]))
