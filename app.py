
#this is the python node for the blockbase app

from flask import Flask, request
import requests
import json
import hashlib
import datetime

url="http://www.mershcap.co.zw/core.php"

def hashing(text):
	
	#this is the hashing function
	text=text.encode()
	hashn=hashlib.sha256(text)
	hashn=hashn.hexdigest()
	
	return hashn
	
app=Flask(__name__)

@app.route("/userkeys",methods=["POST"])
def userkeys():
	
	#a user wants his account to be hashed for anomity
	details=request.get_json()
	public=details[0]
	private=details[1]
	
	public=hashing(public)
	private=hashing(private)
	
	res=json.dumps([public,private])
	
	return res
	
	
@app.route("/history",methods=["POST"])
def history():
	
	#client wants to know the owner and history of an asset
	asset_tag=request.get_json()
	
	tag=asset_tag[0]
	
	head={'request':'long_history','asset_tag':tag}
	req=requests.post(url,data=head)
	info=json.loads(req.text)
	
	return json.dumps(info[0])

@app.route("/newasset",methods=["POST"])
def add_new():

	#user wants to add a new asset into existance
	details=request.get_json()
	
	time=datetime.datetime.now()
	time=time.strftime("%d-%b-%y %H:%M")
	
	tag=hashing(details[0])
	trans=hashing(tag)
	rec=details[1]
	blo="newtag"
	tra=details[2]
	
	head={'request':'check_trans','asset_tag':tag}
	req=requests.post(url,data=head)
	
	#TODO:check if asset exist in ledger
	det=json.loads(req.text)
	
	if(det[0]=="none"):
		head={'request':'current_trans','timestamp':time,'trans_key':trans,'asset_tag':tag,'receiver':rec,'last_blo':blo,'last_tra':tra}
		req=requests.post(url,data=head)
		
		info=json.loads(req.text)
		return json.dumps(info[0])
		
	else:
		return "trans exist"
	
@app.route("/transact",methods=["POST"])
def transact():

	#a new transaction has been received
	details=request.get_json()
	
	time=datetime.datetime.now()
	time=time.strftime("%d-%b-%y %H:%M")
	
	tag=details[0]
	sender=details[1]
	rec=details[2]
	
	#find last block
	head={'request':'retrive','asset_tag':tag}
	req=requests.post(url,data=head)
	
	info=json.loads(req.text)
	if(info[0]==sender):
		blo=info[1]
		tra=info[2]
		trans=hashing(tag+tra)
		#check if transaction already exist
		head={'request':'check_trans','asset_tag':tag}
		req=requests.post(url,data=head)
		det=json.loads(req.text)
		if(det[0]=="none"):
			head={'request':'current_trans','timestamp':time,'trans_key':trans,'asset_tag':tag,'receiver':rec,'last_blo':blo,'last_tra':tra}
			req=requests.post(url,data=head)
			
			info=json.loads(req.text)
			return json.dumps(info[0])
			
		else:
			return "trans exist"
				
			
		
	else:
		return "invalid sender"
		

@app.route("/assets_owned",methods=["POST"])
def myassets():
	
	#a client wants to know all the assets he has
	details=request.get_json()
	
	public_key=details[0]
	
	head={'request':'assets_owned','public_key':public_key}
	req=requests.post(url,data=head)
	
	info=json.loads(req.text)
	
	return json.dumps(info[0])
	
@app.route("/create_block",methods=["POST"])
def create_block():
	
	#creating block
	text=request.get_json()
	text=hashing(text[0])
	
	head={'request':'create_block','hash':text}
	req=requests.post(url,data=head)
	
	info=json.loads(req.text)
	
	return json.dumps(info[0])
	
	


	
	
	






















