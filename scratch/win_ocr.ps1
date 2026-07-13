# Load required assemblies for Windows Runtime APIs
[void][Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
[void][Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]
[void][Windows.Media.Ocr.OcrEngine, Windows.Media.Ocr, ContentType = WindowsRuntime]
[void][Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]

$biolineDir = "c:\Users\SRUTHI\Desktop\petland oman\Hygiene suppliments\bioline\bioline"
$files = Get-ChildItem -Path $biolineDir -Filter *

# Check if OCR Engine is available
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($engine -eq $null) {
    Write-Host "OCR Engine could not be created from user profile languages. Trying default..."
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
}

if ($engine -eq $null) {
    Write-Error "Windows OCR Engine is not available on this system."
    exit
}

function Await-Async($asyncOp) {
    # Wait for the async operation to complete
    while ($asyncOp.Status -eq [Windows.Foundation.AsyncStatus]::Started) {
        Start-Sleep -Milliseconds 5
    }
    return $asyncOp.GetResults()
}

Write-Host "Windows OCR Engine initialized. Processing files..."
Write-Host "================================================"

foreach ($file in $files) {
    # Check if it is a supported image extension
    if ($file.Extension -match '\.(png|jpg|jpeg|webp|bmp)') {
        $filePath = $file.FullName
        try {
            # GetStorageFile
            $storageFileAsync = [Windows.Storage.StorageFile]::GetFileFromPathAsync($filePath)
            $storageFile = Await-Async $storageFileAsync
            
            $streamAsync = $storageFile.OpenAsync([Windows.Storage.FileAccessMode]::Read)
            $stream = Await-Async $streamAsync
            
            $decoderAsync = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
            $decoder = Await-Async $decoderAsync
            
            $bitmapAsync = $decoder.GetSoftwareBitmapAsync()
            $bitmap = Await-Async $bitmapAsync
            
            $ocrResultAsync = $engine.RecognizeAsync($bitmap)
            $ocrResult = Await-Async $ocrResultAsync
            
            $text = $ocrResult.Text
            
            Write-Host "File: $($file.Name)"
            if ([string]::IsNullOrWhiteSpace($text)) {
                Write-Host "  [No text found]"
            } else {
                # Format text by joining lines nicely or replacement
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
