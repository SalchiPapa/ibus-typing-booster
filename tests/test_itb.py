# -*- coding: utf-8 -*-
# vim:et sts=4 sw=4
#
# ibus-typing-booster - A completion input method for IBus
#
# Copyright (c) 2016 Mike FABIAN <mfabian@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import sys
import os
import unicodedata
import unittest

from gi import require_version
require_version('IBus', '1.0')
from gi.repository import IBus

sys.path.insert(0, "../engine")
from hunspell_table import *
import tabsqlitedb
sys.path.pop(0)

class ItbTestCase(unittest.TestCase):
    def setUp(self):
        self.bus = IBus.Bus()
        # it doesn’t really matter which config file for which language is used
        self.db = tabsqlitedb.tabsqlitedb(
            config_filename ='../hunspell-tables/de_DE.conf',
            user_db_file = ':memory:')
        self.engine = TypingBoosterEngine(
            self.bus,
            '/com/redhat/IBus/engines/table/typing_booster_de_DE/engine/0',
            self.db,
            unit_test = True)
        self.backup_original_settings()
        self.set_default_settings()
        pass

    def tearDown(self):
        self.restore_original_settings()
        del self.engine

    def backup_original_settings(self):
        self.orig_emoji_prediction_mode = (
            self.engine.get_emoji_prediction_mode())
        self.orig_off_the_record_mode = (
            self.engine.get_off_the_record_mode())
        self.orig_auto_commit_characters = (
            self.engine.get_auto_commit_characters())
        self.orig_tab_enable = (
            self.engine.get_tab_enable())
        self.orig_remember_last_used_preedit_ime = (
            self.engine.get_remember_last_used_preedit_ime())
        self.orig_page_size = (
            self.engine.get_page_size())
        self.orig_min_char_complete = (
            self.engine.get_min_char_complete())
        self.orig_show_number_of_candidates = (
            self.engine.get_show_number_of_candidates())
        self.orig_use_digits_as_select_keys = (
            self.engine.get_use_digits_as_select_keys())
        self.orig_current_imes = (
            self.engine.get_current_imes())
        self.orig_dictionary_names = (
            self.engine.get_dictionary_names())
        self.orig_add_direct_input = (
            self.engine.get_add_direct_input())

    def restore_original_settings(self):
        self.engine.set_emoji_prediction_mode(
            self.orig_emoji_prediction_mode)
        self.engine.set_off_the_record_mode(
            self.orig_off_the_record_mode)
        self.engine.set_auto_commit_characters(
            self.orig_auto_commit_characters)
        self.engine.set_tab_enable(
            self.orig_tab_enable)
        self.engine.set_remember_last_used_preedit_ime(
            self.orig_remember_last_used_preedit_ime)
        self.engine.set_page_size(
            self.orig_page_size)
        self.engine.set_min_char_complete(
            self.orig_min_char_complete)
        self.engine.set_show_number_of_candidates(
            self.orig_show_number_of_candidates)
        self.engine.set_use_digits_as_select_keys(
            self.orig_use_digits_as_select_keys)
        self.engine.set_current_imes(
            self.orig_current_imes)
        self.engine.set_dictionary_names(
            self.orig_dictionary_names)
        self.engine.set_add_direct_input(
            self.orig_add_direct_input)

    def set_default_settings(self):
        self.engine.set_emoji_prediction_mode(True)
        self.engine.set_off_the_record_mode(False)
        self.engine.set_auto_commit_characters('')
        self.engine.set_tab_enable(False)
        self.engine.set_remember_last_used_preedit_ime(False)
        self.engine.set_page_size(6)
        self.engine.set_min_char_complete(1)
        self.engine.set_show_number_of_candidates(False)
        self.engine.set_use_digits_as_select_keys(True)
        self.engine.set_current_imes(['NoIme'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.set_add_direct_input(False)

    def test_dummy(self):
        self.assertEqual(True, True)

    def test_single_char_commit_with_space(self):
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'a ')

    def test_single_char_commit_with_arrow_right(self):
        self.engine.do_process_key_event(IBus.KEY_b, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Right, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'b')

    def test_char_space_period_space(self):
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_period, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'a . ')

    def test_direct_input(self):
        self.engine.set_current_imes(['NoIme', 't-latn-post'])
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_quotedbl, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'a" ')

    def test_latn_post(self):
        self.engine.set_current_imes(['t-latn-post', 'NoIme'])
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_quotedbl, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'ä ')

    def test_autocommit_characters(self):
        self.engine.set_current_imes(['NoIme', 't-latn-post'])
        self.engine.set_auto_commit_characters('.')
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_semicolon, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_period, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_b, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'a;. b ')

    def test_set_page_size(self):
        self.engine.set_page_size(3)
        self.assertEqual(
            self.engine._editor.get_lookup_table()._mock_page_size,
            3)
        self.engine.set_page_size(5)
        self.assertEqual(
            self.engine._editor.get_lookup_table()._mock_page_size,
            5)

    def test_complete_word_from_us_english_dictionary(self):
        self.engine.set_current_imes(['NoIme', 't-latn-post'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.assertEqual(self.engine._editor._candidates[0][0], 'cerulean')
        self.engine.do_process_key_event(IBus.KEY_F1, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'cerulean ')

    def test_commit_with_arrows(self):
        self.engine.set_current_imes(['NoIme', 't-latn-post'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.do_process_key_event(IBus.KEY_f, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_o, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_o, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'foo ')
        self.engine.do_process_key_event(IBus.KEY_b, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'foo ')
        self.assertEqual(self.engine._mock_committed_text_cursor_pos, 4)
        self.assertEqual(self.engine._mock_preedit_text, 'bar')
        self.assertEqual(self.engine._mock_preedit_text_cursor_pos, 3)
        self.assertEqual(self.engine._mock_preedit_text_visible, True)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'foo ')
        self.assertEqual(self.engine._mock_preedit_text, 'bar')
        self.assertEqual(self.engine._mock_preedit_text_cursor_pos, 0)
        self.assertEqual(self.engine._mock_preedit_text_visible, True)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'foo bar')
        self.assertEqual(self.engine._mock_committed_text_cursor_pos, 3)
        self.assertEqual(self.engine._mock_preedit_text, '')
        self.assertEqual(self.engine._mock_preedit_text_cursor_pos, 0)
        self.assertEqual(self.engine._mock_preedit_text_visible, False)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'foo  bar')
        self.assertEqual(self.engine._mock_committed_text_cursor_pos, 4)
        self.engine.do_process_key_event(IBus.KEY_b, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_z, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, IBus.ModifierType.CONTROL_MASK)
        self.assertEqual(self.engine._mock_committed_text, 'foo  bar')
        self.assertEqual(self.engine._mock_committed_text_cursor_pos, 4)
        self.assertEqual(self.engine._mock_preedit_text, 'baz')
        self.assertEqual(self.engine._mock_preedit_text_cursor_pos, 0)
        self.assertEqual(self.engine._mock_preedit_text_visible, True)
        self.engine.do_process_key_event(IBus.KEY_Left, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'foo baz bar')
        self.assertEqual(self.engine._mock_committed_text_cursor_pos, 3)
        self.assertEqual(self.engine._mock_preedit_text, '')
        self.assertEqual(self.engine._mock_preedit_text_cursor_pos, 0)
        self.assertEqual(self.engine._mock_preedit_text_visible, False)

    def test_emoji_related_tab_enable_cursor_visible_escape(self):
        self.engine.set_current_imes(['NoIme'])
        self.engine.set_dictionary_names(['en_US'])
        self.engine.set_tab_enable(True)
        self.engine.do_process_key_event(IBus.KEY_c, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_m, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_Tab, 0, 0)
        self.assertEqual(self.engine._editor._candidates[0][0], 'camel')
        self.assertEqual(self.engine._editor._candidates[5][0], '🐫')
        self.assertEqual(self.engine._editor._candidates[5][2],
                         'bactrian camel “two-hump camel”')
        self.engine.do_candidate_clicked(5, 3, 0)
        self.assertEqual(self.engine._editor._candidates[0][0], '🐫')
        self.assertEqual(self.engine._editor._candidates[1][0], '🐪')
        self.assertEqual(
            self.engine._editor.get_lookup_table().cursor_visible,
            False)
        self.engine.do_process_key_event(IBus.KEY_Down, 0, 0)
        self.assertEqual(
            self.engine._editor.get_lookup_table().cursor_visible,
            True)
        self.engine.do_process_key_event(IBus.KEY_Down, 0, 0)
        self.assertEqual(
            self.engine._editor.get_lookup_table().cursor_visible,
            True)
        self.assertEqual(
            self.engine._editor.get_string_from_lookup_table_cursor_pos(),
            '🐪')
        self.engine.do_process_key_event(IBus.KEY_Escape, 0, 0)
        self.assertEqual(
            self.engine._editor.get_lookup_table().cursor_visible,
            False)
        self.assertEqual(
            self.engine._editor.get_lookup_table().get_cursor_pos(),
            0)
        self.assertEqual(
            self.engine._editor.get_string_from_lookup_table_cursor_pos(),
            '🐫')
        self.engine.do_process_key_event(IBus.KEY_Escape, 0, 0)
        self.assertEqual(
            self.engine._editor.get_lookup_table().cursor_visible,
            False)
        self.assertEqual(
            self.engine._editor.get_lookup_table().get_cursor_pos(),
            0)
        self.assertEqual(self.engine._editor._candidates[0][0], 'camel')
        self.assertEqual(self.engine._editor._candidates[5][0], '🐫')
        self.assertEqual(self.engine._editor._candidates[5][2],
                         'bactrian camel “two-hump camel”')
        self.engine.do_process_key_event(IBus.KEY_Down, 0, 0)
        self.assertEqual(
            self.engine._editor.get_lookup_table().cursor_visible,
            True)
        self.assertEqual(
            self.engine._editor.get_string_from_lookup_table_cursor_pos(),
            'camel')
        self.engine.do_process_key_event(IBus.KEY_Escape, 0, 0)
        self.assertEqual(
            self.engine._editor.get_lookup_table().cursor_visible,
            False)
        self.assertEqual(
            self.engine._editor.get_lookup_table().get_cursor_pos(),
            0)
        self.assertEqual(
            self.engine._editor.get_string_from_lookup_table_cursor_pos(),
            'camel')
        self.engine.do_process_key_event(IBus.KEY_Escape, 0, 0)
        self.assertEqual(
            self.engine._editor.get_lookup_table().get_number_of_candidates(),
            0)
        self.assertEqual(self.engine._editor._candidates, [])
        self.assertEqual(self.engine._mock_preedit_text, 'camel')
        self.assertEqual(self.engine._mock_preedit_text_cursor_pos, 5)
        self.assertEqual(self.engine._mock_preedit_text_visible, True)
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine._mock_committed_text, 'camel ')
        self.assertEqual(self.engine._mock_preedit_text, '')
        self.assertEqual(self.engine._mock_preedit_text_cursor_pos, 0)
        self.assertEqual(self.engine._mock_preedit_text_visible, False)

    def test_marathi_add_direct_input(self):
        self.engine.set_current_imes(['mr-itrans'])
        self.engine.set_dictionary_names(['mr_IN'])
        self.engine.set_add_direct_input(True)
        self.assertEqual(
            self.engine.get_current_imes(), ['mr-itrans', 'NoIme'])
        self.assertEqual(
            self.engine.get_dictionary_names(), ['mr_IN', 'en_GB'])
        self.engine.do_process_key_event(IBus.KEY_g, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_r, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_u, 0, 0)
        self.assertEqual(self.engine._mock_preedit_text, 'गुरु')
        self.engine.do_process_key_event(IBus.KEY_Down, 0, IBus.ModifierType.CONTROL_MASK)
        self.assertEqual(self.engine._mock_preedit_text, 'guru')
        self.engine.do_process_key_event(IBus.KEY_Down, 0, IBus.ModifierType.CONTROL_MASK)
        self.assertEqual(self.engine._mock_preedit_text, 'गुरु')
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine._mock_preedit_text, '')
        self.assertEqual(self.engine._mock_committed_text, 'गुरु ')

    def test_korean(self):
        self.engine.set_current_imes(['ko-romaja'])
        self.engine.set_dictionary_names(['ko_KR'])
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_y, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_o, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_g, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.assertEqual(self.engine._mock_preedit_text, '안녕하')
        candidates = [unicodedata.normalize('NFC', x[0])
                      for x in self.engine._editor._candidates]
        self.assertEqual(True, '안녕할듯하다' in candidates)
        self.engine.do_process_key_event(IBus.KEY_l, 0, 0)
        self.assertEqual(self.engine._mock_preedit_text, '안녕할')
        self.engine.do_process_key_event(IBus.KEY_space, 0, 0)
        self.assertEqual(self.engine._mock_preedit_text, '')
        self.assertEqual(self.engine._mock_committed_text, '안녕할 ')
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_y, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_e, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_o, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_n, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_g, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_h, 0, 0)
        self.engine.do_process_key_event(IBus.KEY_a, 0, 0)
        self.assertEqual(self.engine._mock_preedit_text, '안녕하')
        candidates = [unicodedata.normalize('NFC', x[0])
                      for x in self.engine._editor._candidates]
        self.assertEqual(True, '안녕할' in candidates)
        self.assertEqual('안녕할', candidates[0])
