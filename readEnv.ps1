# https://stackoverflow.com/questions/72236557/how-do-i-read-a-env-file-from-a-ps1-script
Get-Content .env | ForEach-Object {
  $name, $value = $_.split('=')
  if ([string]::IsNullOrWhiteSpace($name) || $name.Contains('#')) {
   continue
  }
  Set-Content env:\$name $value
}