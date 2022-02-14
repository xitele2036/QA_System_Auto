# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import os
import unittest

from py_vulcanize import resource


class ResourceUnittest(unittest.TestCase):

  def testBasic(self):
    r = resource.Resource('/a', '/a/b/c.js')
    self.assertEqual('b.c', r.name)
    self.assertEqual(os.path.join('b', 'c.js'), r.relative_path)
    self.assertEqual('b/c.js', r.unix_style_relative_path)
