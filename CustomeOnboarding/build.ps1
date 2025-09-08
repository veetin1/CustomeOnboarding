$exclude = @("venv", "CustomeOnboarding.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "CustomeOnboarding.zip" -Force