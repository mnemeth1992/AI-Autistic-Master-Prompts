$TargetFile = "c:\Users\Misi\Downloads\AI Autistic Master Prompts\inditas.bat"
$WorkingDir = "c:\Users\Misi\Downloads\AI Autistic Master Prompts"

# Desktop Shortcut
$DesktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath("Desktop"), "Prompt Asszisztens.lnk")
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($DesktopPath)
$Shortcut.TargetPath = $TargetFile
$Shortcut.WorkingDirectory = $WorkingDir
$Shortcut.Description = "Keresztény Digitális Termék Prompt Asszisztens"
$Shortcut.IconLocation = "shell32.dll,221"
$Shortcut.Save()

# App Directory Shortcut
$LocalShortcut = [System.IO.Path]::Combine($WorkingDir, "Prompt Asszisztens.lnk")
$Shortcut2 = $WshShell.CreateShortcut($LocalShortcut)
$Shortcut2.TargetPath = $TargetFile
$Shortcut2.WorkingDirectory = $WorkingDir
$Shortcut2.Description = "Keresztény Digitális Termék Prompt Asszisztens"
$Shortcut2.IconLocation = "shell32.dll,221"
$Shortcut2.Save()

Write-Host "Desktop shortcut created successfully at: $DesktopPath"
