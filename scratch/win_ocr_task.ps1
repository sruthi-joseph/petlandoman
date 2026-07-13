# Load WinRT types into PowerShell
[void][Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
[void][Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]
[void][Windows.Media.Ocr.OcrEngine, Windows.Media.Ocr, ContentType = WindowsRuntime]
[void][Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]

# Load System.Runtime.WindowsRuntime assembly
$assemblyPath = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Runtime.WindowsRuntime.dll"
[System.Reflection.Assembly]::LoadFile($assemblyPath) | Out-Null

# Helper function to await WinRT IAsyncOperation<T> using reflection to call AsTask<T>
function Await-WinRT($asyncOp, $type) {
    # Find the appropriate AsTask generic method
    $methods = [System.WindowsRuntimeSystemExtensions].GetMethods()
    $asTaskMethod = $methods | Where-Object { 
        $_.Name -eq "AsTask" -and 
        $_.GetGenericArguments().Count -eq 1 -and
        $_.GetParameters().Count -eq 1 -and
        $_.GetParameters()[0].ParameterType.Name -like "*IAsyncOperation*"
    } | Select-Object -First 1
    
    if ($asTaskMethod -eq $null) {
        throw "Could not find AsTask method on WindowsRuntimeSystemExtensions"
    }
    
    # Cast target type to System.Type
    $targetType = $type -as [Type]
    if ($targetType -eq $null) {
        throw "Could not resolve type: $type"
    }
    
    $concreteMethod = $asTaskMethod.MakeGenericMethod($targetType)
    $task = $concreteMethod.Invoke($null, @($asyncOp))
    
    # Wait for the task to complete
    $task.Wait() | Out-Null
    return $task.Result
}

$biolineDir = "c:\Users\SRUTHI\Desktop\petland oman\Hygiene suppliments\bioline\bioline"
$files = Get-ChildItem -Path $biolineDir -Filter *

# Check if OCR Engine is available
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($engine -eq $null) {
    Write-Host "OcrEngine returned null."
    exit
}

Write-Host "Windows OCR Engine initialized. Processing files..."
Write-Host "================================================"

foreach ($file in $files) {
    # Only process supported image formats (PNG, JPG, BMP) - Windows BitmapDecoder does not support AVIF/WEBP natively without codecs
    if ($file.Extension -match '\.(png|jpg|jpeg|bmp)') {
        $filePath = $file.FullName
        try {
            # GetStorageFileAsync -> returns StorageFile
            $storageFileAsync = [Windows.Storage.StorageFile]::GetFileFromPathAsync($filePath)
            $storageFile = Await-WinRT $storageFileAsync ([Windows.Storage.StorageFile])
            
            # OpenAsync -> returns IRandomAccessStreamWithContentType
            $streamAsync = $storageFile.OpenAsync([Windows.Storage.FileAccessMode]::Read)
            $streamType = [Windows.Storage.Streams.IRandomAccessStreamWithContentType]
            if ($null -eq $streamType) {
                $streamType = [Windows.Storage.Streams.IRandomAccessStream]
            }
            $stream = Await-WinRT $streamAsync $streamType
            
            # BitmapDecoder.CreateAsync -> returns BitmapDecoder
            $decoderAsync = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
            $decoder = Await-WinRT $decoderAsync ([Windows.Graphics.Imaging.BitmapDecoder])
            
            # GetSoftwareBitmapAsync -> returns SoftwareBitmap
            $bitmapAsync = $decoder.GetSoftwareBitmapAsync()
            $bitmap = Await-WinRT $bitmapAsync ([Windows.Graphics.Imaging.SoftwareBitmap])
            
            # RecognizeAsync -> returns OcrResult
            $ocrResultAsync = $engine.RecognizeAsync($bitmap)
            $ocrResult = Await-WinRT $ocrResultAsync ([Windows.Media.Ocr.OcrResult])
            
            $text = $ocrResult.Text
            
            Write-Host "File: $($file.Name)"
            if ([string]::IsNullOrWhiteSpace($text)) {
                Write-Host "  [No text found]"
            } else {
                Write-Host "  Text: $($text -replace '\r?\n', ' ')"
            }
            Write-Host "------------------------------------------------"
        }
        catch {
            Write-Host "File: $($file.Name) - Error: $_"
            Write-Host "------------------------------------------------"
        }
    }
}
