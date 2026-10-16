import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_commands  # noqa: E402


ROOT_HELP = """Usage:
  braid [command]

Available Commands:
  bot         Share intent decisions on GitHub pull requests
  review      Record a review verdict for a braid

Flags:
  -h, --help   help for braid
"""

REVIEW_HELP = """Usage:
  braid review <braid-id> [flags]

Flags:
      --verdict string   review verdict: approved|requested-changes|blocked

Global Flags:
      --verbose   enable debug logging
"""

BOT_HELP = """Available Commands:
  enable      Turn the bot on

Flags:
  -h, --help   help for bot
"""

HELP = {
    ("braid",): ROOT_HELP,
    ("braid", "review"): REVIEW_HELP,
    ("braid", "bot"): BOT_HELP,
    ("braid", "bot", "enable"): "Flags:\n  -h, --help   help for enable\n",
}


def read_help(path):
    return check_commands.parse_help(HELP[path])


class PageCommandTests(unittest.TestCase):
    def test_reads_inline_code_and_indented_shell_blocks(self):
        text = (
            "Run `braid bot enable`, once.\n\n"
            "1. Approve:\n\n"
            "    ```sh\n"
            "    braid review <braid-id> --verdict approved\n"
            "    ```\n\n"
            "```python\nbraid = 1\n```\n"
            "The `braid-daemon` binary and `braid bot enable` again.\n"
        )

        self.assertEqual(
            ["braid review <braid-id> --verdict approved", "braid bot enable"],
            check_commands.page_commands(text),
        )


class CheckCommandTests(unittest.TestCase):
    def test_accepts_commands_the_help_lists(self):
        self.assertEqual([], check_commands.check_command("braid bot enable", read_help))
        self.assertEqual(
            [],
            check_commands.check_command(
                "braid review <braid-id> --verdict approved --verbose", read_help
            ),
        )

    def test_reports_unknown_subcommands(self):
        errors = check_commands.check_command("braid bots enable", read_help)

        self.assertEqual(1, len(errors))
        self.assertIn("has no bots subcommand", errors[0])

    def test_reports_unknown_flags(self):
        errors = check_commands.check_command("braid bot enable --everywhere", read_help)

        self.assertEqual(1, len(errors))
        self.assertIn("has no --everywhere flag", errors[0])

    def test_reports_values_outside_a_fixed_set(self):
        errors = check_commands.check_command(
            "braid review <braid-id> --verdict=approve", read_help
        )

        self.assertEqual(1, len(errors))
        self.assertIn("not approve", errors[0])

    def test_arguments_after_the_command_path_are_not_subcommands(self):
        self.assertEqual(
            [], check_commands.check_command("braid review braid_0123", read_help)
        )


if __name__ == "__main__":
    unittest.main()
