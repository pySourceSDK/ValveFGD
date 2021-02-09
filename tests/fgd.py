import unittest
from valvefgd.fgd import *
from faker import Faker
from faker.providers import BaseProvider

fake = Faker()


class Provider(BaseProvider):

    def classType(self):
        class_types = ['BaseClass', 'PointClass', 'SolidClass',
                       'KeyFrameClass', 'MoveClass', 'FilterClass']
        return class_types[fake.random_int(0, len(class_types)-1)]

    def ioValueType(self):
        io_value_types = ['integer', 'void', 'bool', 'string', 'color255',
                          'float', 'target_destination', 'vector']
        return io_value_types[fake.random_int(0, len(io_value_types)-1)]

    def propertyValueType(self):
        property_value_types = ["angle", "origin", "studio", "integer", "float",
                                "choices", "target_source", "target_destination",
                                "color255", "string", "node_dest", "filterclass",
                                "sound", "sprite", "vector", "decal", "sidelist",
                                "material", "vecline", "angle_negative_pitch",
                                "axis", "instance_file", "instance_variable",
                                "instance_parm"]
        type_index = fake.random_int(0, len(property_value_types)-1)
        return property_value_types[type_index]

    def classDef(self):
        entity_def_names = ['base', 'color', 'iconsprite', 'sphere', 'studio',
                            'sweptplayerhull', 'size', 'line', 'studioprop',
                            'sprite', 'decal', 'overlay', 'sidelist',
                            'overlay_transition', 'wirebox', 'light',
                            'lightprop', 'lightcone', 'keyframe', 'animator',
                            'halfgridsnap', 'quadbounds', 'cylinder',
                            'frustum', 'instance']
        classdef = {}
        name = entity_def_names[fake.random_int(0, len(entity_def_names)-1)]
        classdef['name'] = name
        classdef['args'] = ['parameter1', '"parameter2"', '0 0 0']
        return classdef

    def editorClassDef(self):
        editor_data_types = ['MaterialExclusion', 'AutoVisGroup', 'mapsize']
        type_index = fake.random_int(0, len(editor_data_types)-1)
        return editor_data_types[type_index]


fake.add_provider(Provider)

suffix = 0


class FgdProvider(BaseProvider):

    def FgdEditorData(self):
        return FgdEditorData(
            class_type=fake.editorClassDef())

    def FgdEntity(self, name=None):
        ++suffix
        return FgdEntity(
            class_type=fake.classType(),
            definitions=[],
            name=name or (fake.first_name() + str(suffix)),
            description=fake.text(max_nb_chars=40))

    def FgdEntitySpawnflag(self, value=None):
        if not value:
            value = fake.random_int(min=0, max=100)
        return FgdEntitySpawnflag(
            value=value,
            display_name=fake.text(max_nb_chars=40),
            default_value=fake.pybool())

    def FgdEntityInput(self, name=None):
        ++suffix
        return FgdEntityInput(
            name=name or (fake.first_name() + str(suffix)),
            value_type=fake.ioValueType(),
            description=fake.text(max_nb_chars=40))

    def FgdEntityOutput(self, name=None):
        ++suffix
        return FgdEntityOutput(
            name=name or (fake.first_name() + str(suffix)),
            value_type=fake.ioValueType(),
            description=fake.text(max_nb_chars=40))

    def FgdEntityProperty(self, name=None):
        ++suffix
        return FgdEntityProperty(
            name=name or (fake.first_name() + str(suffix)),
            value_type=fake.propertyValueType(),
            readonly=fake.pybool(),
            display_name=fake.text(max_nb_chars=25),
            default_value=fake.random_int(0, 100),
            description=fake.text(max_nb_chars=40))

    def FgdEntityPropertyChoice(self):
        return FgdEntityPropertyChoice(
            value=fake.random_int(min=0, max=100),
            display_name=fake.text(max_nb_chars=40))


fake.add_provider(FgdProvider)


class FgdTestCase(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def testFgd(self):
        fgd = Fgd()
        entities = []
        for i in range(0, 10):
            entities.append(fake.FgdEntity(fake.first_name() + str(i)))
        for ent in entities:
            fgd.add_entity(ent)
        for ent in entities:
            self.assertTrue(ent in fgd.entities)
        self.assertEqual(len(entities), len(fgd.entities))

        self.assertRaises(EntityNotFound, fgd.entity_by_name,
                          'likely not a name')
        for ent in entities:
            resultEnt = fgd.entity_by_name(ent.name)
            self.assertEqual(ent, resultEnt)

    def testFgdIncludes(self):
        grandpa_fgd = Fgd()
        papa_fgd = Fgd()
        moma_fgd = Fgd()
        fgd = Fgd()
        self.assertEqual(0, len(fgd.includes))
        fgd.add_include(None)
        self.assertEqual(0, len(fgd.includes))
        papa_fgd.add_include(grandpa_fgd)
        fgd.add_include(papa_fgd)
        fgd.add_include(moma_fgd)

        self.assertEqual(0, len(fgd.entities))
        fgd.add_entity(None)
        self.assertEqual(0, len(fgd.entities))

        self.assertEqual(0, len(fgd.editor_data))
        fgd.add_editor_data(None)
        self.assertEqual(0, len(fgd.editor_data))

        for i in range(0, 5):
            grandpa_fgd.add_entity(fake.FgdEntity())
        for i in range(0, 10):
            papa_fgd.add_entity(fake.FgdEntity())
        for i in range(0, 10):
            moma_fgd.add_entity(fake.FgdEntity())

        for i in range(0, 2):
            grandpa_fgd.add_editor_data(fake.FgdEditorData())
        for i in range(0, 3):
            papa_fgd.add_editor_data(fake.FgdEditorData())
        papa_fgd.add_editor_data(FgdEditorData('include', "grandpa.fgd"))
        for i in range(0, 3):
            moma_fgd.add_editor_data(fake.FgdEditorData())

        self.assertEqual(25, len(fgd.entities))
        self.assertEqual(9, len(fgd.editor_data))

        for i in range(0, 15):
            fgd.add_entity(fake.FgdEntity())
        for i in range(0, 4):
            fgd.add_editor_data(fake.FgdEditorData())
        fgd.add_editor_data(FgdEditorData('include', "papa.fgd"))

        self.assertEqual(40, len(fgd.entities))
        self.assertEqual(14, len(fgd.editor_data))

        expected_grandpa_repr = "<Fgd {'includes': [0], 'entities': [5], 'editor_data': [2]}>"
        self.assertEqual(expected_grandpa_repr, repr(grandpa_fgd))
        expected_papa_repr = "<Fgd {'includes': [1], 'entities': [15], 'editor_data': [6]}>"
        self.assertEqual(expected_papa_repr, repr(papa_fgd))
        expected_fgd_repr = "<Fgd {'includes': [3], 'entities': [40], 'editor_data': [14]}>"
        self.assertEqual(expected_fgd_repr, repr(fgd))

        # uncollapsed fgd_str

        expected_grandpa_fgd = ""
        for editor_data in grandpa_fgd._editor_data:
            expected_grandpa_fgd += editor_data.fgd_str()+'\n\n'
        for entity in grandpa_fgd._entities:
            expected_grandpa_fgd += entity.fgd_str()+'\n\n'
        self.assertEqual(expected_grandpa_fgd, grandpa_fgd.fgd_str())

        expected_papa_fgd = ""
        for editor_data in papa_fgd._editor_data:
            expected_papa_fgd += editor_data.fgd_str()+'\n\n'
        for entity in papa_fgd._entities:
            expected_papa_fgd += entity.fgd_str()+'\n\n'
        self.assertEqual(expected_papa_fgd, papa_fgd.fgd_str())

        expected_fgd = ""
        for editor_data in fgd._editor_data:
            expected_fgd += editor_data.fgd_str()+'\n\n'
        for entity in fgd._entities:
            expected_fgd += entity.fgd_str()+'\n\n'
        self.assertEqual(expected_fgd, fgd.fgd_str())

        # collapsed fgd_str
        expected_grandpa_fgd = ""
        for editor_data in grandpa_fgd.editor_data:
            if editor_data.class_type != 'include':
                expected_grandpa_fgd += editor_data.fgd_str()+'\n\n'
        for entity in grandpa_fgd.entities:
            expected_grandpa_fgd += entity.fgd_str()+'\n\n'
        self.assertEqual(expected_grandpa_fgd, grandpa_fgd.fgd_str(True))

        expected_papa_fgd = ""
        for editor_data in papa_fgd.editor_data:
            if editor_data.class_type != 'include':
                expected_papa_fgd += editor_data.fgd_str()+'\n\n'
        for entity in papa_fgd.entities:
            expected_papa_fgd += entity.fgd_str()+'\n\n'
        self.assertEqual(expected_papa_fgd, papa_fgd.fgd_str(True))

        expected_fgd = ""
        for editor_data in fgd.editor_data:
            if editor_data.class_type != 'include':
                expected_fgd += editor_data.fgd_str()+'\n\n'
        for entity in fgd.entities:
            expected_fgd += entity.fgd_str()+'\n\n'
        self.assertEqual(expected_fgd, fgd.fgd_str(True))

    def test_entity_inheritance(self):
        grandpapa_fgd = Fgd()
        papa_fgd = Fgd()
        papa_fgd.add_include(grandpapa_fgd)
        fgd = Fgd()
        fgd.add_include(papa_fgd)

        grandpapa_env = FgdEntity('PointClass',
                                  [{'name': 'base', 'args': ['deadpapa']}],
                                  'grandpa_env', '')
        grandpapa_fgd.add_entity(grandpapa_env)

        grandpapa_fire = FgdEntity('PointClass', [], 'grandpa_fire', '')
        grandpapa_fgd.add_entity(grandpapa_fire)

        papa_env_fire = FgdEntity('PointClass',
                                  [{'name': 'papa_things', 'args': ['not really']},
                                   {'name': 'base',
                                    'args': ['grandpa_env', 'grandpa_fire']}],
                                  'papa_env_fire', '')
        papa_fgd.add_entity(papa_env_fire)
        env_fire = FgdEntity('PointClass',
                             [{'name': 'base',
                               'args': ['papa_env_fire']}],
                             'env_fire')
        papa_fgd.add_entity(env_fire)

        self.assertEqual(0, len(grandpapa_env.parents))
        self.assertEqual(0, len(grandpapa_fire.parents))
        self.assertTrue(grandpapa_env in papa_env_fire.parents)
        self.assertTrue(grandpapa_fire in papa_env_fire.parents)
        self.assertEqual(2, len(papa_env_fire.parents))
        self.assertEqual(1, len(env_fire.parents))
        self.assertTrue(papa_env_fire in env_fire.parents)

    def test_entity_inherited_content(self):

        # vestigial
        vestigial = FgdEntity('PointClass', [], 'vestigial',
                              'should be included, it is recursive')
        vestigial._properties = [fake.FgdEntityProperty('0')]
        vestigial._inputs = [fake.FgdEntityInput('0')]
        vestigial._outputs = [fake.FgdEntityOutput('0')]
        vestigial._spawnflags = [fake.FgdEntitySpawnflag(1000)]

        # env
        env = FgdEntity('PointClass',
                        [{'name': 'base', 'args': ['vestigial']}],
                        'env', "it's")
        env._parents = [vestigial]
        env._properties = [fake.FgdEntityProperty('1'), fake.FgdEntityProperty('2'),
                           fake.FgdEntityProperty('3')]
        env._inputs = [fake.FgdEntityInput('1'), fake.FgdEntityInput('larry'),
                       fake.FgdEntityInput('2'), fake.FgdEntityInput('garry')]
        env._outputs = [fake.FgdEntityOutput()]
        env._spawnflags = [fake.FgdEntitySpawnflag(1),
                           fake.FgdEntitySpawnflag(4)]

        # fire
        fire = FgdEntity('PointClass',
                         [{'name': 'base', 'args': ['vestigial']}],
                         'fire', "hot")
        fire._properties = [fake.FgdEntityProperty('1'),
                            fake.FgdEntityProperty('5')]
        fire._inputs = [fake.FgdEntityInput('3'), fake.FgdEntityInput('larry')]
        fire._outputs = [fake.FgdEntityOutput(), fake.FgdEntityOutput()]
        fire._spawnflags = [fake.FgdEntitySpawnflag(4), fake.FgdEntitySpawnflag(5),
                            fake.FgdEntitySpawnflag(6)]

        # env_fire
        env_fire = FgdEntity('PointClass',
                             [{'name': 'base', 'args': ['env', 'fire']}],
                             'env_fire', "it's pretty hot")
        env_fire._parents = [env, fire]
        env_fire._properties = [fake.FgdEntityProperty('2')]
        env_fire._inputs = [fake.FgdEntityInput('4'), fake.FgdEntityInput('5'),
                            fake.FgdEntityInput('garry')]
        env_fire._outputs = [fake.FgdEntityOutput(), fake.FgdEntityOutput(),
                             fake.FgdEntityOutput()]
        env_fire._spawnflags = [fake.FgdEntitySpawnflag(10)]

        # properties
        self.assertEqual(5, len(env_fire.properties))
        for p in env_fire._properties:
            self.assertTrue(p in env_fire.properties)
        for p in env._properties:
            if p.name != '2' and p.name != '1':
                self.assertTrue(p in env_fire.properties)
        for p in fire._properties:
            self.assertTrue(p in env_fire.properties)
        for p in vestigial._properties:
            self.assertTrue(p in env_fire.properties)

        # inputs
        self.assertEqual(8, len(env_fire.inputs))
        for i in env_fire._inputs:
            if i.name != 'garry':
                self.assertTrue(i in env_fire.inputs)
        for i in env._inputs:
            self.assertTrue(i in env_fire.inputs)
        for i in fire._inputs:
            if i.name != 'larry':
                self.assertTrue(i in env_fire.inputs)
        for i in vestigial._inputs:
            self.assertTrue(i in env_fire.inputs)

        # outputs
        self.assertEqual(7, len(env_fire.outputs))
        for o in env_fire._outputs:
            self.assertTrue(o in env_fire.outputs)
        for o in env.outputs:
            self.assertTrue(o in env_fire.outputs)
        for o in fire.outputs:
            self.assertTrue(o in env_fire.outputs)

        # spawnflags
        self.assertEqual(4, len(env_fire.spawnflags))
        for sf in env_fire._spawnflags:
            self.assertTrue(sf in env_fire.spawnflags)
        for sf in env.spawnflags:
            self.assertTrue(sf in env_fire.spawnflags)
        for sf in fire.spawnflags:
            self.assertTrue(sf not in env_fire.spawnflags)
        for sf in vestigial.spawnflags:
            self.assertTrue(sf in env_fire.spawnflags)

    # FgdEntityProperty

    def test_entity_properties(self):
        class_type = 'PointClass'
        definitions = []
        name = 'env_fire'
        description = 'an entity description'
        properties = []
        spawnflags = []
        inputs = []
        outputs = []

        entity = FgdEntity(class_type, definitions, name, description,
                           properties, spawnflags, inputs, outputs)
        self.assertEqual(entity.class_type, class_type)
        self.assertEqual(entity.definitions, definitions)
        self.assertEqual(entity.name, name)
        self.assertEqual(entity.description, description)

        self.assertEqual(entity.inputs, inputs)
        self.assertEqual(entity.outputs, outputs)
        self.assertEqual(entity.properties, properties)
        self.assertEqual(entity.spawnflags, spawnflags)

        base_entity = FgdEntity(class_type, definitions, name, description)
        self.assertEqual(base_entity.class_type, class_type)
        self.assertEqual(base_entity.definitions, definitions)
        self.assertEqual(base_entity.name, name)
        self.assertEqual(base_entity.description, description)

        self.assertEqual(base_entity.inputs, [])
        self.assertEqual(base_entity.outputs, [])
        self.assertEqual(base_entity.properties, [])
        self.assertEqual(base_entity.spawnflags, [])

    def test_entity_searches(self):
        properties = [fake.FgdEntityProperty('p1'),
                      fake.FgdEntityProperty('p2'),
                      fake.FgdEntityProperty('p3'),
                      fake.FgdEntityProperty('p4')]
        spawnflags = [fake.FgdEntitySpawnflag('s1'),
                      fake.FgdEntitySpawnflag('s2'),
                      fake.FgdEntitySpawnflag('s3'),
                      fake.FgdEntitySpawnflag('s4')]
        inputs = [fake.FgdEntityInput('i1'), fake.FgdEntityInput('i2'),
                  fake.FgdEntityInput('i3'), fake.FgdEntityInput('i4')]
        outputs = [fake.FgdEntityOutput('01'), fake.FgdEntityOutput('o2'),
                   fake.FgdEntityOutput('o3'), fake.FgdEntityOutput('o4')]
        entity = fake.FgdEntity()
        entity._properties = properties
        entity._spawnflags = spawnflags
        entity._inputs = inputs
        entity._outputs = outputs

        property = entity.property_by_name(properties[2].name)
        self.assertEqual(property, properties[2])
        self.assertRaises(PropertyNotFound, entity.property_by_name, 404)

        spawnflag = entity.spawnflag_by_value(spawnflags[2].value)
        self.assertEqual(spawnflag, spawnflags[2])
        self.assertRaises(SpawnflagNotFound,
                          entity.spawnflag_by_value, 'a string')

        input = entity.input_by_name(inputs[2].name)
        self.assertEqual(input, inputs[2])
        self.assertRaises(InputNotFound, entity.input_by_name, 404)

        output = entity.output_by_name(outputs[2].name)
        self.assertEqual(output, outputs[2])
        self.assertRaises(OutputNotFound, entity.output_by_name, 404)

    def test_entity_schemas(self):
        class_type = 'PointClass'
        definitions = []
        name = 'env_fire'
        description = 'an entity description'
        properties = []
        spawnflags = []
        inputs = []
        outputs = []
        definitions = [fake.classDef(), fake.classDef(), fake.classDef()]
        properties = [fake.FgdEntityProperty('p1'),
                      fake.FgdEntityProperty('p2'),
                      fake.FgdEntityProperty('p3'),
                      fake.FgdEntityProperty('p4'),
                      fake.FgdEntityProperty('p5'),
                      fake.FgdEntityProperty('p6')]
        spawnflags = [fake.FgdEntitySpawnflag('s1'),
                      fake.FgdEntitySpawnflag('s2'),
                      fake.FgdEntitySpawnflag('s3'),
                      fake.FgdEntitySpawnflag('s4'),
                      fake.FgdEntitySpawnflag('s5')]
        inputs = [fake.FgdEntityInput('i1'), fake.FgdEntityInput('i2')]
        outputs = [fake.FgdEntityOutput('o1'), fake.FgdEntityOutput('o2'),
                   fake.FgdEntityOutput('o3')]
        entity = FgdEntity(class_type, definitions, name, description,
                           properties, spawnflags, inputs, outputs)

        self.assertEqual(len(inputs), len(entity.inputs_schema))
        self.assertEqual(len(outputs), len(entity.outputs_schema))
        self.assertEqual(len(properties) + 2, len(entity.properties_schema))
        self.assertEqual(len(spawnflags), len(entity.spawnflags_schema))
        self.assertEqual(inputs[0].schema, entity.inputs_schema[0])
        self.assertEqual(outputs[0].schema, entity.outputs_schema[0])
        self.assertEqual(properties[0].schema, entity.properties_schema[0])
        self.assertEqual(spawnflags[0].schema, entity.spawnflags_schema[0])

        self.assertEqual(entity.name, entity.schema['name'])
        self.assertEqual(entity.definitions, entity.schema['definitions'])
        self.assertEqual(entity.class_type, entity.schema['class_type'])
        self.assertEqual(entity.properties_schema, entity.schema['properties'])
        self.assertEqual(entity.inputs_schema, entity.schema['inputs'])
        self.assertEqual(entity.outputs_schema, entity.schema['outputs'])
        self.assertEqual(entity.spawnflags_schema, entity.schema['spawnflags'])

    def test_entity_repr_and_fgd_str(self):
        class_type = 'PointClass'
        definitions = []
        name = 'env_fire'
        description = 'an entity description'
        properties = []
        spawnflags = []
        inputs = []
        outputs = []
        entity = FgdEntity(class_type, definitions, name, description,
                           properties, spawnflags, inputs, outputs)
        entity2 = FgdEntity(class_type, definitions, name, description)
        expected_repr = "<FgdEntity {'type': 'PointClass', " + \
            "'name': 'env_fire', " + \
            "'description': 'an entity description', [...]}>"
        expected_fgd_str = '@PointClass = env_fire : "an entity description" []'

        self.assertEqual(repr(entity), expected_repr)
        self.assertEqual(entity.fgd_str(), expected_fgd_str)
        self.assertEqual(repr(entity2), expected_repr)
        self.assertEqual(entity2.fgd_str(), expected_fgd_str)

        definitions = [fake.classDef(), fake.classDef(), fake.classDef()]
        properties = [fake.FgdEntityProperty(), fake.FgdEntityProperty(),
                      fake.FgdEntityProperty(), fake.FgdEntityProperty()]
        spawnflags = [fake.FgdEntitySpawnflag(), fake.FgdEntitySpawnflag(),
                      fake.FgdEntitySpawnflag(), fake.FgdEntitySpawnflag()]
        inputs = [fake.FgdEntityInput(), fake.FgdEntityInput(),
                  fake.FgdEntityInput(), fake.FgdEntityInput()]
        outputs = [fake.FgdEntityOutput(), fake.FgdEntityOutput(),
                   fake.FgdEntityOutput(), fake.FgdEntityOutput()]
        entity3 = FgdEntity(class_type, definitions, name, description,
                            properties, spawnflags, inputs, outputs)
        expected_repr = "<FgdEntity {'type': 'PointClass', " + \
            "'name': 'env_fire', " + \
            "'description': 'an entity description', [...]}>"
        expected_fgd_str = '@PointClass '
        for defo in definitions:
            expected_fgd_str += defo['name'] + '('
            for arg in defo['args']:
                expected_fgd_str += arg + ', '
            expected_fgd_str = expected_fgd_str.rstrip(', ') + ') '

        expected_fgd_str += '= env_fire : "an entity description"\n['
        for p in properties:
            expected_fgd_str += '\n\t' + p.fgd_str()

        expected_fgd_str += '\n\tspawnflags(flags) =\n\t['
        for s in spawnflags:
            expected_fgd_str += '\n\t\t' + s.fgd_str()
        expected_fgd_str += '\n\t]'
        for i in inputs:
            expected_fgd_str += '\n\t' + i.fgd_str()
        for o in outputs:
            expected_fgd_str += '\n\t' + o.fgd_str()
        expected_fgd_str += '\n]'
        self.assertEqual(repr(entity3), expected_repr)
        self.assertEqual(entity3.fgd_str(), expected_fgd_str)

    def test_property_properties(self):
        name = 'targetname'
        value_type = 'integer'
        readonly = True
        display_name = 'Target Name'
        default_value = '1'
        description = 'short desc1'
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description)
        self.assertEqual(property.name, name)
        self.assertEqual(property.value_type, value_type)
        self.assertEqual(property.readonly, readonly)
        self.assertEqual(property.display_name, display_name)
        self.assertEqual(property.default_value, default_value)
        self.assertEqual(property.description, description)
        self.assertEqual(property.choices, None)

    def test_property_properties_with_choices(self):
        name = 'targetname'
        value_type = 'choices'
        readonly = True
        display_name = 'Target Name'
        default_value = '1'
        description = 'short desc1'
        choice1 = FgdEntityPropertyChoice(1, 'first choice')
        choice2 = FgdEntityPropertyChoice(2, 'second choice')
        choice3 = FgdEntityPropertyChoice(3, 'third choice')
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description,
                                     [choice1, choice2, choice3])
        self.assertEqual(property.name, name)
        self.assertEqual(property.value_type, value_type)
        self.assertEqual(property.readonly, readonly)
        self.assertEqual(property.display_name, display_name)
        self.assertEqual(property.default_value, default_value)
        self.assertEqual(property.description, description)
        self.assertEqual(len(property.choices), 3)

    def test_property_choice_by_name(self):
        name = 'targetname'
        value_type = 'integer'
        readonly = True
        display_name = 'Target Name'
        default_value = 1
        description = 'short desc1'
        choice1 = FgdEntityPropertyChoice(1, 'first choice')
        choice2 = FgdEntityPropertyChoice(2, 'second choice')
        choice3 = FgdEntityPropertyChoice(3, 'third choice')
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description,
                                     [choice1, choice2, choice3])
        self.assertRaises(ChoiceNotFound, property.choice_by_value, 1)
        self.assertRaises(ChoiceNotFound, property.choice_by_value, 2)
        self.assertRaises(ChoiceNotFound, property.choice_by_value, 3)
        self.assertRaises(ChoiceNotFound, property.choice_by_value, 4)

        name = 'targetname'
        value_type = 'choices'
        readonly = True
        display_name = 'Target Name'
        default_value = 1
        description = 'short desc1'
        choice1 = FgdEntityPropertyChoice(1, 'first choice')
        choice2 = FgdEntityPropertyChoice(2, 'second choice')
        choice3 = FgdEntityPropertyChoice(3, 'third choice')
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description,
                                     [choice1, choice2, choice3])
        self.assertEqual(property.choice_by_value(1), choice1)
        self.assertEqual(property.choice_by_value(2), choice2)
        self.assertEqual(property.choice_by_value(3), choice3)
        self.assertRaises(ChoiceNotFound, property.choice_by_value, 4)

    def test_property_schema(self):
        name = 'targetname'
        value_type = 'integer'
        readonly = True
        display_name = 'Target Name'
        default_value = '1'
        description = 'short desc1'
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description)
        self.assertEqual(property.schema['name'], name)
        self.assertEqual(property.schema['type'], value_type)
        self.assertEqual(property.schema['readonly'], readonly)
        self.assertEqual(property.schema['display_name'], display_name)
        self.assertEqual(property.schema['default_value'], default_value)
        self.assertEqual(property.schema['description'], description)
        self.assertFalse('choices' in property.schema)

    def test_property_schema_with_choices(self):
        name = 'targetname'
        value_type = 'integer'
        readonly = True
        display_name = 'Target Name'
        default_value = '1'
        description = 'short desc1'
        choice1 = FgdEntityPropertyChoice(1, 'first choice')
        choice2 = FgdEntityPropertyChoice(2, 'second choice')
        choice3 = FgdEntityPropertyChoice(3, 'third choice')
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description,
                                     [choice1, choice2, choice3])
        self.assertEqual(property.schema['name'], name)
        self.assertEqual(property.schema['type'], value_type)
        self.assertEqual(property.schema['readonly'], readonly)
        self.assertEqual(property.schema['display_name'], display_name)
        self.assertEqual(property.schema['default_value'], default_value)
        self.assertEqual(property.schema['description'], description)
        self.assertTrue('choices' not in property.schema)

        name = 'targetname'
        value_type = 'choices'
        readonly = True
        display_name = 'Target Name'
        default_value = '1'
        description = 'short desc1'
        choice1 = FgdEntityPropertyChoice(1, 'first choice')
        choice2 = FgdEntityPropertyChoice(2, 'second choice')
        choice3 = FgdEntityPropertyChoice(3, 'third choice')
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description,
                                     [choice1, choice2, choice3])
        self.assertEqual(property.schema['name'], name)
        self.assertEqual(property.schema['type'], value_type)
        self.assertEqual(property.schema['readonly'], readonly)
        self.assertEqual(property.schema['display_name'], display_name)
        self.assertEqual(property.schema['default_value'], default_value)
        self.assertEqual(property.schema['description'], description)
        self.assertTrue('choices' in property.schema)
        self.assertEqual(len(property.schema['choices']), 3)
        self.assertEqual(property.schema['choices'][0], choice1.schema)
        self.assertEqual(property.schema['choices'][1], choice2.schema)
        self.assertEqual(property.schema['choices'][2], choice3.schema)

    def test_property_repr(self):
        name = 'targetname'
        value_type = 'integer'
        readonly = True
        display_name = 'Target Name'
        default_value = '1'
        description = 'short desc1'
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description)
        expected = "<FgdEntityProperty {'name': 'targetname', " + \
                   "'value_type': 'integer', " + \
                   "'description': 'short desc1', [...]}>"
        self.assertEqual(repr(property), expected)

    def test_property_fgd_str(self):
        name = 'targetname'
        value_type = 'integer'
        readonly = True
        display_name = 'Target Name'
        default_value = '1'
        description = 'short desc1'
        choice1 = FgdEntityPropertyChoice(1, 'first choice')
        choice2 = FgdEntityPropertyChoice(2, 'second choice')
        choice3 = FgdEntityPropertyChoice(3, 'third choice')
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description,
                                     [choice1, choice2, choice3])
        expected = 'targetname(integer) readonly : ' + \
                   '"Target Name" : "1" : "short desc1"'
        self.assertEqual(property.fgd_str(), expected)

        name = 'targetname'
        value_type = 'integer'
        readonly = False
        display_name = None
        default_value = None
        description = 'short desc1'
        choice1 = FgdEntityPropertyChoice(1, 'first choice')
        choice2 = FgdEntityPropertyChoice(2, 'second choice')
        choice3 = FgdEntityPropertyChoice(3, 'third choice')
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description,
                                     [choice1, choice2, choice3])
        expected = 'targetname(integer) : : : "short desc1"'
        self.assertEqual(property.fgd_str(), expected)

    def test_property_with_choices_fgd_str(self):
        name = 'targetname'
        value_type = 'choices'
        readonly = False
        display_name = 'Target Name'
        default_value = 1
        description = 'short desc1'
        choice1 = FgdEntityPropertyChoice(1, 'first choice')
        choice2 = FgdEntityPropertyChoice(2, 'second choice')
        choice3 = FgdEntityPropertyChoice(3, 'third choice')
        property = FgdEntityProperty(name, value_type, readonly, display_name,
                                     default_value, description,
                                     [choice1, choice2, choice3])
        expected = 'targetname(choices) : "Target Name" : 1 : "short desc1" ='
        expected += '\n\t['
        expected += '\n\t\t' + choice1.fgd_str()
        expected += '\n\t\t' + choice2.fgd_str()
        expected += '\n\t\t' + choice3.fgd_str()
        expected += '\n\t]'
        self.assertEqual(property.fgd_str(), expected)

    # FgdEntityInput
    def test_input_properties(self):
        name = 'onuser1'
        value_type = 'void'
        description = 'short desc1'
        input = FgdEntityInput(name, value_type, description)
        self.assertEqual(input.name, name)
        self.assertEqual(input.value_type, value_type)
        self.assertEqual(input.description, description)

    def test_input_schema(self):
        name = 'onuser2'
        value_type = 'void'
        description = 'short desc2'
        input = FgdEntityInput(name, value_type, description)
        self.assertEqual(input.schema['name'], name)
        self.assertEqual(input.schema['type'], value_type)
        self.assertEqual(input.schema['description'], description)

    def test_input_fgd_str(self):
        name = 'onuser3'
        value_type = 'void'
        description = 'short desc3'
        input = FgdEntityInput(name, value_type, description)
        expected = 'input onuser3(void) : "short desc3"'
        self.assertEqual(input.fgd_str(), expected)

    def test_input_repr(self):
        name = 'onuser4'
        value_type = 'void'
        description = 'short desc4'
        input = FgdEntityInput(name, value_type, description)
        expected = "<FgdEntityInput {'name': 'onuser4', " + \
                   "'value_type': 'void', " + \
                   "'description': 'short desc4'}>"
        self.assertEqual(repr(input), expected)

    # FgdEntityOutput
    def test_output_properties(self):
        name = 'onuser1'
        value_type = 'void'
        description = 'short desc1'
        output = FgdEntityOutput(name, value_type, description)
        self.assertEqual(output.name, name)
        self.assertEqual(output.value_type, value_type)
        self.assertEqual(output.description, description)

    def test_output_schema(self):
        name = 'onuser2'
        value_type = 'void'
        description = 'short desc2'
        output = FgdEntityOutput(name, value_type, description)
        self.assertEqual(output.schema['name'], name)
        self.assertEqual(output.schema['type'], value_type)
        self.assertEqual(output.schema['description'], description)

    def test_output_fgd_str(self):
        name = 'onuser3'
        value_type = 'void'
        description = 'short desc3'
        output = FgdEntityOutput(name, value_type, description)
        expected = 'output onuser3(void) : "short desc3"'
        self.assertEqual(output.fgd_str(), expected)

    def test_output_repr(self):
        name = 'onuser4'
        value_type = 'void'
        description = 'short desc4'
        output = FgdEntityOutput(name, value_type, description)
        expected = "<FgdEntityOutput {'name': 'onuser4', " + \
                   "'value_type': 'void', " + \
                   "'description': 'short desc4'}>"
        self.assertEqual(repr(output), expected)

    # FgdEntitySpawnflag
    def test_spawnflag_properties(self):
        value = 0
        display_name = 'spawnflag1'
        default_value = False
        spawnflag = FgdEntitySpawnflag(value, display_name, default_value)
        self.assertEqual(spawnflag.value, value)
        self.assertEqual(spawnflag.display_name, display_name)
        self.assertEqual(spawnflag.default_value, default_value)

    def test_spawnflag_schema(self):
        value = 2
        display_name = 'spawnflag2'
        default_value = False
        spawnflag = FgdEntitySpawnflag(value, display_name, default_value)
        self.assertEqual(spawnflag.schema['value'], value)
        self.assertEqual(spawnflag.schema['display_name'], display_name)
        self.assertEqual(spawnflag.schema['default_value'], default_value)

    def test_spawnflag_fgd_str(self):
        value = 1
        display_name = 'spawnflag3'
        default_value = True
        spawnflag = FgdEntitySpawnflag(value, display_name, default_value)
        self.assertEqual(spawnflag.fgd_str(), '1 : "spawnflag3" : 1')

    def test_spawnflag_repr(self):
        value = 1
        display_name = 'spawnflag3'
        default_value = True
        spawnflag = FgdEntitySpawnflag(value, display_name, default_value)
        expected = "<FgdEntitySpawnflag {'value': 1, " + \
                   "'display_name': 'spawnflag3', " + \
                   "'default_value': True}>"
        self.assertEqual(repr(spawnflag), expected)

    # FgdEntityPropertyChoice
    def test_choice_properties(self):
        value = 0
        display_name = 'choice1'
        choice = FgdEntityPropertyChoice(value, display_name)
        self.assertEqual(choice.value, value)
        self.assertEqual(choice.display_name, display_name)

    def test_choice_schema(self):
        value = 2
        display_name = 'choice2'
        choice = FgdEntityPropertyChoice(value, display_name)
        self.assertEqual(choice.schema['value'], value)
        self.assertEqual(choice.schema['display_name'], display_name)

    def test_choice_fgd_str(self):
        value = 1
        display_name = 'choice3'
        choice = FgdEntityPropertyChoice(value, display_name)
        self.assertEqual(choice.fgd_str(), '1 : "choice3"')

        value = "1"
        display_name = 'choice3'
        choice = FgdEntityPropertyChoice(value, display_name)
        self.assertEqual(choice.fgd_str(), '"1" : "choice3"')

    def test_choice_repr(self):
        value = 1
        display_name = 'choice3'
        choice = FgdEntityPropertyChoice(value, display_name)
        expected = "<FgdEntityPropertyChoice {'value': 1, " + \
                   "'display_name': 'choice3'}>"
        self.assertEqual(repr(choice), expected)

    # FgdEditorData
    def test_editor_data_str(self):
        class_type = 'include'
        data = "something.fgd"
        name = None
        editor_data = FgdEditorData(class_type, data, name)
        self.assertEqual(editor_data.class_type, class_type)
        self.assertEqual(editor_data.data, data)
        self.assertEqual(editor_data.name, name)

    def test_editor_data_tuple(self):
        class_type = 'mapsize'
        data = (-100, 100)
        name = None
        editor_data = FgdEditorData(class_type, data, name)
        self.assertEqual(editor_data.class_type, class_type)
        self.assertEqual(editor_data.data, data)
        self.assertEqual(editor_data.name, name)

    def test_editor_data_dict(self):
        class_type = 'AutoVisGroup'
        data = {'visgroups1': ['1', '2']}
        name = 'Custom'
        editor_data = FgdEditorData(class_type, data, name)
        self.assertEqual(editor_data.class_type, class_type)
        self.assertEqual(editor_data.data, data)
        self.assertEqual(editor_data.name, name)

    def test_editor_data_list(self):
        class_type = 'MaterialExclusion'
        data = ['materialfolder1', 'materialfolder2', 'materialfolder1']
        name = None
        editor_data = FgdEditorData(class_type, data, name)
        self.assertEqual(editor_data.class_type, class_type)
        self.assertEqual(editor_data.data, data)
        self.assertEqual(editor_data.name, name)

    def test_editor_data_str_fgd_str(self):
        class_type = 'include'
        data = u"something.fgd"
        name = None
        editor_data = FgdEditorData(class_type, data, name)
        expected = '@include "something.fgd"'
        self.assertEqual(editor_data.fgd_str(), expected)

    def test_editor_data_tuple_fgd_str(self):
        class_type = 'mapsize'
        data = (-100, 100)
        name = None
        editor_data = FgdEditorData(class_type, data, name)
        expected = '@mapsize(-100, 100)'
        self.assertEqual(editor_data.fgd_str(), expected)

    def test_editor_data_dict_fgd_str(self):
        class_type = 'AutoVisGroup'
        data = {'visgroups1': ['1', '2']}
        name = 'Custom'
        editor_data = FgdEditorData(class_type, data, name)
        expected = '@AutoVisGroup = "Custom"\n[\n\t"visgroups1"\n\t[\n\t\t"1"\n\t\t"2"\n\t]\n]'
        self.assertEqual(editor_data.fgd_str(), expected)

    def test_editor_data_list_fgd_str(self):
        class_type = 'MaterialExclusion'
        data = ['materialfolder1', 'materialfolder2', 'materialfolder3']
        name = None
        editor_data = FgdEditorData(class_type, data, name)
        expected = '@MaterialExclusion\n[\n\t"materialfolder1"\n\t"materialfolder2"\n\t"materialfolder3"\n]'
        self.assertEqual(editor_data.fgd_str(), expected)

    def test_editor_data_repr(self):
        class_type = 'AutoVisGroup'
        data = {'visgroups1': ['1', '2']}
        name = 'Custom'
        editor_data = FgdEditorData(class_type, data, name)
        expect = "<FgdEditorData of type 'AutoVisGroup' named 'Custom', [...]>"
        self.assertEqual(repr(editor_data), expect)
