import unittest

import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fluids import fluid_factory, Q_, Quantity
from fluids.fluids import Point_of_State

import CoolProp.CoolProp as CP

class Test_Q_(unittest.TestCase):
    
    def test_bv(self):
        return self.assertEqual(Q_(5,'N').bv == Q_(5,'N').base_value == 5, True)
    
    def test_percent(self):
        return self.assertEqual(Q_(5,'percent').units, 'percent')
    
    def test_ppM(self):
        return self.assertEqual(Q_(1000,'ppM').units, 'ppM')
    
    def test_percent_bv(self):
        return self.assertEqual(Q_(5,'percent').bv, 0.05)
    
    def test_ppM_bv(self):
        return self.assertEqual(Q_(1000,'ppM').bv, 0.001)
    

class Point(Point_of_State):
    @staticmethod
    def _generic_function(*args):
        return args
    
Point.acceptable_args = dict()
Point.register('x','unit_of_x')
    
class Test_Point_of_State(unittest.TestCase):
    
    def test_Point_of_State_property_x(self):
        p = Point(a='va',b='vb',c='vc')
        return self.assertEqual(p.x, ('x', 'a', 'va', 'b', 'vb', 'c', 'vc'))

class Test_fluid_factory(unittest.TestCase):
    
    def test_Air_definition(self):
        Air = fluid_factory('Air')
        p = Air(T=273.15,P=1e5)
        return self.assertEqual(p._arg_list,['T',273.15,'P',1e5,'Air'])
    
    def test_Air_definition_name(self):
        Air = fluid_factory('Air')
        p = Air(T=273.15,P=1e5,name='Point')
        return self.assertEqual(p.name,'Point')

    def test_Air_with_units_definition(self):
        Air = fluid_factory('Air',with_units=True)
        p = Air(T=Q_(273.15,'K'),P=Q_(1e5,'Pa'))
        ok = (p.T.m_as('degC')==0) and (p.P.m_as('Pa')==1e5)
        return self.assertEqual(ok,True)

    def test_Air_with_units_definition_name(self):
        Air = fluid_factory('Air',with_units=True)
        p = Air(T=Q_(273.15,'degC'),P=Q_(1e5,'Pa'),name='Point')
        return self.assertEqual(p.name,'Point')

    def test_Air_calculation(self):
        Air = fluid_factory('Air')
        p = Air(T=273.15, P=1e5)
        ok = True
        for arg in p.acceptable_args:
            if not arg in ['T','P']:
                ok = ok and (getattr(p,arg,None)==CP.PropsSI(arg,'T',273.15,'P',1e5,'Air'))
        return self.assertEqual(ok,True)

    def test_Air_with_units_calculation(self):
        Air = fluid_factory('Air',with_units=True)
        p = Air(T=Q_(0,'degC'), P=Q_(1e5,'Pa'))
        ok = True
        for arg in p.acceptable_args:
            if not arg in ['T','P']:
                ok = ok and (
                    getattr(p,arg,None).bv == CP.PropsSI(arg,'T',273.15,'P',1e5,'Air')
                )
        return self.assertEqual(ok,True)
    
    def test_Air_with_units_register(self):
        Air = fluid_factory('Air',with_units=True)
        Air.register('SMOLAR','J/mol/K')
        return self.assertEqual('SMOLAR' in Air.acceptable_args,True)
    
    def test_Air_with_units_unregister(self):
        Air = fluid_factory('Air',with_units=True)
        Air.unregister('P')
        return self.assertEqual('P' in Air.acceptable_args, False)
        

    def test_HA_definition(self):
        HA = fluid_factory('HumidAir')
        p = HA(T=293.15,W=10e-3)
        return self.assertEqual(p._arg_list,['T',293.15,'W',10e-3,'P',101325])

    def test_HA_definition_name(self):
        HA = fluid_factory('HumidAir')
        p = HA(T=273.15,R=50e-2,name='Point')
        return self.assertEqual(p.name,'Point')

    def test_HA_with_units_definition(self):
        HA = fluid_factory('HumidAir', with_units=True)
        p = HA(T=Q_(293.15,'K'), W=10e-3)
        return self.assertEqual(p._arg_list,['T',293.15,'W',10e-3,'P',101325])
    
    def test_HA_definition_name(self):
        HA = fluid_factory('HumidAir',with_units=True)
        p = HA(T=Q_(273.15,'degC'),R=50e-2,name='Point')
        return self.assertEqual(p.name,'Point')

    def test_HA_calculation(self):
        HA = fluid_factory('HumidAir')
        p = HA(T=293.15,W=10e-3)
        ok = True
        for arg in p.acceptable_args:
            if not p in ['T','W','P']:
                ok = ok and (
                    getattr(p,arg,None)==CP.HAPropsSI(arg,'T',293.15,'W',10e-3,'P',101325)
                )
        return self.assertEqual(ok,True)
    
    def test_HA_with_units_calculation(self):
        HA = fluid_factory('HumidAir',with_units=True)
        p = HA(T=Q_(293.15,'K'),W=10e-3)
        ok = True
        for arg in p.acceptable_args:
            if not p in ['T','W','P']:
                ok = ok and (
                    getattr(p,arg,None).bv==CP.HAPropsSI(arg,'T',293.15,'W',10e-3,'P',101325)
                )
        return self.assertEqual(ok,True)
    
    def test_HA_with_units_register(self):
        HA = fluid_factory('HumidAir',with_units=True)
        HA.register('Cha','J/kg/K')
        return self.assertEqual('Cha' in HA.acceptable_args, True)
    
    def test_HA_with_units_unregister(self):
        HA = fluid_factory('HumidAir',with_units=True)
        HA.unregister('W')
        return self.assertEqual('W' in HA.acceptable_args, False)

if __name__ == '__main__':

    unittest.main()
