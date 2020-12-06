class Gui:
    def __init__(self, *args, **kwargs):
        self.name = args[0]
        for key in kwargs.keys():            
            self.add(key, kwargs[key]) 
        
    def add(self, attr, value):
        setattr(self, attr, value) 

    def check(self,*attr_names):
        for name in attr_names:
            if not hasattr(self,name):
                raise AttributeError(name, self)

    def replace(self, obj):
        self.__dict__ = obj.__dict__

class EditField(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check('value')

class Button(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class Image(Gui):
    '''has to contain file,width,height parameters'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self,'width'):
            self.width = 500.0
        if not hasattr(self,'height'):
            self.height = 350.0        
        if not hasattr(self,'image'):
            self.image = None

class Switcher(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.check('icon')

type_list = ['toggles','list','dropdown']

class SingleSelect(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self,'options'):             
            self.options = [] 

class TreeSelect(SingleSelect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)         
        self.type = 'list' #for GUI
        if hasattr(self,'elems'): #elems is list of (name, key, parent_key [,optional object reference])
            self.set_elems(self.elems)
        
    def getElem(self, elemId):                
        return next((e for e in self.elems if elemId == e[1]), None)

    def setvalue_byname(self, nokey):        
        self.value = next((e[1] for e in self.elems if nokey == e[0]), None)

    def get_name_value(self):
        if self.value:
            el = self.getElem(self.value)
            if el:
                return el[0]

    def set_elems(self, elems):
        self.elems = elems
        options = []
        def make4root(eparent, level):
            options.append((eparent, level))
            childs = [e for e in self.elems if e[2] == eparent[1]]
            childs.sort(key= lambda e: e[0])
            for c in childs:
                make4root(c, level + 1)

        elems = {e[1] for e in self.elems}
        roots = [e for e in self.elems if not e[2] in elems]
        roots.sort(key= lambda e: e[0])
        for root in roots:
            make4root(root, 0)
        self.options = []
        for el in options:
            vlines = el[1] - 1
            str = '|' * vlines if vlines > 0 else ''
            if el[1]:
                str += '\\'
            str += el[0][0]
            self.options.append([str, el[0][1]])        

TableActions = {'*': 'SMswitch', '!': 'Edit', '+':'Add', '-':'Delete'}       

class Table(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'actions'):
            self.actions = '+-!*'                    
        self.check('rows', 'headers','value')

    def selected_list(self):                            
        return [self.value] if self.value != -1 else [] if type(self.value) == int else self.value
        
class Block(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.top_childs = args[1] if len(args) > 1 else []
        self.childs = list(args[2:])
        self.check()

    def check(self):
        ch_names = set()        
        for child in self.childs:
            if isinstance(child, list) or isinstance(child, tuple):
                for sub in child:                                        
                    if sub.name in ch_names:                        
                        print(f'Error: block {self.name} contains duplicated name {sub.name}!')
                        return
                    ch_names.add(sub.name)
            else:
                if child.name in ch_names:
                    print(f'Error: block {self.name} contains duplicated name {child.name}!')
                    return        
                ch_names.add(child.name)

class Dialog:    
    def __init__(self, name, text, actions, callback, content = None):
        self.name = name
        self.text = text
        self.content = Block('root',[], *content, dialog = True) if content else None
        self.buttons = actions
        self.callback = callback        
        
class Screen(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.type = 'Screen'

    def check(self):
        bl_names = set()
        for bl in self.blocks:                        
            if bl.name in bl_names:
                print(f'Error: screen {self.name} contains duplicated name {bl.name}!')
                return
            bl_names.add(bl.name)
        