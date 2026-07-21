# Load WinRT types into PowerShell
[void][Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
[void][Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]
[void][Windows.Media.Ocr.OcrEngine, Windows.Media.Ocr, ContentType = WindowsRuntime]
[void][Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]

# Load System.Runtime.WindowsRuntime assembly
$assemblyPath = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Runtime.WindowsRuntime.dll"
[System.Reflection.Assembly]::LoadFile($assemblyPath) | Out-Null

$logoFiles = @(
    "c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo.png",
    "c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_transparent.png",
    "c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_white_transparent.png"
)

# Check if OCR Engine is available
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($engine -eq $null) {
    Write-Host "OcrEngine returned null."
    exit
}

Write-Host "Windows OCR Engine initialized. Analyzing logo bounding boxes..."
Write-Host "================================================================"

foreach ($filePath in $logoFiles) {
    if (Test-Path $filePath) {
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
            
            Write-Host "File: $filePath"
            Write-Host "Full Text: $($ocrResult.Text -replace '\r?\n', ' ')"
            
            foreach ($line in $ocrResult.Lines) {
                foreach ($word in $line.Words) {
                    $rect = $word.BoundingRect
                    Write-Host "  Word: '$($word.Text)' at X=$($rect.X), Y=$($rect.Y), W=$($rect.Width), H=$($rect.Height)"
                }
            }
            Write-Host "------------------------------------------------"
        }
        catch {
            Write-Host "File: $filePath - Error: $_"
            Write-Host "------------------------------------------------"
        }
    } else {
        Write-Host "File not found: $filePath"
        Write-Host "------------------------------------------------"
    }
}
