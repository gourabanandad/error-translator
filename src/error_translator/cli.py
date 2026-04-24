"""
Command Line Interface (CLI) module for the Error Translator.

This module provides the terminal entry point (`explain-error`). It parses arguments,
handles standard input streams, executes target Python scripts, and uses the Rich library
to format and display the translated error output beautifully.
"""
import json
import sys
import argparse
from .core import translate_error
from importlib.metadata import version, PackageNotFoundError

# Import Rich UI Components for beautiful terminal output
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.table import Table
from rich import box

# Attempt to load the application version for the --version flag
try:
    VERSION = version("error-translator-cli-v2")
except PackageNotFoundError:
    VERSION = "unknown (not installed via pip)"

# Initialize the global rich console for styled terminal output
console = Console()


def _print_title_banner():
    """Prints the stylish title banner for the CLI."""
    banner = Text()
    banner.append("Error Translator CLI\n", style="bold bright_magenta")
    banner.append("Translate Python tracebacks into clear, actionable guidance.", style="cyan")
    console.print(
        Panel(
            banner,
            border_style="magenta",
            padding=(1, 2),
            expand=False,
        )
    )

def print_about():
    """Prints a polished 'about' view using rich components, showcasing features and metadata."""
    _print_title_banner()

    # Project metadata table
    meta = Table.grid(padding=(0, 1))
    meta.add_column(style="bold white", justify="right")
    meta.add_column(style="green")
    meta.add_row("Version", VERSION)
    meta.add_row("Author", "Gourabananda Datta")
    meta.add_row("Repository", "https://github.com/gourabanandad/error-translator-cli-v2")
    console.print(Panel(meta, title="[bold cyan]Project[/]", border_style="cyan", expand=False))

    # Feature highlights
    features = Text()
    features.append("• Offline and fast translation\n", style="white")
    features.append("• Human-readable explanations\n", style="white")
    features.append("• Actionable fix suggestions\n", style="white")
    features.append("• Optional AST-level insight", style="white")
    console.print(Panel(features, title="[bold green]Features[/]", border_style="green", expand=False))

    # Quick start examples
    examples = Text()
    examples.append("explain-error run your_script.py\n", style="bold cyan")
    examples.append("explain-error \"TypeError: ...\"\n", style="bold cyan")
    examples.append("cat error.log | explain-error", style="bold cyan")
    console.print(Panel(examples, title="[bold yellow]Quick Start[/]", border_style="yellow", expand=False))


def print_result(result: dict):
    """
    Print the translated error output in a polished, professional, multi-panel layout.
    
    Args:
        result (dict): The dictionary containing explanation, fix, file, line, code, etc.
    """
    console.print()

    # Handle unexpected errors gracefully
    if result.get("error") and not result.get("matched_error"):
        message = result.get("message", "An unexpected error occurred.")
        console.print(
            Panel(
                f"[bold red]{message}[/]",
                title="[bold red]Error[/]",
                border_style="red",
                box=box.ROUNDED,
                expand=False,
            )
        )
        return

    # Detected error panel
    error_title = result.get("matched_error", "Unknown Error")
    console.print(
        Panel(
            f"[bold white]{error_title}[/]",
            title="[bold red]Detected Error[/]",
            border_style="red",
            box=box.ROUNDED,
            expand=False,
        )
    )

    # Location panel
    file_name = result.get("file")
    line_no = result.get("line", "?")
    if file_name and file_name != "Unknown File":
        console.print(
            Panel(
                f"[yellow]File:[/] {file_name}\n[yellow]Line:[/] {line_no}",
                title="[bold yellow]Location[/]",
                border_style="yellow",
                box=box.ROUNDED,
                expand=False,
            )
        )

    # Code context panel using syntax highlighting
    if result.get("code"):
        try:
            start_line = int(line_no)
        except (TypeError, ValueError):
            start_line = 1

        syntax = Syntax(
            result["code"],
            "python",
            theme="monokai",
            line_numbers=True,
            start_line=start_line,
            word_wrap=True,
        )
        console.print(Panel(syntax, title="[bold blue]Code Context[/]", border_style="blue", box=box.ROUNDED))

    # Explanation panel
    explanation = result.get("explanation", "No explanation available.")
    console.print(
        Panel(
            f"[white]{explanation}[/]",
            title="[bold cyan]Explanation[/]",
            title_align="left",
            border_style="cyan",
            box=box.ROUNDED,
            expand=False,
        )
    )

    # Suggested fix panel
    fix = result.get("fix", "No suggested fix available.")
    console.print(
        Panel(
            f"[bold green]{fix}[/]",
            title="[bold green]Suggested Fix[/]",
            title_align="left",
            border_style="green",
            box=box.ROUNDED,
            expand=False,
        )
    )

    # AST insight panel (if applicable)
    if result.get("ast_insight"):
        console.print(
            Panel(
                f"[white]{result['ast_insight']}[/]",
                title="[bold magenta]AST Insight[/]",
                title_align="left",
                border_style="magenta",
                box=box.ROUNDED,
                expand=False,
            )
        )


def print_result_json(result: dict):
    """Prints the translated error as a single-line JSON object on stdout (useful for jq and tooling)."""
    print(json.dumps(result, ensure_ascii=False))


def run_script(script_name: str, *, as_json: bool = False):
    """
    Run a target Python script and dynamically intercept/translate traceback output if it fails.
    
    Args:
        script_name (str): The script to run.
        as_json (bool): Whether to output the error translation in JSON format instead of Rich UI.
    """
    import subprocess
    try:
        # Run the script and capture stdout and stderr
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            # Script succeeded, just print its normal output
            print(result.stdout, end="")
        else:
            # Script failed, print partial stdout and translate the error output
            if result.stdout:
                print(result.stdout, end="")

            translation = translate_error(result.stderr)
            if as_json:
                print_result_json(translation)
            else:
                print_result(translation)

    except FileNotFoundError:
        # Handling the case where the provided script doesn't exist
        if as_json:
            print(json.dumps({
                "error": "script_not_found",
                "message": f"Could not find script '{script_name}'",
            }))
        else:
            console.print(
                Panel(
                    f"[bold red]Could not find script '{script_name}'[/]",
                    title="[bold red]Execution Error[/]",
                    border_style="red",
                    box=box.ROUNDED,
                    expand=False,
                )
            )
    except Exception as exc:
        # Catch-all for unexpected runtime issues with the sub-process
        if as_json:
            print(json.dumps({
                "error": "runtime_failure",
                "message": str(exc),
            }))
        else:
            console.print(
                Panel(
                    f"[bold red]{exc}[/]",
                    title="[bold red]Runtime Error[/]",
                    border_style="red",
                    box=box.ROUNDED,
                    expand=False,
                )
            )

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="explain-error",
        description="Error Translator — Turn cryptic Python tracebacks into clear, actionable advice.",
        epilog="""
Examples:
  explain-error run my_script.py
  explain-error "NameError: name 'usr_count' is not defined"
  cat error.log | explain-error
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-a", "--about", action="store_true", help="Display information about the tool.")
    parser.add_argument("-v", "--version", action="store_true", help="Show the current version of the tool.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output the translated error as a JSON object.")
    parser.add_argument("args", nargs="*", help="Positional arguments.")

    parsed_args = parser.parse_args()

    # Handle meta-flags
    if parsed_args.about:
        print_about()
        sys.exit(0)
    
    if parsed_args.version:
        console.print(f"Error Translator CLI Version: [bold green]{VERSION}[/]")
        sys.exit(0)
    
    # Choose output strategy
    emit = print_result_json if parsed_args.as_json else print_result

    # Handle piped input (e.g. `cat error.log | explain-error`)
    if not sys.stdin.isatty():
        error_input = sys.stdin.read()
        if error_input.strip():
            emit(translate_error(error_input))
            return

    # Provide help if no arguments are passed
    if not parsed_args.args:
        parser.print_help()
        sys.exit(1)

    # Detect the "run <script.py>" sub-command
    if parsed_args.args[0] == "run" and len(parsed_args.args) > 1:
        script_name = parsed_args.args[1]
        run_script(script_name, as_json=parsed_args.as_json)
    else:
        # Otherwise, treat the entire string of arguments as a raw traceback text
        error_input = " ".join(parsed_args.args)
        emit(translate_error(error_input))

if __name__ == "__main__":
    main()