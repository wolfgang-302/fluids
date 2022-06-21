from abc import ABC, abstractstaticmethod

import CoolProp.CoolProp as CP


# for working with physical units
from pint import UnitRegistry
ureg = UnitRegistry()

# percent and part per Million (ppM) are frequently used in HVAC
ureg.define('percent=1e-2=%')
ureg.define('ppM=1e-6')

# Q_ is a shortcut for Quantity
Quantity = Q_ = ureg.Quantity

# make it easy to return the value
# of a quantity q in base_units of q
def base_value(q):
    ''' return value of Quantity q in base units'''
    return q.to_base_units().magnitude

# make base_value (and bv) properties of Q_
Q_.base_value = Q_.bv = property(base_value)



T_0 = 273.15 # K, 0°C
p_amb = 101325 # Pa, normal pressure (Normaldruck)
    

class Point_of_State(ABC):
    ''' A point of state is defined by exactly two values in case of
        fluids or exactly three values in case of humid air.
        
        Point_of_State is never instanciated by itself. It needs to
        be subclassed.
        
        A point of state has properties to reflect physical properties
        of the corresponding fluid. These properties are determined 
        using CoolProp.    
    '''
    def __init__(self, **kwargs):
        # init given values as internal variables
        for k,v in kwargs.items():
            setattr(self, f'_{k}',v)
        
        # self._arg_list is used to determine other values
        # with the help of the CoolProp package
        self._arg_list = [v for t in kwargs.items() for v in t]
        
    # this is implemented in derived classes
    @abstractstaticmethod
    def _generic_function(*args):
        ''' for humid air this is CP.HAPropsSI, 
            for other fluids defined in CoolProps
            this is CP.PropsSi
        '''
        pass

    # defined in derived classes
    #acceptable_args = None
    
    def _generic_property(self, arg):
        ''' works only if arg is in self.acceptable_args
            
            arg is the name of a variable of state of the fluid.
            It is stored as a property of self.
            
            The value of property arg is either 
            predefined or determined exactly one time
            using self._generic_function.
            
            The self._generic_function is CP.PropsSI
            or CP.HAPropsSI depending on the
            used class
        '''
        # seems this never happens
        #if not arg in self.acceptable_args:
        #    raise Exception(f'dont know property {arg}')
        
        v = getattr(self, f'_{arg}',None)
        if v is None:
            # determine and save property for further use
            v = self._generic_function(arg,*self._arg_list)
            setattr(self,f'_{arg}',v)
        return v
    
    @classmethod
    def register(cls,q,u):
        ''' register quantity q with unit u in cls.acceptable_args
            and define q as property of cls
        '''
        if q in cls.acceptable_args:
            raise Exception(f'Property {q} is already registered in {__class__}')
        cls.acceptable_args[q]=u
        setattr(cls,q,property(lambda self, arg=q: self._generic_property(arg)))
            
    @classmethod
    def unregister(cls,q):
        ''' delete quantity q from cls.acceptable_args
            and delete property q from cls
        '''
        if not q in cls.acceptable_args:
            raise Exception(f'Property {q} not found in {__class__}')
        del cls.acceptable_args[q]
        delattr(cls,q)
        
    @property
    def args(self):
        ''' return dict of values of all known properties
            (variables of state) in self.acceptable_args 
        '''
        return {k:getattr(self,k) for k in self.acceptable_args}
    
    @property
    def args_or_errormessages(self):
        ''' return dict with values for all known properties
            (variables of state) in self.acceptable_args 
            that can be determined without raising an errormessage.
            
            in case of an errormessage, the corresponding massage is 
            returned for this arg instead.
            
            This method is useful for interactive exploration of
            a point of state only.
        '''
        res = dict()
        for k in self.acceptable_args:
            try:
                v = getattr(self,k)
            except Exception as e:
                v = e
            res[k] = v
        return res
    
    def subset(self,*args):
        ''' return dict with values for specified properties 
            (variables of state) from self.acceptable_args.
            Each arg must be registered in self.acceptable_args
        '''
        return {k: getattr(self,k) for k in args if k in self.acceptable_args}

class Fluid(Point_of_State):
    ''' This class is for fluids that use CP.PropsSI 
    
        A fluid is determinded by the attribute 'fluid', e.g. 'Air' or 'Water'. 
        This attribute is not defined here but inside the function
        fluid_factory(...), e.g
        Air = fluid_factory('Air') # or
        Air_with_units = fluid_factory('Air',with_units=True)
        
        It uses CP.PropsSI as _generic_function to determine variables of state.

        For a special fluid a point of state is defined by two variables of state.
        These variables of state must be defined during the instanciation of a point 
        of state, e.g.
        
        P_0 = Air(
            T=273.15,
            P=101325,
            name='P_0'
        ) # or
        P_0_with_units = Air_with_units(
            T=Q_(0,'degC'), # 0°C is the same as 273.15 K
            P=Q_(101325,'Pa'),
            name='P_0_with_units'
        )
        
        Each Fluid has its own dict of acceptable_args. An entry of Fluid.acceptable_args 
        is a pair (key: value), where key is the name of a variable of state and value the 
        corresponding unit, e.g.
        
           'T': 'K'  # (The Temperature 'T' has unit 'K')
           'P': 'Pa' # (The pressure 'P' has unit 'Pa')
        
        Once, P_0 has been defined, other variables of state can be obtained.
        
        H = P_0.H # or
        H = P_0_with_units.H
    '''
    # _fluid is defined in fluid_factory(...)
    #_fluid = None
    # acceptable_args is defined in fluid_factory(...)
    #acceptable_args = None 
    _generic_function = CP.PropsSI
    
    def __init__(self,name=None, **kwargs):
        self.name = name
        super().__init__(**kwargs)
        self._arg_list.append(self._fluid)
        
# dict of some acceptable args (variables of state) for fluids
Fluids_acceptable_args =  {
    'P': 'Pa', 'Pcrit': 'Pa', 'T': 'K', 'Tcrit': 'K', 'D': 'kg/m**3', 'H': 'J/kg',
    'U': 'J/kg', 'S': 'J/kg/K', 'A': 'm/s', 'L': 'W/m/K',
    'M': 'kg/mol', 'C': 'J/kg/K', 'CVMASS': 'J/kg/K', 'Q': '', 'Z': '', 'V': 'Pa*s'
}


class HAPoint_of_State(Point_of_State):
    ''' this class is for humid air and uses CP.HAPropsSI as _generic_function. 
    
        A point of state of humid air is defined by exactly three variables
        of state. One of these variables always is the pressure P which defaults
        to P = 101325 Pa. 
    '''
    
    _generic_function = CP.HAPropsSI
    
    def __init__(self,name=None, **kwargs):
        self.name = name
        
        # P is in list of kwargs or defaults to self._P_default
        # HAPoint_of_State._P_default is defined in fluid_factory(...)
        P = kwargs.pop('P',self._P_default)
        
        # in some cases the dict of kwargs has to be changed.
        # in these cases, the original values are kept
        # in internal variables and not determined from
        # CP.HAPropsSI. To simplify this process, first
        # an arg_dict is created. This finally determines
        # self._args_list
        arg_dict = {k:v for k,v in kwargs.items()}
        arg_dict['P'] = P
        
        epsilon = 0.621945 # M_Water/M_Air
        
        if 'W' in kwargs and 'R' in kwargs:
            # to combine W and R is not possible in CoolProps.HumidAir
            # work around this by replacing W by psi_w
            del arg_dict['W']
            W = self._W = kwargs['W']
            arg_dict['psi_w'] = W/(epsilon+W)
                                    
        if 'D' in kwargs and 'R' in kwargs:
            # to combine D and R is not possible in CoolProps.HumidAir
            # work around this by replacing D by psi_w
            del arg_dict['D']
            D = self._D = kwargs['D']
            
            # determine psi_w from P,D (and T=T_0 as dummy)
            psi_w = arg_dict['psi_w'] = CP.HAPropsSI('psi_w','P',P,'D',D,'T',T_0)
            self._W = epsilon*psi_w/(1-psi_w)
        
        super().__init__(**arg_dict)
    
    
    def dew_point(self,name=None):
        ''' The dew_point is defined by T=self.D and R=1 '''
        return self.__class__(T=self.D, R=1, name=name)
    
    def bulb_point(self,name=None):
        ''' The bulb_point is defined by T=self.B and R=1 '''
        return self.__class__(T=self.B, R=1, name=name)
    
    def mix(self,other,other_part,name=None):
        ''' a mixture of self and other is defined by
               mix.W = (1-other_part)*self.W + other_part*other.W
                     = self.W + other_part*(other.W-self.W)
               mix.H = (1-other_part)*self.H + other_part*other.H
                     = self.H + other_part*(other.H-self.H)
            where 0<= other_part <= 1
        '''
        if not (0 <= other_part <= 1):
            raise Exception(f'other_part = {other_part} is not in [0,1]')
            
        x = self.W + other_part*(other.W-self.W)
        h = self.H + other_part*(other.H-self.H)
        return self.__class__(W=x,H=h,name=name)
    
    def hom_coord(self,other,lambda_,name=None):
        ''' hom_coord means to treat (1-lambda_) and lambda_
            as homogenious coordinates of self and other.
            Here, lambda_ can be any value and is not restricted
            to [0,1]. The result is defined as the vector
              lambda_*(other-self)
            in the vector space <W,H> spanned by the state
            variables W and H starting from self.
            
            For 0 <= lambda_ <= 1, self.mix and self.hom_coord 
            is the same point of state.
        '''
        x = self.W + lambda_*(other.W-self.W)
        h = self.H + lambda_*(other.H-self.H)
        return self.__class__(W=x,H=h,name=name)

# dict of some acceptable args (variables of state) for humid air
HAPoint_of_State_acceptable_args = {
    'P': 'Pa', 'W': '', 'T': 'K', 'R': '', 'H': 'J/kg', 'S': 'J/kg/K',
    'B': 'K', 'D': 'K', 'Vda': 'm**3/kg', 'Vha': 'm**3/kg', 'M': 'Pa*s',
    'K': 'W/m/K', 'C': 'J/kg/K', 'P_w': 'Pa', 'psi_w': ''
}


class Units():
    def __init__(self,name=None, **kwargs):
        units = self.acceptable_args
        # treat v and Q_(v,'')  as the same Quantity Q_(v,'')
        # only do this for dimensionless values because this
        # may lead to ambigious results for offset units like 'degC'
        one = Q_(1,'')
        myargs = {k:v*one if units[k]==ureg.dimensionless else v for k,v in kwargs.items()}

        # convert to corresponding units and strip units to define point of state
        super().__init__(name=name,**{k: v.m_as(units[k]) for k,v in myargs.items()})
    
    def _generic_property(self,arg):
        ''' Determine value from super()._generic_property() 
            and apply unit to the result
        '''
        units = self.acceptable_args
        return Q_(super()._generic_property(arg), units[arg])
    
    def subset_to(self,**kwargs):
        ''' each kwarg is a dict of up to three values:
              - a quantity q
              - a unit u
              - a number n to round to
        '''
        def get_kwarg(v):
            q = v['q']
            u = v.get('u',None)
            n = v.get('n',None)
            res = getattr(self,q)
            if u is not None: res = res.to(u) 
            if n is not None: res = res.round(n)
            return res
        return {k:get_kwarg(v) for k,v in kwargs.items()}
    
    def subset_m_as(self,**kwargs):
        ''' each kwarg is a dict of up to three values:
              - a quantity q
              - a unit u
              - a number n to round to
        '''
        def get_kwarg(v):
            q = v['q']
            u = v.get('u',None)
            n = v.get('n',None)
            res = getattr(self,q)
            res = res.m_as(u) if u is not None else res.m
            return round(res,n) if n is not None else res

        return {k:get_kwarg(v) for k,v in kwargs.items()}
        


def fluid_factory(fluid,with_units=False,**kwargs):
    if fluid == 'HumidAir':
        if with_units:
            ThisFluid = type(f'{fluid}_with_Units', (Units, HAPoint_of_State), dict())
            ThisFluid._P_default = kwargs.pop('P_default',Q_(p_amb,'Pa')).bv
        else:
            ThisFluid = type(f'{fluid}',(HAPoint_of_State,), dict())
            ThisFluid._P_default = kwargs.pop('P_default',p_amb)        

        # register the above acceptable args
        ThisFluid.acceptable_args = dict()
        for q,u in HAPoint_of_State_acceptable_args.items():
            ThisFluid.register(q,u)


    else:
        if with_units:
            ThisFluid = type(f'{fluid}_with_Units', (Units,Fluid),{'_fluid': fluid})
        else:
            ThisFluid = type(f'{fluid}', (Fluid,), {'_fluid': fluid})
        
        # (re)define ThisFluid.acceptable_args to ensure,
        # each fluid has its own dict of acceptable_args
        ThisFluid.acceptable_args = dict()
        for k,v in Fluids_acceptable_args.items():
            ThisFluid.register(k,v)
        
    return ThisFluid
