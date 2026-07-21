# C# Source code for OCR that extracts bounding boxes
$source = @"
using System;
using System.IO;
using System.Threading.Tasks;
using System.Collections.Generic;
using Windows.Storage;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;

public class WordInfo {
    public string Text { get; set; }
    public double X { get; set; }
    public double Y { get; set; }
    public double Width { get; set; }
    public double Height { get; set; }
}

public class OcrHelper {
    public static List<WordInfo> RecognizeWords(string imagePath) {
        try {
            return RecognizeWordsAsync(imagePath).GetAwaiter().GetResult();
        } catch (Exception ex) {
            Console.WriteLine("C# Exception: " + ex.ToString());
            return null;
        }
    }

    private static async Task<List<WordInfo>> RecognizeWordsAsync(string imagePath) {
        StorageFile file = await StorageFile.GetFileFromPathAsync(imagePath);
        using (var stream = await file.OpenAsync(FileAccessMode.Read)) {
            var decoder = await BitmapDecoder.CreateAsync(stream);
            using (var bitmap = await decoder.GetSoftwareBitmapAsync()) {
                var engine = OcrEngine.TryCreateFromUserProfileLanguages();
                if (engine == null) {
                    throw new Exception("OcrEngine TryCreateFromUserProfileLanguages returned null");
                }
                var result = await engine.RecognizeAsync(bitmap);
                var wordList = new List<WordInfo>();
                foreach (var line in result.Lines) {
                    foreach (var word in line.Words) {
                        wordList.Add(new WordInfo {
                            Text = word.Text,
                            X = word.BoundingRect.X,
                            Y = word.BoundingRect.Y,
                            Width = word.BoundingRect.Width,
                            Height = word.BoundingRect.Height
                        });
                    }
                }
                return wordList;
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

$logoFiles = @(
    "c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo.png",
    "c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_transparent.png",
    "c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_white_transparent.png"
)

Write-Host "Processing logos..."
Write-Host "================================================"

foreach ($filePath in $logoFiles) {
    if (Test-Path $filePath) {
        Write-Host "File: $filePath"
        try {
            $words = [OcrHelper]::RecognizeWords($filePath)
            if ($words -eq $null) {
                Write-Host "  No word data returned (or exception occurred)."
            } elseif ($words.Count -eq 0) {
                Write-Host "  [No text found]"
            } else {
                foreach ($w in $words) {
                    Write-Host "    Word: '$($w.Text)' -> X=$($w.X), Y=$($w.Y), W=$($w.Width), H=$($w.Height)"
                }
            }
        }
        catch {
            Write-Host "  Invoke Error: $_"
        }
        Write-Host "------------------------------------------------"
    } else {
        Write-Host "File not found: $filePath"
        Write-Host "------------------------------------------------"
    }
}
