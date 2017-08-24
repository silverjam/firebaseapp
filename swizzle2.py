from objc_util import *
from inspect import getargspec

c.method_setImplementation.restype = c_void_p
c.method_setImplementation.argtypes = [c_void_p, c_void_p]

c.method_getImplementation.restype = c_void_p
c.method_getImplementation.argtypes = [c_void_p]

''' Make `swizzledFunc` run instead of `method` '''
def replaceImplementation(method, swizzledFunc):
	originalMethodName = 'original' + method.sel_name.replace(':', '_')
	originalMethodNameNumber = 0
	while hasattr(method.obj, originalMethodName):
		originalMethodNameNumber += 1
		originalMethodName = 'original' + str(originalMethodNameNumber) + method.sel_name.replace(':', '_')
	swizzledMethodName = 'swizzled' + method.sel_name.replace(':', '_')
	swizzledMethodNameNumber = 0
	while hasattr(method.obj, swizzledMethodName):
		swizzledMethodNameNumber += 1
		swizzledMethodName = 'swizzled' + str(swizzledMethodNameNumber) + method.sel_name.replace(':', '_')
	swizzledFuncName = 'swizzledFunc' + '_' * (len(getargspec(swizzledFunc).args) - 2)
	locals()[swizzledFuncName] = swizzledFunc
	locals()[swizzledFuncName].__name__ = swizzledFuncName
	newFuncName = 'newFunc' + '_' * (len(getargspec(swizzledFunc).args) - 2)
	args = getargspec(swizzledFunc).args
	tempLocals = locals()
	exec('def {}({}): from objc_util import ObjCInstance; ObjCInstance({}).{}({})'.format(newFuncName, ', '.join(args), getargspec(swizzledFunc).args[0], swizzledMethodName, ', '.join(['ObjCInstance({})'.format(arg) for arg in args[2:]])), globals(), tempLocals)
	locals()[newFuncName] = tempLocals[newFuncName]
	locals()[newFuncName].__name__ = newFuncName
	TempClass = create_objc_class('TempClass', ObjCClass('NSObject'), methods = [locals()[swizzledFuncName], locals()[newFuncName]])
	swizzledImp = c.method_getImplementation(ObjCInstanceMethod(TempClass.new(), swizzledFuncName).method)
	originalImp = c.method_getImplementation(method.method)
	newImp = c.method_getImplementation(ObjCInstanceMethod(TempClass.new(), newFuncName).method)
	try:
		originalMethod = method.obj.__getattr__(originalMethodName)
		swizzledMethod = method.obj.__getattr__(swizzledMethodName)
		c.method_setImplementation(originalMethod.method, originalImp)
		c.method_setImplementation(swizzledMethod.method, swizzledImp)
	except Exception as e:
		print(e)
		className = method.obj._get_objc_classname()
		c.class_addMethod(ObjCClass(className).ptr, sel(originalMethodName), originalImp, c.method_getTypeEncoding(method.method))
		c.class_addMethod(ObjCClass(className).ptr, sel(swizzledMethodName), swizzledImp, c.method_getTypeEncoding(method.method))
	c.method_setImplementation(method.method, newImp)

''' Make `swizzledFunc` run before `method` '''
def insertImplementation(method, swizzledFunc):
	originalMethodName = 'original' + method.sel_name.replace(':', '_')
	originalMethodNameNumber = 0
	while hasattr(method.obj, originalMethodName):
		originalMethodNameNumber += 1
		originalMethodName = 'original' + str(originalMethodNameNumber) + method.sel_name.replace(':', '_')
	swizzledMethodName = 'swizzled' + method.sel_name.replace(':', '_')
	swizzledMethodNameNumber = 0
	while hasattr(method.obj, swizzledMethodName):
		swizzledMethodNameNumber += 1
		swizzledMethodName = 'swizzled' + str(swizzledMethodNameNumber) + method.sel_name.replace(':', '_')
	swizzledFuncName = 'swizzledFunc' + '_' * (len(getargspec(swizzledFunc).args) - 2)
	locals()[swizzledFuncName] = swizzledFunc
	locals()[swizzledFuncName].__name__ = swizzledFuncName
	newFuncName = 'newFunc' + '_' * (len(getargspec(swizzledFunc).args) - 2)
	args = getargspec(swizzledFunc).args
	tempLocals = locals()
	exec('def {}({}): from objc_util import ObjCInstance; self = ObjCInstance({}); self.{}({}); self.{}({})'.format(newFuncName, ', '.join(args), getargspec(swizzledFunc).args[0], swizzledMethodName, ', '.join(['ObjCInstance({})'.format(arg) for arg in args[2:]]), originalMethodName, ', '.join(['ObjCInstance({})'.format(arg) for arg in args[2:]])), globals(), tempLocals)
	locals()[newFuncName] = tempLocals[newFuncName]
	locals()[newFuncName].__name__ = newFuncName
	TempClass = create_objc_class('TempClass', ObjCClass('NSObject'), methods = [locals()[swizzledFuncName], locals()[newFuncName]])
	swizzledImp = c.method_getImplementation(ObjCInstanceMethod(TempClass.new(), swizzledFuncName).method)
	originalImp = c.method_getImplementation(method.method)
	newImp = c.method_getImplementation(ObjCInstanceMethod(TempClass.new(), newFuncName).method)
	try:
		originalMethod = method.obj.__getattr__(originalMethodName)
		swizzledMethod = method.obj.__getattr__(swizzledMethodName)
		c.method_setImplementation(originalMethod.method, originalImp)
		c.method_setImplementation(swizzledMethod.method, swizzledImp)
	except:
		className = method.obj._get_objc_classname()
		c.class_addMethod(ObjCClass(className).ptr, sel(originalMethodName), originalImp, c.method_getTypeEncoding(method.method))
		c.class_addMethod(ObjCClass(className).ptr, sel(swizzledMethodName), swizzledImp, c.method_getTypeEncoding(method.method))
	c.method_setImplementation(method.method, newImp)

''' Make `swizzledFunc` run after `method` '''
def appendImplementation(method, swizzledFunc):
	originalMethodName = 'original' + method.sel_name.replace(':', '_')
	originalMethodNameNumber = 0
	while hasattr(method.obj, originalMethodName):
		originalMethodNameNumber += 1
		originalMethodName = 'original' + str(originalMethodNameNumber) + method.sel_name.replace(':', '_')
	swizzledMethodName = 'swizzled' + method.sel_name.replace(':', '_')
	swizzledMethodNameNumber = 0
	while hasattr(method.obj, swizzledMethodName):
		swizzledMethodNameNumber += 1
		swizzledMethodName = 'swizzled' + str(swizzledMethodNameNumber) + method.sel_name.replace(':', '_')
	swizzledFuncName = 'swizzledFunc' + '_' * (len(getargspec(swizzledFunc).args) - 2)
	locals()[swizzledFuncName] = swizzledFunc
	locals()[swizzledFuncName].__name__ = swizzledFuncName
	newFuncName = 'newFunc' + '_' * (len(getargspec(swizzledFunc).args) - 2)
	args = getargspec(swizzledFunc).args
	tempLocals = locals()
	exec('def {}({}): from objc_util import ObjCInstance; self = ObjCInstance({}); self.{}({}); self.{}({})'.format(newFuncName, ', '.join(args), getargspec(swizzledFunc).args[0], originalMethodName, ', '.join(['ObjCInstance({})'.format(arg) for arg in args[2:]]), swizzledMethodName, ', '.join(['ObjCInstance({})'.format(arg) for arg in args[2:]])), globals(), tempLocals)
	locals()[newFuncName] = tempLocals[newFuncName]
	locals()[newFuncName].__name__ = newFuncName
	TempClass = create_objc_class('TempClass', ObjCClass('NSObject'), methods = [locals()[swizzledFuncName], locals()[newFuncName]])
	swizzledImp = c.method_getImplementation(ObjCInstanceMethod(TempClass.new(), swizzledFuncName).method)
	originalImp = c.method_getImplementation(method.method)
	newImp = c.method_getImplementation(ObjCInstanceMethod(TempClass.new(), newFuncName).method)
	try:
		originalMethod = method.obj.__getattr__(originalMethodName)
		swizzledMethod = method.obj.__getattr__(swizzledMethodName)
		c.method_setImplementation(originalMethod.method, originalImp)
		c.method_setImplementation(swizzledMethod.method, swizzledImp)
	except:
		className = method.obj._get_objc_classname()
		c.class_addMethod(ObjCClass(className).ptr, sel(originalMethodName), originalImp, c.method_getTypeEncoding(method.method))
		c.class_addMethod(ObjCClass(className).ptr, sel(swizzledMethodName), swizzledImp, c.method_getTypeEncoding(method.method))
	c.method_setImplementation(method.method, newImp)

''' Restore the default implementation of `method` ''' 
def resetImplementation(method):
	try:
		originalMethodName = 'original' + method.sel_name.replace(':', '_')
		originalMethod = method.obj.__getattr__(originalMethodName)
		originalImp = c.method_getImplementation(originalMethod.method)
		c.method_setImplementation(method.method, originalImp)
	except:
		pass
