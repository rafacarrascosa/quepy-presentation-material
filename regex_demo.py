# -*- coding: utf-8 -*-
from quepy.regex import *


class Example_1(RegexTemplate):
    test_string = u"What is aluminum"

    def make_regex(self):
        regex = Token("What") + Lemma("be") + Pos("NN")
        return regex

    def semantics(self, match):
        return match


class Example_2(RegexTemplate):
    test_string = u"What is jumped"

    def make_regex(self):
        regex = Token("What") + Lemma("be") + Pos("NN")
        return regex

    def semantics(self, match):
        return match


class Example_3(RegexTemplate):
    test_string = u"What is love"

    def make_regex(self):
        regex = Pos("WP") + Lemma("be") + Thing()
        return regex

    def semantics(self, match):
        return match


class Example_4(RegexTemplate):
    test_string = u"a a b b a a a"

    def make_regex(self):
        a = Token("a")
        b = Token("b")
        regex = Star((a + a) | b) + a
        return regex

    def semantics(self, match):
        return match


class Example_8(RegexTemplate):
    test_string = u"How long is The Neverending Story?"

    def make_regex(self):
        A = Pos("WP") + Lemmas("be the duration of")
        B = Lemma("how") + Lemma("long") + Lemma("be")

        regex = (A | B) + Movie() + Pos(".")
        return regex

    def semantics(self, match):
        return match


class Example_9(RegexTemplate):
    test_string = u"The Matrix"

    def make_regex(self):
        class Movie(Particle):
            regex = Question(Pos("DT")) + \
                    Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

            def semantics(self, match):
                return match.words.tokens

        regex = Movie()
        return regex

    def semantics(self, match):
        return match


###
### Begin boilerplate
###

import inspect
from quepy.tagger import get_tagger
from quepy import settings
from refo import Question, Plus

# Put your nltk path here:
settings.NLTK_DATA_PATH = ["/home/rafael/deploy/nltk/data"]
tagger = get_tagger()


class Thing(Particle):
    regex = Any()

    def semantics(self, match):
        return match.words.tokens


class Movie(Particle):
    regex = Question(Pos("DT")) + \
            Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def semantics(self, match):
        return match.words.tokens


HTML_TEMPLATE = """
<html><body>
<table style="border:0" align="center">
    <tr>
        <td colspan="3"><h2 style="text-align: center"> </h2></td>
    </tr>
    <tr><td colspan="3"><hr /></td></tr>
    {rows}
</table>
</body></html>
"""

QUERY_TEMPLATE = """
<tr>
    <td colspan="3"><h2 style="text-align: center">{name}</h2></td>
</tr>
<tr>
    <td>
        <b style="text-align: center"></b><br /> <pre>{code}</pre> </td>
    <td style="padding-left: 30px">
        <b style="text-align: center"></b><br /> {string}
        <br /> {understood} </td>
    <td style="padding-left: 30px">
        <b style="text-align: center"></b><br /> <pre>{groups}</pre> </td>
</tr>
<tr>
    <td colspan="3"><hr /></td>
</tr>
"""


def templates_to_html(templates):
    rows = ""
    for template in templates:
        try:
            string = template.test_string
        except:
            continue
        #name = template.__name__.capitalize()
        name = ""
        code = inspect.getsource(template.make_regex)
        code = code.split("\n")
        code = "\n".join(code[1:-2])
        words = list(tagger(string))
        instance = template()
        instance.regex = instance.make_regex()
        match, _ = instance.get_semantics(words)
        groups = "None"
        if match is not None:
            groups = {}
            for particle in match._particles:
                groups[particle] = getattr(match, particle)
        rows += QUERY_TEMPLATE.format(name=name,
                                      code=code,
                                      string=string,
                                      understood=" ".join(map(str, words)),
                                      groups=groups)

    html = HTML_TEMPLATE.format(rows=rows)
    with open("regex_inform.html", "w") as filehandler:
        filehandler.write(html)


templates = []
for name, value in sorted(globals().items()):
    if isinstance(value, type) and issubclass(value, RegexTemplate):
        try:
            templates.append(value)
        except:
            pass
templates_to_html(templates)