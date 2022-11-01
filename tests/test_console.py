#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  31 21:38:09 2022
@author: SirSanctified
"""
import sys
import unittest
import inspect
# import pep8
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from console import HBNBCommand
from models import *


class TestConsole(unittest.TestCase):
    """
    class for testing HBNBCommand class' methods
    """
    classes = ["User", "State", "Review", "Place", "City", "BaseModel"]

    @classmethod
    def setUpClass(cls):
        """
        Set up class method for the doc tests
        """
        cls.setup = inspect.getmembers(HBNBCommand, inspect.isfunction)


    def test_module_docstring(self):
        """
        Tests if module docstring documentation exist
        """
        self.assertTrue(len(HBNBCommand.__doc__) >= 1)

    def test_class_docstring(self):
        """
        Tests if class docstring documentation exist
        """
        self.assertTrue(len(HBNBCommand.__doc__) >= 1)

    def test_help_console_cmd(self):
        """
            Test <help>
        """
        expected = """
Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update
\n"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            self.assertEqual(expected, f.getvalue())

    def test_help_quit_console_cmd(self):
        """
            Tests <help quit>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
            self.assertRegex(f.getvalue(), 'Quit command+')

    def test_help_EOF_console_cmd(self):
        """
            Tests <help EOF>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
            self.assertRegex(f.getvalue(), 'ctrl-d command+')

    def test_help_create_console_cmd(self):
        """
            Tests <help create>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
            self.assertRegex(f.getvalue(), 'Creates+')

    def test_create_console_cmd_should_fail_without_clsname(self):
        """
            Test <create>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            expected = "** class name missing **\n"
            self.assertEqual(expected, f.getvalue())

    def test_create_console_cmd_should_fail_with_wrong_clsname(self):
        """
            Test <create WrongClsName>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create WrongClsName")
            expected = "** class doesn't exist **\n"
            self.assertEqual(expected, f.getvalue())

    def test_create_console_cmd_should_work_properly(self):
        """
            Test <create BaseModel>
        """
        for className in TestConsole.classes:
            instance_before = len(storage.all())
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create {}".format(className))
                instance_after = len(storage.all())
                key_id = className + "." + f.getvalue().strip("\n")
                self.assertIn(key_id, storage.all().keys())
                self.assertEqual(instance_before + 1, instance_after)

    def test_help_show_console_cmd(self):
        """
            Tests <help show>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            self.assertRegex(f.getvalue(), 'Prints+')

    def test_show_console_cmd_should_fails_without_clsname(self):
        """
            Tests <show>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            expected = "** class name missing **\n"
            self.assertEqual(expected, f.getvalue())

    def test_show_console_cmd_should_fail_with_wrong_clsname(self):
        """
        Test <show WrongClsName>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show WrongClsName")
            expected = "** class doesn't exist **\n"
            self.assertEqual(expected, f.getvalue())

    def test_show_console_cmd_should_fail_without_id(self):
        """
        Test <show BaseModel>
        """
        for className in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("show {}".format(className))
                expected = "** instance id missing **\n"
                self.assertEqual(expected, f.getvalue())

    def test_show_console_cmd_should_fail_with_wrong_id(self):
        """
        Test <show BaseModel 1212121212>
        """
        for className in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("show {} 1212121212".format(className))
                expected = "** no instance found **\n"
                self.assertEqual(expected, f.getvalue())

    def test_help_destroy_console_cmd(self):
        """
        Tests <help destroy>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
            self.assertRegex(f.getvalue(), 'Deletes+')

    def test_destroy_console_cmd_should_fails_without_clsname(self):
        """
        Tests <destroy>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            expected = "** class name missing **\n"
            self.assertEqual(expected, f.getvalue())

    def test_destroy_console_cmd_should_fail_without_id(self):
        """
        Test <destroy BaseModel>
        """
        for className in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("destroy {}".format(className))
                expected = "** instance id missing **\n"
                self.assertEqual(expected, f.getvalue())

    def test_destroy_console_cmd_should_fail_with_wrong_id(self):
        """
        Test <destroy BaseModel 1212121212>
        """
        for className in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("destroy {} 12121212".format(className))
                expected = "** no instance found **\n"
                self.assertEqual(expected, f.getvalue())

    def test_help_all_console_cmd(self):
        """
        Tests <help all>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
            self.assertRegex(f.getvalue(), 'Prints all+')

    def test_all_console_cmd_should_fail_with_wrong_clsname(self):
        """
        Test <all WrongClsName>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all WrongClsName")
            expected = "** class doesn't exist **\n"
            self.assertEqual(expected, f.getvalue())

    def test_all_command(self):
        """
            test <all>
            test <all> <className>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            res = []
            for key, val in storage.all().items():
                res.append(str(val))
            self.assertEqual(eval(f.getvalue()), res)
        for className in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("all {}".format(className))
                res = []
                for key, val in storage.all().items():
                    if val.__class__.__name__ == className:
                        res.append(str(val))
                self.assertEqual(eval(f.getvalue()), res)

    def test_help_update_console_cmd(self):
        """
        Tests <help update>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
            self.assertRegex(f.getvalue(), 'Updates+')

    def test_update_console_cmd_should_fails_without_clsname(self):
        """
        Tests <update>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            expected = "\n** class name missing **\n"
            self.assertEqual(expected, f.getvalue())

    def test_update_console_cmd_should_fail_with_wrong_clsname(self):
        """
        Test <update WrongClsName>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update WrongClsName")
            expected = "WrongClsName\n** class doesn't exist **\n"
            self.assertEqual(expected, f.getvalue())

    def test_update_console_cmd_should_fail_without_id(self):
        """
        Test <update BaseModel>
        """
        for className in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("update {}".format(className))
                expected = f"{className}\n** instance id missing **\n"
                self.assertEqual(expected, f.getvalue())

    def test_update_console_cmd_should_fail_with_wrong_id(self):
        """
        Test <update BaseModel 1212121212>
        """
        for className in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("update {} 1212121".format(className))
                expected = f"{className} 1212121\n** no instance found **\n"
                self.assertEqual(expected, f.getvalue())
