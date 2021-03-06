#!/usr/bin/env python
# Copyright (c) 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import re
import unittest

from py_vulcanize import parse_html_deps
from py_vulcanize import html_generation_controller


class ParseTests(unittest.TestCase):

  def test_parse_empty(self):
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse('')
    self.assertEqual([], module.scripts_external)
    self.assertEqual([], module.inline_scripts)
    self.assertEqual([], module.stylesheets)
    self.assertEqual([], module.imports)

  def test_parse_none(self):
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(None)
    self.assertEqual([], module.scripts_external)
    self.assertEqual([], module.inline_scripts)
    self.assertEqual([], module.stylesheets)
    self.assertEqual([], module.imports)

  def test_parse_script_src_basic(self):
    html = """<!DOCTYPE html>
              <html>
                <head>
                  <script src="polymer.min.js"></script>
                  <script src="foo.js"></script>
                </head>
                <body>
                </body>
              </html>"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual(['polymer.min.js', 'foo.js'], module.scripts_external)
    self.assertEqual([], module.inline_scripts)
    self.assertEqual([], module.stylesheets)
    self.assertEqual([], module.imports)
    self.assertNotIn(
        'DOCTYPE html',
        module.html_contents_without_links_and_script)

  def test_parse_link_rel_import(self):
    html = """<!DOCTYPE html>
              <html>
                <head>
                  <link rel="import" href="x-foo.html">
                </head>
                <body>
                </body>
              </html>"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual([], module.scripts_external)
    self.assertEqual([], module.inline_scripts)
    self.assertEqual([], module.stylesheets)
    self.assertEqual(['x-foo.html'], module.imports)

  def test_parse_script_inline(self):
    html = """<polymer-element name="tk-element-proto">
                <template>
                </template>
                <script>
                  py_vulcanize.require("foo");
                  py_vulcanize.require('bar');
                </script>
              </polymer-element>"""

    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual([], module.scripts_external)
    self.assertEqual(1, len(module.inline_scripts))
    self.assertEqual([], module.stylesheets)
    self.assertEqual([], module.imports)

    script0 = module.inline_scripts[0]
    val = re.sub(r'\s+', '', script0.contents)
    inner_script = """py_vulcanize.require("foo");py_vulcanize.require('bar');"""
    self.assertEqual(inner_script, val)

    self.assertEqual(3, len(script0.open_tags))
    self.assertEqual('polymer-element', script0.open_tags[2].tag)

    self.assertNotIn(
        'py_vulcanize.require("foo");',
        module.html_contents_without_links_and_script)

  def test_parse_script_inline_and_external(self):
    html = """<polymer-element name="tk-element-proto">
                <template>
                </template>
                <script>window = {}</script>
                <script src="foo.js"></script>
                <script>window = undefined</script>
              </polymer-element>"""

    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual(3, len(module.scripts))
    self.assertEqual('window = {}', module.scripts[0].contents)
    self.assertEqual("foo.js",module.scripts[1].src)
    self.assertTrue(module.scripts[1].is_external)
    self.assertEqual('window = undefined', module.scripts[2].contents)
    self.assertEqual([], module.imports)

  def test_parse_script_src_sripping(self):
    html = """
<script src="blah.js"></script>
"""
    module = parse_html_deps.HTMLModuleParser().Parse(html)
    self.assertEqual('',
                      module.html_contents_without_links_and_script)

  def test_parse_link_rel_stylesheet(self):
    html = """<polymer-element name="hi">
                <template>
                  <link rel="stylesheet" href="frameworkstyles.css">
                </template>
              </polymer-element>"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual([], module.scripts_external)
    self.assertEqual([], module.inline_scripts)
    self.assertEqual(['frameworkstyles.css'], module.stylesheets)
    self.assertEqual([], module.imports)

    class Ctl(html_generation_controller.HTMLGenerationController):

      def GetHTMLForStylesheetHRef(self, href):
        if href == 'frameworkstyles.css':
          return '<style>FRAMEWORK</style>'
        return None

    gen_html = module.GenerateHTML(Ctl())
    ghtm = """<polymer-element name="hi">
                <template>
                  <style>FRAMEWORK</style>
                </template>
              </polymer-element>"""
    self.assertEqual(ghtm, gen_html)

  def test_parse_inline_style(self):
    html = """<style>
  hello
</style>"""
    module = parse_html_deps.HTMLModuleParser().Parse(html)
    self.assertEqual(html, module.html_contents_without_links_and_script)

    class Ctl(html_generation_controller.HTMLGenerationController):

      def GetHTMLForInlineStylesheet(self, contents):
        if contents == '\n  hello\n':
          return '\n  HELLO\n'
        return None

    gen_html = module.GenerateHTML(Ctl())
    ghtm = """<style>
  HELLO
</style>"""
    self.assertEqual(ghtm, gen_html)

  def test_parse_style_import(self):
    html = """<polymer-element name="x-blink">
                <template>
                  <style>
                    @import url(awesome.css);
                  </style>
                </template>
              </polymer-element>"""
    parser = parse_html_deps.HTMLModuleParser()
    self.assertRaises(lambda: parser.Parse(html))

  def test_nested_templates(self):
    orig_html = """<template>
                  <template>
                    <div id="foo"></div>
                  </template>
                </template>"""
    parser = parse_html_deps.HTMLModuleParser()
    res = parser.Parse(orig_html)
    html = res.html_contents_without_links_and_script
    self.assertEqual(html, orig_html)

  def test_html_contents_basic(self):
    html = """<a b="c">d</a>"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual(html, module.html_contents_without_links_and_script)

  def test_html_contents_with_entity(self):
    html = """<a>&rarr;</a>"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual('<a>\u2192</a>',
                      module.html_contents_without_links_and_script)

  def test_html_content_with_charref(self):
    html = """<a>&#62;</a>"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual('<a>&gt;</a>',
                      module.html_contents_without_links_and_script)

  def test_html_content_start_end_br(self):
    html = """<a><br /></a>"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual('<a><br/></a>',
                      module.html_contents_without_links_and_script)

  def test_html_content_start_end_img(self):
    html = """<a><img src="foo.png" id="bar" /></a>"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual('<a><img id="bar" src="foo.png"/></a>',
                      module.html_contents_without_links_and_script)

  def test_html_contents_with_link_stripping(self):
    html = """<a b="c">d</a>
              <link rel="import" href="x-foo.html">"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual("""<a b="c">d</a>""",
                      module.html_contents_without_links_and_script.strip())

  def test_html_contents_with_style_link_stripping(self):
    html = """<a b="c">d</a>
              <link rel="stylesheet" href="frameworkstyles.css">"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual("""<a b="c">d</a>""",
                      module.html_contents_without_links_and_script.strip())

  def test_br_does_not_raise(self):
    html = """<div><br/></div>"""
    parser = parse_html_deps.HTMLModuleParser()
    parser.Parse(html)

  def test_p_does_not_raises(self):
    html = """<div></p></div>"""
    parser = parse_html_deps.HTMLModuleParser()
    parser.Parse(html)

  def test_link_endlink_does_not_raise(self):
    html = """<link rel="stylesheet" href="foo.css"></link>"""
    parser = parse_html_deps.HTMLModuleParser()
    parser.Parse(html)

  def test_link_script_does_not_raise(self):
    html = """<link rel="stylesheet" href="foo.css">
              <script>
              </script>"""
    parser = parse_html_deps.HTMLModuleParser()
    parser.Parse(html)

  def test_script_with_script_inside_as_js(self):
    html = """<script>
              var html_lines = [
                '<script>',
                '<\/script>',
              ];
              </script>"""
    parser = parse_html_deps.HTMLModuleParser()
    parser.Parse(html)

  def test_invalid_script_escaping_raises(self):
    html = """<script>
              var html_lines = [
                '<script>',
                '< /script>',
              ];
              </script>"""
    parser = parse_html_deps.HTMLModuleParser()

    def DoIt():
      parser.Parse(html)
    self.assertRaises(Exception, DoIt)

  def test_script_with_cdata(self):
    html = """<script></h2></script>"""
    parser = parse_html_deps.HTMLModuleParser()
    module = parser.Parse(html)
    self.assertEqual(1, len(module.inline_scripts))
    self.assertEqual('</h2>', module.inline_scripts[0].contents)
