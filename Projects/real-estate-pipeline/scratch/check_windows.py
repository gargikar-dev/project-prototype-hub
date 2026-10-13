import subprocess
import json

cmd = ["powershell", "-Command", "Get-Process | Where-Object MainWindowTitle | Select-Object Id, ProcessName, MainWindowTitle | ConvertTo-Json"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", res.stdout)
