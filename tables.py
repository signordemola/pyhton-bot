import argparse

from database.models import create_tables, drop_tables


def main():
    parser =argparse.ArgumentParser(description="A script to manage database tables")

    parser.add_argument(
        "action",
        choices=["create", "drop"],
        help="The action to perform: create, update, drop tables",
    )

    args = parser.parse_args()

    if args.action == "create":
        print("Creating tables...")
        try:
            create_tables()
            print("Tables created successfully")
        except Exception as e:
            print(f"Failed to create tables: {e}")

    elif args.action == "drop":
        print("Dropping tables...")
        try:
            drop_tables()
            print("Tables dropped successfully")
        except Exception as e:
            print(f"Failed to drop tables: {e}")


if __name__ == "__main__":
    main()