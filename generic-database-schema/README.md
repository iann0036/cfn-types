# Generic::Database::Schema

See the [docs](docs).

## Example

```
Resources:
    MyDatabaseSchema:
        Type: Generic::Database::Schema
        Properties:
            ClusterArn: arn:aws:rds:us-east-1:123456789012:cluster:mycluster
            SecretArn: arn:aws:secretsmanager:us-east-1:123456789012:secret:myadminsecret-abc123
            Databases:
              - Name: mydb
                Tables:
                  - Name: mytable
                    PrimaryKey:
                        Name: user_id
                        Type: uuid
                        Default: uuid_generate_v4()
                    Columns:
                      - Name: mycolumn
                        Type: TEXT
                        Nullable: true
                        Default: "'mydefaultstringvalue'"
                Extensions:
                  - uuid-ossp
                SQL:
                  - SELECT 1;
            SQL:
              - SELECT 1;
            Users:
              - Name: myuser
                SecretId: arn:aws:secretsmanager:us-east-1:123456789012:secret:myusersecret-abc123
                SuperUser: true
                Grants:
                  - Database: mydb
                    Privileges:
                      - CONNECT
                  - Database: mydb
                    Table: mytable
                    Privileges:
                      - SELECT
            SQLIdempotency: RUN_ONCE
```
