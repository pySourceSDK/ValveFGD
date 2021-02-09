import os
import unittest

from valvefgd import *


class ParseTestCase(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_bms(self):
        fgd = FgdParse('tests/fgds/bms/bms.fgd')
        self.assertTrue(fgd)

    def test_cs(self):
        fgd = FgdParse('tests/fgds/cs/halflife-cs.fgd')
        self.assertTrue(fgd)

    def test_csgo(self):
        fgd = FgdParse('tests/fgds/csgo/csgo.fgd')
        self.assertTrue(fgd)

    def test_cstrike(self):
        fgd = FgdParse('tests/fgds/css/cstrike.fgd')
        self.assertTrue(fgd)

    def test_dod(self):
        fgd = FgdParse('tests/fgds/dod/halflife-DOD2-expert.fgd')
        self.assertTrue(fgd)

    def test_dods(self):
        fgd = FgdParse('tests/fgds/dods/dod.fgd')
        self.assertTrue(fgd)

    def test_ep1(self):
        fgd = FgdParse('tests/fgds/ep1/cstrike.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/ep1/dod.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/ep1/halflife2.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/ep1/hl2mp.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/ep1/portal.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/ep1/sdk.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/ep1/tf.fgd')
        self.assertTrue(fgd)

    def test_garrysmod(self):
        fgd = FgdParse('tests/fgds/garrysmod/garrysmod.fgd')
        self.assertTrue(fgd)

    def test_hl(self):
        fgd = FgdParse('tests/fgds/hl/halflife.fgd')
        self.assertTrue(fgd)

    def test_hldc(self):
        fgd = FgdParse('tests/fgds/hldc/dmc.fgd')
        self.assertTrue(fgd)

    def test_hl2(self):
        fgd = FgdParse('tests/fgds/hl2/halflife2.fgd')
        self.assertTrue(fgd)

    def test_left4dead(self):
        fgd = FgdParse('tests/fgds/left4dead/left4dead.fgd')
        self.assertTrue(fgd)

    def test_left4dead2(self):
        fgd = FgdParse('tests/fgds/left4dead2/left4dead2.fgd')
        self.assertTrue(fgd)

    def test_orangebox(self):
        fgd = FgdParse('tests/fgds/orangebox/cstrike.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/orangebox/dod.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/orangebox/halflife2.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/orangebox/hl2mp.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/orangebox/portal.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/orangebox/sdk.fgd')
        self.assertTrue(fgd)
        fgd = FgdParse('tests/fgds/orangebox/tf.fgd')
        self.assertTrue(fgd)

    def test_portal(self):
        fgd = FgdParse('tests/fgds/portal/portal.fgd')
        self.assertTrue(fgd)

    def test_portal2(self):
        fgd = FgdParse('tests/fgds/portal2/portal2.fgd')
        self.assertTrue(fgd)

    def test_ricochet(self):
        fgd = FgdParse('tests/fgds/ricochet/ricochet.fgd')
        self.assertTrue(fgd)

    def test_swarm(self):
        fgd = FgdParse('tests/fgds/swarm/swarm.fgd')
        self.assertTrue(fgd)

    def test_tf(self):
        fgd = FgdParse('tests/fgds/tf/tf.fgd')
        self.assertTrue(fgd)

    def test_tfc(self):
        fgd = FgdParse('tests/fgds/tfc/tf15f.fgd')
        self.assertTrue(fgd)

    def test_notfound(self):
        self.assertRaises(IOError, FgdParse,
                          'tests/fgds/not_a_file.fgd')

    def test_parseTypes(self):
        fgd = FgdParse('tests/fgds/tf/tf.fgd')

        for ent in fgd.entities:
            self.assertTrue(isinstance(ent, FgdEntity))

            self.assertTrue(isinstance(ent.class_type, str))
            self.assertTrue(isinstance(ent.definitions, list))
            self.assertTrue(isinstance(ent.name, str))
            self.assertTrue(isinstance(ent.description, str) or
                            ent.description == None)

            for d in ent.definitions:
                self.assertTrue(isinstance(d, dict))
                self.assertTrue(isinstance(d['name'], str))
                if 'args' in d:
                    self.assertTrue(isinstance(d['args'], list))
                    for a in d['args']:
                        self.assertTrue(isinstance(a, str))

            for p in ent.parents:
                self.assertTrue(isinstance(p, FgdEntity))
            for p in ent.properties:
                self.assertTrue(isinstance(p, FgdEntityProperty))

                self.assertTrue(isinstance(p.name, str))
                self.assertTrue(isinstance(p.value_type, str))
                self.assertTrue(isinstance(p.readonly, bool))
                self.assertTrue(isinstance(p.display_name, str) or
                                p.display_name == None)
                self.assertTrue(isinstance(p.default_value, str) or
                                isinstance(p.default_value, int) or
                                p.default_value == None)
                self.assertTrue(isinstance(p.description, str) or
                                p.description == None)
                if p.choices != None:
                    for c in p.choices:
                        self.assertTrue(isinstance(c, FgdEntityPropertyChoice))
                        self.assertTrue(isinstance(c.value, int) or
                                        isinstance(c.value, str))
                        self.assertTrue(isinstance(c.display_name, str))
            for i in ent.inputs:
                self.assertTrue(isinstance(i, FgdEntityInput))
                self.assertTrue(isinstance(i.name, str))
                self.assertTrue(isinstance(i.value_type, str))
                self.assertTrue(isinstance(i.description, str))
            for o in ent.outputs:
                self.assertTrue(isinstance(o, FgdEntityOutput))
                self.assertTrue(isinstance(o.name, str))
                self.assertTrue(isinstance(o.value_type, str))
                self.assertTrue(isinstance(o.description, str))
            for s in ent.spawnflags:
                self.assertTrue(isinstance(s, FgdEntitySpawnflag))
                self.assertTrue(isinstance(s.value, int))
                self.assertTrue(isinstance(s.display_name, str))
                self.assertTrue(isinstance(s.default_value, bool))

        for editor_data in fgd.editor_data:
            self.assertTrue(isinstance(editor_data, FgdEditorData))
            self.assertTrue(isinstance(editor_data.class_type, str))
            self.assertTrue(isinstance(editor_data.name, str) or
                            editor_data.name == None)

            self.assertTrue(isinstance(editor_data.data, str) or
                            isinstance(editor_data.data, tuple) or
                            isinstance(editor_data.data, list) or
                            isinstance(editor_data.data, dict))

        for include in fgd.includes:
            self.assertTrue(isinstance(include, Fgd))
