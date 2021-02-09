from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import dict
from builtins import open
from builtins import int
from future import standard_library
standard_library.install_aliases()

import os  # NOQA: E402
from pyparsing import *  # NOQA: E402
from .fgd import *  # NOQA: E402


# Basic parsers
def protectUnescapedCharacters(quoted_string):
    result = quoted_string.pop()
    if result:
        result = result.replace('\\r', '\r')
        result = result.replace('\r', '\\r')
    return result


pp_name = Word(alphanums+'_')
pp_nums = Word(nums+'-.')
pp_value = Word(nums+'-. ')  # maybe space delimited vertex

pp_quoted = Combine(QuotedString('"') + Optional(OneOrMore(
    Suppress('+') + QuotedString('"'))), adjacent=False)

pp_quoted.setParseAction(protectUnescapedCharacters)
pp_comment = Literal('//') + SkipTo(lineEnd)

pp_default_value = QuotedString('"') | pp_nums

pp_EntityPropertyChoiceValue = pp_nums.setParseAction(tokenMap(int)) | pp_quoted

pp_EntityPropertyChoice = pp_EntityPropertyChoiceValue\
    .setResultsName('value') + ':' + QuotedString('"')\
    .setResultsName('display_name') + Optional(Suppress(pp_comment))

pp_EntityPropertyChoices = Suppress('[') + \
    Optional(OneOrMore(
        pp_EntityPropertyChoice
        .setParseAction(lambda toks: FgdEntityPropertyChoice(**toks)))
    .setResultsName('choices')) + Suppress(']')

pp_EntitySpawnflag = pp_nums.setResultsName('value')\
                            .setParseAction(tokenMap(int)) + \
    ':' + QuotedString('"').setResultsName('display_name') + \
    ':' + pp_nums.setResultsName('default_value')\
                 .setParseAction(lambda toks: bool(int(toks[0].strip('"')))) + \
    Optional(Suppress(pp_comment))
pp_EntitySpawnflag.setParseAction(lambda toks: FgdEntitySpawnflag(**toks))

pp_EntitySpawnflags = Suppress(CaselessLiteral('spawnflags') + '(' +
                               CaselessLiteral('flags') + ')' + '=' + '[') + \
    Optional(OneOrMore(pp_EntitySpawnflag).setResultsName('spawnflags')) + \
    Suppress(']')

# Property parsers
pp_property_name = pp_name.setResultsName('name')
pp_property_value_type = pp_name.setResultsName('value_type')
pp_property_readonly = Literal('readonly').setParseAction(
    bool).setResultsName('readonly')
pp_property_display_name = Optional(pp_quoted.setResultsName('display_name'))
pp_property_default = Optional(pp_default_value.setResultsName('default_value'))
pp_description = Optional(pp_quoted.setResultsName('description'))


pp_EntityProperty = pp_property_name + '(' + pp_property_value_type + ')' + \
    Optional(pp_property_readonly) + \
    Optional(':' + pp_property_display_name) + \
    Optional(':' + pp_property_default) + \
    Optional(':' + pp_description) + \
    Optional('=' + pp_EntityPropertyChoices)
pp_EntityProperty.setParseAction(
    lambda toks: FgdEntityProperty(**toks.asDict()))


pp_EntityInput = Literal('input') + pp_property_name + \
    '(' + pp_property_value_type + ')' + ':' + pp_description
pp_EntityInput.setParseAction(lambda toks: FgdEntityInput(**toks))

pp_EntityOutput = Literal('output') + pp_property_name + \
    '(' + pp_property_value_type + ')' + ':' + pp_description
pp_EntityOutput.setParseAction(lambda toks: FgdEntityOutput(**toks))

pp_properties = Suppress(pp_comment) | \
    pp_EntityInput | pp_EntityOutput | pp_EntitySpawnflags | pp_EntityProperty

pp_EntityProperties = Suppress('[') + \
    Optional(OneOrMore(pp_properties).setResultsName('properties_and_io')) + \
    Suppress(']')


# Entity parsers

def make_Entity(entity_data):
    dataDict = entity_data.asDict()
    if 'definitions' not in dataDict:
        dataDict['definitions'] = []
    if 'properties_and_io' in dataDict:
        dataDict['inputs'] = []
        dataDict['outputs'] = []
        dataDict['properties'] = []
        for pio in dataDict.pop('properties_and_io'):
            if isinstance(pio, FgdEntityInput):
                dataDict['inputs'].append(pio)
            if isinstance(pio, FgdEntityOutput):
                dataDict['outputs'].append(pio)
            if isinstance(pio, FgdEntityProperty):
                dataDict['properties'].append(pio)
    entity = FgdEntity(**dataDict)
    return entity


pp_entity_class_type = pp_name.setResultsName('class_type')
pp_entity_name = pp_name.setResultsName('name')
pp_entity_description = Optional(':' + pp_description)

pp_entity_definition_arg = pp_value | pp_name | QuotedString(
    '"', unquoteResults=False)
pp_entity_definition_args = Optional(delimitedList(
    pp_entity_definition_arg))

pp_entity_definition = pp_name.setResultsName('name') + \
    Optional(Suppress('(') + pp_entity_definition_args +
             Suppress(')')).setResultsName('args')

pp_entity_definitions = Optional(OneOrMore(
    pp_entity_definition
    .setParseAction(lambda toks: dict(**toks.asDict())))) \
    .setResultsName('definitions')

pp_entity = Suppress('@') + pp_entity_class_type + \
    pp_entity_definitions + '=' + pp_entity_name + \
    pp_entity_description + pp_EntityProperties
pp_entity.setParseAction(make_Entity)


# Editor data parsers
pp_include = Literal('@') + Literal('include').setResultsName('class_type') + \
    pp_quoted.setResultsName('data')
pp_include.setParseAction(lambda toks: FgdEditorData(**toks))

pp_mapsize_data = (pp_nums + Suppress(',') + pp_nums)\
    .setParseAction(lambda s, l, toks: tuple(toks.asList()))

pp_mapsize = Literal('@') + \
    Literal('mapsize').setResultsName('class_type') + \
    (Suppress('(') + pp_mapsize_data + Suppress(')'))\
    .setParseAction(lambda toks: tuple(toks)).setResultsName('data')
pp_mapsize.setParseAction(lambda toks: FgdEditorData(**toks))

pp_material_ex_data = OneOrMore(QuotedString('"'))
pp_material_ex = Literal('@') + \
    Literal('MaterialExclusion').setResultsName('class_type') + \
    Suppress(
    '[') + Optional(pp_material_ex_data).setResultsName('data') + Suppress(']')
pp_material_ex.setParseAction(lambda toks: FgdEditorData(**toks.asDict()))

pp_autovisgroup_data_list = QuotedString('"').setResultsName('key') + \
    Suppress('[') + \
    Optional(OneOrMore(QuotedString('"'))).setResultsName('value') + \
    Suppress(']')

pp_autovisgroup_data = Suppress('[') + Optional(OneOrMore(
    pp_autovisgroup_data_list
    .setParseAction(lambda toks: (toks['key'], toks['value'].asList()))))\
    .setParseAction(lambda toks: dict(toks.asList()))\
    .setResultsName('data') + Suppress(']')
pp_autovisgroup = Literal('@') + \
    Literal('AutoVisGroup').setResultsName('class_type') + \
    Literal('=') + pp_quoted.setResultsName('name') + pp_autovisgroup_data
pp_autovisgroup.setParseAction(lambda toks: FgdEditorData(**toks.asDict()))

pp_fgd = OneOrMore(pp_mapsize | pp_include | pp_material_ex |
                   pp_autovisgroup | pp_entity).ignore(pp_comment)


def FgdParse(filename):
    """Parse a .fgd file and return a FGD object
    :param filename: A path to the .fgd file to be parsed
    :type filename: string
    :return: a FGD object
    :rtype: FGD
    """

    game_data = Fgd()

    filepath = os.path.abspath(filename)
    filedir = os.path.dirname(filepath)

    try:
        f = open(filename, "r", encoding="iso-8859-1")
        results = pp_fgd.parseFile(f)
        f.close()
    except Exception as e:
        raise

    for i in results:
        if isinstance(i, FgdEditorData):
            if i.class_type == 'include':
                include_path = os.path.join(filedir, i.data)
                base_game_data = FgdParse(include_path)
                game_data.add_include(base_game_data)
            game_data.add_editor_data(i)
    for i in results:
        if isinstance(i, FgdEntity):
            game_data.add_entity(i)

    return game_data
