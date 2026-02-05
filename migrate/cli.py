import sys
from migrate.go_migrator import GoMigrationEngine

if len(sys.argv) < 2:
    print("Usage: python -m migrate.cli <python_file>")
    sys.exit(1)

engine = GoMigrationEngine()
go_code, test_code = engine.migrate_full_file(sys.argv[1])

print("=== GENERATED GO CODE ===")
print(go_code)

print("\n=== GENERATED TEST CODE ===")
print(test_code)
