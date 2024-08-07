#Because sometimes, bothering to go through your mod list is too much of a pain to care
#Run it once and a input and output folder will be generated, afterwords just shove your mods in Input and if thresh mutations are
#detected it will put create a patch 


import glob
import os 
import json
import sys
import datetime


os.makedirs("Input", exist_ok=True)
os.makedirs("Output", exist_ok=True)



#FileInputList = glob.glob("**/*", root_dir="Input\\", recursive=True)


ScriptBeginning = str(datetime.datetime.now())




def ModJsonBuilder(id, name):
	JsonBuildList = []
	JsonEntry = {}
	JsonEntry["type"] = "MOD_INFO"
	JsonEntry["id"] = str("Ph_" + id + "_ClassRemover")
	JsonEntry["name"] = str("ClassRem_" + name)
	JsonEntry["authors"] = ["Scarlet", "PythonInterpreter"]
	JsonEntry["description"] = "Generated via script on {0} for mod {1}".format(ScriptBeginning, name)
	JsonEntry["category"] = "rebalance"
	JsonEntry["dependencies"] = [id]
	JsonBuildList.append(JsonEntry)
	return JsonBuildList




def JsonEvaluator(inputpath):
	InputData = open(inputpath)
	JsonInputData = json.load(InputData)
	exportlist = []
	if type(JsonInputData) == dict:
		#print("Fuck you {} again from the JsonEvaluator".format(CurrentPath))
		JsonInputDataString = JsonInputData 
		JsonInputData = []
		JsonInputData.append(JsonInputDataString)
	for x in JsonInputData:
		typecheck = x.get("type")
		thresholdtrue = x.get("threshold")
		if typecheck == "mutation":
			threshentry = {}
			threshentry["type"] = typecheck
			if x.get("id") != None:
				threshentry["id"] = x.get("id")
				threshentry["copy-from"] = x.get("id")
			if x.get("ident") != None:
				threshentry["id"] = x.get("ident")
				threshentry["copy-from"] = x.get("ident")
			threshentry["cancels"] = []
			exportlist.append(threshentry)
	InputData.close()
	return exportlist









#print("Reading folders in Input...")
ModFolderList = os.listdir("Input\\")

for ModFolder in ModFolderList:
	modinfoprebuilt = 0
	patchcount = 0
	CurrentPath = str("Input\\" + ModFolder + "\\")
	OutputPath = str("Output\\" + ModFolder + "\\")
	if os.path.isfile(str(CurrentPath + "modinfo.json")) != True:
		continue
	ModInfoReader = open(str(CurrentPath + "modinfo.json"), mode="r")
	JSONMODINFO = json.load(ModInfoReader)
	#print(type(JSONMODINFO))
	if type(JSONMODINFO) == dict:
		#print("Fuck you {} for not formatting your modinfojson like a normal person".format(CurrentPath))
		JSONMODINFOSTRING = JSONMODINFO 
		JSONMODINFO = []
		JSONMODINFO.append(JSONMODINFOSTRING)
	for x in JSONMODINFO:
		if x.get("type") == "MOD_INFO":
			MODID = x.get("id")
			MODNAME = x.get("name")
			if type(MODID) != str:
				MODID = x.get("ident")
			#print(type(x))
		
	JSONLIST = glob.glob("**/*.json", root_dir=CurrentPath, recursive=True)
	
	
	for y in JSONLIST:
		WorkingPath = str(CurrentPath + y)
		workinglist = JsonEvaluator(WorkingPath)
		if len(workinglist) == 0:
			#print("No threshold mutations detected in {0}".format(WorkingPath))
			continue
		else:
			FilePath = str(OutputPath + y)
			dir_path, A = os.path.split(FilePath)
			os.makedirs(dir_path, exist_ok = True)
			PatchWriter = open(str(OutputPath + y), mode="w+")
			if A != "modinfo.json":
				json.dump(workinglist, PatchWriter, indent = 4)
				patchcount += 1
			elif A == "modinfo.json":
				ModInfoJsonList = ModJsonBuilder(MODID, MODNAME)
				modinfoprebuilt = 1
				ListCombine = ModInfoJsonList + workinglist
				json.dump(workinglist, PatchWriter, indent = 4)
				patchcount += 1
			PatchWriter.close()
			
		
	
	if patchcount != 0 and modinfoprebuilt == 0:
		ModInfoWriter = open(str(OutputPath + "modinfo.json"), mode="w+")
		ModInfoJsonList = ModJsonBuilder(MODID, MODNAME)
		json.dump(ModInfoJsonList, ModInfoWriter, indent = 4)
		ModInfoWriter.close()
		
	if patchcount != 0:
		os.rename(OutputPath, str("Output\\" + ModInfoJsonList[0]["id"]))
	
	ModInfoReader.close()

