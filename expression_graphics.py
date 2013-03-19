# -*- coding: utf-8 -*-
from quepy.semantics import FixedType, HasKeyword, IsRelatedTo, FixedRelation
HasKeyword.relation = "rdfs:label"


def example_0():
    e = HasKeyword(u"John")
    return e


def example_1():
    class IsPerson(FixedType):
        fixedtype = "foaf:Person"

    e = IsPerson()
    return e


def example_2():
    class IsPerson(FixedType):
        fixedtype = "foaf:Person"

    e = IsPerson() + HasKeyword(u"John")
    return e


def example_3():
    class IsPerson(FixedType):
        fixedtype = "foaf:Person"

    a = IsPerson() + HasKeyword(u"John")
    e = IsRelatedTo(a)
    return e


def example_4():
    class IsPerson(FixedType):
        fixedtype = "foaf:Person"

    a = IsPerson() + HasKeyword(u"John")
    e = IsPerson() + HasKeyword(u"Mary") + IsRelatedTo(a)
    return e


def example_5():
    class IsPerson(FixedType):
        fixedtype = "foaf:Person"

    class BirthDateOf(FixedRelation):
        relation = "dbpprop:birthDate"
        reverse = True

    john = IsPerson() + HasKeyword(u"John")
    e    = BirthDateOf(john)
    return e


def example_6():
    class HeadOf(FixedRelation):
        relation = ""
        reverse=True

    # The cat ate a fish

    the  = HasKeyword(u"The")
    cat  = HasKeyword(u"cat")  + HeadOf(the)
    a    = HasKeyword(u"a")
    fish = HasKeyword(u"fish") + HeadOf(a)
    ate  = HasKeyword(u"ate")  + HeadOf(cat) + HeadOf(fish)
    return ate



###
### Begin boilerplate
###


import sys
import base64
import subprocess
from quepy.printout import expression_to_dot, expression_to_sparql
from xml.sax.saxutils import escape
import inspect


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
    <td style="padding-left: 10px">
        <b style="text-align: center"></b><br /> <pre>{sparql}</pre> </td>
    <td style="padding-left: 10px">
        <img src="data:image/png;base64,{image_base64}" />
    </td>
</tr>
<tr>
    <td colspan="3"><hr /></td>
</tr>
"""


def expressions_to_html(expressions):
    rows = ""
    for expression in expressions:
        dot_string = expression_to_dot(expression)
        target, query = expression_to_sparql(expression)

        dot_path = "/tmp/quepy_graph.dot"
        cmdline = "dot -Tpng %s" % dot_path

        with open(dot_path, "w") as filehandler:
            filehandler.write(dot_string)

        try:
            call = subprocess.Popen(cmdline.split(), stdout=subprocess.PIPE)
            output, _ = call.communicate()
        except OSError:
            msg = "Error running '{}': the program 'dot' was not found."
            print msg.format(cmdline)
            sys.exit(1)

        image_base64 = base64.b64encode(output)

        query = "\n".join([x for x in query.split("\n")
                           if not x.startswith("PREFIX")])
        query = escape(query)
        code = expression.source_code.split("\n")
        name = code[0].replace("def", "").replace("_", " ").strip(" :()")
        code = "\n".join(code[1:-2])
        rows += QUERY_TEMPLATE.format(name=name.capitalize(),
                                      code=code,
                                      sparql=query,
                                      image_base64=image_base64)

    html = HTML_TEMPLATE.format(rows=rows)
    with open("expression_inform.html", "w") as filehandler:
        filehandler.write(html)


expressions = []
for name, value in sorted(globals().items()):
    if "example" in name:
        try:
            e = value()
            e.source_code = inspect.getsource(value)
            expressions.append(e)
        except:
            pass
expressions_to_html(expressions)