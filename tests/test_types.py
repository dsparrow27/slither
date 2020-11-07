"""A simple test for nested compound networks
"""
import os
import unittest

from zoo.libs.utils import unittestBase
from slither import api


class TestTypes(unittestBase.BaseUnitest):
    def setUp(self):
        self.app = api.Application()

    def test_kFloat(self):
        typeCls = self.app.registry.dataTypeClass("kFloat", value=10.0, default=0.0)
        self.assertEqual(typeCls.value(), 10.0)
        self.assertEqual(typeCls.default, 0.0)

    def test_kInt(self):
        typeCls = self.app.registry.dataTypeClass("kInt", value=10, default=0)
        self.assertEqual(typeCls.value(), 10)
        self.assertEqual(typeCls.default, 0)

    def test_kString(self):
        typeCls = self.app.registry.dataTypeClass("kString", value="helloworld", default="")
        self.assertEqual(typeCls.value(), "helloworld")
        self.assertEqual(typeCls.default, "")

    def test_kBool(self):
        typeCls = self.app.registry.dataTypeClass("kBool", value=True, default=False)
        self.assertEqual(typeCls.value(), True)
        self.assertEqual(typeCls.default, False)

    def test_kDict(self):
        typeCls = self.app.registry.dataTypeClass("kDict", value={"key": "value"}, default={})
        self.assertEqual(typeCls.value(), {"key": "value"})
        self.assertEqual(typeCls.default, {})

    def test_kFile(self):
        typeCls = self.app.registry.dataTypeClass("kFile", value="~/Documents/test.json", default="")
        self.assertEqual(typeCls.value(), "~/Documents/test.json")
        self.assertEqual(typeCls.default, "")

    def test_kDirectory(self):
        typeCls = self.app.registry.dataTypeClass("kDirectory", value="~/Documents", default="")
        self.assertEqual(typeCls.value(), "~/Documents")
        self.assertEqual(typeCls.default, "")

    def test_kList(self):
        typeCls = self.app.registry.dataTypeClass("kList", value=[], default=[])
        self.assertEqual(typeCls.value(), [])
        self.assertEqual(typeCls.default, [])

    def test_kMulti(self):
        typeCls = self.app.registry.dataTypeClass("kMulti", value="", default="")
        self.assertEqual(typeCls.value(), "")
        self.assertEqual(typeCls.default, "")
