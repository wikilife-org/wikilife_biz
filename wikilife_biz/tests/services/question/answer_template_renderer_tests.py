# coding=utf-8

from wikilife_biz.services.question.answer_template_renderer import \
    AnswerTemplateRenderer
from wikilife_biz.tests.services.question.base_question_test import BaseQuestionTest


class AnswerTemplateRendererTests(BaseQuestionTest):
   
    tpl_rdr = None
   
    def setUp(self):
        self.tpl_rdr = AnswerTemplateRenderer()

    def test_simple(self):
        tpl = '"a %s c" %v()'
        
        value = "b"
        
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a b c"

    def test_lower(self):
        tpl = '"a %s c" %v_lower()'
        
        value = 'B'
        
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a b c"

    def test_capitalize(self):
        #tpl = 'a capitalize(%s) c'
        #tpl = '"a "+capitalize("%s")+" c"'
        #tpl = 'a v_capitalize() c'
        tpl = '"a %s c" %v_capitalize()'
        
        value = 'foo'
        
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a Foo c"

    def test_tyn(self):
        tpl = '"a %s c" %v_tyn("foo", "bar")'
        
        value = 'Yes'
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a foo c"

        value = 'yes'
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a foo c"

        value = 'YES'
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a foo c"

        value = 'No'
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a bar c"

        value = 'no'
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a bar c"
        
        value = 'NO'
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a bar c"

    def test_tyn_void_yes(self):
        tpl = '"a %s c" %v_tyn("", "foo")'
        
        value = 'Yes'
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a c"

        value = 'No'
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a foo c"

    def test_tyn_other(self):
        tpl = '"a %s c" %v_tyn("vyes", "vno")'
        
        value = 'Other'
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a Other c"

    def test_tyn__lower_other(self):
        tpl = '"a %s c" %v_tyn_lower("vyes", "vno")'
        
        value = 'Other'
        r = self.tpl_rdr.render(tpl, value)
        print r
        assert r == "a other c"
