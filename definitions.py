import json
import pprint
from datetime import datetime


class Status(object):
	""" Class that define status of test """
	def __init__(self, status="not defined"):
		self.status = status

	def formatDataForEmail(self):
		text="\n-------------------------- TEST STATUS -------------------------------------"
		if self.status is None:
			text+="STATUS :: "+self.status
		else:
			text+="STATUS :: "
		return text

	@staticmethod
	def decode(value):
		info=Status()
		for key in info.__dict__.keys():
			info.__dict__[key]=str(value[key])
		return info

class LogInfo(object):
	""" Class that define logging information """
	def __init__(self, logPath="not defined",allowCBCollect=False,uploadPath="not defined"):
		self.logPath = logPath
		self.allowCBCollect=allowCBCollect
		self.uploadPath=uploadPath
	@staticmethod
	def decode(value):
		info=LogInfo()
		for key in info.__dict__.keys():
			info.__dict__[key]=str(value[key])
		return info

class ErrorInfo(object):
	""" Class that defines Error information"""
	def __init__(self, error="no error", desc=""):
		self.error = error
		self.desc = desc

	def formatDataForEmail(self):
		text="\n-------------------------- ERROR INFO BEGIN -------------------------------------"
		text+="\n\t ERROR :: "+str(PrintObject.PrintSpaceIfNull(self.error))
		text+="\n\t DESCRIPTION :: "+str(PrintObject.PrintSpaceIfNull(self.desc))
		text+="\n-------------------------- ERROR INFO END   -------------------------------------"
		return text

	@staticmethod
	def decode(value):
		info=ErrorInfo()
		for key in info.__dict__.keys():
			info.__dict__[key]=str(value[key])
		return info

class Phase(object):
	""" Class that defines phase of a test case """
	def __init__(self, name="Not defined", desc="Not defined", status="Not defined", time="Not defined"):
		self.name = name
		self.desc = desc
		self.status = status
		self.time = time

	def formatDataForEmail(self):
		text = "\n----------------------PHASE "+str(self.name)+" BEGIN  ------------------------------"
		text+="\n\t Description :: "+PrintObject.PrintSpaceIfNull(self.desc)
		text+="\n\t Status :: "+PrintObject.PrintSpaceIfNull(self.status.status)
		text+="\n\t Start Time :: "+str(PrintObject.PrintSpaceIfNull(self.time.begin))
		text+="\n\t End Time :: "+str(PrintObject.PrintSpaceIfNull(self.time.end))
		text+= "\n----------------------PHASE "+str(self.name)+" END  -------------------------------\n\n"
		return text

	@staticmethod
   	def decode(value):
		info=Phase()
		for key in info.__dict__.keys():
			if key == 'status':
				info.__dict__[key]=Status.decode(value[key])
			elif key == 'time':
				info.__dict__[key]=TimeInfo.decode(value[key])
			else:
				info.__dict__[key]=str(value[key])
		return info

class PhaseInfo(object):
	""" Class that defines phase information 
		in terms of all phases and the current phase
		of the test case """
	def __init__(self, phases=None, current=None):
		self.phases = phases
		self.current = current

	def formatDataForEmail(self):
		text="\n-------------------------- PHASES PHASE BEGIN -------------------------------------\n"
		for phase in self.phases:
			text+=phase.formatDataForEmail()
		text+="\n--------------------------- PHASES PHASE END --------------------------------------\n"
		return text

	@staticmethod
	def decode(value):
		info=PhaseInfo()
		for key in info.__dict__.keys():
			if key == 'phases':
				list=[]
				for phase in value[key]:
					list.append(Phase.decode(phase))
				info.__dict__[key]=list
			else:
				info.__dict__[key]=Phase.decode(value[key])
		return info

class EmailInfo(object):
	"""" Class that defines email information for sending out notification """
	def __init__(self, emailTo="Not defined", emailFrom="Not defined", server="Not defined", sendEmail=False):
		self.emailTo = emailTo
		self.emailFrom = emailFrom
		self.server = server
		self.sendEmail= False;
	
	@staticmethod
	def decode(value):
		info=EmailInfo()
		for key in info.__dict__.keys():
			info.__dict__[key]=str(value[key])
		return info

class TimeInfo(object):
	"""" Class that defines time informaiton for test run """
	def __init__(self, begin="not defined", end="not defined"):
		self.begin = begin
		self.end = end

	def convertToString(self):
    		self.begin=str(self.begin)
    		self.end=str(self.end)

	@staticmethod
	def decode(value):
		info=TimeInfo()
		for key in info.__dict__.keys():
			info.__dict__[key]=str(value[key])
		return info

class TestInfo(object):
	""" Class that defines all meta data related to a running test case """
	def __init__(self, id="not defined", name="not defined", desc="not defined", expiry="Not Defined",buildVersion="Not Defined",time=None, phaseInfo=None, statusInfo=None, errorInfo=None, emailInfo=None, log=None):
		self.id=id
		self.name=name
		self.desc=desc
		self.time=time
		self.phaseInfo=phaseInfo
		self.statusInfo=statusInfo
		self.errorInfo=errorInfo
		self.emailInfo=emailInfo
		self.log=log
		self.buildVersion=buildVersion
		self.expiry=expiry

	def convertTimeToString(self):
    		self.time.convertToString()
    		for phase in self.phaseInfo.phases:
        		phase.time.convertToString()

	def formatDataForEmail(self):
		subject=self.name+"::"+self.desc+"::"+self.statusInfo.status
		text="\n \n THIS IS A SYSTEM GENERATED EMAIL  \n"
		text+="\n-------------------------- TEST INFORMATION -------------------------------------\n"
		text+="\n\t Name :: "+PrintObject.PrintSpaceIfNull(self.name)
		text+="\n\t Description :: "+PrintObject.PrintSpaceIfNull(self.desc)
		text+="\n\t Test Status :: "+PrintObject.PrintSpaceIfNull(self.statusInfo.status)
		text+="\n\t Start Time :: "+PrintObject.PrintSpaceIfNull(self.time.begin)
		text+="\n\t End Time :: "+PrintObject.PrintSpaceIfNull(self.time.end)
		text+="\n\t Logs Path :: "+PrintObject.PrintSpaceIfNull(self.log.logPath)
		text+=self.errorInfo.formatDataForEmail()
		text+=self.phaseInfo.formatDataForEmail()
		return subject,text

	@staticmethod
	def decode(data):
		info=TestInfo()
		for key in info.__dict__.keys():
			if key == 'time':
				info.__dict__[key]=TimeInfo.decode(data[key])
			elif key == 'phaseInfo':
				info.__dict__[key]=PhaseInfo.decode(data[key])
			elif key == 'emailInfo':
				info.__dict__[key]=EmailInfo.decode(data[key])
			elif key == 'log':
				info.__dict__[key]=LogInfo.decode(data[key])
			elif key == 'statusInfo':
				info.__dict__[key]=Status.decode(data[key])
			elif key == 'errorInfo':
				info.__dict__[key]=ErrorInfo.decode(data[key])
			else:
				info.__dict__[key]=data[key]
		return info


class PrintObject(object):
	""" This method can convert an object into a dictionary """
	@staticmethod  
	def toDictionary(data):
		dict={}
		for key in data.__dict__.keys():
			if hasattr(data.__dict__[key],'__dict__'):
				if len(data.__dict__[key].__dict__.keys()) > 0:
					if type(data.__dict__[key]) is list:
						l=[]
						for val in data.__dict__[key]:
							d=Print.Object.toDictionary(val)
							l.append(d)
						dict[key]=l
					else:
						dict[key]=PrintObject.toDictionary(data.__dict__[key])
			else:
				if type(data.__dict__[key]) is list:
					l=[]
					for val in data.__dict__[key]:
						d=PrintObject.toDictionary(val)
						l.append(d)
					dict[key]=l
				else:
					dict[key]=str(data.__dict__[key])
		return dict

	#staticmethod
	@staticmethod
	def PrintSpaceIfNull(data):
		if data is None:
			return "Not Defined"
                return data

def main():
	#Example of How Test Information is generated
	st=datetime.now()
	ed=datetime.now()
	diff=ed-st
	log=LogInfo("path_123")
	timeInfo=TimeInfo(begin=str(st),end=str(ed))
	status = Status(status="Healthy")
	phase1=Phase(name="1",desc="phase 1",status=status,time=timeInfo)
	phase2=Phase(name="2",desc="phase 2",status=status,time=timeInfo)
	phase3=Phase(name="3",desc="phase 3",status=status,time=timeInfo)
	dictP=[phase1,phase2,phase3]
	current = phase2
	error=ErrorInfo(error=None,desc="No Error")
	phaseInfo=PhaseInfo(phases=	dictP,current=current)
	emailInfo=EmailInfo(emailTo="parag@couchbase.com",emailFrom="parag@couchbase.com",server="127.0.0.1",sendEmail=True)
	testInfo=TestInfo(id="UID",name="Jason Testing",desc="Just for fun Test",emailInfo=emailInfo,phaseInfo=phaseInfo,log=log, errorInfo=error,time=timeInfo,statusInfo=status)
	
	data = PrintObject.toDictionary(testInfo)
        testInfo=TestInfo.decode(data)
        print PrintObject.toDictionary(testInfo)

	val= json.dumps(PrintObject.toDictionary(testInfo),separators=(',',':'),sort_keys=True,indent=4)
	print val

	#f = open('data.txt','w')
	#f.write(val) # python will convert \n to os.linesep
	#f.close()
	#json_data=open("./data.txt").read()

 	#data = json.loads(json_data)
 	#test=TestInfo.decode(data)
	#print toDictionary(test)
	
if __name__ == "__main__":
    main()

