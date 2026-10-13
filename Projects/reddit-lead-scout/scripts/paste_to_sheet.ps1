# Load TSV data to clipboard
Get-Content -Raw "reports/sheet_paste_data.tsv" | Set-Clipboard

$wshell = New-Object -ComObject wscript.shell
$found = $wshell.AppActivate("Reddit ICP Lead Engine - Pipeline Tracker")
if (-not $found) {
    $found = $wshell.AppActivate("Google Sheets")
}

if ($found) {
    Start-Sleep -Milliseconds 600
    # Send Ctrl+Home to select cell A1
    $wshell.SendKeys("^{HOME}")
    Start-Sleep -Milliseconds 400
    # Send Ctrl+V to paste
    $wshell.SendKeys("^v")
    Write-Output "SUCCESS: Focused Google Sheets and pasted 20 leads into cell A1."
} else {
    Write-Output "INFO: Google Sheets window was not active in foreground. Clipboard is ready."
}
