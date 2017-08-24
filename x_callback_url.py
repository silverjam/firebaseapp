# coding: utf-8
import swizzle
from objc_util import *
import ctypes
import json, urllib
import uuid
import sys
import webbrowser

NSURLComponents = ObjCClass('NSURLComponents')
appDelegate = UIApplication.sharedApplication().delegate()
_handler = None
_requestID = None

class x_callback_response (object):
	full_url = None
	source_app = None
	parameters = None
	
	def __str__(self):
		return '<x_callback_response: source_app = {}, parameters = {}>'.format(self.source_app, self.parameters)

def open_url(url, handler):
	global _handler
	global _requestID
	_requestID = uuid.uuid1()
	_handler = handler
	url_with_uuid = url + 'xcallbackresponse-' + str(_requestID)
	webbrowser.open(url_with_uuid)

def application_openURL_sourceApplication_annotation_(_self, _sel, app, url, source_app, annotation):
	url_str = str(ObjCInstance(url))
	
	if not 'xcallbackresponse-' + str(_requestID) in url_str:
		print('not from x-callback-url, will run original function')
		obj = ObjCInstance(_self)
		orig_name = c.sel_getName(_sel).decode("utf-8")
		#print(dir(obj))
		
		original_method = swizzle.get_orig_method(obj, _sel)
		
		#orig_meth_name = 'original'+orig_name
		#original_method = getattr(obj, , None)
		#original_method = ObjCInstanceMethod(ObjCInstance(app), orig_meth_name)
		
		if original_method:
			_annotation = ObjCInstance(annotation) if annotation else None
			return original_method(ObjCInstance(obj), ObjCInstance(url), ObjCInstance(source_app), _annotation)
	else:
		x_callback_info = x_callback_response()
		x_callback_info.full_url = url_str
		x_callback_info.source_app = str(ObjCInstance(source_app))
		
		query = NSURLComponents.componentsWithURL_resolvingAgainstBaseURL_(nsurl(url_str), False)
		x_callback_info.parameters = dict()
		for queryItem in query.queryItems():
			x_callback_info.parameters[str(queryItem.name())] = str(queryItem.value())
			
		if _handler:
			_handler(x_callback_info)
		return True



# Do the swizzling
cls = ObjCInstance(c.object_getClass(appDelegate.ptr))

swizzle.swizzle(cls, 'application:openURL:sourceApplication:annotation:', application_openURL_sourceApplication_annotation_)


if __name__ == '__main__':
	import console
	console.clear()
	
	url = 'safari://google.com'
	
	def my_handler(info):
		print(info.full_url)
		print(info.parameters['text'])
	
	open_url(url, my_handler)
	
	print("foofoo")
