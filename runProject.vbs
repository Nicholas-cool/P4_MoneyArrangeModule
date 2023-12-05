set ws=WScript.CreateObject("WScript.Shell")
ws.Run "runServer.bat",1

set ks=WScript.CreateObject("WScript.Shell")
ks.Run "showPages.bat",0