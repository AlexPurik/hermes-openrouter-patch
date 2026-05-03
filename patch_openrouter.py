"""This script comments out the OpenRouter attribution headers in the agent code, which may be necessary to avoid issues with OpenRouter's policies.

Can be run from anywhere. It will automatically find the ~/.hermes/hermes-agent/ directory.
"""

from pathlib import Path


def comment_lines(file_path: str | Path, targets: list[str]) -> None:
    path = Path(file_path)
    if not path.exists():
        print(f"  [SKIP] File not found: {path}")
        return

    lines = path.read_text(encoding="utf-8").splitlines()

    targets_set = set(targets)
    result = []
    patched = False

    for line in lines:
        if any(t in line for t in targets_set):
            if not line.lstrip().startswith("#"):
                indent = len(line) - len(line.lstrip())
                result.append(" " * indent + "# " + line.lstrip())
                patched = True
            else:
                result.append(line)
        else:
            result.append(line)

    path.write_text("\n".join(result) + "\n", encoding="utf-8")
    if patched:
        print(f"  [OK] Patched: {path}")
    else:
        print(f"  [SKIP] No matching lines: {path}")


def find_hermes_directory() -> Path | None:
    """Find the .hermes/hermes-agent directory in user's home."""
    home = Path.home()
    hermes_path = home / ".hermes" / "hermes-agent"

    if hermes_path.exists() and hermes_path.is_dir():
        return hermes_path

    return None


def main():
    print("=" * 60)
    print("OpenRouter Attribution Headers Patch")
    print("=" * 60)

    # Find hermes directory
    hermes_dir = find_hermes_directory()

    if hermes_dir is None:
        print("\nCould not find .hermes/hermes-agent directory automatically.")
        example_path = Path.home() / ".hermes" / "hermes-agent"
        print(f"Example path: {example_path}")
        print()
        user_path = input("Please specify the path to hermes-agent directory: ").strip()

        if not user_path:
            print("No path provided. Exiting.")
            return

        hermes_dir = Path(user_path).expanduser()

        if not hermes_dir.exists():
            print(f"Error: Directory not found: {hermes_dir}")
            return
    else:
        print(f"\nFound hermes directory: {hermes_dir}")

    # Ask for confirmation
    print()
    response = input("Do you want to apply the patch? (y/N): ").strip().lower()

    if response != "y":
        print("Patch cancelled.")
        return

    # Apply patch
    print("\nApplying patch...\n")

    files_to_patch = [
        (
            "run_agent.py",
            [
                '"HTTP-Referer": "https://hermes-agent.nousresearch.com"',
                '"X-OpenRouter-Title": "Hermes Agent"',
                '"X-OpenRouter-Categories": "productivity,cli-agent"',
            ],
        ),
        (
            "agent/auxiliary_client.py",
            [
                '"HTTP-Referer": "https://hermes-agent.nousresearch.com"',
                '"X-OpenRouter-Title": "Hermes Agent"',
                '"X-OpenRouter-Categories": "productivity,cli-agent"',
            ],
        ),
        (
            "tests/run_agent/test_provider_attribution_headers.py",
            [
                'assert headers["X-OpenRouter-Title"] == "Hermes Agent"',
                'assert headers["HTTP-Referer"] == "https://hermes-agent.nousresearch.com"',
                'assert headers["X-Title"] == "Hermes Agent"',
                'assert headers["User-Agent"].startswith("HermesAgent/")',
            ],
        ),
    ]

    for file_path, targets in files_to_patch:
        full_path = hermes_dir / file_path
        comment_lines(full_path, targets)

    print("\n" + "=" * 60)
    print("OpenRouter attribution headers have been successfully patched.")
    print("=" * 60)


if __name__ == "__main__":
    main()
