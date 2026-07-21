# Render PDF page using Windows.Data.Pdf
[CmdletBinding()]
param(
    [string]$PdfPath = "c:\Users\SRUTHI\Desktop\petland oman\assets\docs\logo.pdf",
    [string]$OutputPath = "c:\Users\SRUTHI\Desktop\petland oman\scratch\pdf_render.png"
)

# Load assembly
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Data.Pdf.PdfDocument, Windows.Data.Pdf, ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime] | Out-Null

function Render-PdfPage {
    param($pdfPath, $outputPath)
    
    $fileTask = [Windows.Storage.StorageFile]::GetFileFromPathAsync($pdfPath)
    $file = $fileTask.GetAwaiter().GetResult()
    
    $docTask = [Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($file)
    $doc = $docTask.GetAwaiter().GetResult()
    
    if ($doc.PageCount -gt 0) {
        $page = $doc.GetPage(0)
        
        $stream = New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
        $renderOptions = New-Object Windows.Data.Pdf.PdfPageRenderOptions
        
        $renderTask = $page.RenderToStreamAsync($stream, $renderOptions)
        $renderTask.GetAwaiter().GetResult()
        
        # Save stream to file
        if (-not (Test-Path $outputPath)) {
            $folderPath = [System.IO.Path]::GetDirectoryName($outputPath)
            $fileName = [System.IO.Path]::GetFileName($outputPath)
            $folderTask = [Windows.Storage.StorageFolder]::GetFolderFromPathAsync($folderPath)
            $folder = $folderTask.GetAwaiter().GetResult()
            $createTask = $folder.CreateFileAsync($fileName, [Windows.Storage.CreationCollisionOption]::ReplaceExisting)
            $outFile = $createTask.GetAwaiter().GetResult()
        } else {
            $outStorageFileTask = [Windows.Storage.StorageFile]::GetFileFromPathAsync($outputPath)
            $outFile = $outStorageFileTask.GetAwaiter().GetResult()
        }
        
        $fileStreamTask = $outFile.OpenAsync([Windows.Storage.FileAccessMode]::ReadWrite)
        $fileStream = $fileStreamTask.GetAwaiter().GetResult()
        
        $copyTask = [Windows.Storage.Streams.RandomAccessStream]::CopyAsync($stream, $fileStream)
        $copyTask.GetAwaiter().GetResult()
        
        $fileStream.Dispose()
        $stream.Dispose()
        Write-Host "Success rendering page to $outputPath"
    } else {
        Write-Host "PDF has 0 pages"
    }
}

try {
    Render-PdfPage -pdfPath $PdfPath -outputPath $OutputPath
} catch {
    Write-Error $_
}
