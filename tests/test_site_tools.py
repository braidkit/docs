import pathlib
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_llms  # noqa: E402
import page_markdown  # noqa: E402
import site_config  # noqa: E402


class SiteConfigTests(unittest.TestCase):
    def test_load_site_config_rejects_non_mapping_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "mkdocs.yml"
            path.write_text("- not\n- a\n- mapping\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "YAML mapping"):
                site_config.load_site_config(path)

    def test_real_config_resolves_authored_titles_and_routes(self):
        config = site_config.load_site_config()
        pages = site_config.site_pages(config)

        self.assertEqual(17, len(pages))
        self.assertEqual("Documentation", pages[0].title)
        self.assertEqual("", pages[0].url)
        self.assertEqual("index.html", pages[0].dest_uri)
        self.assertEqual(
            "getting-started/installation/index.html",
            pages[2].dest_uri,
        )

    def test_nested_navigation_keeps_page_order(self):
        config = {
            "nav": [
                {"Home": "index.md"},
                {"Guides": [{"Install": "guides/install.md"}]},
                "reference.md",
            ]
        }

        self.assertEqual(
            [
                ("Home", "index.md"),
                ("Install", "guides/install.md"),
                ("Reference", "reference.md"),
            ],
            site_config.nav_entries(config),
        )

    def test_navigation_rejects_empty_and_unsupported_entries(self):
        with self.assertRaisesRegex(ValueError, "lists no pages"):
            site_config.nav_entries({"nav": []})

        with self.assertRaisesRegex(ValueError, "unsupported nav entry"):
            site_config.nav_entries({"nav": [42]})

    def test_site_pages_rejects_missing_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = {
                "docs_dir": temporary,
                "nav": [{"Missing": "missing.md"}],
            }

            with self.assertRaisesRegex(ValueError, "does not exist"):
                site_config.site_pages(config)

    def test_routes_cover_index_and_flat_page_shapes(self):
        self.assertEqual("", site_config.page_route("index.md"))
        self.assertEqual("guides/", site_config.page_route("guides/index.md"))
        self.assertEqual(
            "guides/install/",
            site_config.page_route("guides/install.md"),
        )
        self.assertEqual(
            "guides/install/index.html",
            site_config.html_destination("guides/install.md"),
        )

    def test_unterminated_front_matter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unterminated"):
            site_config.split_front_matter("---\ntitle: Broken\n")

    def test_optional_and_invalid_front_matter(self):
        plain = "# No front matter\n"
        self.assertEqual(({}, plain), site_config.split_front_matter(plain))

        with self.assertRaises(yaml.YAMLError):
            site_config.split_front_matter("---\ntitle: [broken\n---\n")

        with self.assertRaisesRegex(ValueError, "YAML mapping"):
            site_config.split_front_matter("---\n- not\n- a mapping\n---\n")

    def test_flat_html_destination(self):
        self.assertEqual(
            "guides/install.html",
            site_config.html_destination(
                "guides/install.md",
                use_directory_urls=False,
            ),
        )


class PublishingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temporary.name)
        self.docs = self.root / "docs"
        self.site = self.root / "site"
        (self.docs / "guides").mkdir(parents=True)
        self.site.mkdir()
        (self.docs / "index.md").write_text(
            "---\ntitle: Authored home\ndescription: Start here.\n---\n\n# Home\n",
            encoding="utf-8",
        )
        (self.docs / "guides" / "install.md").write_text(
            "---\n"
            "title: Install\n"
            "description: Install Braid.\n"
            "draft: true\n"
            "---\n\n"
            "# Install\n\n"
            "Draft body.\n",
            encoding="utf-8",
        )
        self.config = {
            "site_url": "https://docs.example.com/",
            "docs_dir": str(self.docs),
            "site_dir": str(self.site),
            "nav": [
                {"Home": "index.md"},
                {"Guides": [{"Installation": "guides/install.md"}]},
            ],
        }

    def tearDown(self):
        self.temporary.cleanup()

    def test_llms_corpus_uses_authored_title_and_omits_draft_body(self):
        index, full = build_llms.render(
            site_config.nav_entries(self.config),
            self.docs,
            self.config["site_url"],
        )

        self.assertIn("[Authored home](https://docs.example.com/)", index)
        self.assertIn("[Install](https://docs.example.com/guides/install/)", index)
        self.assertIn("Outline only", index)
        self.assertIn("## Authored home", full)
        self.assertNotIn("Draft body.", full)

    def test_sidecar_publisher_runs_without_mkdocs(self):
        page_markdown.publish_markdown(self.config)

        home = (self.site / "index.md").read_text(encoding="utf-8")
        install = (self.site / "guides" / "install.md").read_text(
            encoding="utf-8"
        )
        home_meta, home_body = site_config.split_front_matter(home)
        install_meta, _ = site_config.split_front_matter(install)

        self.assertEqual("Authored home", home_meta["title"])
        self.assertEqual("https://docs.example.com/", home_meta["url"])
        self.assertEqual("# Home\n", home_body)
        self.assertEqual(
            "https://docs.example.com/guides/install/",
            install_meta["url"],
        )

    def test_llms_requires_descriptions_and_existing_sources(self):
        (self.docs / "index.md").write_text(
            "---\ntitle: Missing description\n---\n\n# Home\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(SystemExit, "has no 'description'"):
            build_llms.render(
                site_config.nav_entries(self.config),
                self.docs,
                self.config["site_url"],
            )

        with self.assertRaisesRegex(SystemExit, "does not exist"):
            build_llms.render(
                [("Missing", "missing.md")],
                self.docs,
                self.config["site_url"],
            )


if __name__ == "__main__":
    unittest.main()
