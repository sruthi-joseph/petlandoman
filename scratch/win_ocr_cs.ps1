# C# Source code for OCR
$source = @"
using System;
using System.IO;
using System.Threading.Tasks;
using Windows.Storage;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;

public class OcrHelper {
    public static string Recognize(string imagePath) {
        try {
            return RecognizeAsync(imagePath).GetAwaiter().GetResult();
        } catch (Exception ex) {
            return "ERROR: " + ex.Message;
        }
    }

    private static async Task<string> RecognizeAsync(string imagePath) {
        StorageFile file = await StorageFile.GetFileFromPathAsync(imagePath);
        using (var stream = await file.OpenAsync(FileAccessMode.Read)) {
            var decoder = await BitmapDecoder.CreateAsync(stream);
            using (var bitmap = await decoder.GetSoftwareBitmapAsync()) {
                var engine = OcrEngine.TryCreateFromUserProfileLanguages();
                if (engine == null) {
                    return "ERROR: OcrEngine returned null";
                }
                var result = await engine.RecognizeAsync(bitmap);
                return result.Text;
            }
        }
    }
}
"@

try {
    $winmd = "C:\Windows\System32\WinMetadata\Windows.winmd"
    $rt = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Runtime.WindowsRuntime.dll"
    
    Add-Type -TypeDefinition $source -ReferencedAssemblies $rt, $winmd
    Write-Host "C# OCR Helper successfully compiled!"
}
catch {
    Write-Error "Failed to compile C# helper: $_"
    exit
}

$biolineDir = "c:\Users\SRUTHI\Desktop\petland oman\Hygiene suppliments\bioline\bioline"
$files = Get-ChildItem -Path $biolineDir -Filter *

Write-Host "Processing files..."
Write-Host "================================================"

foreach ($file in $files) {
    if ($file.Extension -match '\.(png|jpg|jpeg|bmp)') {
        $filePath = $file.FullName
        try {
            $text = [OcrHelper]::Recognize($filePath)
            Write-Host "File: $($file.Name)"
            if ($text.StartsWith("ERROR:")) {
                Write-Host "  Error: $text"
            } elseif ([string]::IsNullOrWhiteSpace($text)) {
                Write-Host "  [No text found]"
            } else {
                Write-Host "  Text: $($text -replace '\r?\n', ' ')"
            }
            Write-Host "------------------------------------------------"
        }
        catch {
            Write-Host "File: $($file.Name) - Invoke Error: $_"
            Write-Host "------------------------------------------------"
        }
    }
}
