import unittest

from fluids import fluid_factory, Q_, Quantity
import CoolProp.CoolProp as CP

class TestPoint_of_State(unittest.TestCase):
    
    def test_Air_definition(self):
        Air = fluid_factory('Air')
        p = Air(T=273.15,P=1e5)
        return self.assertEqual(p._arg_list,['T',273.15,'P',1e5,'Air'])
    

    def test_Air_with_units_definition(self):
        Air = fluid_factory('Air',with_units=True)
        p = Air(T=Q_(273.15,'K'),P=Q_(1e5,'Pa'))
        ok = (p.T.m_as('degC')==0) and (p.P.m_as('Pa')==1e5)
        return self.assertEqual(ok,True)

    def test_Air_calculation(self):
        Air = fluid_factory('Air')
        p = Air(T=273.15, P=1e5)
        return self.assertEqual(p.H,CP.PropsSI('H','T',273.15,'P',1e5,'Air'))

    def test_Air_with_units_calculation(self):
        Air = fluid_factory('Air',with_units=True)
        p = Air(T=Q_(0,'degC'), P=Q_(1e5,'Pa'))
        return self.assertEqual(p.H.m_as('J/kg'),CP.PropsSI('H','T',273.15,'P',1e5,'Air'))

    def test_HA_definition(self):
        HA = fluid_factory('HumidAir')
        p = HA(T=293.15,W=10e-3)
        return self.assertEqual(p._arg_list,['T',293.15,'W',10e-3,'P',101325])

    def test_HA_with_units_definition(self):
        HA = fluid_factory('HumidAir', with_units=True)
        p = HA(T=Q_(293.15,'K'), W=10e-3)
        return self.assertEqual(p._arg_list,['T',293.15,'W',10e-3,'P',101325])

if __name__ == '__main__':

    unittest.main()
