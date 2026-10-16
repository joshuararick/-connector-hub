Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

Dim aiArmyPath
aiArmyPath = fso.GetSpecialFolder(0).Drive & "\Users\" & sh.ExpandEnvironmentStrings("%USERNAME%") & "\OneDrive\Documents\Ai Army\agent-maker-starter"

If Not fso.FolderExists(aiArmyPath) Then
    MsgBox "Could not find Ai Army at: " & aiArmyPath, 16, "AI Army Error"
    WScript.Quit
End If

' Install deps and start server
Dim cmd
cmd = "cmd /k ""cd /d """ & aiArmyPath & """ && python -m venv .venv 2>nul & .venv\Scripts\python -m pip install -e . -q & echo. & echo AI Army starting at http://localhost:7777 & .venv\Scripts\python -m agent_maker.web.app"""

sh.Run cmd, 1, False

' Open browser after 3 seconds
WScript.Sleep 3000
sh.Run "http://localhost:7777"
