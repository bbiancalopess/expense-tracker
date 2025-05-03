#!/usr/bin/env python3
"""
Script to manage the system's migrations
"""

import argparse
from database.migration_manager import MigrationManager


def main():
    parser = argparse.ArgumentParser(description="Migrations Manager")

    # Possible arguments
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--up-all", action="store_true", help="Applies all pending migrations"
    )
    group.add_argument(
        "--up",
        type=str,
        metavar="MIGRATION",
        help="Applies an specific migration (ex.: 0001_initial)",
    )
    group.add_argument(
        "--down", type=str, metavar="MIGRATION", help="Reverts an specific migration"
    )
    group.add_argument("--status", action="store_true", help="Shows migrations status")

    args = parser.parse_args()

    manager = MigrationManager()

    if args.up_all:
        manager.apply_all_pending()
    elif args.up:
        manager.apply_migration(args.up)
    elif args.down:
        manager.rollback_migration(args.down)
    elif args.status:
        print("\n=== Migrations status ===")
        print("Applied migrations:", manager.get_applied_migrations())
        print("Pending migrations:", manager.get_pending_migrations())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
