# fluids

**Use Properties of Fluids in Jupyter Notebooks**

The package `fluids` is based on `CoolProp`. It is a wrapper around the functions

`CoolProp.CoolProp.PropsSI`

and

`CoolProp.CoolProp.HAPropsSI`


If you want to determine the properties of a fluid, e.g. Air, `fluids` can be used in the following way:


```python
from fluids import fluid_factory
Air = fluid_factory('Air')
```

The properties of Air for $T=273.15\,\mathrm{K}$, $P=100 000\,\mathrm{Pa}$ are found by


```python
point = Air(T=273.15,P=1e5,name='point')
point.args
```




    {'P': 100000.0,
     'Pcrit': 3786000.0,
     'T': 273.15,
     'Tcrit': 132.5306,
     'D': 1.2761465510726724,
     'H': 399290.7894624132,
     'U': 320929.8834082108,
     'S': 3796.181850244674,
     'A': 331.4400967167516,
     'L': 0.024360013660200727,
     'M': 0.02896546,
     'C': 1005.6581806254104,
     'CVMASS': 716.9406259938061,
     'Q': -1.0,
     'Z': 0.9994061416798139,
     'V': 1.7218206132823325e-05}



Using `CoolProp.CoolProp.PropsSI` it is possible to determine a lot more properties of fluids. If needed, additional properties (with their units) can be registered for a fluid. For example


```python
Air.register('SMOLAR','J/mol/K')
```


```python
point.args
```




    {'P': 100000.0,
     'Pcrit': 3786000.0,
     'T': 273.15,
     'Tcrit': 132.5306,
     'D': 1.2761465510726724,
     'H': 399290.7894624132,
     'U': 320929.8834082108,
     'S': 3796.181850244674,
     'A': 331.4400967167516,
     'L': 0.024360013660200727,
     'M': 0.02896546,
     'C': 1005.6581806254104,
     'CVMASS': 716.9406259938061,
     'Q': -1.0,
     'Z': 0.9994061416798139,
     'V': 1.7218206132823325e-05,
     'SMOLAR': 109.95815353598809}



In `fluids` it is possible to use units (based on the module `pint`):


```python
from fluids import Q_ # or Quantity
```


```python
Air_with_units = fluid_factory('Air',with_units=True)
```


```python
point_with_units = Air_with_units(T=Q_(0,'degC'),P=Q_(1,'bar'),name='point_with_units')
point_with_units.args
```




    {'P': 100000.0 <Unit('pascal')>,
     'Pcrit': 3786000.0 <Unit('pascal')>,
     'T': 273.15 <Unit('kelvin')>,
     'Tcrit': 132.5306 <Unit('kelvin')>,
     'D': 1.2761465510726724 <Unit('kilogram / meter ** 3')>,
     'H': 399290.7894624132 <Unit('joule / kilogram')>,
     'U': 320929.8834082108 <Unit('joule / kilogram')>,
     'S': 3796.181850244674 <Unit('joule / kelvin / kilogram')>,
     'A': 331.4400967167516 <Unit('meter / second')>,
     'L': 0.024360013660200727 <Unit('watt / kelvin / meter')>,
     'M': 0.02896546 <Unit('kilogram / mole')>,
     'C': 1005.6581806254104 <Unit('joule / kelvin / kilogram')>,
     'CVMASS': 716.9406259938061 <Unit('joule / kelvin / kilogram')>,
     'Q': -1.0 <Unit('dimensionless')>,
     'Z': 0.9994061416798139 <Unit('dimensionless')>,
     'V': 1.7218206132823325e-05 <Unit('pascal * second')>}



It is possible to pretty print the properties:


```python
for k,v in point_with_units.args.items():
    print(f'{k} = {v:~P}')
```

    P = 100000.0 Pa
    Pcrit = 3786000.0 Pa
    T = 273.15 K
    Tcrit = 132.5306 K
    D = 1.2761465510726724 kg/m³
    H = 399290.7894624132 J/kg
    U = 320929.8834082108 J/kg
    S = 3796.181850244674 J/K/kg
    A = 331.4400967167516 m/s
    L = 0.024360013660200727 W/K/m
    M = 0.02896546 kg/mol
    C = 1005.6581806254104 J/K/kg
    CVMASS = 716.9406259938061 J/K/kg
    Q = -1.0
    Z = 0.9994061416798139
    V = 1.7218206132823325×10⁻⁵ Pa·s


## Humid Air

Humid Air is a special case. The corresponding function is `CoolProp.CoolProp.HAPropsSI`

To determine a point of state of humid air, exactly three values are needed. One of this values must be the total pressure `P`. The default is `P = 101325` (Pa) if no value for P is defined.

To find the properties of humid air for T=20°C, R=50%, P=101325 Pa use


```python
HA = fluid_factory('HumidAir')
point = HA(T=273.15+20,R=50e-2,name='point')
point.args
```




    {'P': 101325,
     'W': 0.007293697701992549,
     'T': 293.15,
     'R': 0.5,
     'H': 38622.83892391293,
     'S': 139.97016819060187,
     'B': 286.92646885824075,
     'D': 282.42442581534783,
     'Vda': 0.8398598461778416,
     'Vha': 0.8337785177191823,
     'M': 1.814316044123345e-05,
     'K': 0.025866132503697774,
     'C': 1019.8524499561333,
     'P_w': 1174.488985425371,
     'psi_w': 0.011591305062179829}




```python
# or, with units
HAu = fluid_factory('HumidAir',with_units=True)
point_with_units = HAu(T=Q_(20,'degC'),R=Q_(50,'percent'),name='point_with_units')
point_with_units.args
```




    {'P': 101325.0 <Unit('pascal')>,
     'W': 0.007293697701992549 <Unit('dimensionless')>,
     'T': 293.15 <Unit('kelvin')>,
     'R': 0.5 <Unit('dimensionless')>,
     'H': 38622.83892391293 <Unit('joule / kilogram')>,
     'S': 139.97016819060187 <Unit('joule / kelvin / kilogram')>,
     'B': 286.92646885824075 <Unit('kelvin')>,
     'D': 282.42442581534783 <Unit('kelvin')>,
     'Vda': 0.8398598461778416 <Unit('meter ** 3 / kilogram')>,
     'Vha': 0.8337785177191823 <Unit('meter ** 3 / kilogram')>,
     'M': 1.814316044123345e-05 <Unit('pascal * second')>,
     'K': 0.025866132503697774 <Unit('watt / kelvin / meter')>,
     'C': 1019.8524499561333 <Unit('joule / kelvin / kilogram')>,
     'P_w': 1174.488985425371 <Unit('pascal')>,
     'psi_w': 0.011591305062179829 <Unit('dimensionless')>}


