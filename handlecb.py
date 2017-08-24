import sys
import requests
import callback

handler = callback.InfoHandler(sys.argv)

AUTH_RES_TAG = "auth_cb"

@handler.cmd(AUTH_RES_TAG)
def cb_handler(tok):
	print('cb_handler: ' + tok)
	url = 'http://localhost:8008/done'
	requests.get(url)
	
def get_cb_url():
	cb_url = callback.url(AUTH_RES_TAG, script='firebaseapp/handlecb', tok='REFRESH_TOKEN')
	return cb_url 
		
if __name__ == "__main__":
	handler.handle()
	

