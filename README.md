# fluids

**Use Properties of Fluids in Jupyter Notebooks**

The package `fluids` is based on `CoolProp`. It is a wrapper around the functions

`CoolProp.CoolProp.PropsSI`

and

`CoolProp.CoolProp.HAPropsSI`

For reference see http://www.coolprop.org/


If you want to determine the properties of a fluid like Air, `fluids` can be used in the following way:


```python
from fluids import fluid_factory
Air = fluid_factory('Air')
```

The properties of Air for a temperature of $T=273.15\,\mathrm{K}$, and a pressure of $P=100 000\,\mathrm{Pa}$ are found by


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



A list of all available properties can be found following the link

http://www.coolprop.org/coolprop/HighLevelAPI.html#table-of-string-inputs-to-propssi-function



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



It is possible to pretty print the result:


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

Humid Air is a special case of a fluid. The corresponding function is `CoolProp.CoolProp.HAPropsSI`

To determine a point of state of humid air, exactly three values are needed. One of this values must be the total pressure `P`. The default value for the pressure is `P = 101325` (Pa) if no value for P is defined.

To find the properties of humid air for temperature of T=20°C, a relative humidity of R=50% and a total pressure of P=101325 Pa use


```python
HA = fluid_factory('HumidAir')
point = HA(T=273.15+20,R=50e-2,name='point') # not nessecary to define P=101325
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
point_with_units = HAu(
    T=Q_(20,'degC'),
    R=Q_(50,'percent'), # or R=0.5
    name='point_with_units'
) # not nessecary to define P=Q_(101325,'Pa')
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



As for other fluids it is possible to register additional properties. A list of properties of humid air can be found following the link

http://www.coolprop.org/fluid_properties/HumidAir.html#table-of-inputs-outputs-to-hapropssi



```python
HAu.register('Cha','J/kg/K') # Mixture specific heat per unit humid air
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
     'psi_w': 0.011591305062179829 <Unit('dimensionless')>,
     'Cha': 1012.4678157748747 <Unit('joule / kelvin / kilogram')>}



### Define default pressure for Humid Air

If a default pressure different from `Q_(101325,'Pa')` is needed, this can be archieved by:

`HA = fluid_factory('HumidAir',P_default=95000)`

or

`HA = fluid_factory('HumidAir',with_units=True, P_default=Q_(95000,'Pa'))`


```python
HA = fluid_factory('HumidAir',with_units=True, P_default=Q_(95000,'Pa'))
```


```python
point = HA(T=Q_(20,'degC'),R=50e-2,name='point')
point.args
```




    {'P': 95000.0 <Unit('pascal')>,
     'W': 0.007783888419487314 <Unit('dimensionless')>,
     'T': 293.15 <Unit('kelvin')>,
     'R': 0.5 <Unit('dimensionless')>,
     'H': 39882.038958452504 <Unit('joule / kilogram')>,
     'S': 163.14630978463654 <Unit('joule / kelvin / kilogram')>,
     'B': 286.76917718799103 <Unit('kelvin')>,
     'D': 282.42467768085453 <Unit('kelvin')>,
     'Vda': 0.896495138629698 <Unit('meter ** 3 / kilogram')>,
     'Vha': 0.8895708186362018 <Unit('meter ** 3 / kilogram')>,
     'M': 1.8137145921054082e-05 <Unit('pascal * second')>,
     'K': 0.025861409942910148 <Unit('watt / kelvin / meter')>,
     'C': 1020.6665065054794 <Unit('joule / kelvin / kilogram')>,
     'P_w': 1174.266281013783 <Unit('pascal')>,
     'psi_w': 0.012360697694881927 <Unit('dimensionless')>}



The default pressure is only used, if no pressure is defined:


```python
point_2 = HA(
    T=Q_(20,'degC'),
    R=50e-2,
    P=Q_(2,'bar'), # different from default of Q_(95000,'Pa')
    name='point_2'
)
point_2.args
```




    {'P': 200000.0 <Unit('pascal')>,
     'W': 0.003684810641674053 <Unit('dimensionless')>,
     'T': 293.15 <Unit('kelvin')>,
     'R': 0.5 <Unit('dimensionless')>,
     'H': 29228.736705025192 <Unit('joule / kilogram')>,
     'S': -90.00061952241548 <Unit('joule / kelvin / kilogram')>,
     'B': 288.61554630908495 <Unit('kelvin')>,
     'D': 282.4203286674543 <Unit('kelvin')>,
     'Vda': 0.42290250683411085 <Unit('meter ** 3 / kilogram')>,
     'Vha': 0.42134991219379075 <Unit('meter ** 3 / kilogram')>,
     'M': 1.8193129789730992e-05 <Unit('pascal * second')>,
     'K': 0.02591390134464176 <Unit('watt / kelvin / meter')>,
     'C': 1014.729336766021 <Unit('joule / kelvin / kilogram')>,
     'P_w': 1177.9523862185358 <Unit('pascal')>,
     'psi_w': 0.005889761931092679 <Unit('dimensionless')>}



Usually, not all properties of a point of state are needed. To get the specific enthalpy `H` from `point_2`, type 


```python
point_2.H
```




29228.736705025192 joule/kilogram




```python
# or, i.e.
point_2.H.to('kJ/kg').round(2)
```




29.23 kilojoule/kilogram




```python
# or
print(f"H = {point_2.H.to('kJ/kg').round(2):~P}")
```

    H = 29.23 kJ/kg

