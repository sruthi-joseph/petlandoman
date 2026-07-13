# Load WinRT types into PowerShell
[void][Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
[void][Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]
[void][Windows.Media.Ocr.OcrEngine, Windows.Media.Ocr, ContentType = WindowsRuntime]
[void][Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]

# Load System.Runtime.WindowsRuntime assembly
$assemblyPath = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Runtime.WindowsRuntime.dll"
[System.Reflection.Assembly]::LoadFile($assemblyPath) | Out-Null

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
    if ($file.Extension -match '\.(png|jpg|jpeg|bmp)') {
        $filePath = $file.FullName
        try {
            # GetStorageFile
            $storageFileAsync = [Windows.Storage.StorageFile]::GetFileFromPathAsync($filePath)
            $awaiter1 = [System.WindowsRuntimeSystemExtensions]::GetAwaiter($storageFileAsync)
            $storageFile = $awaiter1.GetResult()
            
            # OpenAsync
            $streamAsync = $storageFile.OpenAsync([Windows.Storage.FileAccessMode]::Read)
            $awaiter2 = [System.WindowsRuntimeSystemExtensions]::GetAwaiter($streamAsync)
            $stream = $awaiter2.GetResult()
            
            # BitmapDecoder
            $decoderAsync = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
            $awaiter3 = [System.WindowsRuntimeSystemExtensions]::GetAwaiter($decoderAsync)
            $decoder = $awaiter3.GetResult()
            
            # SoftwareBitmap
            $bitmapAsync = $decoder.GetSoftwareBitmapAsync()
            $awaiter4 = [System.WindowsRuntimeSystemExtensions]::GetAwaiter($bitmapAsync)
            $bitmap = $awaiter4.GetResult()
            
            # RecognizeAsync
            $ocrResultAsync = $engine.RecognizeAsync($bitmap)
            $awaiter5 = [System.WindowsRuntimeSystemExtensions]::GetAwaiter($ocrResultAsync)
            $ocrResult = $awaiter5.GetResult()
            
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
