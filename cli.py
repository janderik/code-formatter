#!/usr/bin/env python3
"""Command-line interface for code-formatter."""
import argparse
import sys
from src.formatter.engine import CodeFormatter


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog='fmt',
        description='Multi-language code formatter'
    )

    parser.add_argument(
        'paths',
        nargs='*',
        default=['.'],
        help='Files or directories to format'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check formatting without modifying files'
    )
    parser.add_argument(
        '--config',
        help='Config file path'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List supported languages'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    formatter = CodeFormatter(config_file=args.config)

    if args.list:
        print("Supported languages:")
        for ext in formatter.get_supported_extensions():
            lang = formatter.get_language(f"file{ext}")
            print(f"  {ext} ({lang})")
        return 0

    all_results = []
    for path in args.paths:
        results = formatter.format_path(path, check_only=args.check)
        all_results.extend(results)

    # Print results
    formatted = 0
    errors = 0

    for result in all_results:
        if result.get('success'):
            if result.get('formatted'):
                formatted += 1
                if args.verbose:
                    print(f"Formatted: {result['file']}")
            elif args.check:
                print(f"OK: {result['file']}")
        else:
            errors += 1
            print(f"Error: {result['file']}: {result.get('error', 'Unknown error')}")

    # Summary
    if args.check:
        if errors > 0:
            print(f"\n{errors} file(s) would be formatted")
            return 1
        print(f"\nAll {len(all_results)} file(s) are properly formatted")
        return 0
    else:
        print(f"\nFormatted {formatted} file(s), {errors} error(s)")
        return 0 if errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
