import json
import sys
import argparse
from .core import translate_error
from importlib.metadata import version, PackageNotFoundError

# Import Rich UI Components
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.table import Table
from rich import box

try:
    VERSION = version("error-translator-cli-v2")
except PackageNotFoundError:
    VERSION = "unknown (not installed via pip)"

# Initialize the global rich console
console = Console()


def _print_title_banner():
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
    """Prints a polished about view using rich components."""
    _print_title_banner()

    meta = Table.grid(padding=(0, 1))
    meta.add_column(style="bold white", justify="right")
    meta.add_column(style="green")
    meta.add_row("Version", VERSION)
    meta.add_row("Author", "Gourabananda Datta")
    meta.add_row("Repository", "https://github.com/gourabanandad/error-translator-cli-v2")
    console.print(Panel(meta, title="[bold cyan]Project[/]", border_style="cyan", expand=False))

    features = Text()
    features.append("• Offline and fast translation\n", style="white")
    features.append("• Human-readable explanations\n", style="white")
    features.append("• Actionable fix suggestions\n", style="white")
    features.append("• Optional AST-level insight", style="white")
    console.print(Panel(features, title="[bold green]Features[/]", border_style="green", expand=False))

    examples = Text()
    examples.append("explain-error run your_script.py\n", style="bold cyan")
    examples.append("explain-error \"TypeError: ...\"\n", style="bold cyan")
    examples.append("cat error.log | explain-error", style="bold cyan")
    console.print(Panel(examples, title="[bold yellow]Quick Start[/]", border_style="yellow", expand=False))


def print_result(result: dict):
    """Print translated output in a polished, professional layout."""
    console.print()

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
    """Prints the translated error as a single-line JSON object on stdout."""
    print(json.dumps(result, ensure_ascii=False))


def run_script(script_name: str, *, as_json: bool = False):
    """Run a Python script and translate traceback output if it fails."""
    import subprocess
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(result.stdout, end="")
        else:
            if result.stdout:
                print(result.stdout, end="")

            translation = translate_error(result.stderr)
            if as_json:
                print_result_json(translation)
            else:
                print_result(translation)

    except FileNotFoundError:
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

    if parsed_args.about:
        print_about()
        sys.exit(0)
    
    if parsed_args.version:
        console.print(f"Error Translator CLI Version: [bold green]{VERSION}[/]")
        sys.exit(0)
    
    emit = print_result_json if parsed_args.as_json else print_result

    if not sys.stdin.isatty():
        error_input = sys.stdin.read()
        if error_input.strip():
            emit(translate_error(error_input))
            return

    if not parsed_args.args:
        parser.print_help()
        sys.exit(1)

    if parsed_args.args[0] == "run" and len(parsed_args.args) > 1:
        script_name = parsed_args.args[1]
        run_script(script_name, as_json=parsed_args.as_json)
    else:
        error_input = " ".join(parsed_args.args)
        emit(translate_error(error_input))

if __name__ == "__main__":
    main()