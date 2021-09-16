
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

@app.route("/userkeys")
def userkeys():
	
	#a user wants his account to be hashed for anomity
	public=request.args.get("public_key","")
	private=request.args.get("private_key","")
	
	public=hashing(public)
	private=hashing(private)
	
	res=json.dumps([public,private])
	
	return res
	
	
@app.route("/history")
def history():
	
	#client wants to know the owner and history of an asset
	
	tag=request.args.get("asset_tag","")
	
	head={'request':'long_history','asset_tag':tag}
	req=requests.post(url,data=head)
	info=json.loads(req.text)
	
	data=[{'number':0,'time':'time','receiver':'owner'}]
	i=1
	for x in info[0]:
		y={'number':i,'time':x[0],'receiver':x[3]}
		data.append(y)
		i=i+1
	
	return json.dumps(data)

@app.route("/newasset")
def add_new():

	#user wants to add a new asset into existance
	time=datetime.datetime.now()
	time=time.strftime("%d-%b-%y %H:%M")
	
	tag=hashing(request.args.get("asset_tag",""))
	trans=hashing(tag)
	rec=request.args.get("receiver","")
	blo="newtag"
	tra=request.args.get("descr","")
	
	#adding the purpose and location
	purp=request.args.get("purpose","")
	loca=request.args.get("location","")
	
	head={'request':'check_trans','asset_tag':tag}
	req=requests.post(url,data=head)
	
	#TODO:check if asset exist in ledger
	det=json.loads(req.text)
	
	if(det[0]=="none"):
		head={'request':'current_trans','timestamp':time,'trans_key':trans,'asset_tag':tag,'receiver':rec,'last_blo':blo,'last_tra':tra,'purp':purp,'loca':loca}
		req=requests.post(url,data=head)
		
		info=json.loads(req.text)
		return json.dumps(info[0])
		
	else:
		return "trans exist"
	
@app.route("/transact")
def transact():

	#a new transaction has been received
	time=datetime.datetime.now()
	time=time.strftime("%d-%b-%y %H:%M")
	
	tag=request.args.get("asset_tag","")
	sender=request.args.get("sender","")
	rec=request.args.get("receiver","")
	purp=request.args.get("purpose","")
	loca=request.args.get("location","")
	
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
			head={'request':'current_trans','timestamp':time,'trans_key':trans,'asset_tag':tag,'receiver':rec,'last_blo':blo,'last_tra':tra,'purp':purp,'loca':loca}
			req=requests.post(url,data=head)
			
			info=json.loads(req.text)
			return json.dumps(info[0])
			
		else:
			return "trans exist"
				
			
		
	else:
		return "invalid sender"
		

@app.route("/assets_owned")
def myassets():
	
	#a client wants to know all the assets he has
	public_key=request.args.get("public_key","")
	
	head={'request':'assets_owned','public_key':public_key}
	req=requests.post(url,data=head)
	
	info=json.loads(req.text)
	
	data=[{'number':'Number','asset_tag':'Asset tag','desc':'Description'}]
	i=1
	
	for x in info[0]:
		y={'number':i,'asset_tag':x[1],'desc':x[3]}
		i=i+1
		data.append(y)
	
	return json.dumps(data)
	
@app.route("/create_block")
def create_block():
	
	#creating block
	text=request.args.get("hash","")
	text=hashing(text[0])
	
	head={'request':'create_block','hash':text}
	req=requests.post(url,data=head)
	
	info=json.loads(req.text)
	
	return json.dumps(info[0])
	
	


	
	
	






















