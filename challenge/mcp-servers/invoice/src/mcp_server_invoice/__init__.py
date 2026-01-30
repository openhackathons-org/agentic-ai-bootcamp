from . import server_http
import asyncio
import argparse

def main():
    parser = argparse.ArgumentParser(description='Invoice MCP Server')
    parser.add_argument('--db-path', 
                       default="data/chinook.db",
                       help='Path to SQLite database file')

    args = parser.parse_args()

    # streamable http MCP server
    asyncio.run(server_http.main(args.db_path))

__all__ = ['main','server']