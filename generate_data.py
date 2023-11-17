from faker import Faker

def generate_sql_inserts(num_rows=10):
    fake = Faker()
    sql_values = []

    for i in range(1, num_rows + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        job = fake.job()
        sql_values.append(f"({i}, '{first_name}', '{last_name}', '{job}')")

    sql_statement = "insert into people values\n" + ",\n".join(sql_values) + ";"
    return sql_statement

if __name__ == "__main__":
  sql_statement = generate_sql_inserts()
  print(sql_statement)
