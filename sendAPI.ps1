# send_api_request.ps1

# Prompt the user for input
$user_id = Read-Host "Enter User ID"
$session_id = Read-Host "Enter Session ID"
$message = Read-Host "Enter your message"

# Prepare the JSON body
$body = @{
    user_id = $user_id
    session_id = $session_id
    message = $message
} | ConvertTo-Json

# Set the headers
$headers = @{
    "Content-Type" = "application/json"
}

# Send the API request
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/message" -Method POST -Headers $headers -Body $body
    Write-Host "Response from API:`n"
    $response | Format-List
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Keep the window open until the user presses Enter
Read-Host -Prompt "Press Enter to exit"
